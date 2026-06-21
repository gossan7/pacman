# Logbook - Victor

*Personal log, consolidated from my commits across the project. Coordination
points refer to our Discord / in-person syncs.*

**29/05** - Set up the base project structure.

**01/06** - Built the base `Renderer` class and the empty concrete renderer
classes to fix the rendering architecture.

**03/06** - Refactor and cleanup across almost every file, with bug
corrections.

**04/06** - Menu engine, then the `window_handler`, a boilerplate menu renderer
followed by a cleaner version.

**05/06** - `RegionPopupEngine` (the base for the overlay menus).

**08/06** - Pop-up region + quit engine, added the frightened ("fatigue")
mode.

**09/06** - Scores engine, controls engine, and catching the escape key so it
can be handled by the engines.

**14/06** - Pause menu and the fullscreen fix, score register, another in-game
fullscreen fix.

**15/06** - Score register now writes scores to the file, sorted by score,
fixed the sorting, restricted name entry to alphanumeric characters and
spaces.

**17/06** - Reworked the cheat-renderer toggle and added the Konami code,
wrote the docstrings and a first README draft.