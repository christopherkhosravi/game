# CLAUDE.md — HNOV Project

## Project Overview

HNOV ("a movement story") is a single-file 2D platformer built with vanilla HTML5 Canvas and JavaScript. The entire game lives in `hnov_5.html` (~1130 lines). No build tools, no frameworks, no dependencies.

The game is a vertical climb — the player spawns on a ground floor and ascends through platforms to reach a goal flag at the top. The core identity is **floaty, moon-gravity movement** with chained abilities (jump, bounce, float, dash, wall-slide).

## File Structure

```
game/
├── CLAUDE.md                 ← this file
├── hnov_5.html               ← THE game (only production file)
├── alignment_test.html       ← debug tool for background frame alignment
├── process_sprites.py        ← sprite processing utility
├── animations/
│   ├── background/
│   │   ├── background 1–3.jpg      (static stills, not used in game)
│   │   ├── background.mp4          (source video, not used in game)
│   │   └── frames/
│   │       └── frame_001–161.jpg   (animated background sequence)
│   ├── building_prepped.png      (building sprite, 287×984 RGBA — parapet strip used for floor)
│   ├── cutscene_1_real.mp4       (cutscene clip 1 — "Fuck yeah, I love me my Chai tea.")
│   ├── cutscene_1.mp4            (cutscene clip 2 — "OH SHIT!")
│   ├── cutscene_2.mp4            (cutscene clip 3 — "Give me my tea back!")
│   ├── spikes.png                (spike strip enemy sprite, 1024×1024 RGBA, white bg removed)
│   ├── countdown_3.png           (countdown sprite, step 3)
│   ├── countdown_2.png           (countdown sprite, step 2)
│   ├── countdown_1.png           (countdown sprite, step 1)
│   ├── countdown_go.png          (countdown sprite, GO!)
│   ├── kullad/
│   │   └── 1–193.png             (end-flag sprite animation — chai cup, 640×640 RGBA, black bg removed)
│   └── transparent/
│       ├── bounce/      1–4.png    (only 2–3 used in SPRITE_DEFS; frame 1 skipped via firstFrame:2)
│       ├── dash/        1–3.png    (only 1–2 used in SPRITE_DEFS)
│       ├── dead hang/   1.png
│       ├── dying/       1–4.png
│       ├── idle/        1–4.png
│       ├── jump/        1–4.png    (shared by jump + fall states)
│       ├── run/         1–3.png
│       ├── stomp/       1–4.png    (asset only, no game reference)
│       └── wall grab/   1.png
└── old shit/                 ← archived older versions, do not touch
```

## Architecture (inside hnov_5.html)

Single `<script>` block, organized in sections marked with `// ───` headers:

1. **CANVAS & CTX** — 1680x945 canvas, 2x world scale (world is 840x472.5 visible)
2. **PALETTE** — color constants object `P`
3. **LEVEL** — platform arrays, enemies, goal, quake constants
4. **PHYSICS CONSTANTS** — gravity, speeds, timers (all named constants at top)
5. **PLAYER** — `makePlayer()` factory, player state object
6. **PARTICLES** — `spawnParticles()` + per-frame array
7. **INPUT** — keydown/keyup with `justPressed`/`justReleased` buffers
8. **CAMERA** — vertical-follow with 0.1 lerp, horizontal locked (level = viewport width)
9. **COLLISION HELPERS** — AABB `resolveX`/`resolveY`
10. **GAME STATE** — title / playing / win / dead
11. **UPDATE** — main game tick: physics, abilities, animation state machine
12. **SPRITE SYSTEM** — PNG frame loader, `SPRITE_DEFS`, `drawHnov()`
13. **BACKGROUND** — 10-frame ping-pong from `animations/background/frames/`
14. **RENDER** — `drawWorld()`, `drawVignette()`, `drawScanlines()`, overlays
15. **LOOP + INIT** — `requestAnimationFrame` loop, `startGame()`

## Locked Layers — Do NOT Change Without Explicit Permission

These systems are tuned and intentional. Do not modify them unless the user specifically asks:

- **Physics constants** (lines ~190–211): gravity, jump force, dash speed, bounce, friction, coyote/buffer frames
- **SPRITE_DEFS frame counts**: bounce=2 (starts from file 2.png via `firstFrame:2`), dash=2, etc. — extra frames on disk are intentional unused spares
- **Player hitbox** (w:12, h:16) and sprite anchor math in `drawHnov()`
- **Platform layout** (`staticPlats` array) and goal position
- **Camera system** — lerp factor, clamping logic, 2x scale relationship
- **Control mapping** — WASD only (arrows removed), Space, double-tap A/D for dash, R

## GitHub Pages Deployment

The live game is served from the `gh-pages` branch via **legacy build** (`build_type: legacy`, source branch `gh-pages`, path `/`). There is no custom Actions workflow — GitHub's built-in Pages builder handles it.

**If a deployment gets stuck:**
GitHub sometimes creates a "pages build and deployment" Actions workflow that enters a `waiting` state while the legacy build also stalls. These can conflict. Fix:
```
curl -s -X POST \
  -H "Authorization: token <PAT>" \
  "https://api.github.com/repos/christopherkhosravi/game/pages/builds"
```
This triggers a fresh legacy build directly. Once status returns `"built"`, the stuck Actions run auto-cancels. The live site at `https://christopherkhosravi.github.io/game/hnov_5.html` should reflect the latest `gh-pages` commit.

**Always push to both branches after every code change:**
```
git push origin main
git push origin main:gh-pages
```

## Standing Rules

### Before Every Task
- **Read `CLAUDE.md` first.** If the user says "read CLAUDE.md" or starts a new session, re-read this file before doing anything.
- **Only re-read CLAUDE.md at the start of a new session or when explicitly told to.** Do not re-read it between tasks in the same session.
- **Read the relevant section(s) of `hnov_5.html`** before making changes. Never edit code you haven't read in this session.

### Code Changes
- All game code goes in `hnov_5.html`. Do not split into separate JS/CSS files unless explicitly asked.
- Preserve the section-header comment style (`// ─── SECTION NAME ───`).
- Do not add comments, docstrings, or type annotations to code you didn't change.
- Do not refactor, "clean up," or reorganize code adjacent to your change.
- Do not add features beyond what was asked.

### Git Commits
- Do not commit unless the user explicitly asks.
- Do not push unless the user explicitly asks.
- Keep commit messages short (1–2 lines) and focused on what changed and why.
- **Always push to gh-pages after every push to main** — the game is served from the gh-pages branch on GitHub Pages, so both branches must stay in sync.
- **Always use GitHub as the source of truth.** Clone or pull from the remote repo at the start of every session before making any changes. Never assume local files are up to date.

### Files and Assets
- **Never ask the user to save files to their machine.** If a file needs to be added to the repo, push it to GitHub directly, then pull from remote. All files come from and go to the remote repo — do not instruct the user to manually place files locally.

### Verification
- After any gameplay-affecting change, note what the user should test (e.g., "try jumping off the left wall on platform 3").
- If a change touches physics or collision, call out which locked-layer constants were and were not modified.

