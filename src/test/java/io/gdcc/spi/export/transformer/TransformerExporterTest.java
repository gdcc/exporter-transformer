package io.gdcc.spi.export.transformer;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.io.ByteArrayOutputStream;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.OutputStream;
import java.io.StringReader;
import java.net.URISyntaxException;
import java.util.Locale;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

import io.gdcc.spi.export.ExportDataProvider;
import jakarta.json.Json;
import jakarta.json.JsonArray;
import jakarta.json.JsonObject;
import jakarta.json.JsonReader;

public class TransformerExporterTest {

    static TransformerExporter transformerExporter;
    static OutputStream outputStream;
    static ExportDataProvider dataProvider;

    public static JsonObject parse(final String fileName) throws FileNotFoundException, URISyntaxException {
        final String f = TransformerExporterTest.class.getClassLoader().getResource(fileName).getFile();
        final JsonReader jsonReader = Json.createReader(new FileReader(f));
        final JsonObject object = jsonReader.readObject();
        jsonReader.close();
        return object;
    }

    @BeforeAll
    public static void setUp() {
        transformerExporter = new TransformerExporter();
        outputStream = new ByteArrayOutputStream();
        dataProvider = new ExportDataProvider() {
            @Override
            public JsonObject getDatasetJson() {
                try {
                    return parse("source.json");
                } catch (final Exception e) {
                    throw new RuntimeException(e);
                }
            }

            @Override
            public JsonObject getDatasetORE() {
                return Json.createObjectBuilder().build();
            }

            @Override
            public JsonArray getDatasetFileDetails() {
                return Json.createArrayBuilder().build();
            }

            @Override
            public JsonObject getDatasetSchemaDotOrg() {
                return Json.createObjectBuilder().build();
            }

            @Override
            public String getDataCiteXml() {
                return "";
            }
        };
    }

    @AfterEach
    public void tearDown() {
    }

    @Test
    public void testGetFormatName() {
        assertEquals("transformer_json", transformerExporter.getFormatName());
    }

    @Test
    public void testGetDisplayName() {
        assertEquals("Transformer example", transformerExporter.getDisplayName(Locale.US));
        assertEquals("Exemple de transformer", transformerExporter.getDisplayName(Locale.FRANCE));
        assertEquals("Exemple de transformateur", transformerExporter.getDisplayName(Locale.CANADA_FRENCH));
        assertEquals("Default transformer example", transformerExporter.getDisplayName(Locale.GERMAN));
    }

    @Test
    public void testIsHarvestable() {
        assertEquals(false, transformerExporter.isHarvestable());
    }

    @Test
    public void testIsAvailableToUsers() {
        assertEquals(true, transformerExporter.isAvailableToUsers());
    }

    @Test
    public void testGetMediaType() {
        assertEquals("application/json", transformerExporter.getMediaType());
    }

    @Test
    public void testExportDataset() throws Exception {
        transformerExporter.exportDataset(dataProvider, outputStream);
        final String expected = parse("result.json").toString();
        System.out.println(outputStream.toString());
        final JsonReader jsonReader = Json.createReader(new StringReader(outputStream.toString()));
        final JsonObject actual = jsonReader.readObject();
        jsonReader.close();
        assertEquals(expected.trim(), actual.get("example").toString().trim());
    }

}
