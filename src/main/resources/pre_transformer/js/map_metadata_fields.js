mapSubField = function (subField) {
    if (typeof subField === 'string') {
        return subField;
    }
    var mappedSubField = {};
    subField.forEach(function (value) {
        if (value.keySet) {
            value.keySet().forEach(function (key) {
                var mapped = mapSubField(value.get(key).value);
                mappedSubField[key] = mappedSubField[key] ? mappedSubField[key].add(mapped) : new List([mapped]);
            });
        } else {
            mappedSubField = subField;
        }
    });
    return mappedSubField;
};

res = {};
x.stream().forEach(function (field) {
    var mapped = mapSubField(field.value);
    res[field.typeName] = res[field.typeName] ? res[field.typeName].add(mapped) : new List([mapped]);
});
