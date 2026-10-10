# Contributing

Thanks for taking a look at **fermentation-shorts**. This repository is
primarily a personal content-production workspace for a faceless YouTube
channel about home fermentation, so it is not an open-source project looking
for broad contributions — but suggestions, fixes and issue reports are
welcome.

## Before you open a pull request

1. **Read [`README.md`](README.md)** — especially the "Before delivering any
   animated file" section. It documents the two bugs that keep coming back
   (`transform=` overriding an animation, and `transform-origin` keyword
   values) and the exact checks that catch them.
2. **Run the validator on anything you touch:**

   ```bash
   python _validar-short.py                                  # the whole project
   python _validar-short.py alho/shorts-garlic-honey-en.html  # a single file
   ```

   It must print `TOTAL DE PROBLEMAS: 0` for the file you changed. The two
   files under `video-longo/` are a known false positive (they are a 16:9
   player, not a 405×720 short, and their CSS variables such as `#cap` are
   read as suspicious hex colours).
3. **Look at the result — do not trust a grep.** Layout, colour and shape are
   invisible to text search:

   ```bash
   python _revisar-cenas.py <file>.html --final     # contact sheet of every scene
   python _captura-upload.py <file>.html --cenas 0,6  # real 1080x1920 frames
   ```

   `--final` freezes each animation at its last frame. Without it the sheet is
   rendered at `t=0` and every element using `animation-fill-mode: both` looks
   invisible.

## Editing rules for this repository

- **One edit per message, per file.** Two edits to the same file in the same
  batch are applied against the same snapshot and the second silently wins.
  Either make one edit at a time, or put every replacement in a Python script
  that asserts each anchor was found (`assert text.count(old) == 1`) and
  aborts without writing if one is missing.
- **Anchor block replacements on the separator, not on the next `def`.** These
  files carry comments between scenes, so a lookahead like `(?=\n\ndef x)`
  never matches.
- **Never rewrite line endings.** The generators detect the end-of-line
  character of each anchor; `.gitattributes` therefore stores files with
  `-text` so git never converts them.
- **Do not commit `.mp4` files.** They are regenerable and gitignored.

## Commit messages

Short, imperative, one line where possible:

```
Fix transform= bug in 3 beetroot scenes
Add beet kvass short (#28)
```

## Reporting a problem

Open an issue using the templates in `.github/ISSUE_TEMPLATE/`. If it is about
a rendered short, please say **which file** and, if you can, attach the
contact sheet produced by `_revisar-cenas.py`.
