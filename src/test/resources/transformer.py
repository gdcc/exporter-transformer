res["title"] = x["preTransformed"]["datasetVersion"]["metadataBlocks"]["citation"]["title"]

res["author"] = []
for author in x["preTransformed"]["datasetVersion"]["metadataBlocks"]["citation"]["author"]:
    res["author"].append(author["authorName"])

res["files"] = []
for distribution in x["datasetSchemaDotOrg"]["distribution"]:
    res["files"].append(distribution["contentUrl"])