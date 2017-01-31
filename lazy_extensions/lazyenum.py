from django.db.models import PositiveSmallIntegerField


class LazyEnum(object):
    class Value(tuple):
        def __init__(self, tup):
            super(LazyEnum.Value, self).__init__()
            self.value = tup[0]
            self.name = tup[1]

        def __eq__(self, other):
            return other in [
                (self.value, self.name),
                (self.name, self.value),
                self.value,
                self.name,
                self.name.upper(),
            ]

        def __int__(self):
            return self.value

        def __str__(self):
            return self.name

        def __repr__(self):
            return "<Value: {0.name!r}, {0.value!r}>".format(self)

    def __init__(self, *values, **kwargs):
        super(LazyEnum, self).__init__(**kwargs)
        self.values = tuple(
            LazyEnum.Value((i, name)) for i, name in enumerate(values)
        )
        for value in self.values:
            setattr(self, str(value).upper(), value)

    def __len__(self):
        return len(self.values)

    def __getitem__(self, key):
        return self.values[key]

    def __iter__(self):
        return iter(self.values)

    def from_id(self, idx):
        return self.values[idx]

    def __repr__(self):
        return "<LazyEnum: {}>".format(", ".join(repr(x) for x in self.values))


class LazyEnumField(PositiveSmallIntegerField):
    def __init__(self, choices, *args, **kwargs):
        super(LazyEnumField, self).__init__(choices=choices,
                                            *args, **kwargs)
        self.enum = choices

    def from_db_value(self, value, expression, connection, context):
        return self.enum.from_id(value)

    def to_python(self, value):
        if isinstance(value, LazyEnum.Value) and value in self.enum:
            return value

        options = [v for v in self.enum if v == value]
        if len(options) == 1:
            return options[0]

        return None
