# /verify-offline

The offline path is the one most likely to be quietly broken and the one that matters most in the field. Never report a task complete on the strength of an online check alone.

1. Build and serve the site locally over HTTPS or `localhost` — service workers do not register otherwise.
2. Using the browser subagent, load the home page fresh with an empty cache. Confirm the service worker registers and reaches the activated state.
3. Navigate to all nine post routes in English. Then switch to Hindi and navigate all nine again. This populates the cache the way a real first visit does.
4. Go offline: set the browser to offline mode, or stop the local server entirely. Stopping the server is the stronger test — browser offline mode sometimes still serves from the HTTP cache rather than the service worker.
5. Hard-navigate (not just client-side route) to each of the ten routes. Every one must render fully: title band, key directives, complete instruction list, version stamp.
6. Toggle language while offline. Both directions. The Devanagari must render in the real font, not a fallback — check a conjunct-heavy line such as any string containing "क्षेत्र" or "सुनिश्चित", and compare against the online screenshot.
7. Confirm the offline indicator appears and shows the cached content's version stamp.
8. Confirm the Control Room button still produces a `tel:` action offline.
9. Restart the browser entirely and reload while still offline. This catches caches that only survive in memory.
10. Change `meta.version` in `content.json`, rebuild, and confirm an existing install picks up the new version rather than serving stale instructions. A cache that never invalidates is worse than no cache.

Record every step's result in the Walkthrough, with screenshots for steps 5, 6, and 10. "Offline works" without the version-invalidation check in step 10 is an incomplete result.
