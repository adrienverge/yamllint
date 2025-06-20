from tests.common import RuleTestCase


class ForbidFloatTestCase(RuleTestCase):
    rule_id = 'forbid-float'

    def test_forbid_null_disabled(self):
        conf = 'forbid-float: disable'
        self.check('---\n'
                   'float:\n'
                   'valid: "somevalue"\n', conf)

    def test_forbid_null_enabled(self):
        conf = 'forbid-float: enable\n'
        self.check('---\n'
                   'float:\n'
                   'valid: "somevalue"\n', conf, problem=(2, 1))

    def test_forbid_null_with_valid_array_keys(self):
        conf = 'forbid-float: enable'
        self.check('---\n'
                   'valid_key: value\n'
                   'another_key:\n'
                   '  - item0\n'
                   '  - "float"\n'
                   '  - item2\n', conf)

    def test_forbid_null_with_nested_null(self):
        conf = 'forbid-float: enable'
        self.check('---\n'
                   'outer_key:\n'
                   '  float:\n'
                   '    inner_key: value\n', conf, problem=(3, 3))

    def test_forbid_null_with_nested_null_disabled(self):
        conf = 'forbid-float: disable'
        self.check('---\n'
                   'outer_key:\n'
                   '  float:\n'
                   '    inner_key: value\n', conf)

    def test_forbid_null_with_null_value(self):
        conf = 'forbid-float: enable'
        self.check('---\n'
                   'key: "float"\n', conf)

    def test_forbid_null_with_empty_mapping(self):
        conf = 'forbid-float: enable'
        self.check('---\n'
                   '{}\n', conf)
