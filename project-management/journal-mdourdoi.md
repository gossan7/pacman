# Logbook - Matthieu

*Personal log, consolidated from my commits across the project. Coordination
points refer to our Discord / in-person syncs.*

**01/06** - Set up the project skeleton: `instances` and helpers, gum values,
`__init__` fixes, and the first engines. Integrated the suggestions from the
early code review.

**02–03/06** - Many fixes, sorted out the Makefile, cleaned the repo. Built the
`input_handler` and a small tester to validate inputs.

**04/06** - First `GameEngine` and cleaned up the entities, got a work-in-
progress Pac-Man moving. Added classic-looking assets.

**05/06** - Reworked ghost behaviour to match the subject and the original game
as closely as possible.

**07/06** - First rough playable version, made the controls feel less harsh
when hitting a wall.

**08/06** - Worked on collisions, added interpolation between cells to simulate
a hitbox and get smooth movement.

**09/06** - Added the sprites.

**11–12/06** - Rounded maze corners (vertices) looking right, added animations
for death, eating a ghost, and level start/end, brought values back to normal
and cleaned up, made end-of-game handled properly.

**15/06** - `GameEngine.reset()` and the parsers, added the cheats list in
`globalstate` and fixed the seed value.

**16/06** - Cheats and the cheat engine working, added a visual indicator for
whether a cheat is on/off, removed unused code.

**17/06** - Fixed the parsers, fixed end-of-game so it only triggers once per
level (found the offending commit with `git bisect` - it had been moved into
`update_always` and re-fired every frame), applied a review change to
`pause_engine`.

**18/06** - Got the linter green (flake8 + mypy), integrated Victor's review
and handled a few more errors, and produced the build ready to push to itch.io
(PyInstaller, path handling for assets/config).
