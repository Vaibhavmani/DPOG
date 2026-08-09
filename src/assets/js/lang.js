/**
 * Language State Manager for Law & Order Deployment Quick Instructions
 * Supports instant bilingual (EN / HI) toggling, URL query parameters, and localStorage persistence.
 */

(function () {
  'use strict';

  var STORAGE_KEY = 'dp_lang';
  
  function getInitialLanguage() {
    // 1. Check URL query string e.g. ?lang=hi
    var urlParams = new URLSearchParams(window.location.search);
    var langParam = urlParams.get('lang');
    if (langParam === 'hi' || langParam === 'en') {
      return langParam;
    }
    
    // 2. Check localStorage
    try {
      var savedLang = localStorage.getItem(STORAGE_KEY);
      if (savedLang === 'hi' || savedLang === 'en') {
        return savedLang;
      }
    } catch (e) {
      console.warn('localStorage disabled or unavailable:', e);
    }
    
    // 3. Default to English
    return 'en';
  }

  function setLanguage(lang, updateUrl) {
    if (lang !== 'en' && lang !== 'hi') lang = 'en';

    // 1. Immediately update toggle button highlights synchronously for zero latency feedback
    var toggleBtns = document.querySelectorAll('.lang-toggle-btn');
    toggleBtns.forEach(function (btn) {
      var btnLang = btn.getAttribute('data-lang');
      if (btnLang) {
        btn.classList.toggle('active-lang', btnLang === lang);
        btn.setAttribute('aria-pressed', btnLang === lang ? 'true' : 'false');
      }
    });

    var currentLang = document.documentElement.getAttribute('lang');
    if (currentLang === lang && document.body && !document.body.classList.contains('lang-transitioning')) {
      return;
    }

    // 2. Start smooth content crossfade
    if (document.body) {
      document.body.classList.add('lang-transitioning');
    }

    setTimeout(function () {
      // Update document root lang attribute
      document.documentElement.setAttribute('lang', lang);

      // Save to localStorage
      try {
        localStorage.setItem(STORAGE_KEY, lang);
      } catch (e) {
        // Ignore fallback
      }

      // Update URL query parameter without full reload if supported
      if (updateUrl && window.history && window.history.replaceState) {
        var currentUrl = new URL(window.location.href);
        currentUrl.searchParams.set('lang', lang);
        window.history.replaceState({}, '', currentUrl.toString());
      }

      // Dispatch custom event for search or other modules
      window.dispatchEvent(new CustomEvent('dp-lang-changed', { detail: { lang: lang } }));

      setTimeout(function () {
        if (document.body) {
          document.body.classList.remove('lang-transitioning');
        }
      }, 40);
    }, 80);
  }

  function toggleLanguage() {
    var currentLang = document.documentElement.getAttribute('lang') || 'en';
    var newLang = currentLang === 'hi' ? 'en' : 'hi';

    setLanguage(newLang, true);
  }

  // Initialize language on DOM ready
  document.addEventListener('DOMContentLoaded', function () {
    var initialLang = getInitialLanguage();
    setLanguage(initialLang, false);

    // Wire masthead language toggle buttons
    document.addEventListener('click', function (e) {
      var toggleBtn = e.target.closest('.lang-toggle-btn') || e.target.closest('.inline-switch-btn');
      if (toggleBtn) {
        e.preventDefault();
        toggleLanguage();
      }
    });
  });

  // Export global helper
  window.DPLang = {
    get: function () {
      return document.documentElement.getAttribute('lang') || 'en';
    },
    set: setLanguage,
    toggle: toggleLanguage
  };

})();
