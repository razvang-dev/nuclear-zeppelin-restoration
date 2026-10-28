# Dirk Dagger and the Nuclear Zeppelin: Native Resource Restoration

**Technical restoration report | N-Gage 2.0 | 27 October 2026**
**Restoration status: owner-confirmed working reconstruction**

## Overview

*Dirk Dagger and the Nuclear Zeppelin* (*Dirk Dagger II*) is an N-Gage 2.0 game for Symbian, identified by game SID `0x2001AD86`. Its original installation retains the game's executable, most of its artwork, animations, dialogue, localization, and location scripts. A separate protected resource dependency, however, leaves certain chapter controllers and scene definitions unavailable to the ordinary game loader. The absence of those definitions interrupts otherwise intact game systems.

The restoration supplies a small set of native-format resource definitions, allowing the original engine to connect surviving locations, interpret their original scripts, and progress through the game's six chapters. The verified reconstruction contains **22 entries** in a **12,716-byte `protected_general.opes`** archive: twelve controller/location resources and ten targeted dialogue overrides. It does not replace the game engine, redraw the artwork, or patch the distributed EXE or DLL files.

The restoration reconstructs missing scene definitions using the game's original assets and scripts, with placement, layering, and animation alignment checked against the original retail game's presentation in the reviewed scenes.

The project owner has confirmed the complete restoration as working across all six chapters, including its scene composition, animation behavior, interaction regions and map-label placement. The original protected archive has not been decrypted; the replacement is an independently constructed native-format resource archive, not recovered historical plaintext.

## 1. The surviving game and its missing dependency

The examined installation separates executable code, ordinary resources, localization, and protected resources. The notable components are:

| Component | Recorded characteristics | Function |
| --- | --- | --- |
| `dd_ii.exe` | Original Symbian game executable | Runs the native game engine and story logic. |
| `ngifilemanagerfactory_2001AD86.dll` | Game-specific native file-manager factory | Participates in the installed game's resource-handling architecture. |
| `opes_general.opes` | 32,144,179 bytes; 7,313 entries | Principal original artwork, animations, scripts, and location resources. |
| `opes_loc-en.opes` | 190,941 bytes; 696 entries | Original English-language resources. |
| `startup_general.opes` | 390,586 bytes; 62 entries | Startup assets. |
| `protected_loc-en.opes` | 789 bytes; 4 entries | Surviving readable protected-part localization metadata. |
| `protected_general.opes.ngdat` | 39,333-byte encrypted wrapper; declares 39,021 bytes of plaintext | Unrecovered original protected resource dependency. |

These retail-file measurements come from the project inventory. Original installation files are supplied locally by the user.

Resource paths and calls surviving in the main archive identify functional gaps. In particular, the game needs a Chapter 2 entry controller, chapter-specific maps for Chapters 2–4, and significant interactive scenes in Chapters 5–6. The readable protected-part localization data also names the Chapter 2 controller and Chapters 2–4 maps. These surviving relationships supply the reconstruction's interface contract: expected paths, native object types, script handlers, state conditions, and the original destinations those handlers must reach.

A location definition and its referenced behavior are different pieces of the system. An `.fwd` scene specifies what can appear and what is interactive; an `.action` file binds events to commands such as opening locations, invoking dialogues, and changing visit state. The original `.dia` resources, images, animations, and story flags already provide much of the required behavior. Reconstructing the missing connection points is therefore materially different from reimplementing the game.

## 2. Native OPES archive construction

### 2.1 Container layout

OPES is a game resource archive, not the `NGDAT` protected-content wrapper. Its directory records identify internal paths, compression status, stored and expanded sizes, and image metadata. The relevant inspected fields are:

| Position | Size | Representation | Meaning |
| --- | ---: | --- | --- |
| File offset `0` | 4 bytes | ASCII | Signature `opes`. |
| File offset `8` | 4 bytes | Little-endian unsigned integer | Number of directory entries. |
| Each directory record, bytes `0–89` | 90 bytes | NUL-padded bytes | Internal resource path. |
| Directory record byte `90` | 1 byte | As observed | Zero in the inspected layout. |
| Directory record byte `91` | 1 byte | Compression flag | Determines whether the payload is zlib-compressed. |
| Directory record bytes `92–95` | 4 bytes | Little-endian unsigned integer | Stored payload length. |
| Directory record bytes `96–99` | 4 bytes | Little-endian unsigned integer | Expanded payload length. |
| Directory record bytes `100–103` | 4 bytes | Existing image metadata | Width for image resources. |
| Directory record bytes `104–107` | 4 bytes | Existing image metadata | Height for image resources. |

