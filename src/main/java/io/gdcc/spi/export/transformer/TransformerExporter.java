package io.gdcc.spi.export.transformer;

import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.io.StringReader;
import java.io.UnsupportedEncodingException;
import java.net.URI;
import java.net.URISyntaxException;
import java.nio.file.FileSystem;
import java.nio.file.FileSystems;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Base64;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Optional;
import java.util.Set;
import java.util.logging.Logger;
import java.util.regex.Pattern;

import javax.script.ScriptEngine;
import javax.xml.transform.Source;
import javax.xml.transform.URIResolver;
import javax.xml.transform.stream.StreamResult;
import javax.xml.transform.stream.StreamSource;

import org.openjdk.nashorn.api.scripting.NashornScriptEngineFactory;
import org.python.jsr223.PyScriptEngineFactory;

import com.google.auto.service.AutoService;

import io.gdcc.spi.export.ExportDataProvider;
import io.gdcc.spi.export.ExportException;
import io.gdcc.spi.export.Exporter;
import io.github.erykkul.json.transformer.Transformer;
import io.github.erykkul.json.transformer.TransformerFactory;
import io.github.erykkul.json.transformer.Utils;
import jakarta.json.Json;
import jakarta.json.JsonObject;
import jakarta.json.JsonObjectBuilder;
import jakarta.json.JsonReader;
import jakarta.json.JsonString;
import jakarta.json.JsonValue;
import jakarta.json.JsonValue.ValueType;

/**
 * An example transformer exporter that exports dataset metadata as a JSON
 * object.
 * 
 */
// This annotation makes the Exporter visible to Dataverse. How it works is well
// documented on the Internet.
@AutoService(Exporter.class)
// All Exporter implementations must implement this interface or the XMLExporter
// interface that extends it.
public class TransformerExporter implements Exporter {
    private static final String base64 = "base64";
    private static final Logger logger = Logger.getLogger(TransformerFactory.class.getName());
    private static final TransformerFactory factory = TransformerFactory.factory(new NashornScriptEngineFactory());
    private static final PyScriptEngineFactory pyFactory = new PyScriptEngineFactory();
    private static final Pattern escapePattern = Pattern.compile("(\\<|\\>|\"|'|&)");
    private static final Map<String, String> escapeMap = Map.of(
            "<", "&lt;",
            ">", "&gt;",
            "\"", "&quot;",
            "'", "&apos;",
            "&", "&amp;");

    private static String jsonToXml(final JsonObject object) {
        final StringBuilder res = new StringBuilder("<?xml version=\"1.0\" ?><root>");
        asXml(object, res);
        res.append("</root>");
        return res.toString();
    }

    private static void asXml(final JsonObject object, final StringBuilder builder) {
        object.entrySet().forEach((x) -> {
            final String tag = x.getKey();
            final JsonValue value = x.getValue();
            final ValueType t = value.getValueType();
            if (ValueType.OBJECT.equals(t)) {
                builder.append("<").append(tag).append(">");
                asXml(value.asJsonObject(), builder);
                builder.append("</").append(tag).append(">");
            } else if (ValueType.ARRAY.equals(t)) {
                value.asJsonArray().forEach((y) -> {
                    builder.append("<").append(tag).append(">");
                    asXml(y, builder, tag);
                    builder.append("</").append(tag).append(">");
                });
            } else {
                builder.append("<").append(tag).append(">").append(escapeXml(value)).append("</").append(tag)
                        .append(">");
            }
        });
    }

    private static void asXml(final JsonValue value, final StringBuilder builder, final String tag) {
        final ValueType t = value.getValueType();
        if (ValueType.OBJECT.equals(t)) {
            value.asJsonObject().entrySet().forEach((x) -> {
                final String tag2 = x.getKey();
                builder.append("<").append(tag2).append(">");
                asXml(x.getValue(), builder, tag2);
                builder.append("</").append(tag2).append(">");
            });
        } else if (ValueType.ARRAY.equals(t)) {
            value.asJsonArray().forEach((y) -> {
                builder.append("<").append(tag).append(">");
                asXml(y, builder, tag);
                builder.append("</").append(tag).append(">");
            });
        } else {
            builder.append(escapeXml(value));
        }
    }

