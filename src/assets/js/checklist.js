/**
 * Duty Shift Compliance Checklist Controller
 * Handles officer shift verification, progress tracking, and localStorage persistence.
 */

(function () {
  'use strict';

  var contentData = null;
  var currentPostSlug = 'rooftop';
  var checkedState = {};

  function loadSavedChecklist() {
    try {
      var saved = localStorage.getItem('dp_checklist_state');
      if (saved) {
        var parsed = JSON.parse(saved);
        currentPostSlug = parsed.slug || 'rooftop';
        checkedState = parsed.checked || {};
        
        var nameInput = document.getElementById('officer-name');
        var rankInput = document.getElementById('officer-rank');
        var badgeInput = document.getElementById('officer-badge');
        if (nameInput && parsed.officerName) nameInput.value = parsed.officerName;
        if (rankInput && parsed.officerRank) rankInput.value = parsed.officerRank;
        if (badgeInput && parsed.officerBadge) badgeInput.value = parsed.officerBadge;
      }
    } catch (e) {
      console.warn('Could not read checklist from localStorage', e);
    }
  }

  function saveChecklistState() {
    try {
      var nameInput = document.getElementById('officer-name');
      var rankInput = document.getElementById('officer-rank');
      var badgeInput = document.getElementById('officer-badge');

      var payload = {
        slug: currentPostSlug,
        officerName: nameInput ? nameInput.value : '',
        officerRank: rankInput ? rankInput.value : '',
        officerBadge: badgeInput ? badgeInput.value : '',
        checked: checkedState,
        timestamp: new Date().toISOString()
      };
      localStorage.setItem('dp_checklist_state', JSON.stringify(payload));
    } catch (e) {
      console.warn('Could not save checklist state', e);
    }
  }

  function fetchContentData() {
    fetch('../content/content.json')
      .then(function (res) { return res.json(); })
      .then(function (data) {
        contentData = data;
        initChecklistUI();
      })
      .catch(function (err) {
        console.error('Failed to load content for checklist:', err);
      });
  }

  function initChecklistUI() {
    if (!contentData || !contentData.posts) return;

    var selectEl = document.getElementById('post-select');
    if (!selectEl) return;

    selectEl.innerHTML = '';
    contentData.posts.forEach(function (post) {
      var opt = document.createElement('option');
      opt.value = post.slug;
      opt.textContent = post.en.name + ' / ' + post.hi.name;
      if (post.slug === currentPostSlug) opt.selected = true;
      selectEl.appendChild(opt);
    });

    selectEl.addEventListener('change', function () {
      currentPostSlug = this.value;
      checkedState = {};
      renderChecklistItems();
      saveChecklistState();
    });

    renderChecklistItems();

    // Attach listeners to input fields
    ['officer-name', 'officer-rank', 'officer-badge'].forEach(function (id) {
      var el = document.getElementById(id);
      if (el) {
        el.addEventListener('input', saveChecklistState);
      }
    });
  }

  function renderChecklistItems() {
    var container = document.getElementById('checklist-items-container');
    if (!container || !contentData) return;

    var post = contentData.posts.find(function (p) { return p.slug === currentPostSlug; });
    if (!post) return;

    var html = '';
    var totalCount = post.en.instructions.length;
    var completedCount = 0;

    post.en.instructions.forEach(function (instEn, idx) {
      var instHi = post.hi.instructions[idx] || '';
      var itemKey = currentPostSlug + '_' + idx;
      var isChecked = !!checkedState[itemKey];

      if (isChecked) completedCount++;

      html += '<div class="checklist-item-card ' + (isChecked ? 'completed' : '') + '">';
      html += '  <label class="checklist-checkbox-label">';
      html += '    <input type="checkbox" class="checklist-checkbox" data-key="' + itemKey + '" ' + (isChecked ? 'checked' : '') + '>';
      html += '    <span class="custom-checkbox-box"></span>';
      html += '    <div class="checklist-item-text">';
      html += '      <div class="checklist-item-num">DIRECTIVE ' + (idx + 1 < 10 ? '0' + (idx + 1) : (idx + 1)) + '</div>';
      html += '      <div class="lang-en">' + escapeHtml(instEn) + '</div>';
      html += '      <div class="lang-hi">' + escapeHtml(instHi) + '</div>';
      html += '    </div>';
      html += '  </label>';
      html += '</div>';
    });

    container.innerHTML = html;

    // Update Progress Bar
    var percent = totalCount > 0 ? Math.round((completedCount / totalCount) * 100) : 0;
    var barFill = document.getElementById('progress-bar-fill');
    var progressText = document.getElementById('progress-text-val');
    var badgeStatus = document.getElementById('checklist-status-badge');

    if (barFill) barFill.style.width = percent + '%';
    if (progressText) progressText.textContent = completedCount + ' / ' + totalCount + ' Verified (' + percent + '%)';
    if (badgeStatus) {
      if (percent === 100) {
        badgeStatus.textContent = '✓ SHIFT FULLY COMPLIANT';
        badgeStatus.className = 'status-badge-complete';
      } else {
        badgeStatus.textContent = 'IN PROGRESS (' + percent + '%)';
        badgeStatus.className = 'status-badge-pending';
      }
    }

    // Attach checkbox listeners
    var checkboxes = container.querySelectorAll('.checklist-checkbox');
    checkboxes.forEach(function (cb) {
      cb.addEventListener('change', function () {
        var key = this.getAttribute('data-key');
        checkedState[key] = this.checked;
        saveChecklistState();
        renderChecklistItems();
      });
    });
  }

  // Reset checklist handler
  window.resetChecklist = function () {
    if (confirm('Are you sure you want to reset all verified items for this shift?')) {
      checkedState = {};
      saveChecklistState();
      renderChecklistItems();
    }
  };

  // Utility: HTML-escape a string before injecting into innerHTML
  function escapeHtml(str) {
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  document.addEventListener('DOMContentLoaded', function () {
    loadSavedChecklist();
    fetchContentData();
  });

})();