### Updating This File
- When the user gives a new standing instruction (e.g., "from now on always X"), add it to this file under the appropriate section.
- When project structure changes materially (new files, renamed files, new game systems), update the file structure and architecture sections.

## Background Scrolling Solution

**Problem:** Background did not scroll vertically with the camera (stayed fixed) and its bottom edge did not align with the ground platform (was 80px too low).

**Root Cause:** The formula in `drawBackground()` (lines ~839–840) used weak 0.3 parallax `(cam.y - bgCamRef) * 2 * 0.3`, which was so small that the canvas clamping kept `bgY` at a fixed value. Additionally, the baseline positioned the background bottom at the canvas bottom (945px) instead of at world ground level (GROUND_Y).

**Solution:**
- Changed parallax factor from 0.3 to 1.0 (full scrolling)
- Changed baseline from `(CH - dH)` to `(GROUND_Y - cam.y) * 2 - dH`
- Updated clamping lower bound from `CH - dH` to `(GROUND_Y - bgCamRef) * 2 - dH`

**Formula:** `bgY = (GROUND_Y - cam.y) * 2 - dH`
- As `cam.y` increases (player climbs), `bgY` becomes more negative (background scrolls up)
- Background bottom stays at `(GROUND_Y - cam.y) * 2`, which is the canvas Y position where the ground appears
- Clamping allows natural range based on camera position, preventing over-clamping

**Test:** Climb the platforms and verify the background scrolls smoothly upward and the background bottom edge aligns with where the ground platform visually appears on screen.

## Background Dimensions Fix

**Problem:** Background was stretched into portrait and showed a black U-shaped border. The code used hardcoded 704×1280 portrait dimensions while actual frames are 832×480 landscape.

**Root Cause:**
- Code assumed: vW = 704, vH = 1280 (portrait: 0.55 aspect ratio)
- Actual frames: 832×480 (widescreen: 1.73 aspect ratio)
- Stretch factors: 2.03x horizontal, 6.40x vertical (severe non-uniform distortion)
- Black border: Background bottom positioned at GROUND_Y canvas position (865), leaving 80px gap at canvas bottom (945)

**Solution:**
- Changed vW/vH from 704/1280 to 832/480 (actual frame dimensions)
- Kept 2.4x scale factor: dW = 1996.8, dH = 1152
- Changed bgY anchor from GROUND_Y to LH (level height at 1480)
- Updated clamping to match new display height: `Math.max(CH - dH, Math.min(0, bgY))`

**Formula:** `bgY = (LH - cam.y) * 2 - dH`
- On spawn (cam.y = bgCamRef ≈ 1007.5): bgY = 945 - 1152 = -207, background bottom exactly at canvas bottom
- As player climbs (cam.y decreases): bgY increases toward 0, background scrolls up showing higher areas
- Clamping range: [-207, 0] prevents overshoot

**Result:**
- Correct 1.73:1 aspect ratio preserved (no distortion)
- Background bottom-left aligns with canvas bottom-left on spawn
- Smooth vertical scrolling with camera
- No black borders at any camera position

## Spawn Timer System

**What it does:**
- On spawn/respawn, a 3 → 2 → 1 → GO! countdown plays at top-center of the canvas. Player input is disabled during the countdown.
- After "GO!" fades out, a stopwatch starts counting up in `MM:SS.cs` format (centiseconds), displayed top-center.
- Timer stops (frozen) when the player reaches the goal flag.
- Timer stops and resets to 0 immediately on death. On respawn the countdown replays and a fresh timer starts.

**Key variables (GAME STATE section):**
- `countdown` — current display step: 3/2/1 = digit, 0 = "GO!", -1 = inactive
- `countdownTick` — frames elapsed since countdown began (resets each spawn)
- `timerRunning` — true while stopwatch is counting
- `timerStartTime` — `performance.now()` snapshot when timer started
- `timerFrozenMs` — saved elapsed ms when timer was stopped (used for display)

**Countdown timing:** 60 frames per digit (≈1 s each), 40 frames for "GO!" (~0.67 s), then timer starts.

**Countdown art assets:**
Four 512×512 PNG files in `animations/`: `countdown_3.png`, `countdown_2.png`, `countdown_1.png`, `countdown_go.png`. Split from `321go.jpg` (2×2 grid, top-left=3, top-right=2, bottom-left=1, bottom-right=GO!). Each is drawn at 200×200px centered at `(CW/2, 108)`.

**How to swap in custom art assets:**
Change the `img.src` paths in the `COUNTDOWN_IMGS` preload block (top of SPAWN TIMER section) or replace `drawCountdownStep(step, frac)`. Parameters:
- `step`: `3 | 2 | 1` (digit) or `0` ("GO!")
- `frac`: `0.0` (just appeared) → `1.0` (about to change) — drives the GO! fade-out alpha

The stopwatch timer text is `88px "Courier New"`, displayed at `(CW/2, 24)` with `textBaseline = 'top'`. Two draw passes with `shadowColor = '#ff6b9d'` at `shadowBlur = 32` then `14` create the neon pink bloom effect.

**Integration points:**
- `update()` — countdown block runs at top, early-returns (skipping input) while `countdown >= 0`
- `update()` dead block — `timerRunning = false; timerFrozenMs = 0` on first death frame
- `update()` win check — freezes `timerFrozenMs` before setting `timerRunning = false`
- `respawn()` — resets timer and sets `countdown = 3; countdownTick = 0`
- `startGame()` — same reset as `respawn()`
- `render()` — calls `drawSpawnTimer()` when `gameState === 'playing'`

## Background Padding Compensation

**Problem:** Background positioning was mathematically correct (bgX=0, bgY=-207) but visually misaligned. Artwork appeared ~2 character-heights too high and ~3 character-widths too far right.

**Root Cause:** JPG frame files contain intentional padding:
- Top padding: ~60px of black space before the cityscape artwork begins (12.5% of 480px height)
- Left padding: ~30px of black space before buildings reach the left edge
- When the image was positioned to place the bottom-left corner flush with the canvas, the padding was visible and pushed the artwork higher and further right than expected

**Solution:**
- Added padding compensation offsets to the positioning calculations
- Top padding (scaled): `padTopScaled = 60 * 2.4 = 144px`
- Left padding (scaled): `padLeftScaled = 30 * 2.4 = 72px`
- Applied offsets to shift image so padding sits off-screen and visible artwork fills the canvas
- Restored parallax logic: `bgX = -cam.x * 2 * 0.3 - padLeftScaled`
- Restored scroll logic: `bgY = (LH - cam.y) * 2 - dH - padTopScaled`

**Formula:**
- `bgX = -cam.x * 2 * 0.3 - 72` (30% parallax minus left padding offset)
- `bgY = (LH - cam.y) * 2 - dH - 144` (full vertical scroll minus top padding offset)
- Clamping: `Math.max(CW - dW, Math.min(0, bgX))` and `Math.max(CH - dH, Math.min(0, bgY))`

**Result:**
- Visible artwork content fills canvas bottom-left corner on spawn
- Artwork properly framed without excessive padding borders
- Full parallax and vertical scrolling restored
- Background positioning matches visual expectations

