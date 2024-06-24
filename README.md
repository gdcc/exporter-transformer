# Transformer Exporter


## Installation

If not yet configured, set the [dataverse-spi-exporters-directory](https://guides.dataverse.org/en/latest/installation/config.html#dataverse-spi-exporters-directory) configuration value first. Then `cd` into that directory and download the [jar file](https://repo1.maven.org/maven2/io/github/erykkul/dataverse-transformer-exporter/1.0.1/dataverse-transformer-exporter-1.0.1-jar-with-dependencies.jar) together with the examples you want to try out:

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

After restarting the Dataverse, you should be able to use the newly installed RO-Crate exporter:

![image](https://github.com/ErykKul/dataverse-transformer-exporter/assets/101262459/27203e12-5a38-45cb-bf7f-eaa76d5c432a)