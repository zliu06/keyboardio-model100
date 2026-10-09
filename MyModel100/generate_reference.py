#!/usr/bin/env python3
"""Generate a visual reference from this sketch, including Qukeys holds."""
import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

HERE = Path(__file__).resolve().parent
ORDER = (
    list(range(7)) + list(range(16, 23)) + list(range(32, 38))
    + list(range(48, 54)) + [38, 7, 23, 39, 55, 54]
    + list(range(9, 16)) + list(range(25, 32)) + list(range(42, 48))
    + [41] + list(range(58, 64)) + [56, 40, 24, 8, 57]
)
assert len(ORDER) == len(set(ORDER)) == 64

def keymaps(source):
    source = re.sub(r'/\*.*?\*/|//[^\n]*', '', source, flags=re.S)
    result = {}
    for match in re.finditer(r'\[(\w+)\]\s*=\s*KEYMAP_STACKED\s*\(', source):
        name = match[1]
        if name in result:
            continue  # QWERTY is the active, first PRIMARY definition.
        start = match.end()
        depth, cursor = 1, start
        while depth:
            depth += (source[cursor] == '(') - (source[cursor] == ')')
            cursor += 1
        parts, current, nested = [], '', 0
        for char in source[start:cursor - 1] + ',':
            if char == ',' and nested == 0:
                parts.append(current.strip())
                current = ''
            else:
                current += char
                nested += (char == '(') - (char == ')')
        if len(parts) != 64:
            raise ValueError(f'{name}: expected 64 keys, got {len(parts)}')
        result[name] = dict(zip(ORDER, parts))
    return result

ALIASES = {
    '___': ('Prog', 'Transparent / Prog on base'), 'XXX': ('—', 'Disabled'),
    'LeftGui': ('⌘', 'Command'), 'RightGui': ('⌘', 'Command'),
    'LeftControl': ('Ctrl', 'Control'), 'RightControl': ('Ctrl', 'Control'),
    'LeftAlt': ('⌥', 'Option'), 'RightAlt': ('⌥', 'Option'),
    'LeftShift': ('⇧', 'Shift'), 'RightShift': ('⇧', 'Shift'),
    'Spacebar': ('Space', 'Space'), 'Backspace': ('⌫', 'Backspace'),
    'Delete': ('Del', 'Forward Delete'), 'Enter': ('Enter', 'Enter'),
    'Escape': ('Esc', 'Escape'), 'PageUp': ('PgUp', 'Page Up'),
    'PageDown': ('PgDn', 'Page Down'), 'Tab': ('Tab', 'Tab'),
    'Backtick': ('`', 'Backtick'), 'Quote': ("'", 'Quote'),
    'Equals': ('=', 'Equals'), 'Semicolon': (';', 'Semicolon'),
    'Comma': (',', 'Comma'), 'Period': ('.', 'Period'), 'Slash': ('/', 'Slash'),
    'Minus': ('−', 'Minus'), 'Backslash': ('\\', 'Backslash'), 'Pipe': ('|', 'Pipe'),
    'LeftCurlyBracket': ('{', 'Opening brace'), 'RightCurlyBracket': ('}', 'Closing brace'),
    'LeftBracket': ('[', 'Opening bracket'), 'RightBracket': (']', 'Closing bracket'),
    'LeftArrow': ('←', 'Left Arrow'), 'RightArrow': ('→', 'Right Arrow'),
    'UpArrow': ('↑', 'Up Arrow'), 'DownArrow': ('↓', 'Down Arrow'),
    'LEDEffectNext': ('LED', 'Next LED effect'), 'PcApplication': ('Menu', 'Application menu'),
    'KeypadSubtract': ('−', 'Keypad subtract'), 'KeypadAdd': ('+', 'Keypad add'),
    'KeypadMultiply': ('×', 'Keypad multiply'), 'KeypadDivide': ('÷', 'Keypad divide'),
    'mouseUp': ('↑', 'Mouse move up'), 'mouseDn': ('↓', 'Mouse move down'),
    'mouseL': ('←', 'Mouse move left'), 'mouseR': ('→', 'Mouse move right'),
    'mouseBtnL': ('Click L', 'Left mouse button / hold to drag'),
    'mouseBtnR': ('Click R', 'Right mouse button'), 'mouseBtnM': ('Click M', 'Middle mouse button'),
    'mouseWarpNW': ('Warp ↖', 'Warp upper-left quadrant'),
    'mouseWarpNE': ('Warp ↗', 'Warp upper-right quadrant'),
    'mouseWarpSW': ('Warp ↙', 'Warp lower-left quadrant'),
    'mouseWarpSE': ('Warp ↘', 'Warp lower-right quadrant'),
    'mouseWarpEnd': ('Reset', 'End / reset warp sequence'),
    'ScanPreviousTrack': ('Prev', 'Previous track'), 'ScanNextTrack': ('Next', 'Next track'),
    'PlaySlashPause': ('Play', 'Play / pause'), 'Mute': ('Mute', 'Mute audio'),
    'VolumeDecrement': ('Vol −', 'Volume down'), 'VolumeIncrement': ('Vol +', 'Volume up'),
}

