import codecs as codecs
from collections.abc import Iterable as _Iterable
from collections.abc import Iterator as _Iterator
import os as os
import warnings as warnings

def detect_encoding(stream_data: bytes | bytearray) -> str: ...
def auto_decode(stream_data: bytes | bytearray) -> str: ...
def lines_in_files(
    paths: _Iterable[
        str | bytes | os.PathLike[str] | os.PathLike[bytes]
    ],
) -> _Iterator[str]: ...
