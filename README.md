# atomode-docs

Documentation site for [atomode](https://github.com/ophusgroup/atomode), built
with [MyST](https://mystmd.org) and deployed to GitHub Pages at
<https://ophusgroup.github.io/atomode-docs>.

## Local preview

Requires [Node.js](https://nodejs.org) (for the MyST CLI):

```bash
npm install -g mystmd
myst start          # live preview at http://localhost:3000
```

Build the static site:

```bash
myst build          # download the theme
python3 scripts/patch_theme.py   # expand top-level TOC sections
myst build --html   # output in _build/html
```

## Deploy

Pushes to `main` are built and deployed by
[`.github/workflows/deploy.yml`](.github/workflows/deploy.yml). Enable it once
under **Settings → Pages → Source: GitHub Actions**.

## Structure

- `myst.yml` — site config and table of contents
- `index.md`, `get-started/`, `user-guide/`, `reference/` — content
- `style.css` — theme customization (shared with the quantEM docs theme)
- `scripts/patch_theme.py` — post-build theme patch
