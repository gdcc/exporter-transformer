# Transformer Exporter


## Installation

If not yet configured, set the [dataverse-spi-exporters-directory](https://guides.dataverse.org/en/latest/installation/config.html#dataverse-spi-exporters-directory) configuration value first. Then `cd` into that directory and make the new `rocrate` directory:

```shell
mkdir rocrate
```

Download the [config.json](/config.json) and the [transformer.json](/transformer.json) files into that new directory:

```shell
wget -O rocrate/config.json https://raw.githubusercontent.com/erykkul/exporter-ro-crate/main/config.json
wget -O rocrate/transformer.json https://raw.githubusercontent.com/erykkul/exporter-ro-crate/main/transformer.json
```

Download the [dataverse-transformer-exporter](https://github.com/ErykKul/dataverse-transformer-exporter/) jar file from the [Maven Central repository](https://central.sonatype.com/artifact/io.github.erykkul/dataverse-transformer-exporter/versions) and save it under the same name (`rocrate.jar`) as the newly created directory (`rocrate`):

```shell
wget -O rocrate.jar https://repo1.maven.org/maven2/io/github/erykkul/dataverse-transformer-exporter/1.0.0/dataverse-transformer-exporter-1.0.0-jar-with-dependencies.jar
```

After restarting the Dataverse, you should be able to use the newly installed RO-Crate exporter:

![image](https://github.com/ErykKul/exporter-ro-crate/assets/101262459/27203e12-5a38-45cb-bf7f-eaa76d5c432a)