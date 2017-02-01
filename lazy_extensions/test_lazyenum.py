import json

from django.test import TestCase
from django.contrib.auth import get_user_model

from .lazyenum import LazyEnum, LazyEnumField

User = get_user_model()


class StringConversionTests(TestCase):
    def test_lazy_enum(self):
        enum = LazyEnum("a", "b", "c")
        self.assertEqual(len(enum), 3)
        self.assertEqual(len(enum[0]), 2)
        self.assertEqual(enum[0], (0, "a"))
        self.assertEqual(enum[0], ("a", 0))
        self.assertEqual(enum[0], enum[0])
        self.assertEqual(enum[0], "a")
        self.assertEqual(enum[0], 0)
        self.assertNotEqual(enum[0], enum[1])
        test_case = ((0, "a"), (1, "b"), (2, "c"))
        self.assertTrue(all(
            [test_case[i] for x in enum for i, v in enumerate(x)]
        ))
        self.assertEqual(repr(enum), (
            "<LazyEnum: <Value: {!r}, 0>, " +
            "<Value: {!r}, 1>, " +
            "<Value: {!r}, 2>>"
        ).format("a", "b", "c"))
        self.assertEqual(enum[0][0], 0)
        self.assertEqual(enum[0][1], "a")
        self.assertEqual(enum[0][-2], 0)
        self.assertEqual(enum[0][-1], "a")
        self.assertRaises(IndexError, lambda: enum[0][2])
        self.assertRaises(IndexError, lambda: enum[0][-3])

    def test_lazyenumfield_conversions(self):
        enum = LazyEnum("a", "b", "c")
        field = LazyEnumField(enum)
        for i in range(len(enum)):
            self.assertEqual(field.from_db_value(i, None, None, None), enum[i])
        for v in enum:
            self.assertEqual(v, field.to_python(v))
            self.assertEqual(v, field.to_python(tuple(v)))

        self.assertIs(field.to_python("test"), None)

    def test_lazyenum_json(self):
        enum = LazyEnum("a", "b", "c")
        self.assertEqual(json.dumps(enum[0]), json.dumps((0, "a")))
        self.assertRaises(TypeError, lambda: json.dumps(enum))