The header is 12 bytes and each directory record is 112 bytes. Fields not assigned a purpose by the research are retained rather than given invented semantics. Payload streams follow the directory and are located by accumulating stored lengths.

The compression flag is authoritative. The examined original main archive has **6,888 compressed entries with unequal stored and expanded lengths, seven compressed entries whose lengths happen to be equal, and 418 uncompressed equal-length entries**. Comparing the two lengths to guess compression therefore misclassifies valid content. Correct compression marking was a decisive part of making the reconstructed plaintext resources load through the engine's normal archive path.

### 2.2 Building and validating an archive

The archive builder writes native directory records, retains the required file and entry layout, and stores each replacement payload with its corresponding compression marker. The reader verifies directory bounds, unique internal names, zlib stream completion, declared expanded lengths, and exact consumption of the archive without trailing data. A serialize/read-back comparison verifies that each expanded resource matches its intended input.

The verified output has **22 entries**, each marked compressed, with a combined **34,931 expanded resource bytes**. The supplied archive was independently checked for signature, directory count, entry decoding, expanded lengths, unique paths, and absence of trailing bytes. This independently establishes archive integrity alongside the project owner’s confirmation of the finished restoration in the running game.

The reconstructed OPES deliberately contains scripts and scene definitions rather than copies of the original artwork or dialogue library. Its paths are chosen so the original loader resolves references to the surviving retail data.

## 3. FWD scenes, event actions, and original assets

### 3.1 Reconstructing the scene graph

Native `.fwd` data begins with `fwd2DIST`, followed by a big-endian 16-bit version (observed version `1`) and node count. Length-prefixed strings use big-endian 16-bit lengths; coordinate fields commonly use big-endian signed 16-bit values. This differs from OPES directory metadata, which uses little-endian integers.

Scene data contains nested controls and layers; image and animation references; interactive hotspots; conditional, value-specific, and default branches; audio nodes; and position/depth fields. These structures let the existing engine decide visibility, draw order, event targeting, and traversal without a replacement renderer. The original trap-room definition and a surviving plank-room prototype served as structural examples for byte-for-byte round-trip tests of selected node types. The prototype was a format reference, not a complete substitute for the missing room: some of its assets and behavior did not match the surviving final-room scripts.

The research parser/serializer is intentionally described as **validated on selected surviving scenes**, not as a complete decoder of every possible FWD construct. In particular, pickup-node handling remains partially supported. For late map-label adjustments, the known coordinate fields could be changed directly while preserving the surrounding binary records.

### 3.2 Resource-driven event dispatch

Native `.action` files attach behavior to controls using engine-recognized handlers such as `onClick` and inventory-sensitive `onItem`. The reconstructed handlers point to original dialogues and locations with commands including `loadlocation`, `loaddialogue`, `loadgadget`, `locationoffset`, and localized or global state updates. The resulting player interactions remain governed by the original dialogue scripts, inventory checks, and flags.

This distinction matters in puzzles. Rather than assigning a solved state or inserting an item directly, a replacement map or scene normally invokes the game's existing event sequence. Original script effects then update the world state, unlock the next hotspot, animate a character, or route the player onward. The reconstructed controls provide the missing dispatch context; the original game remains responsible for progressing the story.

### 3.3 Art, animation, and coordinate evidence

Original image dimensions are preserved from OPES metadata. For inspecting surviving DSI artwork, the research distinguished two image payload variants:

- DSI marker `0`: pixel data encoded as little-endian RGB565.
- DSI marker `1`: a big-endian 16-bit palette count, big-endian RGB565 palette entries, and byte-sized pixel indices. An optional matching `_a` image supplies alpha.

Native `.anim` resources are text-based animation-frame records carrying image references, duration, coordinates, named endings, and in some cases audio. Their offsets must be interpreted in the context of the particular animation: robot route clips, for example, commonly use absolute room-world positions rather than a uniformly relative origin. Native animation definitions and original artwork are reused instead of being redrawn or replaced by synthesized frames.

## 4. Restoring chapters and navigation

### Chapter 2: entry and town-map dispatch

