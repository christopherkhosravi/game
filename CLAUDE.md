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
│   ├── cutscene_1.mp4            (cutscene clip 1 — plays in full)
│   ├── cutscene_2.mp4            (cutscene clip 2 — plays last 2 seconds only)
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

**Assets:** `animations/billboard_1.png` through `billboard_5.png` — 1024×1024 RGBA PNGs with transparent backgrounds and neon pixel-art billboard designs.

**Assignment (BILLBOARD_PLAT_MAP):**
| Floating slot | staticPlats index | Billboard |
|---|---|---|
| 0 | 3 (platform 1, left, y=1000) | billboard_1 |
| 1 | 4 (platform 2, right, y=770) | billboard_2 |
| 2 | 5 (platform 3, left, y=570) | billboard_3 |
| 3 | 6 (platform 4, right, y=390) | billboard_4 |
| 4 | 7 (platform 5, left, y=220) | billboard_5 |
| 5 | 8 (platform 6 top, y=80) | billboard_3 |

Pattern 1,2,3,4,5,3 — no two adjacent platforms share the same image. Platform 6 (top) reuses billboard_3 because it is not adjacent to platform 3 in the climbing path.

**Implementation:**
- `BILLBOARD_IMGS` — array of 5 `Image` objects preloaded at startup (after background frame loader)
- `BILLBOARD_PLAT_MAP` — `[0,1,2,3,4,2]` maps floating-platform slot to `BILLBOARD_IMGS` index
- `drawWorld()` platform loop converted from `for…of` to indexed `for` loop; `pi >= 3` branches to billboard drawing (drawn in 2× world-scale context, so world coords are used directly)
- Drawing uses the 9-argument `drawImage(img, sx, sy, sw, sh, dx, dy, dw, dh)` to crop transparent padding from the source before scaling.
- `BILLBOARD_CROP` stores the visible content bounding box for each image (measured via Pillow): all 5 images share `sx=165, sw=694`; `sy` is 225 (images 1,3,4) or 224 (images 2,5); `sh` is 601 or 602. Left/right padding is 165px each, top ~225px, bottom ~198px, out of a 1024×1024 canvas.
- Draw formula: `drawH = p.w * c.sh / c.sw` — visible content width fills the platform exactly, height scales proportionally. Overflow below platform bottom is intentional (not clipped).
- Fallback: if image not yet loaded, draws the original brick fill

## God Mode Cheat

**What it does:** Typing the sequence `nggyu` (in order, any time during gameplay) toggles god mode on/off. While active: arrow keys fly the player freely; all gravity, friction, and collision are skipped; death (fall-out, hazards, enemies) is suppressed; a pink "GOD MODE" label appears top-right. Typing the sequence again turns it off. No effect on save state or normal gameplay.

**Key variables:**
- `godMode` (bool) — declared in GAME STATE section alongside `screenShake`.
- `_godSeq` / `_godIdx` — sequence array `['KeyN','KeyG','KeyG','KeyY','KeyU']` and current match index, declared just before the second `keydown` listener in INIT.

**Implementation:**
- **Sequence detection:** Second `keydown` listener checks each key against `_godSeq[_godIdx]`. On full match, toggles `godMode` and resets index. On mismatch, resets (or advances to 1 if the key matches the first step, to handle partial overlaps).
- **Flight block:** Inserted in `update()` immediately after the countdown early-return. If `godMode`: clears `p.dead`, moves player with `ArrowLeft/Right/Up/Down` at 5 px/frame, zeroes `vx/vy`, advances particles, decrements screen shake, calls `updateCamera()`, then returns — skipping all physics, collision, hazard, and win checks.
- **Indicator:** In `render()` after `drawSpawnTimer()`: draws `'GOD MODE'` in `#ff6b9d` bold Courier New 18px, right-aligned at `(CW-16, 16)`.

## Bounce Animation First-Frame Skip

**What it does:** The bounce animation starts on `bounce/2.png` (previously the second frame) instead of `bounce/1.png`. `bounce/1.png` is never shown.

**How:** Two changes in `hnov_5.html`:
1. **SPRITE_DEFS** — bounce entry changed from `frames: 3, loopStart: 1` to `frames: 2, firstFrame: 2`. `firstFrame` tells the loader which file number to start from; `frames` says how many to load. Result: `SPRITE_IMGS['bounce']` = [2.png, 3.png].
2. **Loader** — added `firstFrame` support: `const _f0 = def.firstFrame ?? 1; for (let i = _f0; i < _f0 + def.frames; i++)`. All other animations have no `firstFrame` so they default to 1 and are unaffected.

