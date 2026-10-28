"""Native OPES archive reader and deterministic script archive builder."""
import struct
import zlib

def read_opes(blob):
    if len(blob) < 12 or blob[:4] != b'opes':
        raise ValueError('Invalid OPES header')
    count = struct.unpack_from('<I', blob, 8)[0]
    cursor = 12 + count * 112
    if cursor > len(blob):
        raise ValueError('Truncated index')
    result = {}
    for i in range(count):
        record = blob[12+i*112:124+i*112]
        if record[90] != 0 or record[91] not in (0, 1):
            raise ValueError('Unsupported record marker or compression flag')
        name = record[:90].split(b'\0', 1)[0].decode('latin1')
        compressed, raw = struct.unpack_from('<II', record, 92)
        end = cursor + compressed
        if end > len(blob) or name in result:
            raise ValueError('Truncated payload or duplicate filename')
        payload = blob[cursor:end]
        cursor = end
        # The flag is authoritative, even when compressed length == raw length.
        if record[91]:
            decoder = zlib.decompressobj()
            payload = decoder.decompress(payload) + decoder.flush()
            if not decoder.eof or decoder.unused_data or decoder.unconsumed_tail:
                raise ValueError('Invalid compressed stream')
        if len(payload) != raw:
            raise ValueError(f'Wrong resource size: {name}')
        result[name] = payload
    if cursor != len(blob):
        raise ValueError('Unexpected trailing data')
    return result


def build(assets):
    headers, payloads = [], []
    for name, raw in sorted(assets.items()):
        encoded = name.encode('latin1')
        if len(encoded) >= 90:
            raise ValueError('Filename too long')
        packed = zlib.compress(raw, 9)
        compressed = len(packed) < len(raw)
        payload = packed if compressed else raw
        headers.append(encoded.ljust(91, b'\0') + bytes([compressed]) +
                       struct.pack('<5I', len(payload), len(raw), 0, 0, 1253177177))
        payloads.append(payload)
    return (b'opes' + bytes.fromhex('57f7b14a') + struct.pack('<I', len(assets)) +
            b''.join(headers) + b''.join(payloads))