The Chapter 2 `.action`/`.fwd` controller pair provides the missing entry/menu connection. Its town map restores the chapter's original office, diner, mansion, and docks routes, including first-visit and repeat-visit behavior. The town map also carries a gameplay-critical office dispatch that demonstrates why a reconstructed location must reproduce *events* as well as visible navigation.

The surviving diner dialogue already moves the roadworker into `roadworker=pothole`. On subsequent map-to-office travel, the restored conditional invokes one of two original dialogues according to the current pothole state:

| Situation | Original dialogue invoked | Native resulting state observed in targeted tests |
| --- | --- | --- |
| Bare hole | `outside_office_fill_pothole` | `pothole=null`; `roadworker=repeat`. |
| Tub placed in hole | `outside_office_fill_tub` | `pothole=tub_and_cement`; `roadworker=gone`. |

The filled tub is collected through the game's original pickup interaction. No artificial tub award or chapter-success flag is needed. The **DOCKS** map label was subsequently positioned for both Chapter 2 visit states.

### Chapter 3: discovery-controlled destinations

The Chapter 3 map restores six destinations: office, diner, mansion, docks, morgue, and Heaven's Above tower. Its tower control respects the original `wow_tower` discovery condition. The first mapped arrival invokes the surviving arrival dialogue; repeat visits follow the established tower route. Separate office and diner visit markers remain in place. The **DOCKS**, **MORGUE**, and **HEAVEN'S ABOVE** labels, together with the tower first-visit `Plus` graphic, are positioned within the map's native scene layout.

### Chapter 4: story gates and first-entry presentation

Chapter 4 reconstructs the same six location types with chapter-specific conditions, not a generic copy of Chapter 3. The tower is a normal destination at this stage of the story, while the original mansion progression gate is retained. The first diner entry dispatches the surviving map zoom gadget; later entries use the normal diner scene. Map labels for **DOCKS**, **MORGUE**, and **HEAVEN'S ABOVE**, and the mansion first-visit `Plus` graphic, are integrated into their original map composition.

The reconstruction preserves the distinction between selectable destinations, discovery or visit state, and the native action invoked when a destination is chosen. Its Chapter 4 map contains targeted coordinate adjustments for the intended label and first-visit graphic placement.

## 5. Chapter 5: zeppelin trap-room integration

The trap-room reconstruction comprises `ch5/locations/zepelin_trap.fwd` and its matching `.action`. It uses original panoramic/parallax artwork, scene imagery, animations, and dialogues to reconnect Harry's interactions, the lever and weakened-ray sequence, freeing Dirk, plank placement and retrieval, laser and blade-reflection interactions, Franklin's rescue, and the porthole route to the following location.

The reconstructed native hotspots are intentionally shaped for a panoramic scene navigated by keypad. Full-height interaction strips can retain access to objects while the view pans, whereas narrowly bounded hotspots may leave actions difficult to target. Where action regions overlap, the controls are conditional or spatially separated so an unrelated machinery inspection is not dispatched alongside the active laser interaction. Harry's conversational controls are likewise separated from competing regions.

Important scene placements and their visibility are tied to the original room and story states:

| Element | Scene coordinates | Behavior |
| --- | --- | --- |
| Bound Dirk | `(257, 105)` | Bound pose follows the applicable story condition. |
| Dirk's eyes | `(286, 132)` | Eye overlay is composed with the bound pose. |
| Hanging Franklin | `(715, 69)` | Hanging artwork is used in its corresponding state. |
| Rope | `(538, 69)` | State-dependent rope presentation. |
| Loose planks | `(403, 108)` | Position and pickup availability follow the plank progression state. |

The established standing Franklin and supported-plank placements remain in use. The original plank pickup is progression-gated; supported placements, fallen-plank recovery, and the correct bridge condition are handled through original stateful dialogue and inventory operations. In prior targeted tests, an appropriate combination of bridge and laser states permitted the existing rescue sequence to reach `franklin_state=standing`, `porthole=open_first`, and `rope=dangling`.

These elements connect the scene's original puzzle machinery rather than bypassing it. The completed six-chapter campaign route and subsequent scene-composition refinements are part of the owner-confirmed working restoration.

## 6. Chapter 6: control-room composition and final puzzle systems

