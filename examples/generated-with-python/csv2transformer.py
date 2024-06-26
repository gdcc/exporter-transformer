import csv

res = """{
    "transformations": [
        {
            "append": true,
            "resultPointer": "/@context",
            "expressions": [
                "\\"https://w3id.org/ro/crate/1.0/context\\""
            ]
        },
        {
            "append": true,
            "sourcePointer": "/config",
            "resultPointer": "/@context",
            "expressions": [
                "script(res = { \\"@vocab\\": \\"https://schema.org/\\" })"
            ]
        },
"""


def copy_transformation(source1, source2, source3, target1, target2):
    sep1 = "/" if source1 else ""
    sep2 = "/" if source2 else ""
    sep3 = "/" if source3 else ""
    sep4 = "/" if target1 and target2  else ""
    i = "[i]" if source1 and source2 else ""
    iTarget = i if target1 != "Root" else ""
    iEnd = "[i]" if source3 else ""
    return (
        "        {\n"
        + f'            "sourcePointer": "/preTransformed{sep1}{source1}{sep2}{source2}{i}{sep3}{source3}{iEnd}",\n'
        + f'            "resultPointer": "/{target1}{iTarget}{sep4}{target2}[i]"\n'
        + "        },\n"
    )

def literal_transformation(source1, source2, target1, target2, value):
    sep1 = "/" if source1 else ""
    sep2 = "/" if source2 else ""
    sep3 = "/" if target1 and target2  else ""
    i = "[i]" if source1 and source2 else ""
    iTarget = i if target1 != "Root" else ""
    return (
        "        {\n"
        + f'            "sourcePointer": "/preTransformed{sep1}{source1}{sep2}{source2}{i}",\n'
        + f'            "resultPointer": "/{target1}{iTarget}{sep3}{target2}",\n'
        + '             "expressions": [\n'
        + '                "\\"' + value + '\\""\n'
        + '            ]\n'
        + "        },\n"
    )

def ref_transformation(sourcePointer, target1, target2):
    iTarget = "[i]" if target1 != "Root" else ""
    return (
        "        {\n"
        + f'            "sourcePointer": "{sourcePointer}",\n'
        + f'            "resultPointer": "/{target1}{iTarget}/{target2}[i]/@id"\n'
        + "        },\n"
    )

def literal_ref_transformation(target1, target2, value):
    return (
        "        {\n"
        + f'            "resultPointer": "/{target1}/{target2}/@id",\n'
        + '             "expressions": [\n'
        + '                "\\"' + value + '\\""\n'
        + '            ]\n'
        + "        },\n"
    )

refDictionary = {}
entities = []

with open("dataverse2ro-crate.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    is_header = True
    target1 = ""
    target2 = ""
    source1 = ""
    source2 = ""
    source3 = ""
    for row in csv_reader:
        if is_header:
            is_header = False
            continue
        target1 = row[0] if row[0] else target1
        target2 = row[1]
        source1 = row[2] if row[2] else source1
        source2 = row[3] if row[3] else source2
        source3 = row[4]
        target2 = target2.replace("__", "@")
        if row[0]:
            entities.append(row[0])
            continue
        elif source3.startswith('"'):
            res = res + literal_transformation(source1, source2, target1, target2, source3.replace('"', ''))
        elif source3.startswith('refersTo:'):
            if source3.endswith('"'):
                value = source3.replace('"', '')
                value = value.replace('refersTo:', '')
                res = res + literal_ref_transformation(target1, target2, value)
            else:
                res = res + ref_transformation('--' + source3 + '--', target1, target2)
        else:
            if target2 == "@id":
                refDictionary['--refersTo:' + target1 + '--'] = f'/preTransformed/{source1}/{source2}[i]/{source3}[i]'
            res = res + copy_transformation(source1, source2, source3, target1, target2)

for k, v in refDictionary.items():
    res = res.replace(k, v)

def append_and_delete(entity):
    return (
        "        {\n"
        + '            "append": true,\n'
        + '            "useResultAsSource": true,\n'
        + f'            "sourcePointer": "/{entity}",\n'
        + '            "resultPointer": "/@graph"\n'
        + "        },\n"
        + '        {\n'
        + '            "expressions": [\n'
        + f'                "remove(/{entity})"\n'
        + '            ]'
        + '        },\n'
    )

for v in entities:
    res = res + append_and_delete(v)

res = (
    res
    + """        {
            "append": true,
            "sourcePointer": "/datasetSchemaDotOrg/distribution[i]",
            "resultPointer": "/@graph"
        },
        {
            "useResultAsSource": true,
            "expressions": [
                "script(importJS /js/flatten.js endImport)"
            ]
        }
    ]
}"""
)

f = open("transformer.json", "w")
f.write(res)
f.close()
