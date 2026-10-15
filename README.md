# fellow-survivor-studio.github.io

Organization root site for Fellow Survivor Studio on GitHub Pages
(https://fellow-survivor-studio.github.io/).

- `app-ads.txt` — authorized ad sellers for our apps. AdMob and other ad
  buyers look for it at the root of the developer website listed in Google
  Play, so it has to live here, not under a project site.
- `index.html` — the Korean studio homepage, with an introduction, projects,
  and contact details. Visitors stay on the homepage; there is no redirect.
- `styles.css`, `favicon.svg` — responsive styling and the studio mark.
- `googleabe82689611d6157.html` — Google Search Console verification.
- `.nojekyll` — serves the static files without Jekyll processing.

## Preview and publish

No build step, package install, external fonts, or JavaScript is required.
Run a local static server from the repository root:

```sh
python -m http.server 8765 --bind 127.0.0.1
```

Open http://127.0.0.1:8765. Check both desktop and mobile widths before publishing.

GitHub Pages uses **Deploy from a branch → main → / (root)**. Push the static
files to `main` and wait for the **pages build and deployment** workflow to
finish. The public homepage is https://fellow-survivor-studio.github.io/.

## Content and related sites

Edit company and project copy in `index.html`. Contact and business details
match the existing public Reel Nest policy. Keep project availability labels
up to date; the 환생천마 project is currently identified as preparing for launch.

These separate project sites remain independent of this repository:

- Reel Nest privacy policy: `/reel-nest/`
- Reel Nest terms: `/reel-nest/terms/`
- 환생천마 policies and customer support: `/heavenlydemonreborn/`
- Paper Markdown for Windows:
  https://github.com/fellow-survivor-studio/paper-markdown-for-windows

Keep `app-ads.txt` and the Google verification file at the root when updating
the homepage.