    private static final String escapeXml(final JsonValue value) {
        final String xml = JsonValue.ValueType.STRING.equals(value.getValueType()) ? ((JsonString) value).getString()
                : value.toString();
        return escapePattern.matcher(xml).replaceAll(x -> escapeMap.get(x.group()));
    }

    private final Transformer preTransformer;
    private Transformer transformer;
    private javax.xml.transform.Transformer xmlTransformer;
    private boolean isXmlTransformer = false;
    private String pyScript = null;
    private final Config config;
    private Path outPath;

    // These methods provide information about the Exporter to Dataverse

    /**
     * Default constructor
     */
    public TransformerExporter() {
        this(0);
    }

    /**
     * Constructor with index
     * 
     * @param index the index
     */
    public TransformerExporter(final int index) {
        outPath = null;
        config = config("config.json", index);
        preTransformer = transformer("pre_transformer.json", index);
        if (isXmlTransformer) {
            transformer = null;
            try {
                final URIResolver uriResolver = getResolver(outPath);
                final javax.xml.transform.TransformerFactory xmlTransformerFactory = javax.xml.transform.TransformerFactory
                        .newInstance();
                xmlTransformerFactory.setURIResolver(uriResolver);
                xmlTransformer = xmlTransformerFactory.newTransformer(uriResolver.resolve("transformer.xsl", null));
                xmlTransformer.setParameter("language-code", getLanguageCodeFromEnv());
            } catch (final Exception e) {
                transformer = transformer("transformer.json", index);
                logger.severe("reading XSLT failed: " + e);
            }
        } else if (pyScript != null) {
            xmlTransformer = null;
            transformer = null;
        } else {
            xmlTransformer = null;
            transformer = transformer("transformer.json", index);
        }
    }

    /*
     * The name of the format it creates. If this format is already provided by a
     * built-in exporter, this Exporter will override the built-in one. (Note that
     * exports are cached, so existing metadata export files are not updated
     * immediately.)
     */
    @Override
    public String getFormatName() {
        return config.getFormatName();
    }

    // The display name shown in the UI
    @Override
    public String getDisplayName(final Locale locale) {
        // This example includes the language in the name to demonstrate that locale is
        // available. A production exporter would instead use the locale to generate an
        // appropriate translation.
        return config.getDisplayName(locale);
    }

    // Whether the exported format should be available as an option for Harvesting
    @Override
    public Boolean isHarvestable() {
        return config.isHarvestable();
    }

    // Whether the exported format should be available for download in the UI and
    // API
    @Override
    public Boolean isAvailableToUsers() {
        return config.isAvailableToUsers();
    }

    // Exporters can specify that they require, as input, the output of another
    // exporter. This is done by providing the name of that format in response to a
    // call to this method.
    @Override
    public Optional<String> getPrerequisiteFormatName() {
        return Optional.ofNullable(config.getPrerequisiteFormatName());
    }

    // Defines the mime type of the exported format - used when metadata is
    // downloaded, i.e. to trigger an appropriate viewer in the user's browser.
    @Override
    public String getMediaType() {
        return config.getMediaType();
    }

