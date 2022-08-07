# Nu plugin binary reader
A general binary parser based on [kaitai struct](https://formats.kaitai.io/).

## Require python version
python3.7+

## Usage
1. register the plugin to nushell
```
register -e json plugin.py
```

It will introduce a new command: `from-binary`.  So you can just play with it.

## Usage example
1. read and parse png file:
```
open capture.PNG | from-binary png | get ihdr
```

2. read and parse ttf file:
```
open FiraCode-VF.ttf | from-binary ttf | get directory_table
```

## Note
The `kaitaistruct.py` is just a copy of [kaitai struct python runtime](https://github.com/kaitai-io/kaitai_struct_python_runtime), put it directly here, so we don't need extra requirements.
And `reader/*.py` are just a copy of auto-generated parser, DON'T CHANGE IT.
