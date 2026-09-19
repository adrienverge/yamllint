from collections.abc import Iterator as _Iterator

import yaml as yaml

class Line:
    line_no: int
    start: int
    end: int
    buffer: str

    def __init__(
        self,
        line_no: int,
        buffer: str,
        start: int,
        end: int,
    ) -> None: ...

    @property
    def content(self) -> str: ...

class Token:
    line_no: int
    curr: yaml.Token
    prev: yaml.Token | None
    next: yaml.Token | None
    nextnext: yaml.Token | None

    def __init__(
        self,
        line_no: int,
        curr: yaml.Token,
        prev: yaml.Token | None,
        next: yaml.Token | None,
        nextnext: yaml.Token | None,
    ) -> None: ...

class Comment:
    line_no: int
    column_no: int
    buffer: str
    pointer: int
    token_before: yaml.Token | None
    token_after: yaml.Token | None
    comment_before: Comment | None

    def __init__(
        self,
        line_no: int,
        column_no: int,
        buffer: str,
        pointer: int,
        token_before: yaml.Token | None = None,
        token_after: yaml.Token | None = None,
        comment_before: Comment | None = None,
    ) -> None: ...
    def __eq__(self, other: object) -> bool: ...
    def is_inline(self) -> bool: ...

def line_generator(buffer: str) -> _Iterator[Line]: ...
def comments_between_tokens(
    token1: yaml.Token,
    token2: yaml.Token | None,
) -> _Iterator[Comment]: ...
def token_or_comment_generator(
    buffer: str,
) -> _Iterator[Token | Comment]: ...
def token_or_comment_or_line_generator(
    buffer: str,
) -> _Iterator[Token | Comment | Line]: ...
