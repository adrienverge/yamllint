from tests.common import RuleTestCase


class ForbidIntTestCase(RuleTestCase):
    rule_id = 'forbid-int'

    def test_forbid_null_disabled(self):
        conf = 'forbid-int: disable'
        self.check('---\n'
                   'int:\n'
                   'valid: "somevalue"\n', conf)

    def test_forbid_null_enabled(self):
        conf = 'forbid-int: enable\n'
        self.check('---\n'
                   'int:\n'
                   'valid: "somevalue"\n', conf, problem=(2, 1))

    def test_forbid_null_with_valid_array_keys(self):
        conf = 'forbid-int: enable'
        self.check('---\n'
                   'valid_key: value\n'
                   'another_key:\n'
                   '  - item0\n'
                   '  - "int"\n'
                   '  - item2\n', conf)

    def test_forbid_null_with_nested_null(self):
        conf = 'forbid-int: enable'
        self.check('---\n'
                   'outer_key:\n'
                   '  int:\n'
                   '    inner_key: value\n', conf, problem=(3, 3))

    def test_forbid_null_with_nested_null_disabled(self):
        conf = 'forbid-int: disable'
        self.check('---\n'
                   'outer_key:\n'
                   '  int:\n'
                   '    inner_key: value\n', conf)

    def test_forbid_null_with_null_value(self):
        conf = 'forbid-int: enable'
        self.check('---\n'
                   'key: "int"\n', conf)

    def test_forbid_null_with_empty_mapping(self):
        conf = 'forbid-int: enable'
        self.check('---\n'
                   '{}\n', conf)