    // This method is called by Dataverse when metadata for a given dataset in this
    // format is requested.
    @Override
    public void exportDataset(final ExportDataProvider dataProvider, final OutputStream outputStream)
            throws ExportException {
        try {
            // Write the output format to the output stream.
            if (xmlTransformer != null) {
                final Source src = getPrerequisiteFormatName().isEmpty() ? getInputAsSource(dataProvider)
                        : getPrerequisiteInputAsSource(dataProvider);
                xmlTransformer.transform(src, new StreamResult(outputStream));
            } else if (pyScript != null) {
                final ScriptEngine engine = pyFactory.getScriptEngine();
                final JsonObject input = getPrerequisiteFormatName().isEmpty() ? getInputAsJsonObject(dataProvider)
                        : getPrerequisiteInputAsJsonObject(dataProvider);
                engine.put("x", Utils.asObject(input));
                if (outPath != null) {
                    engine.put("path", outPath.toAbsolutePath().toString());
                }
                engine.put("res", new LinkedHashMap<String, Object>());
                engine.eval(pyScript);
                final Object res = engine.get("res");
                final byte[] bytes = res instanceof String ? ((String) res).getBytes("UTF8")
                        : toBytes(Utils.asJsonValue(res));
                outputStream.write(bytes);
            } else {
                final JsonObject input = getPrerequisiteFormatName().isEmpty() ? getInputAsJsonObject(dataProvider)
                        : getPrerequisiteInputAsJsonObject(dataProvider);
                final JsonObject transformed = transformer.transform(input);
                outputStream.write(transformed.toString().getBytes("UTF8"));
            }
            // Flush the output stream - The output stream is automatically closed by
            // Dataverse and should not be closed in the Exporter.
            outputStream.flush();
        } catch (final Exception e) {
            // If anything goes wrong, an Exporter should throw an ExportException.
            logger.severe("transformation failed: " + e);
            throw new ExportException("Unknown exception caught during JSON export.");
        }
    }

    private Source getInputAsSource(final ExportDataProvider dataProvider) {
        final JsonObject datasetJson = dataProvider.getDatasetJson();
        final JsonObject preTransformed = preTransformer.transform(datasetJson);
        return new StreamSource(new StringReader(jsonToXml(preTransformed)));
    }

    private JsonObject getInputAsJsonObject(final ExportDataProvider dataProvider) {
        final JsonObject datasetJson = dataProvider.getDatasetJson();
        final JsonObject preTransformed = preTransformer.transform(datasetJson);
        final JsonObjectBuilder job = Json.createObjectBuilder();
        job.add("datasetJson", datasetJson);
        job.add("datasetORE", dataProvider.getDatasetORE());
        job.add("datasetSchemaDotOrg", dataProvider.getDatasetSchemaDotOrg());
        job.add("datasetFileDetails", dataProvider.getDatasetFileDetails());
        job.add("preTransformed", preTransformed);
        job.add("config", config.asJsonValue());
        if (outPath != null) {
            job.add("path", outPath.toAbsolutePath().toString());
        }
        return job.build();
    }

    private byte[] toBytes(final JsonValue value) throws UnsupportedEncodingException {
        if (Utils.isObject(value) && value.asJsonObject().size() == 1 && value.asJsonObject().containsKey(base64)) {
            return Base64.getDecoder().decode(value.asJsonObject().getString(base64));
        }
        return value.toString().getBytes("UTF8");
    }

    private Source getPrerequisiteInputAsSource(final ExportDataProvider dataProvider) {
        return new StreamSource(dataProvider.getPrerequisiteInputStream().get());
    }

    private JsonObject getPrerequisiteInputAsJsonObject(final ExportDataProvider dataProvider) throws IOException {
        final byte[] bytes = dataProvider.getPrerequisiteInputStream().get().readAllBytes();
        try (final JsonReader jsonReader = Json.createReader(new ByteArrayInputStream(bytes))) {
            return jsonReader.readObject();
        } catch (final Exception ignore) {
        }
        final String encoded = Base64.getEncoder().encodeToString(bytes);
        return Json.createObjectBuilder().add(base64, encoded).build();
    }

    private URIResolver getResolver(final Path outPath) {
        return (href, base) -> {
            try {
                return new StreamSource(Files.newInputStream(outPath.resolve(href)));
            } catch (final IOException e) {
                logger.severe("resolving URL " + href + " from the XSLT failed: " + e);
                return null;
            }
        };
    }

