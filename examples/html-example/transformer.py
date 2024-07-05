from java.util import List
from java.util import Map


def toHtml(source):
    s = "<ul>"
    for key, value in source.items():
        s = s + "<li>" + key + ": " + valueToHtml(value) + "</li>"
    return s + "</ul>"


def valueToHtml(value):
    if isinstance(value, List):
        return listToHtml(value)
    elif isinstance(value, Map):
        return toHtml(value)
    else:
        return str(value)


def listToHtml(value):
    s = "<ul>"
    for idx, v in enumerate(value):
        s = s + "<li>" + str(idx) + ": " + valueToHtml(v) + "</li>"
    return s + "</ul>"


res = (
    """<!DOCTYPE html>
<html>
<body>

<h1>HTML Python transformer output:</h1>

<p>
"""
    + toHtml(x)
    + """
</p>

</body>
</html>"""
)
