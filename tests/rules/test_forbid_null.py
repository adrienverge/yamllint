from tests.common import RuleTestCase


class ForbidNullTestCase(RuleTestCase):
    rule_id = 'forbid-null'

    def test_forbid_null_disabled(self):
        conf = 'forbid-null: disable'
        self.check('---\n'
                   'null:\n'
                   'valid: "somevalue"\n', conf)

    def test_forbid_null_enabled(self):
        conf = 'forbid-null: enable\n'
        self.check('---\n'
                   'null:\n'
                   'valid: "somevalue"\n', conf, problem=(2, 1))

    def test_forbid_null_with_valid_array_keys(self):
        conf = 'forbid-null: enable'
        self.check('---\n'
                   'valid_key: value\n'
                   'another_key:\n'
                   '  - item0\n'
                   '  - "null"\n'
                   '  - item2\n', conf)

    def test_forbid_null_with_nested_null(self):
        conf = 'forbid-null: enable'
        self.check('---\n'
                   'outer_key:\n'
                   '  null:\n'
                   '    inner_key: value\n', conf, problem=(3, 3))

    def test_forbid_null_with_nested_null_disabled(self):
        conf = 'forbid-null: disable'
        self.check('---\n'
                   'outer_key:\n'
                   '  null:\n'
                   '    inner_key: value\n', conf)

    def test_forbid_null_with_null_value(self):
        conf = 'forbid-null: enable'
        self.check('---\n'
                   'key: "null"\n', conf)

    def test_forbid_null_with_empty_mapping(self):
        conf = 'forbid-null: enable'
        self.check('---\n'
                   '{}\n', conf)
