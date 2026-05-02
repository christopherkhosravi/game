# Audio Assets — Comox (HNOV)

All sounds are **CC0 / Public Domain** via [Kenney.nl](https://kenney.nl).
Do **not** modify the game file yet — this folder is assets-only pending implementation.

---

## sfx/

| File | Cue # | Description | Source pack | Source file |
|------|-------|-------------|-------------|-------------|
| `jump.ogg` | #1 | Short airy whoosh, light and floaty | Kenney Digital Audio | `phaseJump1.ogg` |
| `dash_start.ogg` | #4 | Quick sharp zip/swoosh | Kenney Digital Audio | `phaserUp1.ogg` |
| `dash_expire.ogg` | #5 | Short deceleration sweep | Kenney Digital Audio | `phaserDown1.ogg` |
| `dash_charge_used.ogg` | #13 | Low pip-drain click | Kenney Digital Audio | `lowDown.ogg` |
| `charges_restored.ogg` | #14 | Soft double-pip recharge chime | Kenney Digital Audio | `twoTone1.ogg` |
| `land.ogg` | #15 | Light thud | Kenney Impact Sounds | `impactSoft_medium_000.ogg` |
| `death.ogg` | #16 | Sharp impact hit (death distortion swell) | Kenney Sci-Fi Sounds | `explosionCrunch_000.ogg` |
| `you_died.ogg` | #17 | Short low stab / YOU DIED sting | Kenney Interface Sounds | `error_001.ogg` |
| `countdown_3.ogg` | #18 | Deep-ish game beep (countdown step 3) | Kenney Digital Audio | `pepSound3.ogg` |
| `countdown_2.ogg` | #19 | Same family, slightly higher (countdown step 2) | Kenney Digital Audio | `pepSound4.ogg` |
| `countdown_1.ogg` | #20 | Highest of the three (countdown step 1) | Kenney Digital Audio | `pepSound5.ogg` |
| `go.ogg` | #21 | Bright upward power-up tone (GO!) | Kenney Digital Audio | `powerUp1.ogg` |

## music/

*(empty — music tracks not yet sourced)*

---

## Source packs (in `_sources/`)

All downloaded from kenney.nl under CC0:

| Pack | URL |
|------|-----|
| Digital Audio | https://kenney.nl/assets/digital-audio |
| Interface Sounds | https://kenney.nl/assets/interface-sounds |
| Impact Sounds | https://kenney.nl/assets/impact-sounds |
| Sci-Fi Sounds | https://kenney.nl/assets/sci-fi-sounds |
| UI Audio | https://kenney.nl/assets/ui-audio |
| Music Jingles | https://kenney.nl/assets/music-jingles |

The full extracted packs are in `_sources/extracted/` — swap any file in `sfx/`
for an alternative from the same pack if a choice doesn't feel right after listening.

### Quick swap candidates

| Cue | Alternatives in source packs |
|-----|------------------------------|
| jump | `phaseJump2–5.ogg` (same series, slight variations) |
| dash_start | `phaserUp2–7.ogg` |
| dash_expire | `phaserDown2–3.ogg` |
| dash_charge_used | `lowRandom.ogg` (more organic click) |
| charges_restored | `twoTone2.ogg`, `threeTone1/2.ogg` |
| land | `impactSoft_heavy_000.ogg` (heavier thud), `impactWood_light_000.ogg` |
| death | `explosionCrunch_001–004.ogg`, `lowFrequency_explosion_000.ogg` |
| you_died | `error_002–008.ogg` |
| countdown_3/2/1 | `pepSound1/2/3.ogg` (lower range), `select_001–008.ogg` (cleaner tones) |
| go | `powerUp2–12.ogg`, `zapThreeToneUp.ogg` |
