"""Original native-scene reconstruction, generated from user-owned resources."""
from .fwd import Parser, build, count, pic, anim, hot, cond, val, default
import struct
import copy

def reconstruct(assets):
    old = assets['ch6/locations/zepelin_trap.fwd']
    root = Parser(old).parse()[0]
    assert build(root) == old
    layers = root['children'][0]['children']
    orig = copy.deepcopy(layers)
    main = layers[0]['children'][:4]
    main += [cond('franklin_state', val('null', pic('img/locations/zepelin_trap/ms_franklin', 715, 69, 1)), val('standing', pic('img/locations/zepelin_trap/ms_franklin_standing', 634, 117, 1), anim('ch5/animations/franklin_eyes.anim', 656, 140))), cond('dirk', val('reflecting', pic('img/locations/zepelin_trap/dirk_reflecting', 470, 152, 1), pic('img/locations/zepelin_trap/laser_to_rope', 493, 95, 2), pic('img/locations/zepelin_trap/laser_to_rope_contd', 505, 40, 2)))]
    for var in ['plankOne', 'plankTwo']:
        main += [cond(var, val('left', pic('img/ch5/puzzle1/plank2_place2', 533, 170, 5)), val('right', pic('img/ch5/puzzle1/plank1_place2', 580, 185, 4)), val('water', pic('img/ch5/puzzle1/board1_place2_water', 670 if var == 'plankOne' else 755, 230, 4), hot(var + '_water', 700 if var == 'plankOne' else 800, 258, 670 if var == 'plankOne' else 765, 230, 80, 75)))]
    main += [cond('dirk', val('null', pic('img/locations/zepelin_trap/dirk', 257, 105, 1), anim('ch5/animations/dirk_eyes.anim', 286, 132), cond('harry_dirk', val('repeat', hot('harry_dirk_repeat', 300, 140, 255, 0, 60, 320, 'talk')), default(hot('harry_dirk_first', 300, 140, 255, 0, 60, 320, 'talk')))))]
    main += [cond('rope', val('cut', pic('img/ch5/puzzle1/rope_cut', 538, 69, 0)), val('dangling', pic('img/ch5/puzzle1/rope_cut', 538, 69, 0)), default(pic('img/ch5/puzzle1/rope', 538, 69, 0)))]
    main += [cond('#planks', val('!used', pic('img/locations/zepelin_trap/planks', 403, 108, 1)))]
    beam = copy.deepcopy(orig[0]['children'][10])
    main += [beam, copy.deepcopy(orig[0]['children'][13])]
    main += [hot('evil1', 373, 136, 355, 30, 45, 165), cond('laser_state', val('middle'), default(hot('evil2', 496, 127, 480, 30, 40, 165))), hot('door', 425, 102, 415, 30, 45, 150, 'exit'), cond('franklin_state', val('null', cond('dirk', val('null', hot('franklin_harry', 735, 100, 715, 0, 35, 320, 'talk')), default(cond('franklin', val('null', hot('franklin_first', 660, 90, 635, 15, 55, 140, 'talk')), default(hot('franklin_repeat', 660, 90, 635, 15, 55, 140, 'talk')))))), val('standing', hot('franklin_standing', 650, 154, 630, 110, 55, 100, 'talk'))), cond('dirk', val('free', cond('#planks', val('!used', hot('pickup_planks', 410, 145, 390, 0, 25, 320))), cond('plank_state', val('correct', hot('plank_correct', 550, 205, 515, 160, 65, 75)), default(cond('plankOne^plankTwo', val('left,*', hot('pickup_left_one', 550, 205, 515, 160, 65, 75)), val('*,left', hot('pickup_left_two', 550, 205, 515, 160, 65, 75)), default(hot('plank_left', 550, 205, 515, 160, 65, 75))))), cond('plankOne^plankTwo', val('left,*', hot('place_two_right', 690, 208, 580, 180, 265, 50)), val('*,left', hot('place_one_right', 690, 208, 580, 180, 265, 50)), default(hot('place_unsupported', 690, 208, 580, 180, 265, 50))), cond('laser_state', val('middle', cond('plank_state^barrel_reflection^franklin_state', val('correct,blade,null', hot('laser_ready', 480, 180, 460, 120, 42, 100)), default(hot('laser_not_ready', 480, 180, 460, 120, 42, 100))))), cond('laser_state', val('middle', hot('barrel_middle', 875, 205, 850, 150, 55, 110)), val('down', hot('barrel_down', 875, 205, 850, 150, 55, 110)), default(hot('barrel_first', 875, 205, 850, 150, 55, 110))), cond('barrel_reflection', val('blade', hot('reflector', 875, 223, 850, 210, 55, 40)), val('tip', hot('reflector', 875, 223, 850, 210, 55, 40))))), cond('franklin_state', val('standing', hot('escape', 745, 103, 725, 65, 55, 90, 'exit')), default(hot('escape_locked', 745, 103, 725, 65, 55, 90, 'exit')))]
    layers[0]['children'] = main
    fg = orig[1]['children'][:3]
    fg += [cond('lever_state', val('first_anim', anim('ch5/animations/pull_lever1.anim')), default(pic('img/locations/zepelin_trap/lever_2', 145, 133))), cond('dirk', val('null', cond('hypno_gun^harry_rat', val('null,*', hot('lever_first', 145, 146, 161, 0, 48, 320)), val('repeat,*', hot('lever_repeat', 145, 146, 161, 0, 48, 320)), val('pushed,true', hot('lever_rat', 145, 146, 161, 0, 48, 320)), default(hot('lever_pushed', 145, 146, 161, 0, 48, 320))), cond('hypno_gun_state^hypno_ray^harry_rat', val('weakened,*,true', hot('ray_weak_rat', 90, 130, 0, 0, 160, 320)), val('weakened,null,*', hot('ray_weak_first', 90, 130, 0, 0, 160, 320)), val('weakened,repeat,*', hot('ray_weak_repeat', 90, 130, 0, 0, 160, 320)), val('weakened,off,*', hot('ray_weak_rat', 90, 130, 0, 0, 160, 320)), default(hot('ray_first', 90, 130, 0, 0, 160, 320))))), copy.deepcopy(orig[1]['children'][7])]
    layers[1]['children'] = fg
    main.append(copy.deepcopy(orig[0]['children'][11]))
    main.append(cond('harry_state', val('there', hot('harry_hint', 330, 148, 315, 0, 30, 320, 'talk'))))
    strips = {'evil1': (355, 35), 'door': (415, 25), 'pickup_planks': (390, 25), 'laser_ready': (480, 35), 'laser_not_ready': (480, 35), 'plank_left': (525, 55), 'plank_correct': (525, 55), 'pickup_left_one': (525, 55), 'pickup_left_two': (525, 55), 'place_one_right': (590, 40), 'place_two_right': (590, 40), 'place_unsupported': (590, 40), 'plankOne_water': (690, 25), 'plankTwo_water': (785, 40), 'franklin_harry': (715, 35), 'franklin_first': (715, 35), 'franklin_repeat': (715, 35), 'franklin_standing': (645, 35), 'escape': (730, 45), 'escape_locked': (755, 25), 'barrel_first': (850, 30), 'barrel_down': (850, 30), 'barrel_middle': (850, 30), 'reflector': (880, 30)}

    def strips_in(n):
        if n['type'] == 40:
            x, _, w, _ = n['rect']
            x, w = strips.get(n['name'], (x, w))
            n['rect'] = [x, 0, w, 320]
            if n['name'].startswith('place_'):
                n['point'][0] = 610
            if n['name'] == 'reflector':
                n['point'][0] = 895
            if n['name'] in ['franklin_first', 'franklin_repeat']:
                n['point'][0] = 735
            if n['name'] == 'escape_locked':
                n['point'][0] = 765
        for c in n['children']:
            strips_in(c)
    strips_in(root)
    blob = build(root)
    assert build(Parser(blob).parse()[0]) == blob
    result = {'ch5/locations/zepelin_trap.fwd': blob}
    a = []

    def action(name, script):
        a.append('@' + name + '.onClick\n' + script + '\n')

    def dia(name, stem):
        action(name, 'loaddialogue ch5/dialogues/zepelin_trap_' + stem + '.dia')
    for name, stem in [('harry_dirk_first', 'harry_dirk_first'), ('harry_dirk_repeat', 'harry_dirk_repeat'), ('franklin_harry', 'harry_franklin'), ('harry_hint', 'harry_after_puzzle'), ('rat_first', 'rat'), ('evil1', 'dirk_evil_contraption1'), ('evil2', 'dirk_evil_contraption2'), ('door', 'door'), ('franklin_first', 'dirk_franklin_first'), ('franklin_repeat', 'dirk_franklin_repeat'), ('franklin_standing', 'franklin_standing'), ('pickup_planks', 'pickup_planks'), ('lever_first', 'hypno_gun_first'), ('lever_repeat', 'hypno_gun_repeat'), ('lever_rat', 'hypno_gun_pushed_rat'), ('lever_pushed', 'hypno_gun_pushed'), ('ray_first', 'hypno_ray_first'), ('ray_weak_first', 'hypno_ray_weakened_first'), ('ray_weak_repeat', 'hypno_ray_weakened_repeat'), ('ray_weak_rat', 'hypno_ray_weakened_rat'), ('barrel_first', 'laser_barrel_first'), ('barrel_down', 'laser_barrel_down'), ('barrel_middle', 'laser_barrel_blade_middle'), ('reflector', 'laser_barrel_pickup_reflector'), ('laser_ready', 'laser_floor_repeat'), ('laser_not_ready', 'laser_floor_first'), ('plank_correct', 'dirk_planks_correct'), ('plank_left', 'dirk_planks_half_correct'), ('place_one_right', 'dirk_planks_correct'), ('place_two_right', 'dirk_planks_correct'), ('place_unsupported', 'poolside'), ('escape_locked', 'planks_correct')]:
        dia(name, stem)
    for name in ['barrel_first', 'barrel_down', 'barrel_middle']:
        for item, stem in [('brokenBlade', 'laser_barrel_use_blade'), ('bladeTip', 'laser_barrel_use_blade_tip')]:
            a.append(f'@{name}.onItem {item}\nloaddialogue ch5/dialogues/zepelin_trap_{stem}.dia\n')
    for item, stem in [('plankOne', 'place_plank_one_left'), ('plankTwo', 'place_plank_two_left')]:
        a.append(f'@plank_left.onItem {item}\nloaddialogue ch5/dialogues/zepelin_trap_{stem}.dia\n')
    for name, item, stem in [('place_one_right', 'plankOne', 'place_plank_one_right'), ('place_two_right', 'plankTwo', 'place_plank_two_right'), ('place_unsupported', 'plankOne', 'place_plank_one_water'), ('place_unsupported', 'plankTwo', 'place_plank_two_water'), ('laser_ready', 'bladeTip', 'free_franklin'), ('laser_not_ready', 'bladeTip', 'laser_floor_first_use_tip')]:
        a.append(f'@{name}.onItem {item}\nloaddialogue ch5/dialogues/zepelin_trap_{stem}.dia\n')
    for name, stem in [('plankOne_water', 'pickup_plank_one_water'), ('plankTwo_water', 'pickup_plank_two_water')]:
        dia(name, stem)
    action('pickup_left_one', 'setlocal plankOne null\nitempickup plankOne')
    action('pickup_left_two', 'setlocal plankTwo null\nitempickup plankTwo')
    action('escape', 'loadlocation ch5/locations/zepelin_ledge.fwd\nlocationoffset 0 0')
    result['ch5/locations/zepelin_trap.action'] = '\n'.join(a).encode()
    return result
