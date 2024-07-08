mapSubField = function (subField, multiple) {
    if (typeof subField === 'string') {
        return subField
    }
    var resArray = new List()
    subField.forEach(function (value) {
        if (value.keySet) {
            var mappedSubField = {}
            value.keySet().forEach(function (key) {
                mappedSubField[key] = mapSubField(value.get(key).value, value.get(key).multiple)
            })
            resArray.add(mappedSubField)
        } else {
            resArray.add(value)
        }
    })
    return multiple ? resArray : resArray[0]
}

res = {}
x.keySet().stream().forEach(function (key) {
    res[key] = {}
    x[key].fields.stream().forEach(function (field) {
        res[key][field.typeName] = mapSubField(field.value, field.multiple)
    })
})