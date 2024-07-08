mapSubField = function (subField, multiple) {
    if (typeof subField === 'string') {
        return subField
    }
    var resArray = new List()
    subField.forEach(function (value) {
        if (value.keySet) {
            var mappedSubField = {}
            value.keySet().forEach(function (key) {
                var mapped = mapSubField(value.get(key).value, value.get(key).multiple)
                if (!value.get(key).multiple) {
                    mappedSubField[key] = mapped
                } else {
                    mappedSubField[key] = mappedSubField[key] ? mappedSubField[key].add(mapped) : new List([mapped])
                }
            })
            resArray.add(mappedSubField)
        } else {
            resArray.add(value)
        }
    })
    return multiple ? resArray : resArray[0]
}

res = {}
x.stream().forEach(function (field) {
    var mapped = mapSubField(field.value, field.multiple)
    if (!field.multiple) {
        res[field.typeName] = mapped
    } else {
        res[field.typeName] = res[field.typeName] ? res[field.typeName].addAll(mapped) : mapped
    }
})