    private String getLanguageCodeFromEnv() {
        String localeEnvVar = System.getenv().get("LANG");
        if (localeEnvVar != null) {
            if (localeEnvVar.indexOf('.') > 0) {
                localeEnvVar = localeEnvVar.substring(0, localeEnvVar.indexOf('.'));
            }
        } else {
            localeEnvVar = "en";
        }
        return localeEnvVar;
    }

    private Transformer transformer(final String fileName, final int index) {
        try {
            // when running tests, etc.
            final Path path = Paths.get(TransformerExporter.class.getClassLoader().getResource(fileName).toURI());
            return factory.createFromJsonString(Files.readString(path), path.getParent().toString());
        } catch (final Exception e) {
            try {
                // on the server:
                return factory.createFromJsonString(Files.readString(outPath.resolve(fileName)), outPath.toString());
            } catch (final Exception e3) {
                logger.severe("transformer creation failed (using identity transformer): " + e3);
                return factory.createFromJsonString("{\"transformations\":[{}]}");
            }
        }
    }

    private Config config(final String fileName, final int index) {
        try {
            // when running tests, etc.
            final Path path = Paths.get(TransformerExporter.class.getClassLoader().getResource(fileName).toURI());
            return new Config(Files.readString(path));
        } catch (final Exception e) {
            try {
                // on the server:
                outPath = getOutPath(index);
                final String jsoString = Files.readString(outPath.resolve(fileName));
                return new Config(jsoString);
            } catch (final Exception e3) {
                logger.severe("reading config failed (using using default config): " + e3);
                return new Config("{}");
            }
        }
    }

    private Path getOutPath(final int index) throws URISyntaxException, IOException {
        // lookup config dir
        final List<Path> configs = new ArrayList<>();
        final URI jarUri = TransformerExporter.class.getProtectionDomain().getCodeSource().getLocation().toURI();
        final Path jarPath = Paths.get(jarUri.toString().substring("jar:file:".length(),
                jarUri.toString().length() - ".jar!/".length()));
        final Path parent = jarPath.getParent();
        final Set<Path> xmlTransformers = new HashSet<>();
        final Set<Path> pyTransformers = new HashSet<>();
        Files.walk(parent).forEach(x -> {
            if (x.toFile().isDirectory()) {
                if (Files.exists(x.resolve("config.json")) && (Files.exists(x.resolve("transformer.json"))
                        || Files.exists(x.resolve("transformer.xsl")) || Files.exists(x.resolve("transformer.py")))) {
                    configs.add(x);
                    if (Files.exists(x.resolve("transformer.xsl"))) {
                        xmlTransformers.add(x);
                    } else if (Files.exists(x.resolve("transformer.py"))) {
                        pyTransformers.add(x);
                    }
                }
            }
        });
        final Path outPath = configs.size() == 0 ? jarPath : configs.get(index >= configs.size() ? 0 : index);
        isXmlTransformer = xmlTransformers.contains(outPath);
        if (pyTransformers.contains(outPath)) {
            pyScript = Files.readString(outPath.resolve("transformer.py"));
        }

        // copy the transformers and config from the jar if they are not yet in the
        // config dir
        Files.createDirectories(outPath.resolve("js"));
        final FileSystem fs = FileSystems.newFileSystem(jarUri, new HashMap<>());
        List.of(Paths.get("pre_transformer.json"), Paths.get("pre_transformer.json"), Paths.get("js", "flatten.js"),
                Paths.get("js", "map_metadata_fields.js"), Paths.get("config.json"))
                .stream().filter(x -> !Files.exists(outPath.resolve(x))).forEach(x -> {
                    try {
                        Files.copy(fs.getPath(x.toString()), outPath.resolve(x));
                    } catch (final IOException e2) {
                        logger.severe("file copy failed: " + e2);
                    }
                });
        fs.close();
        // return path
        return outPath;
    }
}
