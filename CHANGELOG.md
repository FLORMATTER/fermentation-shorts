# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Repository scaffolding: `README.md` (English) and `README.pt-BR.md`,
  `LICENSE`, `.gitignore`, `.gitattributes`, `.editorconfig`, `requirements.txt`,
  `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md` and GitHub issue/PR
  templates.
- CI workflow that validates every animated short with `_validar-short.py`.

### Changed

- Manual `*.antes*` backups moved out of the working folders into
  `_arquivo/backups/` and excluded from version control.
- Rendered `.mp4` files (~288 MB) excluded from version control — they are
  regenerable with `_gerar-mp4.js`.

## [0.1.0] - 2026-10-09

### Added

- 28 catalogued video entries (27 Shorts + 1 long-form), all rendered.
- Animated HTML+SVG sources for every entry, in English (`-en`) and Portuguese.
- `galeria-shorts.html` — a clickable gallery of every short.
- Production guides in `guias/`: recording, editing, upload, the 18-week
  posting plan, titles/descriptions/hashtags, and on-screen text.
- Cover images (`capas-canva/`) with an OpenCV pipeline that removes the
  burned-in Portuguese text and rebuilds the background.
- `_validar-short.py` — checks animations, keyframes, orphan `url(#id)`
  references, suspicious hex colours and the `transform=` / `transform-origin`
  bugs.
- `_revisar-cenas.py`, `_zoom-cena.py`, `_captura-upload.py` — render contact
  sheets so layout can actually be *looked at*.
- `_gerar-mp4.js` — renders a short to a constant-frame-rate 1080×1920 `.mp4`
  using a headless Chrome.
- `aulas/` — four introductory lessons on HTML, CSS, animations and the scene
  JavaScript.

[Unreleased]: https://github.com/FLORMATTER/fermentation-shorts/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/FLORMATTER/fermentation-shorts/releases/tag/v0.1.0
