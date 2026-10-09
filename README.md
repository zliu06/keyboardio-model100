# Personal Keyboardio Model 100 configuration

My custom Model 100 firmware, keyboard mappings, and printable layer reference.
The latest layout has left thumb **Enter/Command** and right thumb
**Backspace/Navigation**. All firmware settings live in `MyModel100/MyModel100.ino`.

The flashed layout is stored on the keyboard, so connecting the same keyboard to
another laptop already uses these mappings. Clone this repository to consult the
reference, edit the layout, or build and flash the firmware from that laptop.

## Current thumb layout

Count the left keys from left to right, and the right keys from right to left.

| Position | Left tap | Left hold | Right tap | Right hold |
| --- | --- | --- | --- | --- |
| First | Enter | Command | No separate tap action | Command |
| Second | Backspace | Shift | Space | Shift |
| Third | No separate tap action | Mouse layer | Backspace | Navigation layer |
| Fourth | No separate tap action | Navigation layer | No separate tap action | Mouse layer |

Left palm holds Mouse; right palm holds Navigation. Home-row modifiers remain
available on the typing hand. The tap/hold timeout is 250 ms.

For left-hand Command+Enter, hold **S** and tap the leftmost thumb key.

See [the complete layout](MyModel100/README.md) for home-row modifiers, arrows,
symbols, mouse controls, and layer details.

## Get the files on another laptop

```sh
mkdir -p "$HOME/keyboard"
cd "$HOME/keyboard"
git clone https://github.com/zliu06/keyboardio-model100.git
cd keyboardio-model100
```

This is a public repository. For authenticated pushes, use your configured
GitHub HTTPS credentials or clone with SSH:

```sh
git clone git@github.com:zliu06/keyboardio-model100.git
```

Open `MyModel100/keymap-reference.html` in a browser. Its layer selector shows all
four layers, including modifier holds; the browser Print command prints every
layer. No network connection or firmware toolchain is needed to view it.

## Set up the firmware toolchain

The command-line workflow below is for macOS or Linux and requires Git, Make,
and Python 3.9 or newer. On macOS, install Apple's command-line tools if needed:

```sh
xcode-select --install
```

Install Kaleidoscope separately from this personal configuration repository:

```sh
cd "$HOME/keyboard"
git clone https://github.com/keyboardio/Kaleidoscope.git
cd Kaleidoscope
git checkout d07904a66196cba7a4f2abb8f31d087fd8b72f2b
export KALEIDOSCOPE_DIR="$HOME/keyboard/Kaleidoscope"
make setup
```

`make setup` downloads the Arduino CLI, board packages, and compiler toolchain.
Use the tested GD32 board-core revision after setup:

```sh
git -C "$KALEIDOSCOPE_DIR/.arduino/user/hardware/keyboardio/gd32" checkout d73e13cdb2abb7ede03fc56ca2576a983e38b773
git -C "$KALEIDOSCOPE_DIR/.arduino/user/hardware/keyboardio/gd32" submodule update --init --recursive
```

The tested dependencies are recorded in [dependencies.json](dependencies.json).
The original builds used Arduino CLI 1.5.1. For platform-specific requirements,
see [Kaleidoscope's setup instructions](https://github.com/keyboardio/Kaleidoscope/tree/d07904a66196cba7a4f2abb8f31d087fd8b72f2b#getting-started).

## Build and flash

```sh
cd "$HOME/keyboard/keyboardio-model100/MyModel100"
export KALEIDOSCOPE_DIR="$HOME/keyboard/Kaleidoscope"
make compile
make flash
```

When `make flash` reaches the prompt:

1. Unplug the Model 100.
2. Hold its physical **Prog** key and reconnect it.
3. Press Enter using the laptop keyboard or another keyboard.
4. Release Prog once flashing starts and wait for completion.

The sketch defines the four built-in layers and boots into Base. It retains
Chrysalis support for additional editable layers; the custom Qukeys holds are
defined in the source. This repository contains the compiled layout configuration,
not a dump of the keyboard's EEPROM or separately customized LED settings.

## Edit, regenerate, and synchronize

Edit `MyModel100/MyModel100.ino`, then regenerate the reference:

```sh
cd "$HOME/keyboard/keyboardio-model100"
python3 MyModel100/generate_reference.py
```

The reference generator has a bundled factory-keycap baseline, so it works
without installing Kaleidoscope or relying on another checkout's directory layout.

After building and checking your changes, commit and push them:

```sh
git add MyModel100
git commit -m "Update Model 100 layout"
git push origin main
```

On the other laptop, run `git pull --ff-only` before editing or building. Keep
future edits in this repository so both laptops share the same source.

## License and source

This repository uses [GPLv3 with Kaleidoscope's upstream additional permission](LICENSE).
The firmware is adapted from Keyboardio's Model 100 sketch, and its original
copyright notices are preserved. A copy of the license is also included beside
the sketch in [MyModel100/LICENSE](MyModel100/LICENSE).
