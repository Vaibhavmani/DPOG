/**
 * Service Worker for Law & Order Deployment Quick Instructions
 * Cache Version 11.0 - Guaranteed Fixed Signal Red Call Control Room Bar & Boosted Hindi Typography
 */

var CACHE_NAME = 'dp-instructions-v26.0';

var STATIC_ASSETS = [

  '/',
  '/index.html',
  '/search/',
  '/search/index.html',
  '/checklist/',
  '/checklist/index.html',
  '/rooftop/',
  '/rooftop/index.html',
  '/morcha/',
  '/morcha/index.html',
  '/machan/',
  '/machan/index.html',
  '/vehicle-checking/',
  '/vehicle-checking/index.html',
  '/dfmd/',
  '/dfmd/index.html',
  '/qrt/',
  '/qrt/index.html',
  '/xray/',
  '/xray/index.html',
  '/cctv/',
  '/cctv/index.html',
  '/medical/',
  '/medical/index.html',
  '/content/content.json',
  '/assets/css/app.css?v=17.0',
  '/assets/css/fonts.css',
  '/assets/js/lang.js',
  '/assets/js/search.js',
  '/assets/js/checklist.js?v=8.0',
  '/assets/js/app.js?v=10.0',
  '/manifest.webmanifest',
  '/qr/home.svg',
  '/qr/rooftop.svg',
  '/qr/morcha.svg',
  '/qr/machan.svg',
  '/qr/vehicle-checking.svg',
  '/qr/dfmd.svg',
  '/qr/qrt.svg',
  '/qr/xray.svg',
  '/qr/cctv.svg',
  '/qr/medical.svg',
  '/assets/icons/building-watch.svg',
  '/assets/icons/barricade.svg',
  '/assets/icons/watchtower.svg',
  '/assets/icons/vehicle-check.svg',
  '/assets/icons/door-frame-detector.svg',
  '/assets/icons/rapid-response.svg',
  '/assets/icons/baggage-scanner.svg',
  '/assets/icons/camera-monitor.svg',
  '/assets/icons/ambulance.svg',
  '/assets/images/dp_logo.png',
  '/assets/images/emblem_watermark.png',
  '/assets/images/cover.jpg',
  '/assets/images/rooftop.jpg',
  '/assets/images/morcha.jpg',
  '/assets/images/machan.jpg',
  '/assets/images/vehicle-checking.jpg',
  '/assets/images/dfmd.jpg',
  '/assets/images/qrt.jpg',
  '/assets/images/xray.jpg',
  '/assets/images/cctv.jpg',
  '/assets/images/medical.jpg'
];

// Install Event - Force skip waiting
self.addEventListener('install', function (event) {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function (cache) {
        console.log('[SW v11.0] Pre-caching offline app shell & updated assets');
        return cache.addAll(STATIC_ASSETS);
      })
      .then(function () {
        return self.skipWaiting();
      })
  );
});

// Activate Event - Purge all old caches & claim clients immediately
self.addEventListener('activate', function (event) {
  event.waitUntil(
    caches.keys().then(function (cacheNames) {
      return Promise.all(
        cacheNames.map(function (cacheName) {
          if (cacheName !== CACHE_NAME) {
            console.log('[SW v11.0] Purging outdated cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    }).then(function () {
      return self.clients.claim();
    })
  );
});

// Fetch Event - Network-First for HTML navigations, Cache-First for static assets
self.addEventListener('fetch', function (event) {
  if (event.request.method !== 'GET') return;

  var requestUrl = new URL(event.request.url);

  // Bypass Service Worker completely for Admin Portal and API endpoints
  if (requestUrl.pathname.startsWith('/dp-c9f7e2') ||
      requestUrl.pathname.startsWith('/admin') ||
      requestUrl.pathname.startsWith('/api/')) {
    return;
  }

  // Network-First strategy for HTML pages

  if (event.request.mode === 'navigate' || requestUrl.pathname.endsWith('.html') || requestUrl.pathname.endsWith('/')) {
    event.respondWith(
      fetch(event.request)
        .then(function (networkResponse) {
          var responseToCache = networkResponse.clone();
          caches.open(CACHE_NAME).then(function (cache) {
            cache.put(event.request, responseToCache);
          });
          return networkResponse;
        })
        .catch(function () {
          return caches.match(event.request).then(function (cachedResponse) {
            return cachedResponse || caches.match('/index.html');
          });
        })
    );
    return;
  }

  // Cache-First for images, fonts, css, js
  event.respondWith(
    caches.match(event.request)
      .then(function (cachedResponse) {
        if (cachedResponse) {
          return cachedResponse;
        }

        return fetch(event.request)
          .then(function (networkResponse) {
            if (!networkResponse || networkResponse.status !== 200 || networkResponse.type !== 'basic') {
              return networkResponse;
            }

            var responseToCache = networkResponse.clone();
            var reqUrl = new URL(event.request.url);
            if (reqUrl.protocol === 'http:' || reqUrl.protocol === 'https:') {
              caches.open(CACHE_NAME).then(function (cache) {
                cache.put(event.request, responseToCache).catch(function () {});
              });
            }

            return networkResponse;
          });
      })
  );
});
