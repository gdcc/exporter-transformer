# Transformer Exporter
This Dataverse exporter allows you to have up to a 100 exporters using one single pre-built jar. All you need to do is to download that jar into your exporters directory and create an other directory within the exporters directory (up to 100 of them) containing at least a `config.json` and a `transformer.json` files. Edit these files to achieve the exporter you need. Use the provided [examples](/examples/) and the developer guide section as inspiration.

## Installation

If not yet configured, set the [dataverse-spi-exporters-directory](https://guides.dataverse.org/en/latest/installation/config.html#dataverse-spi-exporters-directory) configuration value first. Then `cd` into that directory you configured and download the [jar file](https://repo1.maven.org/maven2/io/github/erykkul/dataverse-transformer-exporter/1.0.1/dataverse-transformer-exporter-1.0.1-jar-with-dependencies.jar) together with the examples you want to try out:

```shell
# download the jar
wget -O transformer-exporter-1.0.1.jar https://repo1.maven.org/maven2/io/github/erykkul/dataverse-transformer-exporter/1.0.1/dataverse-transformer-exporter-1.0.1-jar-with-dependencies.jar
# download the hello-world example
mkdir hello-world
wget -O hello-world/config.json https://raw.githubusercontent.com/erykkul/dataverse-transformer-exporter/main/examples/hello-world/config.json
wget -O hello-world/transformer.json https://raw.githubusercontent.com/erykkul/dataverse-transformer-exporter/main/examples/hello-world/transformer.json
# download the debug example
mkdir debug
wget -O debug/config.json https://raw.githubusercontent.com/erykkul/dataverse-transformer-exporter/main/examples/debug/config.json
wget -O debug/transformer.json https://raw.githubusercontent.com/erykkul/dataverse-transformer-exporter/main/examples/debug/transformer.json
# download the short-example example
mkdir short-example
wget -O short-example/config.json https://raw.githubusercontent.com/erykkul/dataverse-transformer-exporter/main/examples/short-example/config.json
wget -O short-example/transformer.json https://raw.githubusercontent.com/erykkul/dataverse-transformer-exporter/main/examples/short-example/transformer.json
# download the javascript-transformer example
mkdir javascript-transformer
wget -O javascript-transformer/config.json https://raw.githubusercontent.com/erykkul/dataverse-transformer-exporter/main/examples/javascript-transformer/config.json
wget -O javascript-transformer/transformer.json https://raw.githubusercontent.com/erykkul/dataverse-transformer-exporter/main/examples/javascript-transformer/transformer.json
mkdir javascript-transformer/js
wget -O javascript-transformer/js/short_example.js https://raw.githubusercontent.com/erykkul/dataverse-transformer-exporter/main/examples/javascript-transformer/js/short_example.js
# download the croissant example
mkdir croissant
wget -O croissant/config.json https://raw.githubusercontent.com/erykkul/dataverse-transformer-exporter/main/examples/croissant/config.json
wget -O croissant/transformer.json https://raw.githubusercontent.com/erykkul/dataverse-transformer-exporter/main/examples/croissant/transformer.json
mkdir croissant/js
wget -O croissant/js/croissant.js https://raw.githubusercontent.com/erykkul/dataverse-transformer-exporter/main/examples/croissant/js/croissant.js
# download the basic-ro-crate example
mkdir basic-ro-crate
wget -O basic-ro-crate/config.json https://raw.githubusercontent.com/erykkul/dataverse-transformer-exporter/main/examples/basic-ro-crate/config.json
wget -O basic-ro-crate/transformer.json https://raw.githubusercontent.com/erykkul/dataverse-transformer-exporter/main/examples/basic-ro-crate/transformer.json
# download the generated-with-python example
mkdir generated-with-python
wget -O generated-with-python/config.json https://raw.githubusercontent.com/erykkul/dataverse-transformer-exporter/main/examples/generated-with-python/config.json
wget -O generated-with-python/transformer.json https://raw.githubusercontent.com/erykkul/dataverse-transformer-exporter/main/examples/generated-with-python/transformer.json
```

After restarting the Dataverse, you should be able to use the newly installed exporters (next to the internal exporters):

![image](https://github.com/ErykKul/dataverse-transformer-exporter/assets/101262459/57241319-ce45-40b4-8777-401252f6c4d4)

Each exporter will have at least these files after starting:

![image](https://github.com/ErykKul/dataverse-transformer-exporter/assets/101262459/837405e1-4abe-4470-a9fe-0af3d1ee727d)

All of these files can be edited, if needed. Typically you will only need to edit the `config.json` and the `transformation.json` files.

## Examples

The following examples are provided in the [examples](/examples/) folder:

### Hello World!

Very basic exporter providing always the same output: `{"hello":"World!"}`.

### Debug

This one is important as it uses only the identity transformation on the provided source document. It lets you to see what fields are available for copying and transforming:
- datasetJson (native Dataverse JSON export)
- datasetORE (ORE Dataverse export)
- datasetSchemaDotOrg (Schema.org JSON-LD export)
- datasetFileDetails (files part from the native Dataverse JSON export)
- preTransformed (JSON-pointer friendly version of the native Dataverse JSON export)
- config (the content of the config.json)

## Short example

Another basic example. It copies only the title, the author names and the file download URL to the output.

# Javascript transformer

The same exporter as short-example, but it uses JavaScript instead of a transformer. It illustrates how to use basic JavaScript code as transformations.

# Croissant

This exporter is entirely based on the [Croissant Exporter for Dataverse](https://github.com/gdcc/exporter-croissant). It is simply a port of that exporter into JavaScript that is bundled into a ready to use transformer. It is also a great example to start from when writing your own exporter.

# Basic RO-Crate

This exporter transforms the output from the Schema.org exporter into an RO-Crate compatible output.

# Transformer generated with Python

This exporter is based on the [Customizable RO-Crate Metadata Exporter for Dataverse](https://github.com/gdcc/exporter-ro-crate). You can edit the in the example provided [CSV](/examples/generated-with-python/dataverse2ro-crate.csv) and rerun the Python script to overwrite the default `transformer.json` provided in that example:

```shell
python3 csv2transformer.py
```

After copying the resulting `transformer.json`, together with the provided `config.jar` (you can edit in that file the default `CSV RO-Crate` format name to e.g., `Custom RO-Crate`), you will have a customized RO-Crate exporter.

## Developer guide

The easiest way to start is to write JavasCript code. You can use the provided [Croissant](/examples/croissant/js/croissant.js) code as the start point. Note that the exporters use caching, you will need either to wait until the cache is expired or delete the cached exporter output manually after changing that code to see the result. Also, the JavaScript supported by the transformer exporter is as provided by the [Project Nashorn](https://openjdk.org/projects/nashorn/), you can only use the syntax provided by that project. Additional limitation is that the multiple line statements are not supported. This could be circumvented by using a minimizer, or simply using only single line statements. The best way to start is to first take a look at the provided examples. Finally, you can also access mapped Java classes from the scripts:
- `Map`: `java.util.LinkedHashMap`
- `Set`: `java.util.LinkedHashSet`
- `List`: `java.util.ArrayList`
- `Collectors`: `java.util.stream.Collectors`
- `JsonValue`: `jakarta.json.JsonValue`

You can also try writing the transformations using the language as described [here](https://github.com/ErykKul/json-transformer). It is preferred way for writing straight-forward exporters, for example, when you only need to add one or more fields to already existing exporter format. In that case, you can use the identity transformation followed by a simple copy transformations. See the provided examples for the inspiration.