## Background Scale: Width-Fit to Canvas

**Solution:** Scale background so its width exactly matches the canvas width (CW=1680), maintaining correct aspect ratio. Scale factor is calculated dynamically as CW/704 (no hardcoded value).

**Formula:**
- bgScale = CW / 704 = 1680 / 704 = ~2.3864
- dW = CW = 1680 (exact canvas width)
- dH = 1280 * bgScale = ~3054.5 (portrait height scaled proportionally)
- Aspect ratio preserved: dW/dH = 704/1280 = 0.55
- Scroll and parallax logic unchanged

## Control Remapping — WASD + Arrows, Double-Tap or Q/E Dash, Space/W/Up Jump

**Current bindings:**
- **Move left/right:** A/D or ArrowLeft/ArrowRight (both work simultaneously)
- **Jump:** W, ArrowUp, or Space — all three trigger jump, bounce, and wall-jump
- **Dash left:** double-tap A or ArrowLeft (within 250 ms) or Q
- **Dash right:** double-tap D or ArrowRight (within 250 ms) or E
- **Float:** S (air toggle)
- **Restart:** R

**Implementation:**
- `left = press(['KeyA','ArrowLeft'])`, `right = press(['KeyD','ArrowRight'])`
- `jumpP/jumpH/jumpR` all include `'Space','KeyW','ArrowUp'`
- Keydown listener: double-tap ArrowLeft/ArrowRight (250 ms window) injects `DashLeft`/`DashRight`, same as A/D double-tap; `_lastLeftPress`/`_lastRightPress` track timestamps
- Keydown listener injects `justPressed['DashLeft']` on `KeyQ` and `justPressed['DashRight']` on `KeyE` (same path as double-tap A/D)
- `e.preventDefault()` applied to all four arrow keys unconditionally (prevents page scroll)
- Note: `KeyE` still triggers god-mode export — the `justPressed['DashRight']` injection doesn't conflict because god mode returns before the dash block

