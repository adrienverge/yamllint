from types import ModuleType as _ModuleType

from yamllint.rules import anchors as anchors
from yamllint.rules import braces as braces
from yamllint.rules import brackets as brackets
from yamllint.rules import colons as colons
from yamllint.rules import commas as commas
from yamllint.rules import comments as comments
from yamllint.rules import comments_indentation as comments_indentation
from yamllint.rules import common as common
from yamllint.rules import document_end as document_end
from yamllint.rules import document_start as document_start
from yamllint.rules import empty_lines as empty_lines
from yamllint.rules import empty_values as empty_values
from yamllint.rules import float_values as float_values
from yamllint.rules import hyphens as hyphens
from yamllint.rules import indentation as indentation
from yamllint.rules import key_duplicates as key_duplicates
from yamllint.rules import key_ordering as key_ordering
from yamllint.rules import line_length as line_length
from yamllint.rules import (
    new_line_at_end_of_file as new_line_at_end_of_file,
)
from yamllint.rules import new_lines as new_lines
from yamllint.rules import octal_values as octal_values
from yamllint.rules import quoted_strings as quoted_strings
from yamllint.rules import trailing_spaces as trailing_spaces
from yamllint.rules import truthy as truthy

def get(id: str) -> _ModuleType: ...
