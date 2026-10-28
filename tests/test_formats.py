"""Generated fixtures only; no game resources."""
import struct
import unittest
import zlib
from dirk_restore.opes import build, read_opes
from dirk_restore import fwd
from dirk_restore.package import _fields, _visit

class OpesTests(unittest.TestCase):
    def test_deterministic_roundtrip(self):
        resources = {'z': b'plain', 'a': b'abcd' * 300}
        self.assertEqual(build(resources), build(dict(reversed(list(resources.items())))))
        self.assertEqual(read_opes(build(resources)), resources)

    def test_equal_lengths_still_follow_compression_flag(self):
        raw = next(b'a' * n for n in range(1, 40) if len(zlib.compress(b'a' * n)) == n)
        entry = b'test'.ljust(91, b'\0') + b'\1' + struct.pack('<5I', len(raw), len(raw), 0, 0, 0)
        blob = b'opes' + b'\0' * 4 + struct.pack('<I', 1) + entry + zlib.compress(raw)
        self.assertEqual(read_opes(blob)['test'], raw)

    def test_bad_inputs(self):
        good = build({'a': b'a' * 100, 'b': b'b' * 100})
        duplicate = bytearray(good); duplicate[124:214] = duplicate[12:102]
        bad_flag = bytearray(good); bad_flag[103] = 2
        for blob in (good[:-1], good + b'extra', bytes(duplicate), bytes(bad_flag), good[:11]):
            with self.subTest(size=len(blob)), self.assertRaises(ValueError):
                read_opes(blob)

class FwdTests(unittest.TestCase):
    def scene(self):
        return {'type': 1, 'flag': '01', 'children': [
            fwd.pic('fixture/image', -11, 42, 3),
            fwd.cond('state', fwd.val('active', fwd.hot('click', 10, 20, 0, 0, 30, 40))),
            {'type': 7, 'xydepth': [15, 25, 0], 'text': 'fixture',
             'style': '00' * 18, 'anchors': ['tl', 'tl'], 'children': []}]}

    def test_nested_nodes_and_text(self):
        encoded = fwd.build(self.scene()); parsed = fwd.Parser(encoded).parse()[0]
        self.assertEqual(fwd.build(parsed), encoded)
        self.assertEqual(parsed['children'][0]['xydepth'], (-11, 42, 3))
        self.assertEqual(parsed['children'][2]['text'], 'fixture')

    def test_bad_header_count_truncation(self):
        good = fwd.build(self.scene()); bad_count = bytearray(good); bad_count[10:12] = b'\0\0'
        for blob in (b'bad', good[:-1], good + b'x', bytes(bad_count)):
            with self.subTest(size=len(blob)), self.assertRaises(ValueError):
                fwd.Parser(blob).parse()

class SisTests(unittest.TestCase):
    @staticmethod
    def field(kind, value):
        return struct.pack('<II', kind, len(value)) + value + b'\0' * (-len(value) % 4)

    def test_nested_array_compression(self):
        raw = b'fixture resource' * 100
        compressed = self.field(3, struct.pack('<IQ', 1, len(raw)) + zlib.compress(raw))
        filedata = struct.pack('<I', len(compressed)) + compressed
        array32 = self.field(2, struct.pack('<I', 32) + filedata)
        unit = struct.pack('<I', len(array32)) + array32
        array31 = self.field(2, struct.pack('<I', 31) + unit)
        self.assertEqual(list(_visit(array31, 30, 0, len(array31))), [raw])

    def test_bad_field_bounds(self):
        with self.assertRaises(ValueError):
            list(_fields(struct.pack('<II', 3, 99), 0, 8))
