# yamllint

A linter for YAML files.

[![Build Status](https://travis-ci.org/adrienverge/yamllint.svg?branch=master)](https://travis-ci.org/adrienverge/yamllint)
[![Coverage Status](https://coveralls.io/repos/adrienverge/yamllint/badge.svg?branch=master&service=github)](https://coveralls.io/github/adrienverge/yamllint?branch=master)

Compatible with Python 2 & 3.

## Usage

```sh
yamllint my_file.yml my_other_file.yaml ...
```

```sh
yamllint .
```

```sh
yamllint -c ~/myconfig file.yml
```

```sh
# To output a format parsable (by editors like Vim, emacs, etc.)
yamllint -f parsable file.yml
```

## Installation

```sh
pip install yamllint
```

## Configuration

There is no documentation yet, so here is what you need to know: you can
override some rules, disable them or pass them in *warning* (instead of
*error*). Have a look at the content of `yamllint/conf/default.yml` and create
your own configuration file.

It could look like this:

```yaml
# This is my first, very own configuration file for yamllint!
# It extends the default conf by adjusting some options.

extends: default

rules:
  # 80 should be enough, but don't fail if a line is longer
  line-length:
    max: 80
    level: warning

  # accept both
  #    key:
  #      - item
  # and
  #    key:
  #    - item
  indentation:
    indent-sequences: whatever

  # don't bother me with this rule
  comments-indentation: disable
```

Tip: if you have a `.yamllint` file in your working directory, it will be
automatically loaded as configuration by yamllint.
