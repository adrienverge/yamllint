from tests.common import RuleTestCase


class ForbidBoolTestCase(RuleTestCase):
    rule_id = 'forbid-bool'

    def test_forbid_null_disabled(self):
        conf = 'forbid-bool: disable'
        self.check('---\n'
                   'bool:\n'
                   'valid: "somevalue"\n', conf)

    def test_forbid_null_enabled(self):
        conf = 'forbid-bool: enable\n'
        self.check('---\n'
                   'bool:\n'
                   'valid: "somevalue"\n', conf, problem=(2, 1))

    def test_forbid_null_with_valid_array_keys(self):
        conf = 'forbid-bool: enable'
        self.check('---\n'
                   'valid_key: value\n'
                   'another_key:\n'
                   '  - item0\n'
                   '  - "bool"\n'
                   '  - item2\n', conf)

    def test_forbid_null_with_nested_null(self):
        conf = 'forbid-bool: enable'
        self.check('---\n'
                   'outer_key:\n'
                   '  bool:\n'
                   '    inner_key: value\n', conf, problem=(3, 3))

    def test_forbid_null_with_nested_null_disabled(self):
        conf = 'forbid-bool: disable'
        self.check('---\n'
                   'outer_key:\n'
                   '  bool:\n'
                   '    inner_key: value\n', conf)

    def test_forbid_null_with_null_value(self):
        conf = 'forbid-bool: enable'
        self.check('---\n'
                   'key: "bool"\n', conf)

    def test_forbid_null_with_empty_mapping(self):
        conf = 'forbid-bool: enable'
        self.check('---\n'
                   '{}\n', conf)
