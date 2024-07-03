res["title"] = x["preTransformed"]["datasetVersion"]["metadataBlocks"]["citation"]["title"][0]

res["author"] = []
for author in x["preTransformed"]["datasetVersion"]["metadataBlocks"]["citation"]["author"]:
    res["author"].append(author["authorName"][0])

res["files"] = []
for distribution in x["datasetSchemaDotOrg"]["distribution"]:
    res["files"].append(distribution["contentUrl"])