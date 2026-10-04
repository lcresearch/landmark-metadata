"""Support 0.4.4 FileUtil UTF-8 label semantics on valid UTF-8 payloads.

Only CR, LF and CRLF end a BufferedReader line. Java String.trim() is used only
to discard blank lines: returned nonblank label content is not trimmed.

Malformed UTF-8 is deliberately outside this helper's supported domain. Java
InputStreamReader replaces malformed subsequences, but Python errors='replace'
does not always group those subsequences identically (e.g. UTF-8 encodings of
surrogate code points). Callers must report ABSTAIN, not an incompatibility or
compatible result, when LabelEncodingUnsupported is raised.
"""
import re

_JAVA_LINE_END = re.compile(r"\r\n|\r|\n")
_JAVA_TRIM_CHARS = "".join(chr(code) for code in range(0x21))


class LabelEncodingUnsupported(ValueError):
    """The consumer's replacement-decoder behavior has not been modeled."""


def load_java_utf8_labels(payload: bytes) -> list[str]:
    """Return actual FileUtil label strings for a valid UTF-8 byte payload.

    BOMs and non-CR/LF Unicode separators remain part of label content, matching
    the selected Java API. An empty or all-Java-trim-whitespace line is omitted.
    """
    try:
        text = payload.decode("utf-8", errors="strict")
    except UnicodeDecodeError as error:
        raise LabelEncodingUnsupported(
            "Malformed UTF-8 labels: Java replacement decoding is outside the modeled scope."
        ) from error
    return [line for line in _JAVA_LINE_END.split(text) if line.strip(_JAVA_TRIM_CHARS)]
