# /ship

Pre-deployment gate. Run every check. Any failure stops the deploy — do not ship past a red item and note it for later.

## Blocking content checks

1. No placeholder strings remain anywhere. Grep for `REPLACE-WITH-REAL-NUMBER`, `TODO`, `FIXME`, `Lorem`, `placeholder`.
2. Control Room numbers are real and produce a working `tel:` link.
3. `meta.version` bumped and `meta.updated` set to today.
4. Parity check passes for all nine posts.
5. Confirm with the human that the Hindi has been signed off by the issuing officer. This is a human confirmation, not something you can verify. If it has not happened, stop here.

## Blocking technical checks

6. `/verify-offline` passes in full, including the version-invalidation step.
7. Gzipped HTML + CSS + JS under 100KB, fonts excluded. State the measured number.
8. Lighthouse mobile: Performance, Accessibility, and Best Practices each ≥ 95. Attach the report.
9. `noindex` meta tag present and `robots.txt` disallow in place, unless the human has explicitly reversed this policy in writing.
10. No external requests in the network panel. No CDN, no font host, no analytics.
11. Site works with JavaScript disabled on the home page and all nine post pages.

## QR codes

12. Generate ten QR codes into `qr/`, filenames matching route slugs plus `home`. SVG format.
13. Point them at the dynamic short URLs, not the raw hosting URL, so the destination can be repointed without reprinting physical cards.
14. Scan-test each generated code with a real phone camera before handing them to print. A code that resolves in a decoder library but not in a phone camera app is a failed code.
15. Include the plain URL as small text beneath each code in the print artwork, as a fallback for phones that will not scan.

## Handover

16. Confirm `README.md` covers editing content, bumping the version, redeploying, and regenerating QR codes accurately against what was actually built.
17. Write a Serena memory recording the deployed version, the hosting target, and any decision made during ship that a future session would need.
