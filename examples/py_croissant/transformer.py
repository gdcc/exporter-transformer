def get_bibtex():
    identifier = x["datasetJson"]["identifier"]
    ore_describes = x["datasetORE"]["ore:describes"]
    publication_year = ore_describes["schema:datePublished"][0:4]

    creator_array = x["datasetSchemaDotOrg"]["creator"]
    creators_formatted = creator_array[0]["name"] if len(creator_array) > 0 else ""
    for i in range(1, len(creator_array)):
        creators_formatted = creators_formatted + " and " + creator_array[i]["name"]

    publisher = x["datasetSchemaDotOrg"]["publisher"]["name"]
    title = x["datasetSchemaDotOrg"]["name"]
    pid_as_url = ore_describes["@id"]

    sb = ""
    sb = sb + "@data{" + identifier + "_" + publication_year + ","
    sb = sb + "author = {" + creators_formatted + "},"
    sb = sb + "publisher = {" + publisher + "},"
    sb = sb + "title = {" + title + "},"
    sb = sb + "year = {" + publication_year + "},"
    sb = sb + "url = {" + pid_as_url + "}"
    sb = sb + "}"
    return sb


def get_numeric_type(variable_interval_type):
    if variable_interval_type == "discrete":
        return "sc:Integer"
    if variable_interval_type == "contin":
        return "sc:Float"
    return "sc:Text"


res = {}

context = {}
context["@language"] = "en"
context["@vocab"] = "https://schema.org/"
context["citeAs"] = "cr:citeAs"
context["column"] = "cr:column"
context["conformsTo"] = "dct:conformsTo"
context["cr"] = "http://mlcommons.org/croissant/"
context["rai"] = "http://mlcommons.org/croissant/RAI/"
context["data"] = {"@id": "cr:data", "@type": "@json"}
context["dataType"] = {"@id": "cr:dataType", "@type": "@vocab"}
context["dct"] = "http://purl.org/dc/terms/"
context["examples"] = {"@id": "cr:examples", "@type": "@json"}
context["extract"] = "cr:extract"
context["field"] = "cr:field"
context["fileProperty"] = "cr:fileProperty"
context["fileObject"] = "cr:fileObject"
context["fileSet"] = "cr:fileSet"
context["format"] = "cr:format"
context["includes"] = "cr:includes"
context["isLiveDataset"] = "cr:isLiveDataset"
context["jsonPath"] = "cr:jsonPath"
context["key"] = "cr:key"
context["md5"] = "cr:md5"
context["parentField"] = "cr:parentField"
context["path"] = "cr:path"
context["recordSet"] = "cr:recordSet"
context["references"] = "cr:references"
context["regex"] = "cr:regex"
context["repeated"] = "cr:repeated"
context["replace"] = "cr:replace"
context["sc"] = "https://schema.org/"
context["separator"] = "cr:separator"
context["source"] = "cr:source"
context["subField"] = "cr:subField"
context["transform"] = "cr:transform"
context["wd"] = "https://www.wikidata.org/wiki/"
res["@context"] = context

res["@type"] = "sc:Dataset"
res["conformsTo"] = "http://mlcommons.org/croissant/1.0"

describes = x["datasetORE"]["ore:describes"]
res["name"] = describes["title"]
res["url"] = describes["@id"]
res["creator"] = x["datasetSchemaDotOrg"]["creator"]
res["description"] = x["datasetSchemaDotOrg"]["description"]
res["keywords"] = x["datasetSchemaDotOrg"]["keywords"]
res["license"] = x["datasetSchemaDotOrg"]["license"]
res["datePublished"] = x["datasetSchemaDotOrg"]["datePublished"]
res["dateModified"] = x["datasetSchemaDotOrg"]["dateModified"]
res["includedInDataCatalog"] = x["datasetSchemaDotOrg"]["includedInDataCatalog"]
res["publisher"] = x["datasetSchemaDotOrg"]["publisher"]
res["version"] = describes["schema:version"]
res["citeAs"] = get_bibtex()

funder = x["datasetSchemaDotOrg"].get("funder")
if funder:
    res["funder"] = funder

spatial_coverage = x["datasetSchemaDotOrg"].get("spatialCoverage")
if spatial_coverage:
    res["spatialCoverage"] = spatial_coverage

ore_files = describes["ore:aggregates"]
distribution = []
record_set = []

for i in range(len(x["datasetFileDetails"])):
    file_details = x["datasetFileDetails"][i]
    filename = file_details.get("originalFileName")
    if not filename:
        filename = file_details["filename"]
    file_format = file_details.get("originalFileFormat")
    if not file_format:
        file_format = file_details["contentType"]
    file_size = file_details.get("originalFileSize")
    if not file_size:
        file_size = file_details["filesize"]

    checksum = file_details["checksum"]
    checksum_type = checksum["type"].lower()
    checksum_value = checksum["value"]
    file_id = filename
    directory_label = ore_files[i].get("dvcore:directoryLabel")
    if directory_label:
        file_id = directory_label + "/" + filename

    dist = {}
    dist["@type"] = "cr:FileObject"
    dist["@id"] = file_id
    dist["name"] = filename
    dist["encodingFormat"] = file_format
    dist[checksum_type] = checksum_value
    dist["contentSize"] = str(file_size)
    dist["description"] = file_details.get("description", "")
    dist["contentUrl"] = ore_files[i]["schema:sameAs"]
    distribution.append(dist)
    
    data_tables = file_details.get("dataTables")
    if not data_tables:
        data_tables = []
    
    for j in range(len(data_tables)):
        data_table_object = data_tables[j]
        data_variables = data_table_object["dataVariables"]
        field_set_array = []
        
        for k in range(len(data_variables)):
            data_variable_object = data_variables[k]
            variable_id = str(data_variable_object["id"])
            variable_format_type = data_variable_object["variableFormatType"]
            variable_interval_type = data_variable_object["variableIntervalType"]
            data_type = None
            
            if variable_format_type == "CHARACTER":
                data_type = "sc:Text"
            elif variable_format_type == "NUMERIC":
                data_type = get_numeric_type(variable_interval_type)
            
            field_set = {}
            field_set["@type"] = "cr:Field"
            field_set["name"] = data_variable_object["name"]
            field_set["description"] = data_variable_object["label"]
            field_set["dataType"] = data_type
            field_set["source"] = {"@id": variable_id, "fileObject": {"@id": file_id}}
            field_set_array.append(field_set)
        
        record_set_content = {"@type": "cr:RecordSet"}
        record_set_content["field"] = field_set_array
        record_set.append(record_set_content)

citation = x["datasetSchemaDotOrg"].get("citation")
if citation:
    res["citation"] = citation

temporal_coverage = x["datasetSchemaDotOrg"].get("temporalCoverage")
if temporal_coverage:
    res["temporalCoverage"] = temporal_coverage

if len(distribution) != 0:
    res["distribution"] = distribution

if len(record_set) != 0:
    res["recordSet"] = record_set
