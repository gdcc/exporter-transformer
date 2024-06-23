function getBibtex() {
    var identifier = x.datasetJson.identifier
    var oreDescribes = x.datasetORE["ore:describes"]
    var publicationYear = oreDescribes["schema:datePublished"].substring(0, 4)

    var creatorArray = x.datasetSchemaDotOrg.creator
    var creatorsFormatted = creatorArray.length > 0 ? creatorArray[0] : ""
    for (i = 1; i < creatorArray.length; i++) {
        creatorsFormatted = creatorsFormatted + " and " + creatorArray[i].name
    }
    
    var publisher = x.datasetSchemaDotOrg.publisher.name
    var title = x.datasetSchemaDotOrg.name
    var pidAsUrl = oreDescribes["@id"]
    
    var sb = ""
    sb = sb + "@data{" + identifier + "_" + publicationYear + ","
    sb = sb + "author = {" + creatorsFormatted + "},"
    sb = sb + "publisher = {" + publisher + "},"
    sb = sb + "title = {" + title + "},"
    sb = sb + "year = {" + publicationYear + "},"
    sb = sb + "url = {" + pidAsUrl + "}"
    sb = sb + "}"
    return sb
}

function getNumericType(variableIntervalType) {
    if (variableIntervalType === "discrete") {
        return "sc:Integer"
    }
    if (variableIntervalType === "contin") {
        return "sc:Float"
    }
    return "sc:Text"
}

res = {}

var context = {}
context["@language"] = "en"
context["@vocab"] = "https://schema.org/"
context["citeAs"] = "cr:citeAs"
context["column"] = "cr:column"
context["conformsTo"] = "dct:conformsTo"
context["cr"] = "http://mlcommons.org/croissant/"
context["rai"] = "http://mlcommons.org/croissant/RAI/"
context["data"] = { "@id": "cr:data",  "@type": "@json" }
context["dataType"] = { "@id": "cr:dataType", "@type": "@vocab" }
context["dct"] = "http://purl.org/dc/terms/"
context["examples"] = { "@id": "cr:examples", "@type": "@json" }
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
res.conformsTo = "http://mlcommons.org/croissant/1.0"

var describes = x.datasetORE["ore:describes"]
res["name"] = describes["title"]
res["url"] = describes["@id"]
res["creator"] = x.datasetSchemaDotOrg["creator"]
res["description"] = x.datasetSchemaDotOrg["description"]
res["keywords"] = x.datasetSchemaDotOrg["keywords"]
res["license"] = x.datasetSchemaDotOrg["license"]
res["datePublished"] = x.datasetSchemaDotOrg["datePublished"]
res["dateModified"] = x.datasetSchemaDotOrg["dateModified"]
res["includedInDataCatalog"] = x.datasetSchemaDotOrg["includedInDataCatalog"]
res["publisher"] = x.datasetSchemaDotOrg["publisher"]
res["version"] = describes["schema:version"]
res["citeAs"] = getBibtex()

var funder = x.datasetSchemaDotOrg["funder"]
if (funder) {
    res["funder"] = funder
}

var spatialCoverage = x.datasetSchemaDotOrg["spatialCoverage"]
if (spatialCoverage) {
    res["spatialCoverage"] = spatialCoverage
}

var oreFiles = describes["ore:aggregates"]
var distribution = new List()
var recordSet = new List()

for (i = 0; i < x.datasetFileDetails.length; i++) {
    var fileDetails = x.datasetFileDetails[i]
    var filename = fileDetails["originalFileName"]
    if (!filename) {
        filename = fileDetails["filename"]
    }
    var fileFormat = fileDetails["originalFileFormat"]
    if (!fileFormat) {
        fileFormat = fileDetails["contentType"]
    }
    var fileSize = fileDetails["originalFileSize"]
    if (!fileSize) {
        fileSize = fileDetails["filesize"]
    }

    var checksum = fileDetails["checksum"]
    var checksumType = checksum["type"].toLowerCase()
    var checksumValue = checksum["value"]
    var fileId = filename
    var directoryLabel = oreFiles[i]["dvcore:directoryLabel"]
    if (directoryLabel) {
        fileId = directoryLabel + "/" + filename
    }

    var dist = {}
    dist["@type"] = "cr:FileObject"
    dist["@id"] = fileId
    dist["name"] = filename
    dist["encodingFormat"] = fileFormat
    dist[checksumType] = checksumValue
    dist["contentSize"] = fileSize.toString()
    dist["description"] = fileDetails["description"]
    dist["contentUrl"] = oreFiles[i]["schema:sameAs"]
    distribution.add(dist)
    var dataTables = fileDetails["dataTables"]
    if (!dataTables) {
        dataTables = new List()
    }
    for (j = 0; j < dataTables.length; j++) {
        var dataTableObject = dataTables[j]
        var dataVariables = dataTableObject["dataVariables"]
        var fieldSetArray = new List()
        for (k = 0; k < dataVariables.length; k++) {
            var dataVariableObject = dataVariables[k]
            var variableId = dataVariableObject["id"].toString()
            var variableFormatType = dataVariableObject["variableFormatType"]
            var variableIntervalType = dataVariableObject["variableIntervalType"]
            var dataType = null
            if (variableFormatType === "CHARACTER") {
                dataType = "sc:Text"
            } else if (variableFormatType === "NUMERIC") {
                dataType = getNumericType(variableIntervalType)
            }
            filedSet = {}
            filedSet["@type"] = "cr:Field"
            filedSet["name"] = dataVariableObject["name"]
            filedSet["description"] = dataVariableObject["label"]
            filedSet["dataType"] = dataType
            filedSet["source"] = {"@id": variableId, "fileObject": {"@id": fileId}}
            fieldSetArray.add(fieldSet)
        }
        var recordSetContent = {"@type": "cr:RecordSet"}
        recordSetContent["field"] = fieldSetArray
        recordSet.add(recordSetContent)
    }
}

var citation = x.datasetSchemaDotOrg["citation"]
if (citation) {
    res["citation"] = citation
}
var temporalCoverage = x.datasetSchemaDotOrg["temporalCoverage"]
if (temporalCoverage) {
    res["temporalCoverage"] = temporalCoverage
}
if (distribution.length !== 0) {
    res["distribution"] = distribution
}
if (recordSet.length !== 0) {
    res["recordSet"] = recordSet
}