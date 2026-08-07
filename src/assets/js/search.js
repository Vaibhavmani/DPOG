/**
 * Substring Search Engine for Law & Order Deployment Quick Instructions
 * Performs fast case-insensitive substring search across English & Hindi text simultaneously.
 */

(function () {
  'use strict';

  var contentData = null;

  function loadContentData(callback) {
    if (contentData) {
      if (callback) callback(contentData);
      return;
    }

    fetch('/content/content.json')
      .then(function (res) {
        return res.json();
      })
      .then(function (data) {
        contentData = data;
        if (callback) callback(contentData);
      })
      .catch(function (err) {
        console.error('Error loading content.json for search:', err);
      });
  }

  function escapeRegExp(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }

  function highlightText(text, query) {
    if (!query) return text;
    var regex = new RegExp('(' + escapeRegExp(query) + ')', 'gi');
    return text.replace(regex, '<mark class="search-highlight">$1</mark>');
  }

  function search(query) {
    if (!query || !contentData || !contentData.posts) return [];

    var trimmed = query.trim().toLowerCase();
    if (trimmed.length < 2) return [];

    var results = [];

    contentData.posts.forEach(function (post) {
      var matches = [];

      // Check English & Hindi Names
      if (post.en.name.toLowerCase().includes(trimmed)) {
        matches.push({ type: 'name', lang: 'en', text: post.en.name });
      }
      if (post.hi.name.toLowerCase().includes(trimmed)) {
        matches.push({ type: 'name', lang: 'hi', text: post.hi.name });
      }

      // Check Key Directives
      post.en.keyDirectives.forEach(function (kd) {
        if (kd.toLowerCase().includes(trimmed)) {
          matches.push({ type: 'directive', lang: 'en', text: kd });
        }
      });
      post.hi.keyDirectives.forEach(function (kd) {
        if (kd.toLowerCase().includes(trimmed)) {
          matches.push({ type: 'directive', lang: 'hi', text: kd });
        }
      });

      // Check Full Instructions
      post.en.instructions.forEach(function (inst, idx) {
        if (inst.toLowerCase().includes(trimmed)) {
          matches.push({ type: 'instruction', lang: 'en', index: idx + 1, text: inst });
        }
      });
      post.hi.instructions.forEach(function (inst, idx) {
        if (inst.toLowerCase().includes(trimmed)) {
          matches.push({ type: 'instruction', lang: 'hi', index: idx + 1, text: inst });
        }
      });

      if (matches.length > 0) {
        results.push({
          post: post,
          matches: matches
        });
      }
    });

    return results;
  }

  function renderSearchResults(results, query, container) {
    if (!container) return;

    if (!query || query.trim().length < 2) {
      container.innerHTML = '<p style="text-align:center; padding: 20px; font-weight: 600;">Type at least 2 characters to search instructions...</p>';
      return;
    }

    if (results.length === 0) {
      container.innerHTML = '<p style="text-align:center; padding: 20px; font-weight: 600;">No matching instructions found for "' + escapeHtml(query) + '".</p>';
      return;
    }

    var currentLang = window.DPLang ? window.DPLang.get() : 'en';
    var html = '<div class="search-results-list">';

    results.forEach(function (item) {
      var post = item.post;
      var postTitle = currentLang === 'hi' ? post.hi.name : post.en.name;
      var postUrl = '/' + post.slug + '/?lang=' + currentLang;

      html += '<div class="search-result-card">';
      html += '<a href="' + postUrl + '" class="search-result-title-link" style="text-decoration:none;">';
      html += '<h3 class="search-result-title">' + highlightText(escapeHtml(postTitle), query) + '</h3>';;
      html += '</a>';

      html += '<ul style="list-style:none; display:flex; flex-direction:column; gap:8px;">';
      item.matches.forEach(function (match) {
        var matchPrefix = match.type === 'instruction' ? ('Line ' + match.index + ': ') : '';
        html += '<li class="search-match-text">';
        html += '<strong style="color:var(--navy-deep);">' + matchPrefix + '</strong>';
        html += highlightText(escapeHtml(match.text), query);
        html += '</li>';
      });
      html += '</ul>';
      html += '</div>';
    });

    html += '</div>';
    container.innerHTML = html;
  }

  function escapeHtml(str) {
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  document.addEventListener('DOMContentLoaded', function () {
    var searchInput = document.getElementById('search-input');
    var resultsContainer = document.getElementById('search-results');

    if (searchInput && resultsContainer) {
      loadContentData(function () {
        function triggerSearch() {
          var query = searchInput.value;
          var results = search(query);
          renderSearchResults(results, query, resultsContainer);
        }

        searchInput.addEventListener('input', triggerSearch);

        // Check if initial query in URL parameter e.g. /search/?q=drone
        var urlParams = new URLSearchParams(window.location.search);
        var qParam = urlParams.get('q');
        if (qParam) {
          searchInput.value = qParam;
          triggerSearch();
        }
      });
    }
  });

  window.DPSearch = {
    search: search,
    load: loadContentData
  };

})();
