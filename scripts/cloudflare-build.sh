#!/bin/sh
# Cloudflare Workers build for https://fellowsurvivor.com/
# Copies the tracked files that GitHub Pages publishes into .cf-dist/, leaving out
# repository tooling. wrangler.jsonc runs this before every deploy.
# Needs git and GNU cp (Cloudflare's Linux build image has both).
set -eu
cd "$(dirname "$0")/.."

out=.cf-dist
rm -rf "$out"
mkdir -p "$out"

git ls-files -z -- . \
  ':!README.md' ':!docs/' ':!scripts/' ':!sources/' ':!.github/' ':!.gitignore' ':!.gitattributes' ':!wrangler.jsonc' \
  | xargs -0 cp --parents -t "$out"

# Cloudflare _redirects rules (the file itself is not served).
# - GitHub Pages serves the Search Console file at its .html address; without the first
#   rule Cloudflare would redirect it to the address without .html.
# - Product policy pages live under /products/<product>/. Keep forwarding every earlier
#   address permanently: apps, store listings and github.io links may still point at it.
#   Only the first matching rule applies, so specific rules come before broad ones.
# - Reel Nest (moved 2026-11-06 from the reel-nest repository): the privacy policy was at
#   /reel-nest/ itself (app versions before 1.3.0 link there), the terms at /reel-nest/terms/,
#   previous privacy versions at /reel-nest/archive/<date>/, a product page at /reel-nest/home/,
#   and a copy of the build in /reel-nest/dist/.
cat > "$out/_redirects" <<'EOF'
/googleabe82689611d6157.html /googleabe82689611d6157 200
/heavenlydemonreborn /products/heavenlydemonreborn/ 301
/heavenlydemonreborn/* /products/heavenlydemonreborn/:splat 301
/reel-nest /products/reel-nest/privacy/ 301
/reel-nest/sitemap.xml /products/reel-nest/sitemap.xml 301
/reel-nest/home /products/reel-nest/ 301
/reel-nest/home/* /products/reel-nest/ 301
/reel-nest/terms /products/reel-nest/terms/ 301
/reel-nest/terms/* /products/reel-nest/terms/:splat 301
/reel-nest/archive/* /products/reel-nest/privacy/archive/:splat 301
/reel-nest/dist /products/reel-nest/privacy/ 301
/reel-nest/dist/terms/* /products/reel-nest/terms/:splat 301
/reel-nest/dist/archive/* /products/reel-nest/privacy/archive/:splat 301
/reel-nest/dist/* /products/reel-nest/privacy/:splat 301
/reel-nest/* /products/reel-nest/privacy/:splat 301
EOF

echo "Cloudflare build: $(find "$out" -type f | wc -l) files in $out"
