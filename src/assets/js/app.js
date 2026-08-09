/**
 * Application Core Bootstrapper & PWA / Offline Controller
 */

(function () {
  'use strict';

  // 1. Register Service Worker for Offline PWA Support & Force Refresh
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', function () {
      navigator.serviceWorker.register('/sw.js', { scope: '/' })
        .then(function (reg) {
          console.log('Service Worker registered cleanly with scope:', reg.scope);
          reg.update(); // Check for SW updates on every load
        })
        .catch(function (err) {
          console.warn('Service Worker registration failed:', err);
        });
    });
  }

  // 2. Offline Status Indicator Banner
  function updateOnlineStatus() {
    var banner = document.getElementById('offline-banner');
    if (!banner) return;

    if (!navigator.onLine) {
      banner.classList.add('active');
    } else {
      banner.classList.remove('active');
    }
  }

  window.addEventListener('online', updateOnlineStatus);
  window.addEventListener('offline', updateOnlineStatus);

  // 3. Global Copy & Share Helpers for QR Modal
  window.copyPageURL = function (btn) {
    var url = window.location.href;
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(url).then(function () {
        showCopyFeedback(btn);
      });
    } else {
      var input = document.createElement('input');
      input.value = url;
      document.body.appendChild(input);
      input.select();
      document.execCommand('copy');
      document.body.removeChild(input);
      showCopyFeedback(btn);
    }
  };

  function showCopyFeedback(btn) {
    if (!btn) return;
    var originalText = btn.innerHTML;
    btn.innerHTML = '✓ Copied!';
    btn.style.backgroundColor = '#E8F5E9';
    btn.style.borderColor = '#2E7D32';
    btn.style.color = '#2E7D32';
    setTimeout(function () {
      btn.innerHTML = originalText;
      btn.style.backgroundColor = '';
      btn.style.borderColor = '';
      btn.style.color = '';
    }, 2000);
  }

  window.shareWebsite = function () {
    var shareData = {
      title: 'Delhi Police - Duty Instructions',
      text: 'Scan or open quick duty instructions portal.',
      url: window.location.href
    };
    if (navigator.share) {
      navigator.share(shareData).catch(function () {});
    } else {
      window.copyPageURL(document.querySelector('.qr-copy-url-btn'));
    }
  };

  window.handleQRError = function (imgEl, url) {
    if (!imgEl || imgEl.dataset.handled) return;
    imgEl.dataset.handled = "true";
    fetch(url)
      .then(function (res) { return res.text(); })
      .then(function (svgText) {
        if (svgText && svgText.indexOf('<svg') !== -1) {
          var container = imgEl.parentElement;
          if (container) {
            container.innerHTML = svgText;
          }
        }
      })
      .catch(function (err) {
        console.warn('QR SVG fetch fallback failed:', err);
      });
  };

  // 4. QR Code Modal Viewer & Event Delegation
  function initQRModal() {
    document.addEventListener('click', function (e) {
      var qrBtn = e.target.closest('.qr-view-btn');
      if (qrBtn) {
        e.preventDefault();
        var targetModalId = qrBtn.getAttribute('data-target-modal');
        var modal = document.getElementById(targetModalId || 'qr-modal');
        if (modal) {
          modal.classList.add('active');
        }
      }

      var closeBtn = e.target.closest('.qr-modal-close-btn') || e.target.closest('.qr-modal-overlay');
      if (closeBtn && (e.target.classList.contains('qr-modal-overlay') || e.target.closest('.qr-modal-close-btn'))) {
        var activeModals = document.querySelectorAll('.qr-modal-overlay.active');
        activeModals.forEach(function (m) {
          m.classList.remove('active');
        });
      }

      var printBtn = e.target.closest('.qr-print-btn');
      if (printBtn) {
        activeModals.forEach(function (m) {
          m.classList.remove('active');
        });
      }
    });
  }

  // 5. Restrict DevTools & Inspect Element (Security Hardening)
  document.addEventListener('contextmenu', function (e) {
    e.preventDefault();
  });

  document.addEventListener('keydown', function (e) {
    // Block F12
    if (e.key === 'F12' || e.keyCode === 123) {
      e.preventDefault();
    }
    // Block Ctrl+Shift+I, Ctrl+Shift+J, Ctrl+Shift+C, Ctrl+U
    if (e.ctrlKey && (
      (e.shiftKey && (e.key === 'I' || e.key === 'i' || e.key === 'J' || e.key === 'j' || e.key === 'C' || e.key === 'c')) ||
      (e.key === 'U' || e.key === 'u')
    )) {
      e.preventDefault();
    }
  });

  // Initial check on DOM Ready & Immediate fallback
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
      updateOnlineStatus();
      initQRModal();
    });
  } else {
    updateOnlineStatus();
    initQRModal();
  }

})();
