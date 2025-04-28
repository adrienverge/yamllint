from tests.common import RuleTestCase


class ForbidStrTestCase(RuleTestCase):
    rule_id = 'forbid-str'

    def test_forbid_null_disabled(self):
        conf = 'forbid-str: disable'
        self.check('---\n'
                   'str:\n'
                   'valid: "somevalue"\n', conf)

    def test_forbid_null_enabled(self):
        conf = 'forbid-str: enable\n'
        self.check('---\n'
                   'str:\n'
                   'valid: "somevalue"\n', conf, problem=(2, 1))

    def test_forbid_null_with_valid_array_keys(self):
        conf = 'forbid-str: enable'
        self.check('---\n'
                   'valid_key: value\n'
                   'another_key:\n'
                   '  - item0\n'
                   '  - "str"\n'
                   '  - item2\n', conf)

    def test_forbid_null_with_nested_null(self):
        conf = 'forbid-str: enable'
        self.check('---\n'
                   'outer_key:\n'
                   '  str:\n'
                   '    inner_key: value\n', conf, problem=(3, 3))

    def test_forbid_null_with_nested_null_disabled(self):
        conf = 'forbid-str: disable'
        self.check('---\n'
                   'outer_key:\n'
                   '  str:\n'
                   '    inner_key: value\n', conf)

    def test_forbid_null_with_null_value(self):
        conf = 'forbid-str: enable'
        self.check('---\n'
                   'key: "str"\n', conf)

    def test_forbid_null_with_empty_mapping(self):
        conf = 'forbid-str: enable'
        self.check('---\n'
                   '{}\n', conf)
