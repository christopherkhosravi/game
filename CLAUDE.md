# HNOV — Project Context for Claude Code

## What this is

**HNOV** ("a movement story") is a single-file HTML5 Canvas platformer. The entire game lives in `hnov_5.html`. There is no build step, no npm, no bundler — it's a raw HTML/JS/CSS file served by a static HTTP server.

The aesthetic is intentional: dark purple/indigo palette, pixelated sprites, scanlines, vignette. The feel is floaty and moon-like — not crisp or snappy. Do not "improve" the physics toward a conventional platformer feel. The softness is the point.

---

## How to run it

```bash
python -m http.server 8080
# then open http://localhost:8080/hnov_5.html
```

Claude Code preview server is configured in `.claude/launch.json` as `game` on port 8080.

**You cannot open hnov_5.html directly from disk** (file://) because browsers block loading local assets with relative paths due to CORS. Always use the HTTP server.

---

## Repository

- GitHub: `https://github.com/christopherkhosravi/game.git`
- Branch: `main`
- Git user: `christopherkhosravi` / `christopher.khosravi8@gmail.com`
- GitHub Pages: `https://christopherkhosravi.github.io/game/hnov_5.html` (deployed from `gh-pages` branch, pushed manually with `git push origin main:gh-pages`)

---

## File structure

```
game/
├── hnov_5.html              ← THE GAME. Everything playable is here.
├── alignment_test.html      ← Dev utility: flickers between background frames to check alignment
├── process_sprites.py       ← Batch background removal for all sprites (uses PIL)
├── animations/
│   ├── transparent/         ← LIVE SPRITES (PNGs with alpha). The game loads from here.
│   │   ├── idle/            1.png – 4.png
│   │   ├── run/             1.png – 3.png
│   │   ├── jump/            1.png – 4.png  (also used for 'fall' state)
│   │   ├── bounce/          1.png – 3.png
│   │   ├── dash/            1.png – 3.png
│   │   ├── dying/           1.png – 4.png
│   │   ├── wall grab/       1.png  (folder name has a space — correct, don't rename)
│   │   └── dead hang/       1.png  (folder name has a space — correct, don't rename)
│   ├── background/
│   │   ├── background 1.jpg   ← 3-frame JPG set (legacy, defined in code as BG_IMGS but not used)
│   │   ├── background 2.jpg
│   │   ├── background 3.jpg
│   │   ├── background.mp4     ← Portrait video (704×1280, MJPEG, 5.03s). THE active background.
│   │   └── frames/            ← 161 JPG files (frame_001.jpg – frame_161.jpg). Source material only.
│   ├── [idle|run|jump|bounce|dash|dying|stomp|wall grab]/
│   │                          ← Source JPG frames (photographed/scanned). Not used by the game
│   │                             directly — only the transparent/ PNGs are.
│   ├── sprite_bg_remover.py   ← Corner-sample background removal. Tolerance=30.
│   ├── process_dash.py        ← Converts "new dash 1-3.jpg" → transparent/dash/1-3.png
│   ├── process_bounce.py      ← Converts "new bounce 1-3.jpg" → transparent/bounce/1-3.png
│   ├── build_preview.py       ← Dev tool: assembles sprite grid preview image
│   ├── sprite_assembler.py    ← Dev tool: builds assembly_preview.png from source JPGs
│   └── sprite_assembler_transparent.py ← Dev tool: builds assembly_preview_transparent.png
└── old shit/                  ← Archived versions. Do not touch or reference.
```

---

## Canvas and world coordinates

| Thing | Value |
|---|---|
| Canvas (pixels) | 1680 × 945 |
| World (game units) | 840 × 1480 |
| Scale | 2× (1 world unit = 2 canvas pixels) |
| Ground Y | 1440 |
| Level height | 1480 (vertical climbing level) |

The world is drawn with `ctx.scale(2, 2)` and `ctx.translate(-cam.x, -cam.y)`. When working with positions, always think in **world units** — the 2× scale is applied in `drawWorld()`.

Camera: `cam.x` lags behind the player's horizontal position (horizontal offset is 1/4 canvas width, not centered). Camera follows freely vertically. The camera lerps at 0.1 per frame.

---

## Physics constants — do not change without strong reason

```js
RISE_G     = 0.11   // Very light gravity on the way up — moon feel
FALL_G     = 0.28   // Drifts down, not a drop
JUMP_FORCE = -4.25  // Modest kick
MAX_FALL   = 8      // Never feels heavy
RUN_SPEED  = 2.0    // Deliberate, not zippy
FRICTION   = 0.88   // Air friction when no directional input
```

These were tuned extensively to get the specific floaty feel. Treat them as locked unless the user explicitly asks to change movement feel.

**The dash block is marked "UNTOUCHED" in comments.** This means the dash physics were finalized and must not be modified. The comments `// — dash — UNTOUCHED` and `// — dash — UNTOUCHED BLOCK END` are intentional guards.

---

## Controls

| Key | Action |
|---|---|
| Arrows / WASD | Move |
| Space / W / Up | Jump; Space again in air = bounce |
| Q | Dash left |
| E | Dash right |
| S / Down (in air) | Float / glide |
| Into wall (in air) | Wall slide |
| Jump off wall | Wall jump |
| R | Restart |

---

## Player state machine

States: `idle`, `run`, `jump`, `fall`, `float`, `bounce`, `wall`, `dash`, `dying`

State priority (highest first): `dash` > `wall` > airborne states > `run` > `idle`

Airborne sub-states: `float` > `bounce` > `jump`/`fall` (based on vy)

`fall` uses the same sprite folder as `jump` (both map to `SPRITE_DEFS['jump']`).

---

## Sprite system

Sprites are PNG files with alpha, stored in `animations/transparent/{folder}/{frame}.png`. Frames are numbered from `1`.

**Sprite definitions** (`SPRITE_DEFS`):

| State | Folder | Frames | Loop |
|---|---|---|---|
| idle | idle | 4 | yes |
| run | run | 3 | yes |
| jump | jump | 4 | yes |
| fall | jump | 4 | yes |
| float | dead hang | 1 | yes |
| bounce | bounce | 3 | yes, from frame 1 |
| wall | wall grab | 1 | yes |
| dash | dash | 2 | yes |
| dying | dying | 4 | play-once |

**Sprite size:** 60×80 pixels, drawn at 2× world scale, anchored to the bottom-centre of the hitbox.

**Hitbox:** 12×16 world units (much smaller than the sprite — the sprite is a decorative overlay).

**Ground offset:** States `idle`, `run`, `dying` get an 8px yOffset so the sprite sits on the ground rather than floating. Airborne/wall states have yOffset=0.

**Mirroring quirk:** The `wall grab` and `dash` sprites were exported facing the opposite direction from all other sprites. Their flip logic is inverted via `mirrorStates = ['wall', 'dash']`. If you add new animation states, assume they follow the normal convention unless the asset says otherwise.

**Animation speed:** 16 game frames per animation frame (dash: 9 frames per animation frame).

---

## Background animation

### What currently runs

A hidden `<video>` element (`BG_VIDEO`) loads `animations/background/background.mp4`. The video plays forward natively; when it reaches the end, the `'ended'` event fires, the video pauses, and `bgDir` flips to `-1`. While reversed, `updateBgVideo()` manually steps `currentTime` backward by `1/30` each tick. When `currentTime` reaches 0, `bgDir` flips back to `1` and `play()` is called. This creates a full-duration ping-pong loop.

`drawBackground()` draws `BG_VIDEO` directly to the canvas using `ctx.drawImage(BG_VIDEO, ...)`. The `bgEverReady` flag latches `true` on the first frame where `BG_VIDEO.readyState >= 2`, and acts as a permanent draw gate — once set, it never checks `readyState` again (this prevents blackout during reverse seeks which drop `readyState`).

The 3-frame JPG set (`BG_IMGS`, loaded from `background 1.jpg`, `background 2.jpg`, `background 3.jpg`) is still defined in the code but **not used by the current `drawBackground()`**. It is legacy code.

### background.mp4

`background.mp4` is a **portrait video** (704×1280, MJPEG codec, ~32fps, 5.03s). It is **the active background source** loaded by `BG_VIDEO`.

### Critical lesson: video play() vs currentTime

Never call both `video.play()` AND manually set `video.currentTime` on every animation frame simultaneously — they conflict. Each manual seek drops `readyState`, which stalls the video near frame 0 (the darkest frame), making the background appear black. The current approach: use `play()` for forward direction only, catch the end with the `'ended'` event, then only manually step `currentTime` for the reverse pass (while paused). The `bgEverReady` latch prevents the blackout during reverse seeks.

### The frames/ folder

`animations/background/frames/` contains **161 JPG files** (`frame_001.jpg` – `frame_161.jpg`). These are the source frames extracted from `background.mp4`. They are **not used by the game** — they exist as source material only.

### Background positioning

The background is drawn at **2.4× native resolution** (704×2.4 = 1689.6 wide, 1280×2.4 = 3072 tall). Horizontal parallax at 30% of camera speed, left-anchored when `cam.x === 0`. Vertical parallax at 30%, bottom-anchored to floor level (`bgCamRef = LH - CH/2`).

### Failed approaches (do not repeat)

1. **PNG frame preloader** — extracting frames from the video via `toDataURL()` at load time. Worked in theory but created huge memory overhead and long load times. Was replaced with a simpler PNG file sequence approach, but the PNG files were never created, so the game showed no background at all. Reverted.
2. **PNG file sequence** — loading `frame_001.png` through `frame_010.png` directly. The files don't exist on disk, so the game showed a solid black background. Reverted.
3. **Restricting video to 2s–end range** — adding `BG_LOOP_START = 2` and using `loadedmetadata` to seek to 2s. This caused freezes at turnaround points and complicated the logic without clear benefit. Reverted.

---

## Level layout

Vertical climbing level. Player starts bottom-left, goal is top-centre.

```
Platform 6:  x:300  y:80    w:220  — wide landing pad, goal sits here
Platform 5:  x:90   y:220   w:130  — left, wall-jump reach from plat 4
Platform 4:  x:560  y:390   w:130  — right
Platform 3:  x:90   y:570   w:130  — left, wall-jump reach from plat 2
Platform 2:  x:560  y:770   w:120  — enemy sits here
Platform 1:  x:80   y:1000  w:120  — lower
Floor:        x:32   y:1440  w:LW-64
Left wall:    x:0    y:60    w:16   h:1420
Right wall:   x:LW-16 y:60  w:16   h:1420
```

Goal: `{x:370, y:20, w:24, h:60}` — sits on platform 6.

One stationary enemy on platform 2: `{x:580, y:752, w:18, h:18, range:0, speed:0}`.

---

## Asset pipeline (adding new sprites)

1. Source JPG goes in the appropriate `animations/{state}/` folder, named `1.jpg`, `2.jpg`, etc.
2. Run the appropriate background-removal script:
   - `python animations/sprite_bg_remover.py` — batch, corner-sample method, tolerance=30
   - `python process_sprites.py` — threshold method (R<60 & G<60 & B<60)
   - `python animations/process_dash.py` — for dash frames specifically
   - `python animations/process_bounce.py` — for bounce frames specifically
3. Output PNGs land in `animations/transparent/{state}/`.
4. Update `SPRITE_DEFS` in `hnov_5.html` if adding a new state.

The `rembg` library (AI-based background removal) is used if installed; otherwise falls back to threshold. `rembg` produces cleaner edges on complex backgrounds.

---

## HUD elements

- `HNOV` label + current state name (e.g. `IDLE`, `DASH`, `BOUNCE`)
- Float meter: depletes while holding S/Down in air, refills on ground
- Wall meter: depletes while wall-sliding, refills on ground
- Dash pip: purple = available, red/pink = charging, dark = used

---

## Game states

`title` → `playing` → `win` | `dead`

- `title`: overlay shown, game not ticking
- `playing`: normal gameplay
- `win`: fade + "YOU MADE IT" overlay, R restarts
- `dead`: dying animation plays (4 frames × 60 ticks = 4s), then `dead` overlay, R respawns

---

## Visual effects

- **Screen shake**: set `screenShake = N` (decrements each frame, random offset applied)
- **Particles**: `spawnParticles(x, y, color, count, vxRange, vyRange, life)`
- **Dash ghosts**: 3 trailing ghost sprites captured during dash at frames -9, -18, -27
- **Quake ring**: expanding ring when bounce is triggered (pushes nearby enemies)
- **Bounce impact ring**: red ring + star sparks drawn on the sprite during bounce state
- **Vignette**: radial gradient darkening edges
- **Scanlines**: `rgba(0,0,0,0.025)` every 3 pixels vertically

---

## Palette

```js
P.bg0      = '#0a0a14'  // near-black background
P.platTop  = '#6a5acd'  // platform top edge (purple)
P.h1       = '#e8d8ff'  // sprite light
P.h3       = '#6a5acd'  // sprite dark purple
P.h5       = '#ff6b9d'  // accent pink (used in bounce fx, quake)
P.dashFx   = '#b09aef'  // dash particles
P.bounceFx = '#ffd4e8'  // bounce particles
```

---

## Things that must not be changed without explicit instruction

1. **Dash mechanics** — marked `UNTOUCHED` in code, leave them alone
2. **Physics constants** — the floaty feel is intentional
3. **Sprite folder names** — `wall grab` and `dead hang` have spaces; the code references them with spaces
4. **Canvas size** — 1680×945 (16:9, fits on most screens at 100%)
5. **Hitbox dimensions** — 12×16 world units; changing this breaks all platform collision tuning
6. **`.claude/`** — gitignored, contains local dev server config only