def label(token):
    layer = re.fullmatch(r'(ShiftToLayer|LockLayer)\((\w+)\)', token)
    if layer:
        name = {'FUNCTION': 'Nav', 'MOUSE': 'Mouse', 'NUMPAD': 'Num'}[layer[2]]
        return name, ('Hold for ' if layer[1] == 'ShiftToLayer' else 'Toggle ') + name
    if token.startswith('M('):
        return ('Any', 'Random character macro') if 'ANY' in token else ('Version', 'Firmware version macro')
    name = re.sub(r'^(Key_|Consumer_)', '', token)
    if name in ALIASES:
        return ALIASES[name]
    if re.fullmatch(r'[A-Z0-9]|F\d+', name):
        return name, name
    raise ValueError(f'Unrecognized key: {token}')

def model(source, factory):
    maps = keymaps(source)
    caps = factory if isinstance(factory, dict) else keymaps(factory)['PRIMARY']
    holds = [(scope, int(row) * 16 + int(col), key) for scope, row, col, key in re.findall(
        r'Qukey\((\w+),\s*KeyAddr\((\d+),\s*(\d+)\),\s*(Key_\w+|ShiftToLayer\(\w+\))\)', source)]
    layers = []
    names = {'PRIMARY': 'Base', 'FUNCTION': 'Navigation', 'MOUSE': 'Mouse', 'NUMPAD': 'Numpad'}
    for name in ['PRIMARY', 'FUNCTION', 'MOUSE', 'NUMPAD']:
        keys = []
        for address in range(64):
            supplying = 'PRIMARY' if maps[name][address] == '___' else name
            token = maps[supplying][address]
            short, full = label(token)
            hold = next((label(key)[0] for scope, addr, key in holds
                         if addr == address and scope in ('all_layers', supplying)), '')
            cap = label(caps[address])[0]
            keys.append({'address': address, 'cap': cap, 'label': short, 'full': full,
                         'hold': hold, 'changed': token != caps[address],
                         'detail': f'Factory {cap}: {full}' + (f'; hold {hold}' if hold else '')})
        layers.append({'id': name, 'name': names[name], 'keys': keys})
    return layers

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inline', type=Path, help='Also write an inline conversation reference')
    args = parser.parse_args()
    source = (HERE / 'MyModel100.ino').read_text()
    active_source = re.sub(r'/\*.*?\*/|//[^\n]*', '', source, flags=re.S)
    if not re.search(r'^\s*#define\s+PRIMARY_KEYMAP_QWERTY\s*$', active_source, re.M):
        raise ValueError('Reference currently supports the active QWERTY primary map')
    factory = dict(enumerate(json.loads((HERE / 'factory-keycaps.json').read_text())))
    data = model(source, factory)
    fragment = (HERE / 'reference-template.html').read_text().replace('__KEYMAP_DATA__', json.dumps(data, ensure_ascii=False))
    fragment = fragment.replace('__REFERENCE_DATE__', datetime.now(ZoneInfo('America/Los_Angeles')).strftime('%B %d, %Y'))
    if args.inline:
        args.inline.write_text(fragment)
    standalone = '''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>My Model 100 keymap</title>
<style>:root{color-scheme:light dark;--foreground:light-dark(#182025,#edf0f2);--background:light-dark(#fff,#161a1e);--muted-foreground:light-dark(#505b62,#bdc7ce);--border:light-dark(#bac2c7,#555f68);--accent:light-dark(#e9eff5,#273744);--primary:light-dark(#223d54,#c9e3f5);--primary-foreground:light-dark(#fff,#14202a);--font-size-base:14px}body{font:14px/1.5 system-ui;background:var(--background);color:var(--foreground);max-width:1050px;margin:24px auto;padding:0 16px}.text-small{font-size:12px}.text-muted{color:var(--muted-foreground)}.form-select{font:inherit;padding:6px;background:var(--background);color:var(--foreground);border:1px solid var(--border)}.btn{font:inherit;padding:6px 12px;background:var(--background);color:var(--foreground);border:1px solid var(--border);border-radius:5px}.viz-controls{display:flex;flex-wrap:wrap;gap:12px;align-items:center}button:focus-visible,select:focus-visible{outline:2px solid var(--primary);outline-offset:2px}</style>
</head><body>'''
    (HERE / 'keymap-reference.html').write_text(standalone + fragment + '</body></html>')
    print('Generated keymap-reference.html: 4 layers, 64 positions per layer, Qukeys hold actions included.')

if __name__ == '__main__':
    main()
