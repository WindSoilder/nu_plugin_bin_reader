# Nu plugin binary reader
A [nushell](https://www.nushell.sh/) plugin to read binary data

# Screenshots
## Parsing png and ttf
![parse png and ttf](screenshots/demo.gif)

## Download lib and parse library
![parse gif](examples/demo3.gif)

## Prerequisite
1. `nushell`, It's a nushell plugin, so you need it.
2. `python3.7+`

## Usage
1. register the plugin to nushell
```
register -e json plugin.py
```

It will introduce a new command: `from-binary`.  So you can play with it
You can just do it once.

2. fetch libs
There is `fetcher.nu` to help you download binary reader.  You can do something like this:

```
> use fetcher
> fetcher fetch-lib png
```

It will download "png" binary parser for you.

3. parse relative binary file
Take `png` file as example, you can do the following to get `capture.png` information.

```
open capture.png | from-binary png
```

Then it will output the following:
```
╭───────────┬───────────────────────────────────╮
│ magic     │ [137, 80, 78, 71, 13, 10, 26, 10] │
│ ihdr_len  │ 13                                │
│ ihdr_type │ [73, 72, 68, 82]                  │
│ ihdr      │ {record 7 fields}                 │
│ ihdr_crc  │ [179, 17, 228, 177]               │
│ chunks    │ [table 9 rows]                    │
╰───────────┴───────────────────────────────────╯
```

Ok, what if you want to get the size of png file, you need to know it's stored inside ihdr, so you just need to get `ihdr`.

```
open capture.png | from-binary png | get ihdr
```

So it will output the following:
```
╭────────────────────┬───────────────────╮
│ width              │ 1470              │
│ height             │ 728               │
│ bit_depth          │ 8                 │
│ color_type         │ {record 0 fields} │
│ compression_method │ 0                 │
│ filter_method      │ 0                 │
│ interlace_method   │ 0                 │
╰────────────────────┴───────────────────╯
```

## Note
The `kaitaistruct.py` is just a copy of [kaitai struct python runtime](https://github.com/kaitai-io/kaitai_struct_python_runtime), put it directly here, so we don't need extra requirements.  DON'T CHANGE IT.
And `reader/*.py` are just a copy of auto-generated parser, DON'T CHANGE IT.

## For more references
- [Nushell plugin system](https://www.nushell.sh/book/plugins.html)
- [kaitai struct](https://kaitai.io/)