**Implementation:** Two module-level variables `_lastAPress` and `_lastDPress` (timestamps, ms) are declared alongside `justPressed`/`justReleased`. The first `keydown` listener checks `performance.now() - _lastXPress < 250` on the leading edge of each KeyA/KeyD press (guarded by `!keys[e.code]` so held keys don't retrigger). On a qualifying double-tap it injects a virtual key `'DashLeft'` or `'DashRight'` into `justPressed`, which the existing `dashQP`/`dashEP` variables consume via `jp(['DashLeft'])` / `jp(['DashRight'])`. The dash activation and physics block are otherwise unchanged.

## Death Sequence

**Phases:**
1. **'dying'** — `p.dead = true`, `deathPhase = 'dying'`, `gameState = 'dead'` all set simultaneously at death trigger (`checkHazards()`). `deadOverlayTimer` reset to 0. Gravity (`FALL_G`) applies every tick. Dying animation advances at 16 ticks/frame, 4 frames, play-once. Player has no input. Camera follows.
2. **'fallen'** — Animation held on last frame (animFrame=3). Gravity continues. Character falls until `ry.landed`. No special transition needed — `gameState` is already `'dead'`.

**Timing synchronisation:** All three visual elements — blur, dark overlay, "YOU DIED" panel — start the instant death is triggered. `drawDead()` uses a single `t = deadOverlayTimer / 64` ramp (64 ticks = 4 frames × 16 ticks, matching the animation duration exactly). At t=0 everything is invisible; at t=1 overlay is at full opacity (0.9), panel is full size and alpha 1. The blur (`ctx.filter = 'blur(6px)'`) is always active when `gameState === 'dead'`.

**Key variables:**
- `deathPhase` — `'dying'` | `'fallen'`; initialized in `checkHazards()` enemy collision block; reset to `'dying'` in R-key handler.
- `deadOverlayTimer` — incremented in `drawDead()`, single 0→64 ramp driving all overlay elements simultaneously. Reset to 0 at death trigger and on restart.

**Implementation notes:**
- `gameState = 'dead'` is now set at the death trigger (not on landing), so blur/overlay and animation all start together.
- The `p.dead` block in `update()` no longer sets `gameState = 'dead'` — that moved to `checkHazards()`.
- `updateCamera()` is called inside the dead block (before `return`) so the camera follows the falling player.
- R-key `startGame()` path is guarded with `&& !player.dead` to prevent interrupting the death animation.
- In `render()`, `ctx.filter = 'blur(6px)'` is set before background/world draws and reset to `'none'` after; then `drawDead()` draws the panel; then `drawHnov()` is called a second time (with the 2× scale + camera translate from `ctx.save()`) to place the player sprite above and unblurred.

## Dash Ground Alignment Fix

The `groundStates` array in `drawHnov()` controls which states receive a `+8 px` downward draw offset to compensate for transparent padding at the bottom of sprite PNGs. `'dash'` was missing from this list, causing the sprite to float 8 px above the ground during a ground dash. Adding `'dash'` to `groundStates` applies the same compensation as idle and run.

## Drop-Shadow Ellipse Removed

The `drawHnov()` function previously drew a semi-transparent black ellipse (`rgba(0,0,0,0.20)`, horizontal radius `SPRITE_W * 0.45`, vertical radius 3) just below the player's feet on every frame. It was unconditional — present in the air as well as on the ground. These five lines were removed entirely. No other sprite rendering was changed.

## Floating Platforms — Solid Collision

All floating billboard platforms (staticPlats indices 3–7) use `type:'solid'`, giving full AABB collision on all sides (top landing, ceiling, and side walls). The floor (index 0) and walls (indices 1–2) are also `type:'solid'` and were not changed.

## Billboard Platform Visuals

**What it does:** The 6 floating platforms (staticPlats indices 3–8) are drawn as scaled billboard PNG images instead of the default brick/color fill. Collision boxes are unchanged — only the visual rendering differs. The floor (index 0) and walls (indices 1–2) keep their original appearance.

**Assets:** `animations/billboard_1.png` through `billboard_5.png` — 1024×1024 RGBA PNGs with transparent backgrounds and neon pixel-art billboard designs. `animations/long_billboard.png` — 832×1248 RGBA PNG, portrait chai-tea billboard with hanging mechanism (white bg removed via Pillow flood-fill).

**Assignment (BILLBOARD_PLAT_MAP):**
| Floating slot | staticPlats index | Billboard | Hitbox (w×h) | Content (Pillow getbbox) |
|---|---|---|---|---|
| 0 | 3 (platform 1, y=865) | billboard_1 | 120×104 | 694×601 |
| 1 | 4 (platform 2, y=770) | billboard_2 | 120×104 | 694×602 |
| 2 | 5 (platform 3, y=220) | long_billboard | 270×423 | 559×874 (frame only) |
| 3 | 6 (platform 4, y=390) | billboard_4 | 130×113 | 694×601 |
| 4 | 7 (platform 6, y=80) | billboard_3 | 220×191 | 694×601 |

Pattern 1,2,long,4,3 — no two adjacent platforms share the same image. Platform 5 (billboard_5) was removed.

**Hitbox sizing rule:** `h = round(p.w * content_h / content_w)` — matches `drawH` exactly so the collision box wraps the visible billboard on all sides. The `y` position is the top edge of the visible content (where the player lands).

**Implementation:**
- `BILLBOARD_IMGS` — array of 6 `Image` objects (indices 0–5); billboard_1–5 loaded via loop, long_billboard pushed as index 5
- `BILLBOARD_PLAT_MAP` — `[0,1,5,3,2]` maps floating-platform slot to `BILLBOARD_IMGS` index
- `drawWorld()` platform loop converted from `for…of` to indexed `for` loop; `pi >= 3` branches to billboard drawing (drawn in 2× world-scale context, so world coords are used directly)
- Drawing uses the 9-argument `drawImage(img, sx, sy, sw, sh, dx, dy, dw, dh)` to crop transparent padding from the source before scaling.
- `BILLBOARD_CROP` stores the visible content bounding box for each image (measured via Pillow): billboard_1–5 share `sx=165, sw=694`; long_billboard is `sx=137, sy=81, sw=559, sh=1079`.
- Draw formula: `drawH = p.w * c.sh / c.sw` — visible content width fills the platform exactly, height scales proportionally. Overflow below platform bottom is intentional (not clipped).
- Fallback: if image not yet loaded, draws the original brick fill

## Long Billboard — Platform 3 (staticPlats[5], y=570)

**What it does:** Platform slot 2 (staticPlats index 5, y=570) displays `long_billboard.png` — a portrait-oriented chai-tea billboard with a hanging mechanism. The billboard frame fills the hitbox; the mechanism hangs below with no collision.

**Asset:** `animations/long_billboard.png` — 832×1248 RGBA PNG. Source was `Downloads/long billboard.jpg`. White background removed via Pillow: exterior white (flood-filled from all 4 image edges, label 1, 507,968 px) and all interior white regions with `y_min >= 880` (hanging mechanism trapped pixels) set to alpha=0. White pixels inside the chai-tea photo content (above y=880) are preserved.

**Visible content bounding box (Pillow `getbbox`):** `sx=137, sy=81, sw=559, sh=1079` (full frame + mechanism). Frame ends at approximately y=955 in the source (where content width narrows from 559 to ~330 as the billboard corners taper into the mechanism).

**Platform hitbox (staticPlats[5]):** `{x:90, y:570, w:90, h:141, type:'pass'}`
- `w=90` — narrower than adjacent platforms to suit portrait proportions
- `h=141` — matches the billboard frame visual height at this scale: `round(90 * 874 / 559) = 141` (frame height in source = 955−81 = 874px)
- `type:'pass'` — unchanged; player lands on top, passes through from below/sides

**Draw at runtime:**
- `drawH = 90 * 1079/559 ≈ 174` world units total
- Frame occupies world y=570 to y=711 (141px) — aligns with hitbox
- Mechanism occupies world y=711 to y=744 (33px) — visible below hitbox, no collision

## God Mode Cheat

**What it does:** Typing the sequence `nggyu` (in order, any time during gameplay) toggles god mode on/off. While active: arrow keys fly the player freely; all gravity, friction, and collision are skipped; death (fall-out, hazards, enemies) is suppressed; a pink "GOD MODE" label appears top-right. Typing the sequence again turns it off. No effect on save state or normal gameplay.

**Key variables:**
- `godMode` (bool) — declared in GAME STATE section alongside `screenShake`.
- `_godSeq` / `_godIdx` — sequence array `['KeyN','KeyG','KeyG','KeyY','KeyU']` and current match index, declared just before the second `keydown` listener in INIT.

**Implementation:**
- **Sequence detection:** Second `keydown` listener checks each key against `_godSeq[_godIdx]`. On full match, toggles `godMode` and resets index. On mismatch, resets (or advances to 1 if the key matches the first step, to handle partial overlaps).
- **Flight block:** Inserted in `update()` immediately after the countdown early-return. If `godMode`: clears `p.dead`, moves player with `ArrowLeft/Right/Up/Down` at 5 px/frame, zeroes `vx/vy`, advances particles, decrements screen shake, calls `updateCamera()`, then returns — skipping all physics, collision, hazard, and win checks.
- **Indicator:** In `render()` after `drawSpawnTimer()`: draws `'GOD MODE'` in `#ff6b9d` bold Courier New 18px, right-aligned at `(CW-16, 16)`.
- **Position dot & coords:** Also in the god mode block in `render()`: a red (`#ff0000`) filled circle (radius 5) is drawn at the player's canvas-space centre — `dotX = (player.x + 6 - cam.x) * 2`, `dotY = (player.y + 8 - cam.y) * 2`. World coordinates `(Math.round(player.x), Math.round(player.y))` are drawn in 56px Courier New to the right of the dot (`dotX + 9`, `dotY`), updating in real time.

## Bounce Animation First-Frame Skip

**What it does:** The bounce animation starts on `bounce/2.png` (previously the second frame) instead of `bounce/1.png`. `bounce/1.png` is never shown.

**How:** Two changes in `hnov_5.html`:
1. **SPRITE_DEFS** — bounce entry changed from `frames: 3, loopStart: 1` to `frames: 2, firstFrame: 2`. `firstFrame` tells the loader which file number to start from; `frames` says how many to load. Result: `SPRITE_IMGS['bounce']` = [2.png, 3.png].
2. **Loader** — added `firstFrame` support: `const _f0 = def.firstFrame ?? 1; for (let i = _f0; i < _f0 + def.frames; i++)`. All other animations have no `firstFrame` so they default to 1 and are unaffected.

With these changes `animFrame` 0 → `bounce/2.png`, `animFrame` 1 → `bounce/3.png`, and the loop restarts at 0, so `bounce/1.png` is never loaded or displayed.

## Cutscene System

**What it does:** A cutscene plays between the title screen (BEGIN button) and the countdown. Three clips play in sequence, each in full with no seek offset. A fade out → fade in transition separates each clip. A final fade out leads into the countdown.

**Clips (in order):**
1. `cutsceneVid1` → `cutscene_1_real.mp4` — "Fuck yeah, I love me my Chai tea."
2. `cutsceneVid2` → `cutscene_1.mp4` — "OH SHIT!"
3. `cutsceneVid3` → `cutscene_2.mp4` — "Give me my tea back!"

**Fade schedule:**
1. End of clip 1 (`ended`) → fade out (1800 ms) → clip 2 starts from `currentTime = 0` → fade in (1800 ms)
2. End of clip 2 (`ended`) → fade out (1800 ms) → clip 3 starts from `currentTime = 0` → fade in (1800 ms)
3. End of clip 3 (`ended`) → exit fade to black (3000 ms) → `startGame()`

**Skip:** Space or R → immediately begins exit fade (3000 ms) → countdown.

**Key variables (GAME STATE section):**
- `cutsceneClip` — `1` | `2` | `3`, which video element is active
- `cutsceneExiting` — true when the final exit fade is underway
- `cutsceneExitStart` — `performance.now()` when exit fade began
- `cutsceneFadeState` — `'none'` | `'out'` | `'in'`
- `cutsceneFadeStart` — `performance.now()` when the current fade phase began

**Constants:** `CUTSCENE_FADE_MS = 1800` (each half of an inter-clip fade), `CUTSCENE_EXIT_MS = 3000` (final exit fade).
**Helpers:** `CUTSCENE_VID_IDS = ['cutsceneVid1','cutsceneVid2','cutsceneVid3']`, `CUTSCENE_SUBTITLES` array, `_csVid(clip)` returns the element for clip 1/2/3.

**`drawCutscene()` logic:**
- If `cutsceneExiting`: renders last video frame fading to black over `CUTSCENE_EXIT_MS`, calls `startGame()` at alpha=1.
- Fade-out completion: increments `cutsceneClip`, seeks new video to 0, plays it, transitions to fade-in.
- Fade-in completion: sets `cutsceneFadeState = 'none'` (subtitle appears).
- Subtitle drawn only when `cutsceneFadeState === 'none' && !cutsceneExiting`.

**Implementation:**
- Three hidden `<video>` elements (`cutsceneVid1`–`3`) with `preload="auto" muted playsinline` in the HTML.
- `vid1` and `vid2` share one `ended` listener (via `forEach`) → start fade-out, guarded by `cutsceneFadeState !== 'none'` to prevent collision.
- `vid3 'ended'` listener → sets `cutsceneExiting = true`.
- Skip keydown (Space or R) → pauses all three videos, clears fade state, sets `cutsceneExiting = true`.
- Button click handler calls `beginCutscene` (not `startGame`).

**Architecture note:** `gameState = 'cutscene'` causes `update()` to return early (existing guard `gameState !== 'playing'`), so no game logic runs during the cutscene.

**Subtitles:** `drawCutsceneSubtitle(text)` draws a canvas box matching the title screen overlay style: `background:#0d0d1e`, inner border `2px solid #6a5acd`, outer border `1px solid #3a2a6e` offset 8px, text `#9a8acd` `30px "Courier New"`. Box is centred horizontally, 60px from canvas bottom.

## Wall Grab Charge System — REMOVED

All wall grab limits removed. Wall grab now works indefinitely with no charge count and no meter drain. `wallCharges`, `wallMeter` removed from `makePlayer()`. Wall meter block replaced with just `p.prevWallContact = p.wallContact`. HUD GRAB dots and WALL meter bar removed.

## Floor Visual — Building Parapet Strip

**What it does:** The floor platform (staticPlats[0]) is drawn as a cropped strip of the building rooftop image instead of the default brick fill. Walls (staticPlats[1–2]) are unaffected.

**Floor hitbox (current):** `{x:226, y:GROUND_Y=1440, w:388, h:20, type:'solid'}` — half the original size (was w=LW-64=776, h=40), horizontally centred: x=(LW-388)/2=226. Equal gaps of 210 world units on each side between floor and walls. Vertical position unchanged (y=GROUND_Y=1440).

**Player spawn (current):** `x: LW/2 - 6 = 414, y: GROUND_Y - 16 = 1424` — horizontally centred on the canvas (player w=12, so centre = x+6 = LW/2 = 420). Vertical unchanged.

**Asset:** `animations/building_prepped.png` — 287×984 RGBA PNG of a pixel-art building. The parapet (rooftop edge with AC units) occupies the very top of the image. The image has been cleaned: 121 fully-opaque leading-edge pixels with luminance >120 were made transparent via a Pillow column-walk (for each column, walk from the first opaque pixel downward, zeroing alpha while luminance >120). These were light-grey/white pixels at the top boundary of each content structure causing a visible outline artifact. No semi-transparent pixels are present in this image — all pixels are alpha 0 or 255.

**Source crop:** `sx=0, sy=0, sw=287, sh=137` — rows 0–136 of the source image. `sy=0` ensures nothing is cropped from the top; `sh=137` shows the parapet cap plus a significant portion of the upper building face.

**Flat-top row:** Source row 35 is the first row ≥90% opaque across full width (measured via Pillow) — this is the solid parapet cap and defines the roofline.

**Draw formula** (all values update automatically when hitbox dimensions change):
- `drawH = p.w * c.sh / c.sw` = 388 × 137 / 287 ≈ 185 world units (proportional height)
- `drawY = p.y - c.flatTopRow * (p.w / c.sw)` = 1440 − 35 × (388/287) ≈ 1392.7 world units
  - Source row 35 (flat top) maps to world y = p.y = 1440 → roofline aligns with hitbox top edge ✓
  - Source rows 0–34 (antenna, AC units) render above p.y → fully visible above the floor ✓
- `dx = p.x = 226` (image left edge matches hitbox left edge, centred on canvas)
- Drawn in the 2× world-scale context, so world coordinates are used directly

**Implementation:**
- `BUILDING_IMG` — single `Image` object preloaded alongside billboard images (after BILLBOARD_CROP)
- `BUILDING_PARAPET` — `{sx:0, sy:0, sw:287, sh:137, flatTopRow:35}` source crop + anchor constants
- `drawWorld()` platform loop: `pi === 0` special case draws the parapet via 9-argument `drawImage`; falls through to brick fallback while image loads
- `pi >= 3` billboard case is unchanged; walls (`pi === 1, 2`) fall through to the original brick/glow/pattern rendering

**Test:** Floor shows building parapet centred on canvas with equal gaps (210 world units) on each side to the walls. Roofline sits at floor hitbox top edge. Walls show bricks.

## Wall Building Image

**What it does:** `animations/building_prepped.png` is drawn on both the left and right walls (staticPlats indices 1–2). The image is scaled to the full wall height (h=1420) with width proportional. Right wall draws normally; left wall draws mirrored horizontally via negative `drawW` in the 9-argument `drawImage` call.

**Implementation (drawWorld() platform loop, before the brick fallback):**
- `pi === 1 || pi === 2` branch added before `pi >= 3` billboard branch
- Scale: `drawH = p.h`, `drawW = iw * (drawH / ih)` (aspect-preserving, height-fit)
- Right (pi=2): `ctx.drawImage(img, 0,0,iw,ih, p.x, p.y, drawW, drawH)`
- Left (pi=1): `ctx.drawImage(img, 0,0,iw,ih, p.x+drawW, p.y, -drawW, drawH)`
- Falls back to brick pattern if image not yet loaded
- Reuses the already-preloaded `BUILDING_IMG` object (no new Image() needed)

**Position notes:** Position is tunable — adjust `p.x` offset for left/right placement relative to the wall hitbox. Position was not finalized at implementation time.

## Dash, Float, Wall Grab — Unlimited

All three mechanics have no limits, cooldowns, or resource costs. Removed from `makePlayer()`: `dashCount`, `floatMeter`, `wallMeter`, `wallCharges`. Removed HUD elements: DASH pips, GRAB pips, FLOAT meter bar, WALL meter bar. `#abilityBar` hidden via `display:none`.

**Dash:** `p.dashTimer === 0` guard retained so rapid double-tap doesn't interrupt an active dash. No per-use decrement.

**Float:** S toggles `p.floating` on/off with no drain. Landing still disables float.

**Wall grab:** Meter block removed entirely; wall contact is unlimited. `prevWallContact` retained for fresh-contact detection (used by wall-jump logic).

## Spike Strip Enemy Visual

**What it does:** The stationary enemy (staticPlats hitbox 18×18, sitting on platform 2 at y=752) is drawn using `animations/spikes.png` instead of the previous filled rectangles and eye dots. The hitbox, kill behavior, and patrol range indicator are unchanged — only the visual rendering changed.

**Asset:** `animations/spikes.png` — 1024×1024 RGBA PNG. Generated from `spikes.jpg` (Downloads) by removing the white background using Pillow corner-sampling with tolerance=30. Content bounding box measured via `getbbox()`: `(164, 400, 868, 649)` → 704×249 visible content.

**Background removal:** `python3` one-liner using Pillow. Sampled corner pixels (all near RGB 255,255,255). Pixels within tolerance=30 of white set to alpha=0. Light purple shadow pixels (e.g. RGB 200,193,224) are outside the tolerance threshold and preserved. Result: 937,091 transparent pixels, 111,485 opaque.

**Draw formula** (`drawWorld()`, enemies loop):
- `drawH = e.h` (18 world units, matches hitbox height)
- `drawW = drawH * sw/sh` = 18 × 704/249 ≈ 50.9 world units (aspect-preserving, wider than hitbox)
- `drawX = e.x + (e.w - drawW) / 2` — centred horizontally on the hitbox
- Source crop: `sx=164, sy=400, sw=704, sh=249` (content bounds only, no transparent padding)
- Fallback: original filled rectangles drawn if image not yet loaded

**Locked layers not touched:** Physics constants, hitbox dimensions, kill/collision logic, camera, controls.

## Level Layout Changes — Session 2

### Platform 1 moved (y=1000 → y=865)
staticPlats[3] moved upward. Spike added on left side of top edge: `{x:80, y:847, w:51, h:18}` (standard orientation, sitting on platform top).

### Left-wall spike gauntlet (5 spikes, rot=Math.PI/2)
Five rotated spikes mounted on the left wall, back-to-back from y=825 upward:
- y positions: 825, 774, 723, 672, 621 (each 51px tall, stacked with no gap)
- Hitbox per spike: w=18, h=51 (rotated dimensions — narrow and tall)
- x=10 (partially inside left wall, tips pointing right into level)
- `rot: Math.PI/2` — 90° CW rotation so spike tips face right

### Platform 3 tripled (w:90→270, h:141→423)
staticPlats[5] (x=90, y=570) width and height both tripled. Billboard visual scales automatically via the existing `drawH = p.w * c.sh / c.sw` formula (new drawH ≈ 521, overflows below hitbox intentionally). Six spikes (w=45 each, 6×45=270px total) cover the full top edge at y=552.

### Right-wall spike (rot=-Math.PI/2)
One spike at x=812, y=640: `{x:812, y:640, w:18, h:51, rot:-Math.PI/2}`. Tips point left (away from right wall). x=812 places the right edge at 830, overlapping right wall (x=824) by 6px — symmetric with left-wall spike x=10 overlap.

### Rotated enemy rendering
`drawWorld()` enemy loop now checks `e.rot`. If truthy:
```js
ctx.save();
ctx.translate(e.x + e.w/2, e.y + e.h/2);
ctx.rotate(e.rot);
ctx.drawImage(SPIKES_IMG, c.sx, c.sy, c.sw, c.sh, -e.h/2, -e.w/2, e.h, e.w);
ctx.restore();
```
Draw args `-e.h/2, -e.w/2, e.h, e.w` draw the original (wide) image centered, then rotation reorients it. For `rot=PI/2` the 51×18 source renders as 18×51 in world space with tips pointing right; for `rot=-PI/2` tips point left. Unrotated enemies (`e.rot` falsy) use the original draw path unchanged.

## Removed Platforms

### Platform 5 (staticPlats[7]) — removed session 3
```
{x:90, y:220, w:130, h:16, type:'pass'}
```
- Billboard slot: 4 (pi=7, pi−3=4), BILLBOARD_IMGS[4] = `billboard_5.png`
- BILLBOARD_CROP[4]: `{sx:165, sy:224, sw:694, sh:602}`
- To restore: re-insert as staticPlats[7] before the platform 6 entry, and change BILLBOARD_PLAT_MAP back to `[0,1,5,3,4,2]`

## Level Layout Changes — Session 3

### Platform 5 removed (staticPlats[7])
`{x:90, y:220, w:130, h:16, type:'pass'}` removed. See "Removed Platforms" above for restore data.
`BILLBOARD_PLAT_MAP` trimmed from `[0,1,5,3,4,2]` to `[0,1,5,3,2]` so platform 6 top (now slot 4) still maps to billboard_3 (index 2).

### Platform 3 moved (x:90,y:570 → x:130,y:220)
staticPlats[5] repositioned so left edge = x=130, top edge = y=220 (where platform 5 was). Dimensions and type unchanged (w:270, h:423, solid). Billboard visual rescales automatically.

### Platform 3 top spikes realigned
All 6 top spikes updated: y 552→202 (=220−18), x positions shifted right by 40px to start flush at new platform left edge x=130. New x positions: 130, 175, 220, 265, 310, 355 (6×45=270px, covering full platform width x=130 to x=400). The previous leftmost spike at x=90 was misaligned (40px left of new platform edge).

### Right-wall spike trio at y=250 (rot=-Math.PI/2)
Three spikes added side by side (vertically stacked, downward) at x=812, y=250/301/352. Each: `{w:18, h:51, rot:-Math.PI/2}`. Tips point left into level. Stacked flush with no gap (each h=51).

## Level Layout Changes — Session 4 (redo)

### Vertical play space tripled — upward only

**Wall hitboxes extended:** `h:1420 → h:4180`, `y:LH-1420 → y:LH-4180` on both walls.
- Old play space: GROUND_Y − (LH−1420) = 1440 − 60 = **1380 units**
- New play space: 3 × 1380 = **4140 units** (wall top at y = −2700)
- All platforms, enemies, goal, spawn unchanged — extension is empty space above

**Wall building rendering decoupled from physical height:**
`drawH` changed from `p.h * 1.20` to `1420 * 1.20` (fixed). Anchor changed from `p.y` to `LH-1420` (the original wall top, y=60). This keeps the building image pixel-identical to before — the extended wall space above y≈0 shows background only, which is correct for new empty space.

**Why the previous attempt showed "really long downwards":** `drawH = p.h * 1.20` with the tripled wall (h=4180) produced drawH=5016, stretching the building image 3× and pushing its bottom to y≈2138 — visually far below the floor. The fixed anchor eliminates this.

### Background parallax reduced to 0.3×

Formula changed in `drawBackground()`:
```js
// was: let bgY = (LH - cam.y) * 2 - dH;
let bgY = (CH - dH) - (cam.y - (LH - CH / 2)) * 0.6;
```
- At spawn (cam.y = LH−CH/2 = 1007.5): bgY = CH−dH = 945−dH, then +200 from existing nudges → identical to before
- Per-unit scroll rate: 0.6 canvas-px vs old 2.0 canvas-px = **0.3× camera speed**
- Background stays visible across the full extended play space

## Camera Clamp — Extended Level Top

**Problem:** `updateCamera()` clamped `ty = Math.max(0, ty)`, preventing the camera from scrolling above world y=0. After the walls were extended to `h:4180` (top at y=−2700), the player could climb into that new space but the camera couldn't follow.

**Fix:** Changed the clamp lower bound from `0` to `LH - 4180` (= −2700, the new wall top):
```js
ty = Math.max(LH - 4180, ty); // vertical: clamp to extended level top (y=-2700)
```

**Result:** Camera follows the player freely through the full extended play space above the existing platforms.

## Camera Upper Clamp — y=-2625

`updateCamera()` clamps `ty = Math.max(-2625, ty)`. This prevents the camera from scrolling above world y=−2625, leaving a small buffer (75 units) below the absolute level top at y=−2700.

## All Spike Enemies Removed

The `enemies` array was cleared of all 17 spike entries (platform spikes, left-wall spike gauntlet, platform-3 top spikes, right-wall spikes). The array is now empty. All enemy-loop code (`update`, collision, render) remains in place and is a no-op with an empty array.

**Removed entries (for reference):**
- Platform 2 spike: `{x:564, y:752, w:51, h:18, ox:564, range:0, speed:0, dir:0}`
- Platform 1 spike: `{x:80, y:847, w:51, h:18, ox:80, range:0, speed:0, dir:0}`
- Left wall spikes ×5: x=10, y=825/774/723/672/621, w:18, h:51, rot:Math.PI/2
- Platform 3 top spikes ×6: x=130–355 (step 45), y=202, w:45, h:18
- Right wall spike (prev session): x=812, y=640, w:18, h:51, rot:-Math.PI/2
- Right wall spikes ×3 (session 3): x=812, y=250/301/352, w:18, h:51, rot:-Math.PI/2

## Background Top-Edge Clamp

**Problem:** The vertical parallax formula in `drawBackground()` shifts `bgY` upward as `cam.y` decreases. With the camera now clamped at `y = -2625` (far above the original level), `bgY` reached **+117** at the maximum camera height — leaving a 117px black strip at the top of the canvas.

**Root cause (worked out):**
```
dH  = 1280 * (CW/704 * 1.05) ≈ 3207 px
bgY = (CH − dH) − (cam.y − (LH − CH/2)) × 0.6 + 200
```
At cam.y = −2625: bgY = −2262 − (−3632) × 0.6 + 200 = **+117**

The parallax factor (0.6) doesn't push the image up fast enough to cover the canvas when the camera travels 3632 units above the spawn reference.

**Fix:** One line added in `drawBackground()` after all adjustments:
```js
bgY = Math.min(0, bgY); // clamp: never let top edge drop below canvas top
```
This ensures the background's top edge is always at or above canvas y=0, regardless of how high the camera scrolls. The parallax still runs normally — the clamp only engages when the image would otherwise expose black at the top.

## Wall Three-Part Draw (Rooftop + Tiled Windows + Lower Building)

**Problem (previous approach):** The old code drew the full building image anchored at world y≈−0.61 (rooftop at ground level), then tiled a window slice upward above it. The seam at y=−0.61 was a content mismatch: the tile bottom showed mid-building windows while the original image top showed rooftop/antenna — visually incompatible regions placed flush against each other.

**Solution:** Restructure the wall draw into three parts so the rooftop cap sits at the top of the level and all joins occur within the repeating window section of the source image.

**Three-part structure (per wall, `pi=1` left / `pi=2` right):**

| Part | Source rows | World y range | Purpose |
|---|---|---|---|
| 1 — rooftop cap | 0–431 | `TOP_Y` to `TOP_Y + 431×s` | Rooftop, parapet, upper floors |
| 2 — tiled windows | 148–431 × N tiles | `p1Bot` to `p3Top` | Fill bulk of extended wall height |
| 3 — lower building | 148–984 | `p3Top` to `p3Top + 836×s` | Mid-building down through floor level |

**Key constants:**
- `s = 1704 / 984` — world units per source row (same visual scale as before)
- `TOP_Y = −2668` — rooftop anchor (2 character-heights below ceiling y=−2700)
- `p1Bot = TOP_Y + 431×s ≈ −1921.9` — bottom of part 1
- `tileDestH = 283×s ≈ 490.1` — world units per tile (rows 148–431)
- `nTiles = ceil(max(0, GROUND_Y − p3DestH − p1Bot) / tileDestH) = 4` — tiles needed so part 3 reaches the floor
- `p3Top = p1Bot + 4 × tileDestH ≈ 38.5` — top of part 3; row 148 anchored here

**Seam analysis:**
- Part 1 → tile join (y≈−1921.9): source row 431 meets tile row 148. Both are within the clean repeating window section (rows 148–431), so only a minor offset (~0.05 window heights) is possible.
- Tile → part 3 join (y≈38.5): same rows (431 → 148), same minor offset.
- Both joins are window-to-window — far less noticeable than the previous rooftop-to-window mismatch.

**Mirror:** Left wall (`pi=1`) uses `dx = p.x + p.w`, `dw = −drawW` (negative width mirrors the image). Right wall (`pi=2`) uses `dx = p.x`, `dw = drawW`. Same sign convention for all three drawImage calls.

**Coverage:** Part 3 bottom ≈ world y 1486, which extends past GROUND_Y=1440 (off-screen below floor). No gap at any camera position between y=−2625 and GROUND_Y.

## Kullad End-Flag Sprite Animation

**Asset:** `animations/kullad/` — 193 RGBA PNGs, 640×640px each. Source: `glowing cup.mp4` (24fps, 640×640, black background). Used as the animated goal/end-flag sprite.

**Background removal method:** Per-pixel threshold against black — no flood fill. Each pixel's max channel value determines alpha:
- `max(R,G,B) < 25` → fully transparent (handles H.264 compression artifacts on pure black)
- `25 ≤ max < 70` → linear ramp (soft anti-aliasing edge)
- `max ≥ 70` → fully opaque

Flood fill was avoided because the dark clay cup body (max channel ~85) would be reachable from the black background via chaining, eating the cup interior.

**Frames:** 193 frames covering one full loop (≈8 seconds at 24fps).

## 10 New Billboard Platform Scale-Up (2× Greedy Layout)

**Character width unit:** 12 world units (player `w:12`). **5 character widths** = 60 world units.
**Wall clearance rule:** platform x ≥ 76 (left wall right edge 16 + 60); platform right edge ≤ 764 (right wall left edge 824 − 60).

**Sizing rule:** `new_w = 2 × original_1× visible content width` (measured via Pillow `getbbox()`); `new_h = round(new_w × sh/sw)`. Original 1× w values (pre-scaling): platform4=70, Platform8=190, platform2=85, platform6=140, Platform9=165, Platform3=80, Platform10=210, platform1=75, Platform11=175, platform5=95.

**Placement algorithm:** Greedy largest-first. Sort the 10 platforms by world area (w×h) descending. For each platform scan candidate (x, y) positions across the full level space (Y_MAX=1000 down to Y_MIN=−2550, x constrained by wall clearance), score = minimum Euclidean distance to all already-placed obstacles (walls, floor, and previously placed platforms). Place at the highest-scoring position that has no overlaps. Obstacles include the 6 locked original platforms. After placement, add to obstacle list.

**The 6 locked original platforms (not touched):** slots 2 (billboard_1), 6 (long_billboard), 7 (billboard_4), 10 (billboard_2), 12 (billboard_3), 15 (billboard_5).

**Final layout (10 new platforms):**

| Slot | Image | x | y | w | h | 1× orig w |
|------|-------|---|---|---|---|-----------|
| 0 | platform 4.png | 144 | 600 | 140 | 270 | 70 |
| 1 | Platform 8.png | 228 | 980 | 380 | 280 | 190 |
| 3 | platform 2.png | 124 | -2188 | 170 | 328 | 85 |
| 4 | platform 6.png | 331 | -602 | 280 | 212 | 140 |
| 5 | Platform 9.png | 316 | -243 | 330 | 243 | 165 |
| 8 | Platform 3.png | 542 | -2169 | 160 | 309 | 80 |
| 9 | Platform 10.png | 208 | 186 | 420 | 324 | 210 |
| 11 | platform 1.png | 423 | -1399 | 150 | 289 | 75 |
| 13 | Platform 11.png | 252 | -1011 | 350 | 261 | 175 |
| 14 | platform 5.png | 134 | -1507 | 190 | 367 | 95 |

**Rendering:** Billboard drawing scales `drawH = p.w * c.sh / c.sw` automatically — no separate rendering changes needed.

## God Mode Level Editor

**What it does:** While god mode is active, an in-game level editor allows placing/removing spike enemies and repositioning platforms without editing source code.

**Activation:** Type `nggyu` during gameplay to toggle god mode (and editor) on/off.

**Spike placement:**
- Click anywhere on empty world space → places a 51×18 unrotated spike centred on the click point
- Click on an existing spike → removes it
- Placed spikes are live enemies: they kill the player on contact

**Platform repositioning (staticPlats indices 3+ only; floor/walls are locked):**
- Click a platform → selects it (pink dashed highlight around hitbox); platform and billboard visual move together
- Click and drag a selected platform → freely repositions it
- Arrow keys while a platform is selected → nudge 1 world unit per press (justPressed, not held)
- Shift+ArrowRight while a platform is selected → scale up (w+1, h+1); Shift+ArrowLeft → scale down (min 1); current w×h shown in HUD
- Click empty space → deselects current platform (and places a spike)
- Arrow keys with no platform selected → normal god mode flight (unchanged)

**Export (E key while god mode active):**
- Logs two copy-pasteable code blocks to the browser console: `const enemies = [...]` and `const staticPlats = [...]`
- A "Exported to console" confirmation fades in at the bottom of the canvas for ~2 seconds

**HUD:** Three lines of editor bindings appear top-right below "GOD MODE", showing current selection state. The existing coordinate dot and world-position readout are unchanged.

**Key variables:**
- `editorSelectedPlat` — index into `staticPlats`; -1 = none selected
- `_editorDragActive / _editorDragStartCX/CY / _editorDragPlatX0/Y0` — drag state
- `_editorExportMsg` — countdown frames for the on-screen export confirmation (120 = 2 s)

**Implementation notes:**
- `_canvasToWorld(clientX, clientY)` converts browser client coords → world units via `canvas.getBoundingClientRect()` + the 2× world scale
- Arrow key `preventDefault` added in the first keydown listener when `godMode` is true (prevents page scroll)
- Toggling god mode off resets `editorSelectedPlat` and `_editorDragActive`
- The platform highlight is drawn inside `drawWorld()`'s 2× scaled context, so `lineWidth:1` = 2 canvas pixels

## Platform Hitbox Bottom-Edge Alignment — Sign Face Only

**Goal:** Every billboard platform hitbox wraps the rectangular sign face only — not the pole, pipe, or mounting hardware hanging below it.

**Method:** Per-image pixel measurement using Python/Pillow. For each source image, the per-row horizontal span of non-transparent pixels was computed across the billboard's crop region (`BILLBOARD_CROP[img_idx]`). The sign face bottom row is the last row before the first sustained large span drop — the structural transition from the wide sign rectangle to the narrow pole/pipe below.

**Sign-bottom transitions observed:**
- Square billboards (billboard_1–5, 1024×1024): row ~327–328 in crop, span drops ~123 px from ~642 to ~519 (sign → mount bracket)
- Portrait billboards (long_billboard, platform 1–5, 832×1248): row ~872–873, span drops ~92 px from ~480 to ~388 (sign → pipe)
- platform 6.png (1024×1024): row 458, span drops 145 px from ~755 to ~610 (sign → lower bracket)
- Platform 8.png / Platform 9.png (1344×768): row 591, span drops ~305 px from ~468 to ~160 (sign → pipe)
- Platform 10.png (1344×768): row 491, span drops 163 px from ~837 to ~674 (sign → lower bracket)
- Platform 11.png (1344×768): row 593, span drops 256 px from ~465 to ~209 (sign → pipe)

**Formula:** `p.h = round(p.w * sign_src_rows / c.sw)`
where `sign_src_rows = sign_bottom_row + 1` (number of source rows from crop top through sign face bottom), and `c.sw` is the crop width from `BILLBOARD_CROP`.

**Final h values (all 16 floating platforms):**

| pi | Image | sw | sign_src_rows | p.w | p.h |
|----|-------|----|---------------|-----|-----|
| 3  | platform 4.png   | 559 | 873 | 140 | 219 |
| 4  | Platform 8.png   | 906 | 495 | 464 | 254 |
| 5  | billboard_1.png  | 694 | 328 | 120 |  57 |
| 6  | platform 2.png   | 559 | 874 | 276 | 432 |
| 7  | platform 6.png   | 815 | 459 | 280 | 158 |
| 8  | Platform 9.png   | 906 | 495 | 330 | 180 |
| 9  | long_billboard   | 559 | 873 | 201 | 314 |
| 10 | billboard_4.png  | 694 | 328 | 172 |  81 |
| 11 | Platform 3.png   | 559 | 874 | 260 | 407 |
| 12 | Platform 10.png  | 901 | 492 | 488 | 266 |
| 13 | billboard_2.png  | 694 | 329 | 187 |  89 |
| 14 | platform 1.png   | 560 | 874 | 150 | 234 |
| 15 | billboard_3.png  | 694 | 328 | 150 |  71 |
| 16 | Platform 11.png  | 898 | 496 | 350 | 193 |
| 17 | platform 5.png   | 559 | 874 | 190 | 297 |
| 18 | billboard_5.png  | 694 | 329 | 200 |  95 |

**No other properties changed** — x, y, w, and type are all identical to before.