With these changes `animFrame` 0 → `bounce/2.png`, `animFrame` 1 → `bounce/3.png`, and the loop restarts at 0, so `bounce/1.png` is never loaded or displayed.

## Cutscene System

**What it does:** A cutscene plays between the title screen (BEGIN button) and the countdown. Clip 1 plays in full; clip 2 plays only its last 2 seconds. Fades are event-driven, not time-calculated.

**Fade schedule:**
1. Midpoint of clip 1 (`timeupdate` fires when `currentTime >= duration/2`) → fade out + back in (1800 ms each way), clip 1 continues playing
2. End of clip 1 (`ended`) → fade out (1800 ms), then at full black: seek clip 2 to `duration - 2`, play it, fade back in (1800 ms)
3. End of clip 2 (`ended`) → exit fade to black (3000 ms) → `startGame()`

**Skip:** Space or R → immediately begins exit fade (3000 ms) → countdown. During exit fade the last video frame fades to black before `startGame()` is called.

**Key variables (GAME STATE section):**
- `cutsceneClip` — `1` | `2`, which video element is active
- `cutsceneExiting` — true when the final exit fade is underway
- `cutsceneExitStart` — `performance.now()` when exit fade began
- `cutsceneFadeState` — `'none'` | `'out'` | `'in'`, tracks the mid-cutscene fade phase
- `cutsceneFadeStart` — `performance.now()` when the current fade phase began
- `cutsceneFadeAction` — `'switchToClip2'` | `'none'`, action to execute at peak black
- `cutsceneMidFired` — bool, prevents the midpoint fade from firing more than once

**Constants:** `CUTSCENE_FADE_MS = 1800` (each half of a mid-cutscene fade), `CUTSCENE_EXIT_MS = 3000` (exit fade duration).

**`drawCutscene()` logic:**
- If `cutsceneExiting`: renders last video frame with black overlay ramping from 0→1 over `CUTSCENE_EXIT_MS`, then calls `startGame()` at alpha=1 (canvas is fully black, no flash)
- Otherwise: runs the fade state machine (`out` → peak black → execute action → `in` → `none`); draws current video frame then applies fade overlay on top

**Implementation:**
- Two hidden `<video>` elements (`cutsceneVid1`, `cutsceneVid2`) with `preload="auto" muted playsinline` in the HTML.
- `beginCutscene()` — hides overlay, sets `gameState = 'cutscene'`, resets all fade state, plays vid1 from `currentTime = 0`.
- `drawCutscene()` — called from `render()` early-return when `gameState === 'cutscene'`.
- `vid1 'timeupdate'` listener → fires midpoint fade when `currentTime >= duration/2` (guarded by `cutsceneMidFired`).
- `vid1 'ended'` listener → starts fade-out with `cutsceneFadeAction = 'switchToClip2'`; clip 2 seek+play happens at peak black.
- `vid2 'ended'` listener → sets `cutsceneExiting = true`.
- Skip keydown (Space or R) → sets `cutsceneExiting = true`, pauses both videos, clears `cutsceneFadeState`.
- Button click handler calls `beginCutscene` (not `startGame`).

**Architecture note:** `gameState = 'cutscene'` causes `update()` to return early (existing guard `gameState !== 'playing'`), so no game logic runs during the cutscene.

## Wall Slide Entry Cost

**What it does:** On fresh wall contact (player was not touching the wall the previous frame), 30 points are instantly deducted from `wallMeter`. If the meter drops to 0, `wallContact` and `wallDir` are cleared immediately so the player falls instead of sliding. This cost applies to wall slide only — dead hang (`floatMeter`) is unaffected.

**Key variable:** `prevWallContact` (bool) added to `makePlayer()`. Tracks whether the player was wall-sliding last frame. Initialized to `false`; reset automatically on `respawn()` via `makePlayer()`.

**Implementation (wall meter block, ~line 549):**
```
if (p.wallContact) {
  if (!p.prevWallContact) {
    p.wallMeter = Math.max(0, p.wallMeter - 30);
    if (p.wallMeter === 0) { p.wallContact = false; p.wallDir = 0; }
  }
  if (p.wallContact) {
    p.wallMeter = Math.max(0, p.wallMeter - 1);
    if (p.wallMeter === 0) { p.wallContact = false; p.wallDir = 0; }
  }
} else if (p.onGround) {
  p.wallMeter = Math.min(100, p.wallMeter + 2);
}
p.prevWallContact = p.wallContact;
```

**Test:** Grab a wall with a full meter and verify the meter jumps down 30% immediately. Then let it drain to ~25%, leave the wall, touch it again — player should fall instantly (meter clamped to 0, no slide).

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