The reconstructed `ch6/locations/zeppelin_control_room.fwd` and `.action` connect the control room's medallion, computer, poster, wheel, robot, panel, Franklin, hatch, and return door. Story progression continues through the game's ordinary hypnosis, instruction, and quiz states. Medallion use can set `dirk_idea=real`; the original Franklin/lever sequence can reach `franklin_state=instructive`. On returning to the control room, `franklin_panel_state=instructive` permits the native quiz option to appear. The replacement does not declare a quiz victory, pre-solve the robot, or grant a final-completion flag. Surviving cannon-room and minigame resources remain in the original main archive.

### 6.1 Layers, parallax, and character poses

The restored room differentiates middle-ground and foreground art in the engine's native coordinate spaces. The foreground-to-main scale ratio is **350/250 = 1.4** and the foreground canvas is **1690 × 320**. Foreground elements and their controls follow that layer's parallax rather than being positioned as stationary main-scene overlays.

| Foreground element | Coordinates |
| --- | --- |
| Pet stand | `(424, 126)` |
| Idle pet head | `(466, 84)` |
| Laughing pet head | `(468, 86)` |
| Pet arms | `(466, 126)` |
| Medallion/pendant | `(508, 155)` |
| Piston top | `(1284, 0)` |
| Piston base | `(1253, 238)` |

The pendant rests on the stand in the intended layered composition. The piston is present as separate top and base imagery. Franklin's normal and instructed states use distinct original room-scale sprites and corresponding face overlays:

| Franklin state | Main sprite | Sprite coordinates | Eyes | Mouth |
| --- | --- | --- | --- | --- |
| Normal | `ms_franklin_standing` | `(838, 132)` | `(860, 155)` | `(868, 165)` |
| Instructed | `ms_franklin_hypnotized` (55 × 176) | `(846, 127)` | `(861, 146)` | `(865, 154)` |

These coordinates belong to their respective native scene layers and should not be casually mixed or rescaled. The instructed pose uses the original room-specific sprite rather than a larger illustration prepared for a different camera view.

### 6.2 Robot routing and animation composition

The robot puzzle references original route animations for stop, left, down-right, up-right, and correct-path outcomes. Route animations and their matching statue components must be assembled at the appropriate depth. In the reconstructed scene, the relevant depth values are **statue `1`, robot `2`, and lift `3`**, with a lower depth value drawing in front. Native middle-ground occlusion art covers the computer, floor, podium, and stairs as required by the room.

All **20 programmed route branches** receive the corresponding robot base animation layers beneath their statue layers. This resolves a composition issue in which the statue element alone did not show the complete robot. The four correct-route variants reset the `droid_correct` animation. Ten narrowly scoped `.dia` overrides adjust animation resets without replacing the full original dialogue system.

Six `_s`-suffix route scripts contained references to the stale animation name `droid_third`; the selected overrides reset the animation corresponding to the active route state instead. The surviving `statue_third` naming is mapped to the applicable `statue_stop_third` scene resource. These are identifiable surviving-script/scene integration inconsistencies; without the original protected scene plaintext, they are **not established defects in an observed retail playthrough**.

The scene also contains intentional black fades in authored transitions. Such transitions are not, on their own, evidence of absent sprites or an incomplete resource lookup.

## 7. Resource loading and N-Gage entitlement are separate

The original game loader discovers archives following its `*_general.opes` naming convention. The reconstructed `protected_general.opes` is placed beside the unchanged `opes_general.opes` in the game's private directory. The former protected `protected_general.opes.ngdat` remains renamed with a `.ngdat.disabled` suffix, preventing it from serving as the active encrypted-resource route. The standalone plaintext OPES is the established working approach; replacing it with a synthetic NGDAT is **not** part of this release.

The original encrypted NGDAT declares **39,021 bytes** of plaintext, but that original content was neither decrypted nor recovered. A separate artificial encryption/container round-trip proved only internal consistency of a research object, not successful in-game NGDAT loading. An optional NGDAT-based packaging experiment remains outside the confirmed restoration. The verified standalone OPES remains the known-good baseline. This distinction is fundamental: the project constructs compatible *replacement definitions*, not the original protected data or a recovered decryption key.

Resource reconstruction and the game launcher’s entitlement checks are separate concerns. This project does not supply, generate or validate entitlement records, and it makes no claim to decrypt the original protected NGDAT. Existing legitimate installation files, saves, language resources, EXE and DLLs should be preserved when testing a locally generated OPES.

## 8. Verification and limits

