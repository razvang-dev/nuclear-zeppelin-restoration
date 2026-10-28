"""Read the supported MIME N-Gage distribution and its SIS data fields.

No installer, DRM operation, decryption, or filesystem extraction is performed.
Only the plain main OPES archive is retained. Input identity is checked upstream.
"""
import hashlib
import re
import struct
import zlib

MAX_EXPANDED = 128 * 1024 * 1024


def _length(data, offset, end):
    if offset + 4 > end:
        raise ValueError('Truncated SIS field length')
    low = struct.unpack_from('<I', data, offset)[0]
    offset += 4
    if low & 0x80000000:
        raise ValueError('Extended SIS lengths are outside the supported package format')
    return low, offset


def _fields(data, start, end, implicit_type=None):
    while start < end:
        if implicit_type is None:
            if start + 4 > end:
                raise ValueError('Truncated SIS field type')
            kind = struct.unpack_from('<I', data, start)[0]
            start += 4
        else:
            kind = implicit_type
        length, body = _length(data, start, end)
        stop = body + length
        if stop > end:
            raise ValueError('SIS field exceeds container')
        yield kind, body, stop
        start = (stop + 3) & ~3
        if start > end and stop != end:
            raise ValueError('Invalid SIS field alignment')


def _data_payloads(data, start, end):
    for kind, body, stop in _fields(data, start, end):
        yield from _visit(data, kind, body, stop)


def _visit(data, kind, body, stop):
    if kind == 2:  # SISArray stores the element type only once.
        if body + 4 > stop:
            raise ValueError('Truncated SISArray')
        element = struct.unpack_from('<I', data, body)[0]
        for t, lo, hi in _fields(data, body + 4, stop, element):
            yield from _visit(data, t, lo, hi)
    elif kind in (30, 31, 32):  # SISData, SISDataUnit, SISFileData
        yield from _data_payloads(data, body, stop)
    elif kind == 3:  # SISCompressed
        if body + 12 > stop:
            raise ValueError('Truncated SISCompressed')
        algorithm, size = struct.unpack_from('<IQ', data, body)
        if size > MAX_EXPANDED:
            raise ValueError('Expanded SIS file exceeds limit')
        packed = data[body + 12:stop]
        if algorithm == 0:
            plain = packed
        elif algorithm == 1:
            decoder = zlib.decompressobj()
            plain = decoder.decompress(packed, size + 1)
            if not decoder.eof or decoder.unused_data or decoder.unconsumed_tail:
                raise ValueError('Invalid SIS compressed stream')
        else:
            raise ValueError('Unsupported SIS compression algorithm')
        if len(plain) != size:
            raise ValueError('SIS expanded length mismatch')
        yield plain


def main_archive(package, expected_sha256):
    """Return the main plaintext OPES from the Game MIME part."""
    header = package[:package.find(b'\r\n--')]
    match = re.search(rb'boundary="([^"\r\n]+)"', header)
    if not match:
        raise ValueError('Missing MIME boundary')
    delimiter = b'--' + match.group(1)
    game_parts = []
    for part in package.split(b'\r\n' + delimiter)[1:]:
        headers, separator, payload = part.partition(b'\r\n\r\n')
        if separator and re.search(rb'^Content-ID:\s*<Game>\s*$', headers, re.M | re.I):
            game_parts.append(payload)
    if len(game_parts) != 1:
        raise ValueError('Expected exactly one Game MIME part')
    sis = game_parts[0]
    if len(sis) < 24 or struct.unpack_from('<I', sis)[0] != 0x10201A7A:
        raise ValueError('Unsupported SIS header')
    kind = struct.unpack_from('<I', sis, 16)[0]
    length, body = _length(sis, 20, len(sis))
    end = body + length
    if kind != 12 or end > len(sis):
        raise ValueError('Invalid SISContents')
    matches = []
    # Controller metadata is deliberately skipped; only the SISData tree is read.
    for t, lo, hi in _fields(sis, body, end):
        if t == 30:
            for plain in _visit(sis, t, lo, hi):
                if plain.startswith(b'opes') and hashlib.sha256(plain).hexdigest() == expected_sha256:
                    matches.append(plain)
    if len(matches) != 1:
        raise ValueError('Supported main plaintext archive not found exactly once')
    return matches[0]
