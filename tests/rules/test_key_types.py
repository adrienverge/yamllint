from tests.common import RuleTestCase


class KeyTypesTestCase(RuleTestCase):
    rule_id = 'key-types'

    def test_key_types_disabled(self):
        conf = 'key-types: disable'
        self.check('---\n'
                   'null:\n'
                   'valid: "somevalue"\n', conf)

    def test_key_types_enabled_with_defaults(self):
        conf = 'key-types: enable'
        self.check('---\n'
                   'null:\n'
                   'valid: "somevalue"\n', conf)

    def test_forbid_null_enabled(self):
        conf = 'key-types:\n  forbid-null: true'
        self.check('---\n'
                   'null:\n'
                   'valid: "somevalue"\n', conf, problem=(2, 1))

    def test_forbid_null_disabled(self):
        conf = 'key-types:\n  forbid-null: false'
        self.check('---\n'
                   'null:\n'
                   'valid: "somevalue"\n', conf)

    def test_forbid_bool_enabled(self):
        conf = 'key-types:\n  forbid-bool: true'
        self.check('---\n'
                   'bool:\n'
                   'valid: "somevalue"\n', conf, problem=(2, 1))

    def test_forbid_bool_disabled(self):
        conf = 'key-types:\n  forbid-bool: false'
        self.check('---\n'
                   'bool:\n'
                   'valid: "somevalue"\n', conf)

    def test_forbid_int_enabled(self):
        conf = 'key-types:\n  forbid-int: true'
        self.check('---\n'
                   'int:\n'
                   'valid: "somevalue"\n', conf, problem=(2, 1))

    def test_forbid_int_disabled(self):
        conf = 'key-types:\n  forbid-int: false'
        self.check('---\n'
                   'int:\n'
                   'valid: "somevalue"\n', conf)

    def test_forbid_float_enabled(self):
        conf = 'key-types:\n  forbid-float: true'
        self.check('---\n'
                   'float:\n'
                   'valid: "somevalue"\n', conf, problem=(2, 1))

    def test_forbid_float_disabled(self):
        conf = 'key-types:\n  forbid-float: false'
        self.check('---\n'
                   'float:\n'
                   'valid: "somevalue"\n', conf)

    def test_forbid_str_enabled(self):
        conf = 'key-types:\n  forbid-str: true'
        self.check('---\n'
                   'str:\n'
                   'valid: "somevalue"\n', conf, problem=(2, 1))

    def test_forbid_str_disabled(self):
        conf = 'key-types:\n  forbid-str: false'
        self.check('---\n'
                   'str:\n'
                   'valid: "somevalue"\n', conf)

    def test_multiple_types_enabled(self):
        conf = ('key-types:\n'
                '  forbid-null: true\n'
                '  forbid-bool: true\n'
                '  forbid-int: true')
        self.check('---\n'
                   'null:\n'
                   '  bool:\n'
                   '    int: value\n', conf,
                   problem1=(2, 1), problem2=(3, 3), problem3=(4, 5))

    def test_multiple_types_mixed(self):
        conf = ('key-types:\n'
                '  forbid-null: true\n'
                '  forbid-bool: false\n'
                '  forbid-int: true')
        self.check('---\n'
                   'null:\n'
                   '  bool:\n'
                   '    int: value\n', conf,
                   problem1=(2, 1), problem2=(4, 5))

    def test_with_valid_array_values(self):
        conf = 'key-types:\n  forbid-null: true'
        self.check('---\n'
                   'valid_key: value\n'
                   'another_key:\n'
                   '  - item0\n'
                   '  - "null"\n'
                   '  - item2\n', conf)

    def test_with_nested_forbidden_keys(self):
        conf = 'key-types:\n  forbid-null: true'
        self.check('---\n'
                   'outer_key:\n'
                   '  null:\n'
                   '    inner_key: value\n', conf, problem=(3, 3))

    def test_with_null_value(self):
        conf = 'key-types:\n  forbid-null: true'
        self.check('---\n'
                   'key: "null"\n', conf)

    def test_with_empty_mapping(self):
        conf = 'key-types:\n  forbid-null: true'
        self.check('---\n'
                   '{}\n', conf)

    def test_all_types_forbidden(self):
        conf = ('key-types:\n'
                '  forbid-null: true\n'
                '  forbid-bool: true\n'
                '  forbid-int: true\n'
                '  forbid-float: true\n'
                '  forbid-str: true')
        self.check('---\n'
                   'null: value1\n'
                   'bool: value2\n'
                   'int: value3\n'
                   'float: value4\n'
                   'str: value5\n', conf,
                   problem1=(2, 1), problem2=(3, 1), problem3=(4, 1),
                   problem4=(5, 1), problem5=(6, 1))