The working reconstruction was evaluated with the original game engine in EKA2L1, including chapter navigation, native puzzle events, trap-room composition and the instruction/quiz progression. The project owner has confirmed the current six-chapter restoration as working. These findings do not constitute an original-hardware test or an exhaustive audit of every optional branch; artwork and animation comparisons refer to the reviewed scenes. The work reconstructs missing interfaces and corrects problems in the replacement definitions, without claiming to repair an independently proven defect in the retail executable.

The published build requires a user-supplied, hash-verified original package. It validates each of the 22 reconstructed resources, serializes the native OPES and checks the final file hash. The private verified reference archive is not distributed.

| Locally generated artifact | Size | Verified SHA-256 |
| --- | ---: | --- |
| `protected_general.opes` | 12,716 bytes | `b586611a8a848ed109926d7c2c51b5bc3a3beb1fb9a1cfc0da251347d347b365` |

### Save research is a separate concern

A donated save was used in earlier research to expose chapter selection, extras, and four minigames. Its examined checksum is a four-byte, big-endian, nonreflected CRC with polynomial `0x04C11DB7`, zero initialization, and zero final XOR. This was useful for understanding saved-state behavior, **not** for reconstructing the unavailable resource archive. A save contains no missing original artwork or decryption key, and donated-save functionality is not treated as proof of normal campaign completion. No save is included in the public repository.

## 9. Public source and reproducibility

The public repository presents the original restoration engineering work without redistributing the game. Appropriate public components include the project's own OPES parser/serializer and validator, supported FWD tools, reconstruction/build logic, technical documentation, and tests that operate on data supplied locally by the user. The implemented build process accepts the supported user-supplied package, derives original resources locally, and verifies all 22 expanded payload hashes and the full verified archive SHA-256.

This repository **does not distribute** the original `.n-gage` package, the compiled replacement OPES, synthetic `.dr` entitlement, original NGDAT, emulator builds, ROMs, firmware, extracted game artwork or scripts, private saves, research recordings, or private research archives. Users provide their own original game package. The local build workflow, supported input checksum, per-resource checks and source provenance are documented in `reproducibility.md` and `provenance.md`. Original project source and documentation are distributed under the MIT License with attribution to RazvanG; original game content is outside that license.

The central preservation result is a small, native-format bridge between surviving original resources and missing controller/scene definitions. The original engine continues to execute the game's artwork, logic, and script-driven progression, while the reconstruction supplies the connections that let those systems operate together.

## Appendix: replacement-resource inventory

All paths below are the internal paths of entries in the reconstructed OPES. The expanded sizes are verified against the private reference archive.

| Internal path | Expanded bytes |
| --- | ---: |
| `chapters/chapter2.action` | 228 |
| `chapters/chapter2.fwd` | 386 |
| `ch2/locations/map.action` | 1,131 |
| `ch2/locations/map.fwd` | 1,431 |
| `ch3/locations/map.action` | 994 |
| `ch3/locations/map.fwd` | 1,570 |
| `ch4/locations/map.action` | 837 |
| `ch4/locations/map.fwd` | 1,340 |
| `ch5/locations/zepelin_trap.action` | 4,539 |
| `ch5/locations/zepelin_trap.fwd` | 7,430 |
| `ch6/locations/zeppelin_control_room.action` | 1,527 |
| `ch6/locations/zeppelin_control_room.fwd` | 5,327 |
| `ch6/dialogues/zeppelin_droid_play_correct_s.dia` | 1,126 |
| `ch6/dialogues/zeppelin_droid_play_correct_st.dia` | 1,057 |
| `ch6/dialogues/zeppelin_droid_play_correct_st_cd.dia` | 1,062 |
| `ch6/dialogues/zeppelin_droid_play_correct_st_cu_dn.dia` | 1,069 |
| `ch6/dialogues/zeppelin_droid_play_first_s.dia` | 624 |
| `ch6/dialogues/zeppelin_droid_play_left_s.dia` | 657 |
| `ch6/dialogues/zeppelin_droid_play_right_down_s.dia` | 676 |
| `ch6/dialogues/zeppelin_droid_play_right_up_s.dia` | 669 |
| `ch6/dialogues/zeppelin_droid_play_second_s.dia` | 627 |
| `ch6/dialogues/zeppelin_droid_play_third_s.dia` | 624 |

**Inventory totals:** 22 unique entries; 34,931 expanded bytes; 12,716 bytes in the complete compressed OPES file.
