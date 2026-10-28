"""Combine native templates, original reconstruction recipes and scene builders."""
import copy
import json
from pathlib import Path
from . import fwd, trap5, control6

ROOT = Path(__file__).parent


def manifest():
    return json.loads((ROOT / 'baseline.json').read_text())


def _scene(node, source):
    if 'from' in node:
        value = source
        for index in node['from']:
            value = value['children'][index]
        value = copy.deepcopy(value)
    else:
        value = dict(node['node'], children=[])
    value.update(node.get('set', {}))
    if 'children' in node:
        value['children'] = [_scene(child, source) for child in node['children']]
    return value


def reconstruct(assets):
    result = {}
    # The entry controller is a native chapter4 template with chapter2 references.
    for extension in ('action', 'fwd'):
        value = assets['chapters/chapter4.' + extension]
        if extension == 'action':
            value = value.replace(b'ch4/ch4.gdg', b'ch2/ch2.gdg').replace(b'chapter4Quit', b'chapter2Quit')
        else:
            value = value.replace(b'chapter4.action', b'chapter2.action').replace(b'chapter_4', b'chapter_2')
        result['chapters/chapter2.' + extension] = value
    source = fwd.Parser(assets['ch1/locations/map.fwd']).parse()[0]
    if fwd.build(source) != assets['ch1/locations/map.fwd']:
        raise ValueError('Native map template did not round-trip')
    native_lines = assets['ch1/locations/map.action'].decode().replace('\r\n', '\n').splitlines(keepends=True)
    for chapter in (2, 3, 4):
        recipe = json.loads((ROOT / 'recipes' / f'map{chapter}.json').read_text())
        result[f'ch{chapter}/locations/map.fwd'] = fwd.build(_scene(recipe, source))
        operations = json.loads((ROOT / 'recipes' / f'map{chapter}_actions.json').read_text())
        result[f'ch{chapter}/locations/map.action'] = ''.join(
            ''.join(native_lines[slice(*op['copy'])]) if 'copy' in op else op['write']
            for op in operations).encode()
    result.update(trap5.reconstruct(assets))
    result.update(control6.reconstruct(assets))
    return result
