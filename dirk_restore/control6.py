"""Original native-scene reconstruction, generated from user-owned resources."""
from .fwd import Parser, build, count, pic, anim, hot, cond, val, default
import struct
import copy

def reconstruct(assets):
    old = assets['ch6/locations/zepelin_trap.fwd']
    root = Parser(old).parse()[0]
    layer = root['children'][0]['children'][0]
    geo = bytearray.fromhex(layer['geometry'])
    struct.pack_into('>H', geo, 4, 1207)
    layer['geometry'] = geo.hex()
    root['children'][0]['children'] = [layer]
    room = 'img/locations/zepelin_control_room/'
    import re
    routes = {}
    dialogue_fixes = {}
    baseclips = {'first': 'droid_stop_first', 'second': 'droid_stop_second', 'third': 'droid_stop_third', 'left': 'droid_left', 'right_down': 'droid_down_right', 'right_up': 'droid_up_right', 'correct': 'droid_correct'}
    for fp in sorted((n for n in assets if n.startswith('ch6/dialogues/zeppelin_droid_play') and n.endswith('.dia'))):
        text = assets[fp].decode().replace('\r\n', '\n')
        m = re.search('setlocal droid_anim ([^"\\n]+)', text)
        if not m:
            continue
        state = m.group(1)
        base = re.sub('_(?:s|st)$', '', state)
        robot = baseclips[base]
        fixed = text.replace('resetanimation droid_third', 'resetanimation ' + robot).replace('resetanimation statue_third', 'resetanimation statue_stop_third')
        fm = re.search('setlocal droid_anim ([^"\\n]+)', fixed)
        names = re.findall('resetanimation ([^"\\n]+)', fixed[:fm.start()])
        if robot not in names:
            line = '\t\tstartaction "resetanimation ' + robot + '"\n'
            at = fixed.rfind('\t\tstartaction', 0, fm.start())
            fixed = fixed[:at] + line + fixed[at:]
            names.append(robot)
        clips = []
        for name in dict.fromkeys(names):
            assert 'ch6/animations/' + name + '.anim' in assets, (fp, name)
            clips.append(anim('ch6/animations/' + name + '.anim', 0, 0, 3 if 'lift' in name else 2 if name.startswith('droid') else 1))
        if state in routes:
            assert routes[state] == clips, (fp, state)
        routes[state] = clips
        if fixed != text:
            dialogue_fixes[fp] = fixed
    import json
    result = {k: v.encode() for k, v in dialogue_fixes.items()}
    layer['children'] = [pic(room + 'MG', 0, 0, 10), cond('hatch', val('open', pic(room + 'hatch_open', 683, 234, 4), hot('hatch_open', 748, 254, 680, 230, 145, 60, 'exit')), default(pic(room + 'hatch', 683, 234, 4), hot('hatch_locked', 748, 254, 680, 230, 145, 60))), cond('#medallion', val('inventory'), val('used'), default(pic(room + 'medallion', 546, 112, 1), hot('medallion', 555, 145, 530, 112, 50, 78))), hot('door_trap', 1064, 165, 1025, 55, 85, 190, 'exit'), hot('poster', 65, 180, 30, 135, 65, 110), hot('computer', 155, 170, 115, 125, 100, 100), hot('wheel', 600, 73, 560, 30, 70, 75), hot('fire_label', 649, 85, 635, 55, 45, 55), hot('pet_robot', 580, 112, 565, 95, 45, 45, 'talk'), cond('control_panel', val('null', hot('panel_first', 605, 145, 530, 110, 145, 110)), val('repeat', hot('panel_repeat', 605, 145, 530, 110, 145, 110)), val('completed', hot('panel_completed', 605, 145, 530, 110, 145, 110))), cond('franklin_state^franklin_pos', val('instructive,null', pic('img/ch6/ms_F_instructive', 755, 119, 1), anim('ch6/animations/instructive_eyes.anim', 771, 143), cond('franklin_panel', val('instructive_repeat', hot('franklin_instr_repeat', 775, 155, 750, 105, 65, 110, 'talk')), default(hot('franklin_instr', 775, 155, 750, 105, 65, 110, 'talk')))), val('null,null', pic('img/locations/zepelin_trap/ms_franklin_standing', 755, 117, 1), cond('franklin_panel', val('null', hot('franklin_first', 775, 155, 750, 105, 65, 110, 'talk')), default(hot('franklin_repeat', 775, 155, 750, 105, 65, 110, 'talk')))), val('dehypnotized,null', pic('img/locations/zepelin_trap/ms_franklin_standing', 755, 117, 1), hot('franklin_dehypno', 775, 155, 750, 105, 65, 110, 'talk'))), cond('franklin_mouth', val('franklin', anim('ch6/animations/franklin_mouth.anim', 783, 150)), val('instructive', anim('ch6/animations/instructive_mouth.anim', 771, 155))), cond('droid', val('wait_for_droid_up', anim('ch6/animations/server_droid_lift.anim'), anim('ch6/animations/droidlift_up.anim'))), cond('droid_anim', *[val(state, *clips) for state, clips in sorted(routes.items())]), cond('server_droid_serving', val('stop_serving'), default(anim('ch6/animations/server_droid_serving.anim'))), cond('bobblehead', val('eating', anim('ch6/animations/bobblehead.anim'), anim('ch6/animations/bobblehead_arms2.anim')), val('spring', anim('ch6/animations/bobblehead_spring.anim', 577, 97)), val('laugh', anim('ch6/animations/bobblehead_laugh.anim', 577, 97), anim('ch6/animations/bobblehead_arms.anim', 577, 112)), default(anim('ch6/animations/bobblehead.anim', 577, 97)))]
    layer['children'] += [pic(room + n, x, y, 0) for n, x, y in [('overlay_computer', 151, 151), ('overlay_floor', 525, 240), ('overlay_podium', 533, 121), ('overlay_stairs', 841, 138)]]
    layer['children'].insert(1, pic(room + 'hypno_control_panel', 270, 125, 4))
    ranges = {'poster': (30, 65), 'computer': (115, 105), 'medallion': (530, 30), 'wheel': (560, 45), 'fire_label': (635, 40), 'pet_robot': (315, 50), 'panel_first': (275, 40), 'panel_repeat': (275, 40), 'panel_completed': (275, 40), 'hatch_open': (690, 80), 'hatch_locked': (690, 80), 'franklin_first': (785, 45), 'franklin_repeat': (785, 45), 'franklin_instr': (785, 45), 'franklin_instr_repeat': (785, 45), 'franklin_dehypno': (785, 45), 'door_trap': (1030, 80)}

    def room_strips(n):
        if n['type'] == 40:
            x, w = ranges[n['name']]
            n['rect'] = [x, 0, w, 320]
            if n['name'].startswith('panel_'):
                n['point'][0] = 290
            if n['name'].startswith('franklin_'):
                n['point'][0] = 805
            if n['name'] == 'pet_robot':
                n['point'][:2] = [335, 100]
            if n['name'] == 'fire_label':
                n['point'][0] = 650
        if n['type'] == 3 and n['image'] in ['img/ch6/ms_F_instructive', 'img/locations/zepelin_trap/ms_franklin_standing']:
            n['xydepth'][0] = 785
        if n['type'] == 5 and any((x in n['anim'] for x in ['franklin_mouth', 'instructive_eyes', 'instructive_mouth'])):
            n['xydepth'][0] += 30
        if n['type'] == 5 and 'bobblehead' in n['anim']:
            n['xydepth'][:2] = [312, 125] if 'arms' in n['anim'] else [314, 80] if 'laugh' in n['anim'] else [312, 78]
        for c in n['children']:
            room_strips(c)
    room_strips(root)
    fg = copy.deepcopy(Parser(old).parse()[0]['children'][0]['children'][1])
    g = bytearray.fromhex(fg['geometry'])
    struct.pack_into('>HH', g, 4, 1690, 320)
    fg['geometry'] = g.hex()
    fg['children'] = []
    keep = []
    for n in layer['children']:
        move = n['type'] == 50 and n['var'] in ['#medallion', 'bobblehead', 'control_panel'] or (n['type'] == 3 and n['image'] == room + 'hypno_control_panel') or (n['type'] == 40 and n['name'] == 'pet_robot')
        (fg['children'] if move else keep).append(n)
    layer['children'] = keep
    fg['children'] += [pic(room + 'FG_piston_1', 1284, 0, 2), pic(room + 'FG_piston_2', 1253, 238, 1)]
    root['children'][0]['children'] = [layer, fg]

    def reference_fg(n):
        if n['type'] == 3 and n['image'] == room + 'hypno_control_panel':
            n['xydepth'][:2] = [424, 126]
        if n['type'] == 3 and n['image'] == room + 'medallion':
            n['xydepth'][:2] = [508, 155]
        if n['type'] == 5 and 'bobblehead' in n['anim']:
            n['xydepth'][:2] = [466, 126] if 'arms' in n['anim'] else [468, 86] if 'laugh' in n['anim'] else [466, 84]
        if n['type'] == 40:
            if n['name'] == 'medallion':
                n['rect'] = [508, 0, 58, 320]
                n['point'][:2] = [535, 175]
            if n['name'] == 'pet_robot':
                n['rect'] = [466, 0, 42, 320]
                n['point'][:2] = [487, 110]
            if n['name'].startswith('panel_'):
                n['rect'] = [424, 0, 42, 320]
                n['point'][:2] = [445, 200]
        for c in n['children']:
            reference_fg(c)
    reference_fg(fg)

    def reference_actor(n):
        if n['type'] == 3 and n['image'] == 'img/locations/zepelin_trap/ms_franklin_standing':
            n['xydepth'][:2] = [838, 132]
        if n['type'] == 3 and n['image'] == 'img/ch6/ms_F_instructive':
            n['image'] = n['selected'] = 'img/locations/zepelin_trap/ms_franklin_hypnotized'
            n['xydepth'][:2] = [846, 127]
        if n['type'] == 5:
            if n['anim'] == 'ch6/animations/instructive_eyes.anim':
                n['xydepth'][:2] = [861, 146]
            if n['anim'] == 'ch6/animations/instructive_mouth.anim':
                n['xydepth'][:2] = [865, 154]
            if n['anim'] == 'ch6/animations/franklin_mouth.anim':
                n['anim'] = 'ch5/animations/franklin_mouth.anim'
                n['xydepth'][:2] = [868, 165]
        if n['type'] == 40 and n['name'].startswith('franklin_'):
            n['rect'] = [838, 0, 50, 320]
            n['point'][:2] = [860, 170]
        for c in n['children']:
            reference_actor(c)
        if n['type'] == 51 and n['value'] in ['null,null', 'dehypnotized,null'] and any((c['type'] == 3 and c.get('image') == 'img/locations/zepelin_trap/ms_franklin_standing' for c in n['children'])):
            n['children'].append(anim('ch5/animations/franklin_eyes.anim', 860, 155))
    reference_actor(layer)
    blob = build(root)
    assert build(Parser(blob).parse()[0]) == blob
    result['ch6/locations/zeppelin_control_room.fwd'] = blob
    a = []

    def action(n, v):
        a.append('@' + n + '.onClick\n' + v + '\n')
    for n, stem in [('hatch_locked', 'zepelin_control_locked_hatch'), ('door_trap', 'zeppelin_control_fade_to_trapl_room'), ('poster', 'zeppelin_control_hanginthere_poster'), ('computer', 'zeppelin_control_computer'), ('wheel', 'zeppelin_control_wheel'), ('fire_label', 'zeppelin_control_fire_cannon_label'), ('pet_robot', 'zeppelin_control_pet_robot'), ('medallion', 'zeppelin_control_pickup_medallion'), ('panel_first', 'zeppelin_control_panel_first_hypno_hint'), ('panel_repeat', 'zeppelin_self_destruct_select_panel'), ('panel_completed', 'zeppelin_control_panel_dr_oc_first'), ('franklin_first', 'zeppelin_control_panel_franklin_first'), ('franklin_repeat', 'zeppelin_control_panel_franklin_repeat'), ('franklin_instr', 'zeppelin_control_panel_franklin_instructive'), ('franklin_instr_repeat', 'zeppelin_control_panel_franklin_instructive_rpt'), ('franklin_dehypno', 'zeppelin_control_panel_franklin_dehypnotized_rpt')]:
        action(n, 'loaddialogue ch6/dialogues/' + stem + '.dia')
    action('hatch_open', 'loadlocation ch6/locations/zeppelin_cannon_room.fwd\nlocationoffset -200 0')
    result['ch6/locations/zeppelin_control_room.action'] = '\n'.join(a).encode()
    return result
