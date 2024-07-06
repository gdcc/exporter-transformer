# Transformer Exporter for Dataverse

This exporter allows you to have up to 100 exporters using a single pre-built JAR file. You can add new exporters by adding directories into the exporters directory (see the Installation section below) and placing (and editing) the configuration (`config.json`) and the transformation (`transformer.json`, `transformer.py` or `transformer.xsl`, see also the examples below) files in it.

Supported Dataverse versions: 6.0 - recent.

## Installation

If you haven’t already configured it, set the [dataverse-spi-exporters-directory](https://guides.dataverse.org/en/latest/installation/config.html#dataverse-spi-exporters-directory) configuration value first. Then navigate to the configured directory and download the [JAR file](https://repo1.maven.org/maven2/io/github/erykkul/dataverse-transformer-exporter/1.0.5/dataverse-transformer-exporter-1.0.5-jar-with-dependencies.jar) together with the examples you want to try out:

```shell
# download the jar
wget -O transformer-exporter-1.0.5.jar https://repo1.maven.org/maven2/io/github/erykkul/dataverse-transformer-exporter/1.0.5/dataverse-transformer-exporter-1.0.5-jar-with-dependencies.jar
# download the hello-world example
mkdir hello-world
wget -O hello-world/config.json https://raw.githubusercontent.com/erykkul/dataverse-transformer-exporter/main/examples/hello-world/config.json
wget -O hello-world/transformer.json https://raw.githubusercontent.com/erykkul/dataverse-transformer-exporter/main/examples/hello-world/transformer.json
# download the debug example
mkdir debug
wget -O debug/config.json https://raw.githubusercontent.com/erykkul/dataverse-transformer-exporter/main/examples/debug/config.json
wget -O debug/transformer.json https://raw.githubusercontent.com/erykkul/dataverse-transformer-exporter/main/examples/debug/transformer.json
# etc.
```

After restarting the Dataverse, you should be able to use the newly installed exporters (next to the internal exporters):

![image](https://github.com/ErykKul/dataverse-transformer-exporter/assets/101262459/57241319-ce45-40b4-8777-401252f6c4d4)

Each exporter will have at least these files after starting:

![image](https://github.com/ErykKul/dataverse-transformer-exporter/assets/101262459/837405e1-4abe-4470-a9fe-0af3d1ee727d)

All of these files can be edited, if needed. Typically you will only need to edit the `config.json` and the `transformer.json` files. If you want to add more exporters, your own or from the provided examples, just add a new configuration directory in your exporters directory with at least the `config.json` and the `transformer.json`, `transformer.py` or `transformer.xsl` files there. After restarting the servers the newly added exporters should be ready to use.

## Examples

The following examples are provided in the [examples](/examples/) directory:

### Hello World!

Very basic exporter providing always the same output: `{"hello":"World!"}`.

### Debug

This exporter uses only the identity transformation on the provided source document. It lets you to see what fields are available for copying and transforming:
- `datasetJson`: native Dataverse JSON export
- `datasetORE`: ORE Dataverse export
- `datasetSchemaDotOrg`: Schema.org JSON-LD export
- `datasetFileDetails`: file details from the native Dataverse JSON export
- `preTransformed`: JSON-pointer friendly version of the native Dataverse JSON export
- `config`: the content of the `config.json`

### Short example

This exporter copies only the title, the author names and the file download URL to the output.

### Javascript transformer

The same exporter as the "Short example", but it uses JavaScript instead of copy transformations.

### Croissant

This exporter is entirely based on the [Croissant Exporter for Dataverse](https://github.com/gdcc/exporter-croissant). It is simply a port of that exporter into JavaScript that is bundled into a ready to use transformer. It is also a great example to start from when writing your own exporters.

### Basic RO-Crate

This exporter transforms the output from the Schema.org exporter into an RO-Crate compatible output.

### Transformer generated with Python

This exporter is based on the [Customizable RO-Crate Metadata Exporter for Dataverse](https://github.com/gdcc/exporter-ro-crate). You can edit the provided [CSV file](/examples/generated-with-python/dataverse2ro-crate.csv) and rerun the Python script to overwrite the default `transformer.json`:

```shell
python3 csv2transformer.py
```

After copying the resulting `transformer.json`, together with the provided `config.jar`, you will have a customized RO-Crate exporter (listed as "CSV RO-Crate" by default).

### Debug XML

This exporter outputs the XML version of the native JSON format that can be transformed with XSLT.

### Short example XML

This exporter copies only the title, the author names and the filenames of the dataset version, and outputs them in an XML document.

### Debug written in Python

This exporter is identical to the Debug example in its output (the only difference is that it is written in py) and it lets you to see what fields are available for copying and transforming:
- `datasetJson`: native Dataverse JSON export
- `datasetORE`: ORE Dataverse export
- `datasetSchemaDotOrg`: Schema.org JSON-LD export
- `datasetFileDetails`: file details from the native Dataverse JSON export
- `preTransformed`: JSON-pointer friendly version of the native Dataverse JSON export
- `config`: the content of the `config.json`

### Short example written in Python

This exporter copies only the title, the author names and the filenames of the dataset version, and outputs them in a JSON document. It is written in Python.

### HTML example written in Python

This exporter takes JSON input from a prerequisite exporter (`short_example_py` by default), and displays it as HTML. It is written in Python. In order to change the JSON input for this exporter, change the `prerequisiteFormatName` value in the `config.json` to the format name of the exporter you wish to use as input.

### DDI PDF codebook

This exporter is entirely based on the [DDI PDF Exporter](https://github.com/gdcc/exporter-ddipdf). It is simply a port of that exporter into Python (Jython). It illustrates how to convert XML input to PDF in an exporter.

## Developer guide

The easiest way to start is to write JavasCript code. You can use the provided [Croissant](/examples/croissant/js/croissant.js) code as the start point. You will need to restart the server after changing that code. Note that the exporters use caching, you will need to either to wait until the cache is expired or delete the cached exporter output manually to see the changes.

The JavaScript supported by the transformer exporter is as provided by the [Project Nashorn](https://openjdk.org/projects/nashorn/), you can only use the syntax provided by that project. Additional limitation is that the multiple line statements are not supported. This could be circumvented by using a minimizer, or simply by using only single line statements (empty lines, comments, etc. are fine to include in the JavaScript files). Finally, you can access these Java classes from your scripts:
- `Map`: `java.util.LinkedHashMap`
- `Set`: `java.util.LinkedHashSet`
- `List`: `java.util.ArrayList`
- `Collectors`: `java.util.stream.Collectors`
- `JsonValue`: `jakarta.json.JsonValue`

You can also try writing the transformations using the transformation language as described [here](https://github.com/ErykKul/json-transformer). It is a preferred way for writing straight-forward exporters, for example, when you only need to add one or more fields to an already existing exporter format. In that case, you could use the identity transformation followed by simple copy transformations. You can also start from an already existing example and add new copy, remove, etc., transformations at the end of the `transformer.json` file.

You can also write XML transformations in a similar way, but using the XSLT instead of JSON-transformations, as illustrated in the provided XML examples.

Finally, you can also write your transformers as Python code. You can start from the provided example that can also be run as test:

```shell
mvn test -Dtest="TransformerExporterTest#testPythonScript"
```

You can start by changing the code in the [transformer.py](/src/test/resources/transformer.py), shown below, and testing your code until the desired outcome is achieved (see also [py-input.json](/src/test/resources/py-input.json) and [py-result.json](/src/test/resources/py-result.json)). When you are done, just place the new `transformer.py` together with a `config.json` files in a new folder in the exporters directory (make sure that the transformer-exporter JAR file is also placed in the exporters directory). After restarting the server, your new exporter should be ready to use.

```py
res["title"] = x["preTransformed"]["datasetVersion"]["metadataBlocks"]["citation"]["title"][0]

res["author"] = []
for author in x["preTransformed"]["datasetVersion"]["metadataBlocks"]["citation"]["author"]:
    res["author"].append(author["authorName"][0])

res["files"] = []
for distribution in x["datasetSchemaDotOrg"]["distribution"]:
    res["files"].append(distribution["contentUrl"])
```

Note that you can also use Java classes from your Python code, as explained on the [Jython](https://www.jython.org/) website (the library used by this exporter for the Python language interpretation), e.g.:

```py
from java.lang import System # Java import

print('Running on Java version: ' + System.getProperty('java.version'))
print('Unix time from Java: ' + str(System.currentTimeMillis()))
```

See also the documentation from [Jython](https://www.jython.org/).