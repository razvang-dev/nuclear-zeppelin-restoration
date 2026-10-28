"""Native FWD scene nodes. Pickup type95 parsing is partial; emission unsupported."""
import struct

class Parser:

    def __init__(self, b):
        if len(b) < 12 or b[:10] != b'fwd2DIST\x00\x01':
            raise ValueError('Unsupported FWD header')
        self.b = b
        self.p = 12

    def u(self):
        return struct.unpack('>H', self.take(2))[0]

    def s(self):
        return self.take(self.u()).decode('latin1')

    def take(self, n):
        if n < 0 or self.p + n > len(self.b):
            raise ValueError('Truncated FWD node')
        v = self.b[self.p:self.p + n]
        self.p += n
        return v

    def node(self):
        start = self.p
        t = self.take(1)[0]
        d = {'type': t, 'start': start}
        ch = []
        if t == 1:
            d['flag'] = self.take(1).hex()
            ch = [self.node() for _ in range(struct.unpack('>I', self.take(4))[0])]
        elif t == 30:
            d['geometry'] = self.take(8).hex()
            ch = [self.node() for _ in range(self.u())]
        elif t == 31:
            d['geometry'] = self.take(15).hex()
            ch = [self.node() for _ in range(self.u())]
        elif t == 3:
            d['image'] = self.s()
            d['xydepth'] = struct.unpack('>hhh', self.take(6))
            d['anchors'] = [self.s(), self.s()]
            d['selected'] = self.s()
        elif t == 7:
            d['xydepth'] = struct.unpack('>hhh', self.take(6))
            d['text'] = self.s()
            d['style'] = self.take(18).hex()
            d['anchors'] = [self.s(), self.s()]
        elif t == 5:
            d['xydepth'] = struct.unpack('>hhh', self.take(6))
            d['anim'] = self.s()
        elif t == 40:
            d['point'] = struct.unpack('>hhhh', self.take(8))
            d['name'] = self.s()
            d['rect'] = struct.unpack('>hhhh', self.take(8))
            d['cursor'] = self.s()
            d['tail'] = self.take(1).hex()
        elif t == 95:
            d['point'] = struct.unpack('>hhhh', self.take(8))
            d['xydepth'] = struct.unpack('>hhh', self.take(6))
            d['name'] = self.s()
            d['rect'] = struct.unpack('>hhhh', self.take(8))
            d['item'] = self.s()
        elif t == 50:
            d['scope'] = self.take(2).hex()
            d['var'] = self.s()
            d['flag'] = self.take(1).hex()
            ch = [self.node() for _ in range(self.u())]
        elif t == 51:
            d['value'] = self.s()
            ch = [self.node() for _ in range(self.u())]
        elif t == 52:
            ch = [self.node() for _ in range(self.u())]
        elif t == 80:
            d['flag'] = self.take(1).hex()
            d['sound'] = self.s()
            d['tail'] = self.take(2).hex()
        else:
            raise ValueError(f'unknown type {t} at {start}: {self.b[start:start + 85]!r}')
        d['end'] = self.p
        d['children'] = ch
        return d

    def parse(self):
        nodes = [self.node()]
        if self.p != len(self.b):
            raise ValueError('Trailing FWD bytes')
        if count(nodes[0]) != struct.unpack_from('>H', self.b, 10)[0]:
            raise ValueError('FWD node count mismatch')
        return nodes

def count(n):
    return 1 + sum((count(x) for x in n['children']))

def S(v):
    b = v.encode('latin1')
    return struct.pack('>H', len(b)) + b

def emit(n):
    t = n['type']
    ch = n.get('children', [])
    p = bytes([t])
    sub = b''.join((emit(c) for c in ch))
    if t == 1:
        p += bytes.fromhex(n['flag']) + struct.pack('>I', len(ch)) + sub
    elif t in [30, 31]:
        p += bytes.fromhex(n['geometry']) + struct.pack('>H', len(ch)) + sub
    elif t == 3:
        p += S(n['image']) + struct.pack('>hhh', *n['xydepth']) + b''.join((S(x) for x in n['anchors'])) + S(n['selected'])
    elif t == 7:
        p += struct.pack('>hhh', *n['xydepth']) + S(n['text']) + bytes.fromhex(n['style']) + b''.join((S(x) for x in n['anchors']))
    elif t == 5:
        p += struct.pack('>hhh', *n['xydepth']) + S(n['anim'])
    elif t == 40:
        p += struct.pack('>hhhh', *n['point']) + S(n['name']) + struct.pack('>hhhh', *n['rect']) + S(n['cursor']) + bytes.fromhex(n['tail'])
    elif t == 50:
        p += bytes.fromhex(n['scope']) + S(n['var']) + bytes.fromhex(n['flag']) + struct.pack('>H', len(ch)) + sub
    elif t == 51:
        p += S(n['value']) + struct.pack('>H', len(ch)) + sub
    elif t == 52:
        p += struct.pack('>H', len(ch)) + sub
    elif t == 80:
        p += bytes.fromhex(n['flag']) + S(n['sound']) + bytes.fromhex(n['tail'])
    else:
        raise ValueError(t)
    return p

def build(root):
    return b'fwd2DIST\x00\x01' + struct.pack('>H', count(root)) + emit(root)

def pic(name, x, y, z=0):
    return dict(type=3, image=name, selected=name, xydepth=[x, y, z], anchors=['tl', 'tl'], children=[])

def anim(name, x=0, y=0, z=0):
    return dict(type=5, anim=name, xydepth=[x, y, z], children=[])

def hot(name, x, y, rx, ry, w, h, cursor='examine'):
    return dict(type=40, name=name, point=[x, y, 41, 45], rect=[rx, ry, w, h], cursor=cursor, tail='00', children=[])

def val(v, *ch):
    return dict(type=51, value=v, children=list(ch))

def default(*ch):
    return dict(type=52, children=list(ch))

def cond(v, *ch):
    return dict(type=50, var=v, scope='0000', flag='00', children=list(ch))
