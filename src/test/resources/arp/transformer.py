from java.util import LinkedHashMap

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
      "grantNumber": "https://schema.org/sponsor"
    }
  ]

res ["@graph"] = []

root = LinkedHashMap()
root["@id"] = "./"
res["@graph"].append(root)

root["@type"] = "Dataset"
root["@arpPid"] = x["preTransformed"]["datasetVersion"]["datasetPersistentId"]
root["license"] = {
        "@id": x["preTransformed"]["datasetVersion"]["license"]["uri"]
      }
root["datePublished"] = x["preTransformed"]["datasetVersion"]["publicationDate"]
root["dateOfDeposit"] = x["preTransformed"]["datasetVersion"]["publicationDate"]
'''
      "dateOfDeposit": "2024-04-02",
      "title_hu": "Balaton vízizotóp összetételének adathalmaza",
      "subject": "Earth and Environmental Sciences",
      "title": "Water stable isotope data of Lake Balaton from 1991-2008",
      "depositor": "Hatvani, István Gábor",
      "publication": [
        {
          "@id": "https://w3id.org/arp/ro-id/hdl:21.15109/ARP/PCKHRH/publication/16487"
        },
        {
          "@id": "https://w3id.org/arp/ro-id/hdl:21.15109/ARP/PCKHRH/publication/16502"
        },
        {
          "@id": "https://w3id.org/arp/ro-id/hdl:21.15109/ARP/PCKHRH/publication/16512"
        },
        {
          "@id": "https://w3id.org/arp/ro-id/hdl:21.15109/ARP/PCKHRH/publication/16492"
        },
        {
          "@id": "https://w3id.org/arp/ro-id/hdl:21.15109/ARP/PCKHRH/publication/16491"
        },
        {
          "@id": "https://w3id.org/arp/ro-id/hdl:21.15109/ARP/PCKHRH/publication/16494"
        },
        {
          "@id": "https://w3id.org/arp/ro-id/hdl:21.15109/ARP/PCKHRH/publication/16497"
        }
      ],
      "keyword": [
        {
          "@id": "https://w3id.org/arp/ro-id/hdl:21.15109/ARP/PCKHRH/keyword/16486"
        },
        {
          "@id": "https://w3id.org/arp/ro-id/hdl:21.15109/ARP/PCKHRH/keyword/16510"
        },
        {
          "@id": "https://w3id.org/arp/ro-id/hdl:21.15109/ARP/PCKHRH/keyword/16485"
        },
        {
          "@id": "https://w3id.org/arp/ro-id/hdl:21.15109/ARP/PCKHRH/keyword/16511"
        }
      ],
      "dsDescription": {
        "@id": "https://w3id.org/arp/ro-id/hdl:21.15109/ARP/PCKHRH/dsDescription/16103"
      },
      "otherId": {
        "@id": "https://w3id.org/arp/ro-id/hdl:21.15109/ARP/PCKHRH/otherId/16102"
      },
      "datasetContact": {
        "@id": "https://w3id.org/arp/ro-id/hdl:21.15109/ARP/PCKHRH/datasetContact/16100"
      },
      "author": {
        "@id": "https://w3id.org/arp/ro-id/hdl:21.15109/ARP/PCKHRH/author/16101"
      },
      "productionPlace": [
        "Budapest",
        "Debrecen"
      ],
      "geographicUnit": "decimal degrees (°)",
      "distributionDate": "2024-04-15",
      "unitOfAnalysis": "The delta notation is reported in ‰ or per mil. It refers to the relative difference, in parts per thousand, of the isotopic ratios of a sample and of a reference standard.",
      "characteristicOfSources": "Measurements done on an isotope ration mass spectrometer (IRMS).",
      "kindOfData": [
        "water stable isotope",
        "oxygen stable isotope ratio",
        "hydrogen stable isotope ratio"
      ],
      "language": [
        "English",
        "Hungarian"
      ],
      "geographicCoverage": {
        "@id": "https://w3id.org/arp/ro-id/hdl:21.15109/ARP/PCKHRH/geographicCoverage/16182"
      },
      "topicClassification": {
        "@id": "https://w3id.org/arp/ro-id/hdl:21.15109/ARP/PCKHRH/topicClassification/16178"
      },
      "dateOfCollection": {
        "@id": "https://w3id.org/arp/ro-id/hdl:21.15109/ARP/PCKHRH/dateOfCollection/16175"
      },
      "producer": {
        "@id": "https://w3id.org/arp/ro-id/hdl:21.15109/ARP/PCKHRH/producer/16174"
      },
      "timePeriodCovered": {
        "@id": "https://w3id.org/arp/ro-id/hdl:21.15109/ARP/PCKHRH/timePeriodCovered/16170"
      },
      "contributor": [
        {
          "@id": "https://w3id.org/arp/ro-id/hdl:21.15109/ARP/PCKHRH/contributor/16499"
        },
        {
          "@id": "https://w3id.org/arp/ro-id/hdl:21.15109/ARP/PCKHRH/contributor/16513"
        },
        {
          "@id": "https://w3id.org/arp/ro-id/hdl:21.15109/ARP/PCKHRH/contributor/16514"
        },
        {
          "@id": "https://w3id.org/arp/ro-id/hdl:21.15109/ARP/PCKHRH/contributor/16515"
        },
        {
          "@id": "https://w3id.org/arp
res["@graph"].append(root)/ro-id/hdl:21.15109/ARP/PCKHRH/contributor/16505"
        },
        {
          "@id": "https://w3id.org/arp/ro-id/hdl:21.15109/ARP/PCKHRH/contributor/16508"
        }
      ],
      "grantNumber": [
        {
          "@id": "https://w3id.org/arp/ro-id/hdl:21.15109/ARP/PCKHRH/grantNumber/16490"
        },
        {
          "@id": "https://w3id.org/arp/ro-id/hdl:21.15109/ARP/PCKHRH/grantNumber/16507"
        },
        {
          "@id": "https://w3id.org/arp/ro-id/hdl:21.15109/ARP/PCKHRH/grantNumber/16496"
        }
      ],
      "geographicBoundingBox": {
        "@id": "https://w3id.org/arp/ro-id/hdl:21.15109/ARP/PCKHRH/geographicBoundingBox/16185"
      },
      "hasPart": {
        "@id": "https://w3id.org/arp/ro-id/hdl:21.15109/ARP/PCKHRH/file/29831"
      },
      "dsDescription_hu": {
        "@id": "https://w3id.org/arp/ro-id/hdl:21.15109/ARP/PCKHRH/dsDescription_hu/16419"
      }
    })
'''