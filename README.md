# Transformer Exporter

Example exporter using the [JSON Transformer](https://github.com/erykKul/json-transformer) library for transformation of metadata JSON to OAI ORE JSON format. The transformation has two steps:
- [pre_transformer.json](/transformer-example/src/main/resources//pre_transformer/pre_transformer.json): changes the metadata citation block into a more JSON Pointer friendly structure. This transformer uses the [map_metadata_fields.js](/transformer-example/src/main/resources/pre_transformer/js/map_metadata_fields.js) JavaScript for the metadata citation block transformation.
- [transformer.json](/transformer-example/src/main/resources/transformer.json): copies the metadata fields from the pre-transformed format into OAI ORE format in the `example` field. It also copies the available for transformations metadata formats into the corresponding fields for demo purposes: `datasetJson`, `datasetORE`, `datasetSchemaDotOrg`, `datasetFileDetails`, `dataCiteXml` and `preTransformed`.This transformer uses the [flatten.js](/transformer-example/src/main/resources/js/flatten.js) JavaScript that (at the end of the transformation) eliminates the empty arrays, replaces arrays having only one element with JSON objects, and filters out the `NULL` values in the `example` field.

This example exporter also contains [config](/transformer-example/src/main/resources/config.json) file with the following fields:
- `formatName`: The name of the format it creates. If this format is already provided by a built-in exporter, this Exporter will override the built-in one. (Note thatexports are cached, so existing metadata export files are not updated immediately.)
- `displayName`: The display name shown in the UI. This field can be localized as shown in the example config by adding the localization suffix, e.g., `_en`, `_fr`, `_fr-CA`, etc.
- `harvestable`: Whether the exported format should be available as an option for Harvesting
- `availableToUsers`: Whether the exported format should be available for download in the UI and API
- `mediaType`: Defines the mime type of the exported format - used when metadata is downloaded, i.e. to trigger an appropriate viewer in the user's browser.

The test contains an example transformation from a [test dataset metadata JSON](/transformer-example/src/test/resources/source.json) into a [transformed document](/transformer-example/src/test/resources/result.json). Also, the [pre-transformed intermediary JSON](/transformer-example/src/test/resources/pre_transformed.json) is included in the test resources.

When the built jar is placed in the `dataverse.spi.exporters.directory` directory on the server, this exporter will look for the transformation files in the exporters' directory subfolder having the same name as the jar file (the part before the `.jar`). It is a good practice to rename the jar file and give it a clear name, e.g., corresponding to the metadata format name from the [config](/transformer-example/src/main/resources/config.json) file. If the transformation files and the config file are not there yet, the exporter will copy them from its resources to that location. You can either place your own transformation files and the config file there before deploying the jar, use the default files as provided by this example exporter, or overwrite them later. Mind that these files are cached and you will need to restart the server after replacing these files. Also the exported metadata is cached, you might need to delete the export cache files before seeing the changes in the exported metadata.

All the transformation logic is contained in the transformer JSON files and the JavaScript files as used by those JSON transformers. The documentation on how to write such transformers can be found on the [JSON Transformer](https://github.com/erykKul/json-transformer?tab=readme-ov-file#json-transformer) library GitHub page.

Suppose now that this example does not work for your installation as intended because your installation does not have the persistent identifiers for individual files, i.e., it has only persistent identifiers on the dataset level. In this case, you can adapt the relevant parts of the [transformer.json](/transformer-example/src/main/resources/transformer.json) to address these differences (and replace the reference to the demo Dataverse with the references to your own installation):

```json
        {
            "sourcePointer": "/persistentUrl",
            "resultPointer": "/@id",
            "expressions": [
                "script(res = 'https://demo.dataverse.org/api/datasets/export?exporter=OAI_ORE&persistentId=' + x)"
            ]
        },
```
```json
        {
            "sourcePointer": "/datasetVersion/files[i]/dataFile",
            "resultPointer": "/ore:describes/ore:aggregates[i]/@id",
            "expressions": [
                "script(res = 'https://demo.dataverse.org/file.xhtml?fileId=' + x.id)"
            ]
        },
        {
            "sourcePointer": "/datasetVersion/files[i]/dataFile",
            "resultPointer": "/ore:describes/ore:aggregates[i]/schema:sameAs",
            "expressions": [
                "script(res = 'https://demo.dataverse.org/api/access/datafile/' + x.id)"
            ]
        },
```
```json
        {
            "sourcePointer": "/datasetVersion/files[i]/dataFile",
            "resultPointer": "/ore:describes/schema:hasPart",
            "expressions": [
                "script(res = 'https://demo.dataverse.org/file.xhtml?fileId=' + x.id)"
            ]
        },
```

However, it is better not to hardcode the installation URL in the transformations. Other available formats may already contain the value you need. This is just an example transformation, the ORE metadata export is already available from the `DataProvider` and contains the fields that are needed here. You can use multiple sources when defining your transformations. The example contains all available sources (`datasetJson`, `datasetORE`, `datasetSchemaDotOrg`, `datasetFileDetails`, `dataCiteXml` and `preTransformed`) and it is recommended to check if they contain the values you need, before attempting building the values yourself (e.g., by using scripts, etc.).
