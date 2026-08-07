# suggested_commands

Fill in the exact invocations once the build exists. The shapes below are what this project needs; do not invent flags that were never run.

## Serve locally

Service workers require HTTPS or `localhost`. A file:// open will silently skip service worker registration and make offline testing meaningless.

```
python3 -m http.server 8000 --directory src
# then http://localhost:8000
```

## Content checks

```
# EN/HI instruction parity across all nine posts — the most likely content bug
python3 -c "import json;d=json.load(open('content/content.json'));[print(p['id'], len(p['en']['instructions'])==len(p['hi']['instructions'])) for p in d['posts']]"

# placeholders that must not reach production
grep -rn "REPLACE-WITH-REAL-NUMBER\|TODO\|FIXME" content/ src/
```

## Payload measurement

Measure, do not estimate. Every Walkthrough that changes shipped assets states the real number.

```
find src -name "*.html" -o -name "*.css" -o -name "*.js" | xargs gzip -c | wc -c
```

## Serena

```
serena project index          # once, after the source tree exists
serena memories check         # referential integrity of mem: references
serena memories list
```

## Offline verification

Not a command — a procedure. Run the `/verify-offline` workflow in `.agents/workflows/`. The step that actually catches bugs is the last one: change `meta.version`, rebuild, and confirm an existing install picks it up rather than serving stale instructions.
