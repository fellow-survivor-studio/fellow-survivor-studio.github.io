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
cat > "$out/_redirects" <<'EOF'
/googleabe82689611d6157.html /googleabe82689611d6157 200
/heavenlydemonreborn /products/heavenlydemonreborn/ 301
/heavenlydemonreborn/* /products/heavenlydemonreborn/:splat 301
EOF

echo "Cloudflare build: $(find "$out" -type f | wc -l) files in $out"
