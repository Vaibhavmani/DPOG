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

    if (document.body) {
      document.body.classList.add('lang-transitioning');
    }

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

    // Update all language toggle button labels & ARIA states
    var toggleBtns = document.querySelectorAll('.lang-toggle-btn');
    toggleBtns.forEach(function (btn) {
      var btnLang = btn.getAttribute('data-lang');
      if (btnLang) {
        btn.classList.toggle('active-lang', btnLang === lang);
        btn.setAttribute('aria-pressed', btnLang === lang ? 'true' : 'false');
      } else {
        btn.setAttribute('aria-pressed', lang === 'hi' ? 'true' : 'false');
      }

      var enSpan = btn.querySelector('.lang-label-en');
      var hiSpan = btn.querySelector('.lang-label-hi');
      if (enSpan && hiSpan) {
        if (lang === 'hi') {
          enSpan.style.color = 'var(--white)';
          enSpan.style.textDecoration = 'none';
          hiSpan.style.color = 'var(--alert-yellow)';
          hiSpan.style.textDecoration = 'underline';
        } else {
          enSpan.style.color = 'var(--alert-yellow)';
          enSpan.style.textDecoration = 'underline';
          hiSpan.style.color = 'var(--white)';
          hiSpan.style.textDecoration = 'none';
        }
      }
    });

    // Update inline language switch buttons
    var inlineBtns = document.querySelectorAll('.inline-switch-btn');
    inlineBtns.forEach(function (btn) {
      if (lang === 'hi') {
        btn.textContent = 'Show in English';
      } else {
        btn.textContent = 'Show in हिंदी';
      }
    });

    // Dispatch custom event for search or other modules
    window.dispatchEvent(new CustomEvent('dp-lang-changed', { detail: { lang: lang } }));

    if (window.requestAnimationFrame) {
      window.requestAnimationFrame(function () {
        setTimeout(function () {
          if (document.body) {
            document.body.classList.remove('lang-transitioning');
          }
        }, 180);
      });
    }
  }

  function toggleLanguage() {
    var currentLang = document.documentElement.getAttribute('lang') || 'en';
    var newLang = currentLang === 'hi' ? 'en' : 'hi';

    var docElem = document.documentElement;
    var maxScroll = Math.max(1, docElem.scrollHeight - window.innerHeight);
    var scrollRatio = window.scrollY / maxScroll;

    setLanguage(newLang, true);

    if (window.requestAnimationFrame) {
      window.requestAnimationFrame(function () {
        var newMaxScroll = docElem.scrollHeight - window.innerHeight;
        var targetY = Math.round(scrollRatio * newMaxScroll);
        window.scrollTo({ top: targetY, behavior: 'instant' });
      });
    }
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
