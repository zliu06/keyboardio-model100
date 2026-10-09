# Personal Model 100 layout

This sketch extends the existing personal firmware with four built-in layers:

| Layer | Access | Left hand | Right hand |
| --- | --- | --- | --- |
| PRIMARY (0) | Default | QWERTY | QWERTY |
| NUMPAD (1) | Existing Num key | Base layout | Existing numpad |
| FUNCTION (2) | Hold right thumb Backspace, right Fn, or left former Shift thumb key | Base layout | Original arrows, brackets, media keys, `\` and `\|` |
| MOUSE (3) | Hold left third thumb key, left Fn, or right former Shift thumb key | Original mouse positions | Base layout |

Right Fn holds FUNCTION and left Fn holds MOUSE on every layer. The former left
Fn magic combos remain disabled.

## Thumb keys

Left cluster, in the original Ctrl / Backspace / Command / Shift order:

- Tap Enter; hold Command
- Tap Backspace; hold Shift
- Hold MOUSE; release to return
- Hold FUNCTION; release to return

Right cluster, in the original Ctrl / Space / Alt / Shift order (right to left):

- Command only (no tap action)
- Tap Space; hold Shift
- Tap Backspace; hold FUNCTION/navigation
- Hold MOUSE; release to return

The third key from the left on the left thumb cluster holds MOUSE. The rightmost
thumb key is ordinary Right Command. The second key from the right taps Space
and holds Shift, matching the left Backspace/Shift position. The third key from
the right taps Backspace and holds FUNCTION/navigation.
These actions apply on all four built-in layers. The former Shift thumb keys
retain their layer shortcuts.

Control and Option remain available through home-row holds. The butterfly key
also remains Right Option on the base layer.

For the frequent paired-brace sequence: tap Space, then hold the third thumb
key from the right and press U (`{`), I (`}`), then H (Left Arrow). Release the
thumb key to leave Navigation. Tap it for Backspace; use the leftmost left
thumb key for Enter. For left-hand Command+Enter, hold S (home-row Command)
and tap that leftmost thumb key. H/J/K/L remain Left/Down/Up/Right on FUNCTION.

## Home-row modifiers

Home-row modifiers depend on the active layer:

| Layer | Left-hand home-row mods | Right-hand home-row mods |
| --- | --- | --- |
| PRIMARY | Enabled | Enabled |
| NUMPAD | Enabled | Enabled |
| FUNCTION | Enabled | Disabled |
| MOUSE | Disabled | Enabled |

Where enabled, tapping sends the current layer's key action and holding sends
its original modifier. Holding left-hand mouse keys continues movement or holds
mouse buttons. Holding right-hand arrows allows normal key repeat.

| Base key position | Hold |
| --- | --- |
| A | Left Shift |
| S | Left Command |
| D | Left Option |
| F | Left Control |
| J | Right Control |
| K | Right Option |
| L | Right Command |
| ; | Right Shift |

The existing 250 ms hold timeout and disabled tap-repeat setting are preserved.
The left thumb Enter key holds Command, left Backspace and right Space hold Shift, and
right thumb Backspace holds Navigation on every layer. The rightmost thumb key is
Command only. Right Command also remains available by holding L on PRIMARY
and MOUSE, or the 3 position on NUMPAD.

On PRIMARY, Tab exchanges positions with Page Up, and Escape exchanges positions
with Page Down. The mouse movement, button, and warp positions match the original
combined function layer. Other mouse-layer positions inherit the base layout.

Build this sketch for `keyboardio:gd32:keyboardio_model_100`. Hold the physical
Prog key during upload until flashing begins. See the repository README for setup instructions and the tested dependency versions.

## Mouse controls

Hold the left third thumb key, left Fn, or the right former Shift thumb key,
then use these physical
positions. Labels below refer to the base-layer QWERTY positions.

| Key position | Mouse action |
| --- | --- |
| W | Hold to move up |
| A / S / D | Hold to move left / down / right |
| F | Left mouse button; hold to drag |
| R | Right mouse button |
| V | Middle mouse button |
| G | Warp to the top-left sector |
| Page Up (original Tab position) | Warp to the top-right sector |
| B | Warp to the bottom-left sector |
| Page Down (original Esc position) | Warp to the bottom-right sector |
| T | End/reset the warp sequence |

With the current 2×2 warp grid, the first warp tap jumps to the center of a screen
quadrant. Each subsequent warp tap chooses a quadrant within the previously
selected region, narrowing the target. For example, G then G moves to the center
of the top-left quarter, then the top-left quarter of that region. T ends the
sequence without moving the pointer; the next warp tap starts from the whole
screen. A movement or mouse-button key also ends the warp sequence. Warp keys
do not click; use F for a left click after positioning the pointer.

## Visual labels and reference

Run `python3 generate_reference.py` after editing this sketch to regenerate
`keymap-reference.html`. Open that file in a browser and keep it bookmarked.
Its layer selector displays each key's action and modifier hold beside the
original factory keycap legend. Use the browser's Print command to print all
four layers as a desk reference.

For physical labels, use small removable labels beside the thumb keys:
right to left **CMD**, **SPACE / SHIFT**, **BACKSPACE / NAV**, **MOUSE**. Label the left
thumb keys left to right **ENTER / CMD**, **BACKSPACE / SHIFT**, **MOUSE**, **NAV**. Label the
palm keys **MOUSE** (left) and **NAV** (right). A desk card handles the
secondary layers without putting several legends on every sculpted keycap.

Chrysalis (https://chrysalis.keyboard.io/) also supports the Model 100 and
provides a visual layout and LED editor. This firmware's built-in layers are
compiled into the sketch; home-row and thumb hold actions are configured in
Qukeys. The generated reference includes those holds explicitly.
