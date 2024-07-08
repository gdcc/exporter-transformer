res = {}

res.title = x.preTransformed.datasetVersion.metadataBlocks.citation.title

res.author = new List()
for (i = 0; i < x.preTransformed.datasetVersion.metadataBlocks.citation.author.length; i++) {
  res.author.add(x.preTransformed.datasetVersion.metadataBlocks.citation.author[i].authorName)
}

res.files = new List()
for (i = 0; i < x.datasetSchemaDotOrg.distribution.length; i++) {
  res.files.add(x.datasetSchemaDotOrg.distribution[i].contentUrl)
}