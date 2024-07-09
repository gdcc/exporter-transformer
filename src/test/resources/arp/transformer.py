res["@context"] = [
    "https://w3id.org/ro/crate/1.1/context",
    {
        "country": "https://dataverse.org/schema/geospatial/country",
        "dateOfCollectionStart": "https://dataverse.org/schema/citation/dateOfCollectionStart",
        "subject": "http://purl.org/dc/terms/subject",
        "distributionDate": "https://dataverse.org/schema/citation/distributionDate",
        "geographicBoundingBox": "https://dataverse.org/schema/geospatial/geographicBoundingBox",
        "language": "http://purl.org/dc/terms/language",
        "contributorName": "https://dataverse.org/schema/citation/contributorName",
        "datasetContactName": "https://dataverse.org/schema/citation/datasetContactName",
        "eastLongitude": "https://dataverse.org/schema/geospatial/eastLongitude",
        "producerAbbreviation": "https://dataverse.org/schema/citation/producerAbbreviation",
        "publication": "http://purl.org/dc/terms/isReferencedBy",
        "unitOfAnalysis": "https://dataverse.org/schema/socialscience/unitOfAnalysis",
        "datasetContactAffiliation": "https://dataverse.org/schema/citation/datasetContactAffiliation",
        "journalArticleType": "https://dataverse.org/schema/journal/journalArticleType",
        "keyword": "https://dataverse.org/schema/citation/keyword",
        "timePeriodCoveredStart": "https://dataverse.org/schema/citation/timePeriodCoveredStart",
        "otherIdValue": "https://dataverse.org/schema/citation/otherIdValue",
        "dateOfCollectionEnd": "https://dataverse.org/schema/citation/dateOfCollectionEnd",
        "otherIdAgency": "https://dataverse.org/schema/citation/otherIdAgency",
        "publicationIDType": "http://purl.org/spar/datacite/ResourceIdentifierScheme",
        "author": "http://purl.org/dc/terms/creator",
        "publicationIDNumber": "http://purl.org/spar/datacite/ResourceIdentifier",
        "publicationCitation": "http://purl.org/dc/terms/bibliographicCitation",
        "authorAffiliation": "https://dataverse.org/schema/citation/authorAffiliation",
        "productionPlace": "https://dataverse.org/schema/citation/productionPlace",
        "producerAffiliation": "https://dataverse.org/schema/citation/producerAffiliation",
        "authorName": "https://dataverse.org/schema/citation/authorName",
        "grantNumberAgency": "https://dataverse.org/schema/citation/grantNumberAgency",
        "producer": "https://dataverse.org/schema/citation/producer",
        "depositor": "https://dataverse.org/schema/citation/depositor",
        "contributorType": "https://dataverse.org/schema/citation/contributorType",
        "publicationURL": "https://schema.org/distribution",
        "keywordValue": "https://dataverse.org/schema/citation/keywordValue",
        "geographicCoverage": "https://dataverse.org/schema/geospatial/geographicCoverage",
        "dsDescriptionValue": "https://dataverse.org/schema/citation/dsDescriptionValue",
        "characteristicOfSources": "https://dataverse.org/schema/citation/characteristicOfSources",
        "title": "http://purl.org/dc/terms/title",
        "contributor": "http://purl.org/dc/terms/contributor",
        "otherGeographicCoverage": "https://dataverse.org/schema/geospatial/otherGeographicCoverage",
        "kindOfData": "http://rdf-vocabulary.ddialliance.org/discovery#kindOfData",
        "southLongitude": "https://dataverse.org/schema/geospatial/southLongitude",
        "timePeriodCoveredEnd": "https://dataverse.org/schema/citation/timePeriodCoveredEnd",
        "topicClassValue": "https://dataverse.org/schema/citation/topicClassValue",
        "title_hu": "http://purl.org/dc/terms/title",
        "dsDescription_hu": "https://dataverse.org/schema/citation/dsDescription_hu",
        "westLongitude": "https://dataverse.org/schema/geospatial/westLongitude",
        "otherId": "https://dataverse.org/schema/citation/otherId",
        "dateOfCollection": "https://dataverse.org/schema/citation/dateOfCollection",
        "producerName": "https://dataverse.org/schema/citation/producerName",
        "datasetContact": "https://dataverse.org/schema/citation/datasetContact",
        "topicClassification": "https://dataverse.org/schema/citation/topicClassification",
        "datasetContactEmail": "https://dataverse.org/schema/citation/datasetContactEmail",
        "geographicUnit": "https://dataverse.org/schema/geospatial/geographicUnit",
        "dateOfDeposit": "http://purl.org/dc/terms/dateSubmitted",
        "dsDescription": "https://dataverse.org/schema/citation/dsDescription",
        "grantNumberValue": "https://dataverse.org/schema/citation/grantNumberValue",
        "northLongitude": "https://dataverse.org/schema/geospatial/northLongitude",
        "dsDescriptionValue_hu": "https://dataverse.org/schema/citation/dsDescriptionValue_hu",
        "timePeriodCovered": "https://schema.org/temporalCoverage",
        "grantNumber": "https://schema.org/sponsor",
    },
]

