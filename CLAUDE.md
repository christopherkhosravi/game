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

## Control Remapping — WASD Only, Double-Tap Dash

**What changed:**
- Arrow keys removed from all `press()`/`jp()`/`jr()` calls — WASD is the sole movement input.
- Q and E dash bindings removed.
- Dash is now triggered by double-tapping A (dash left) or D (dash right) within a 250 ms window.
- `e.preventDefault()` narrowed from all arrow keys + Space to Space only.
- Title screen overlay and bottom controls bar updated to reflect new bindings.

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

## One-Way (Pass-Through) Floating Platforms

**What it does:** The 6 floating platforms (staticPlats indices 3–8) use `type:'pass'` instead of `type:'solid'`. The player lands on top but passes through freely from below and from the sides. The floor and walls remain `type:'solid'` and are unaffected.

**How it works:** The collision helpers already segregate by type:
- `resolveY` top-landing check runs for all types — no change needed.
- `resolveY` ceiling check is guarded by `if (p.type === 'solid')` — so jumping into the underside has no effect on `'pass'` platforms.
- `resolveX` skips any platform where `type !== 'solid'` — so walking into the side has no effect.
- Wall-contact detection (line ~512) is also `solid`-only.

The entire fix is changing `type:'solid'` → `type:'pass'` on the 6 floating platform entries in `staticPlats`.

## Billboard Platform Visuals

**What it does:** The 6 floating platforms (staticPlats indices 3–8) are drawn as scaled billboard PNG images instead of the default brick/color fill. Collision boxes are unchanged — only the visual rendering differs. The floor (index 0) and walls (indices 1–2) keep their original appearance.

**Assets:** `animations/billboard_1.png` through `billboard_5.png` — 1024×1024 RGBA PNGs with transparent backgrounds and neon pixel-art billboard designs. `animations/long_billboard.png` — 832×1248 RGBA PNG, portrait chai-tea billboard with hanging mechanism (white bg removed via Pillow flood-fill).

**Assignment (BILLBOARD_PLAT_MAP):**
| Floating slot | staticPlats index | Billboard |
|---|---|---|
| 0 | 3 (platform 1, left, y=1000) | billboard_1 |
| 1 | 4 (platform 2, right, y=770) | billboard_2 |
| 2 | 5 (platform 3, left, y=570) | long_billboard |
| 3 | 6 (platform 4, right, y=390) | billboard_4 |
| 4 | 7 (platform 5, left, y=220) | billboard_5 |
| 5 | 8 (platform 6 top, y=80) | billboard_3 |

Pattern 1,2,long,4,5,3 — no two adjacent platforms share the same image.

**Implementation:**
- `BILLBOARD_IMGS` — array of 6 `Image` objects (indices 0–5); billboard_1–5 loaded via loop, long_billboard pushed as index 5
- `BILLBOARD_PLAT_MAP` — `[0,1,5,3,4,2]` maps floating-platform slot to `BILLBOARD_IMGS` index
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

## Wall Grab Charge System

**What it does:** The player gets 3 wall grab charges per air cycle, shown as dots in the HUD (top-right, labelled GRAB). Each fresh wall contact consumes 1 charge. If 0 charges remain, touching a wall does nothing — the player slides past with no grab. Charges refresh on landing. The continuous `wallMeter` drain while actively grabbing is unchanged (no entry cost).

**Key variables:**
- `wallCharges` (int 0–3) — added to `makePlayer()`. Decremented on fresh wall contact; reset to 3 on `ry.landed`. Reset automatically on `respawn()`/`startGame()` via `makePlayer()`.
- `prevWallContact` (bool) — retained to detect fresh vs. held contact.

**HUD:** Three `abilityPip` dots (`wpip0–wpip2`) labelled GRAB in `#abilityBar`. Lit = charge available, dark = spent.

**Implementation (wall meter block):**
```
if (p.wallContact) {
  if (!p.prevWallContact) {
    if (p.wallCharges === 0) { p.wallContact = false; p.wallDir = 0; }
    else { p.wallCharges--; }
  }
  if (p.wallContact) {
    p.wallMeter = Math.max(0, p.wallMeter - 1/3);
    if (p.wallMeter === 0) { p.wallContact = false; p.wallDir = 0; }
  }
} else if (p.onGround) {
  p.wallMeter = Math.min(100, p.wallMeter + 2);
}
p.prevWallContact = p.wallContact;
```

**Test:** Use 3 wall grabs in the air; 4th touch should not grab. Land and verify all 3 dots refill.

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

## Dash: 3 Uses Per Air Cycle

**What changed:** `dashAvail` (bool) replaced with `dashCount` (int 0–3). The player can dash up to 3 times before landing; each dash decrements the counter. Landing resets it to 3. HUD updated from 1 pip (`pip0`) to 3 pips (`pip0–pip2`). Charging state (pink) shows while grounded and count < 3.

**Key variable:** `dashCount` in `makePlayer()`. All former `dashAvail` references updated.

**Test:** Dash 3 times in the air — 4th attempt should do nothing. Land and verify all 3 dots refill.

## Float: Toggle Instead of Hold

**What changed:** Float is now triggered by pressing S once (toggle on), pressing S again toggles it off. Previously required holding S. The `floatMeter` still drains at 1/3 per frame while floating; hitting 0 auto-disables float. Landing also disables float.

**Implementation:** `downP = jp(['KeyS'])` added to inputs block. Float block now checks `downP` to toggle `p.floating` rather than checking `down` (held).

**Test:** Press S in the air — float should activate and stay on without holding. Press S again to cancel. Let meter drain to 0 and verify float stops automatically.

## Meter Duration and Wall Fall Speed Tuning

**What changed:**
- Float meter drains at `1/3` per frame (was `1`) — 3× longer duration (300 frames from full instead of 100)
- Wall grab meter drains at `1/3` per frame (was `1`) — 3× longer duration (300 frames from full instead of 100; 30-point entry cost unchanged)
- `WALL_SLIDE_G` reduced from `0.07` to `0.035` — fall speed while wall-sliding is halved

**Constants modified:**
- `WALL_SLIDE_G` (line ~211, physics constants section) — `0.07` → `0.035`
- Float drain (line ~547, update section) — `p.floatMeter - 1` → `p.floatMeter - 1/3`
- Wall meter drain (line ~584, update section) — `p.wallMeter - 1` → `p.wallMeter - 1/3`

**Test:** Hold S in the air and verify the float meter drains over ~5 seconds instead of ~1.7 s. Grab a wall and verify the meter drains over ~5 seconds. Wall-sliding should feel noticeably slower descent.

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