from java.util import ArrayList, LinkedHashMap, List, Map

datasetVersion = x["preTransformed"]["datasetVersion"]
root = LinkedHashMap()
about = LinkedHashMap()
res["@graph"] = ArrayList()
res["@graph"].append(root)
res["@graph"].append(about)
root["@id"] = "./"
about["about"] = {"@id": "./"}
about["@id"] = "ro-crate-metadata.json"
about["@type"] = "CreativeWork"
root["@type"] = "Dataset"
root["@arpPid"] = datasetVersion["datasetPersistentId"]
if datasetVersion.containsKey("license") and datasetVersion["license"].containsKey(
    "uri"
):
    root["license"] = {"@id": datasetVersion["license"]["uri"]}
root["datePublished"] = datasetVersion["publicationDate"]

hdl_id = "https://w3id.org/arp/ro-id/" + datasetVersion["datasetPersistentId"] + "/"
idx = 0


def refField(fieldName, field):
    global idx
    idx += 1
    id = hdl_id + fieldName + "/" + str(idx)
    if not field.containsKey("name"):
        name = " ; ".join(field.values())
        field["name"] = name
    field["@id"] = id
    field["@type"] = fieldName
    res["@graph"].append(field)
    return {"@id": id}


hasPart = ArrayList()
files = []
if x["datasetSchemaDotOrg"].containsKey("distribution"):
    files = x["datasetSchemaDotOrg"]["distribution"]
for i, file in enumerate(files):
    if x["datasetFileDetails"][i].containsKey("originalFileSize"):
        file["contentSize"] = x["datasetFileDetails"][i]["originalFileSize"]
    file["hash"] = x["datasetFileDetails"][i]["md5"]
    if not file.containsKey("@id"):
        file["@id"] = file["contentUrl"]
    res["@graph"].append(file)
    hasPart.append({"@id": file["@id"]})

mdBlocks = datasetVersion["metadataBlocks"]
for mdBlock in mdBlocks:
    for field in mdBlocks[mdBlock]:
        if isinstance(mdBlocks[mdBlock][field], List):
            root[field] = ArrayList()
            for subField in mdBlocks[mdBlock][field]:
                if isinstance(subField, Map):
                    root[field].add(refField(field, subField))
                else:
                    root[field].add(subField)
        elif isinstance(mdBlocks[mdBlock][field], Map):
            root[field] = refField(field, mdBlocks[mdBlock][field])
        else:
            root[field] = mdBlocks[mdBlock][field]

root["hasPart"] = hasPart


def doFlatten(v):
    if isinstance(v, List) and v.size() > 0:
        if v.size() > 1:
            mapped = ArrayList()
            for toMap in v:
                mapped.add(doFlatten(toMap))
            return mapped
        else:
            return doFlatten(v.get(0))
    elif isinstance(v, Map):
        m = LinkedHashMap()
        for key in v.keySet():
            m.put(key, doFlatten(v.get(key)))
        return m
    else:
        return v


flattened = LinkedHashMap()
for key in res.keySet():
    flattened.put(key, doFlatten(res.get(key)))

res = flattened
