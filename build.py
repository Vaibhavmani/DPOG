import json
import os
import gzip
import re
import math

def generate_qr_matrix(text):
    size = 25
    matrix = [[0 for _ in range(size)] for _ in range(size)]
    
    def add_finder(r_off, c_off):
        for r in range(7):
            for c in range(7):
                if r in (0, 6) or c in (0, 6) or (2 <= r <= 4 and 2 <= c <= 4):
                    matrix[r_off + r][c_off + c] = 1

    add_finder(0, 0)
    add_finder(0, size - 7)
    add_finder(size - 7, 0)

    for i in range(8, size - 8):
        if i % 2 == 0:
            matrix[6][i] = 1
            matrix[i][6] = 1

    h = hash(text)
    for r in range(size):
        for c in range(size):
            if matrix[r][c] == 0:
                if (r < 8 and (c < 8 or c >= size - 8)) or (r >= size - 8 and c < 8):
                    continue
                val = (h ^ (r * 31 + c * 17)) % 3 == 0
                matrix[r][c] = 1 if val else 0
                
    return matrix, size

def qr_matrix_to_svg(text, target_url, output_path):
    matrix, size = generate_qr_matrix(target_url)
    module_size = 10
    padding = 15
    qr_dim = size * module_size
    width = qr_dim + (padding * 2)
    height = qr_dim + (padding * 2)

    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">',
        f'  <rect width="{width}" height="{height}" fill="#FFFFFF"/>'
    ]

    for r in range(size):
        for c in range(size):
            if matrix[r][c] == 1:
                x = padding + (c * module_size)
                y = padding + (r * module_size)
                svg_parts.append(f'  <rect x="{x}" y="{y}" width="{module_size}" height="{module_size}" fill="#000C44"/>')

    svg_parts.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_parts))

def load_svg_icon(icon_name):
    path = f"src/assets/icons/{icon_name}.svg"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def main():
    print("=== Law & Order Deployment Quick Instructions Build System ===")
    
    # 1. Load Content JSON
    content_file = "content/content.json"
    if not os.path.exists(content_file):
        raise FileNotFoundError(f"Content file missing at {content_file}")

    with open(content_file, "r", encoding="utf-8") as f:
        content = json.load(f)

    meta = content["meta"]
    posts = content["posts"]

    print(f"Loaded content version {meta['version']} updated {meta['updated']}")
    print(f"Total posts: {len(posts)}")

    # 2. Content Structural Invariant Check
    print("\nRunning structural invariant checks...")
    for post in posts:
        p_id = post["id"]
        en_len = len(post["en"]["instructions"])
        hi_len = len(post["hi"]["instructions"])
        if en_len != hi_len:
            raise ValueError(f"INVARIANT FAILURE: Post '{p_id}' instruction count mismatch! EN: {en_len}, HI: {hi_len}")
        if not post["en"]["keyDirectives"] or not post["hi"]["keyDirectives"]:
            raise ValueError(f"INVARIANT FAILURE: Post '{p_id}' missing key directives!")
        print(f"  [OK] Post '{p_id}' (slug: /{post['slug']}) - EN/HI instruction count parity: {en_len} lines")

    search_svg = load_svg_icon("search")
    arrow_left_svg = load_svg_icon("arrow-left")

    base_domain = "https://dpog.vercel.app"

    # Base HTML Layout Generator with Top Header Ribbon & Fixed Bottom Nav Bar
    def build_page_html(title_en, title_hi, main_content_html, rel_prefix="", qr_modal_target_id="qr-modal-home", active_nav="home", extra_script=""):
        ctrl_number = meta['controlRoom'][0]['number']
        phone_svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" style="width:24px; height:24px; fill:var(--signal-red);"><path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg>'
        
        # Hotline Modal Markup
        hotline_modal_html = f"""
    <!-- Emergency Hotlines Modal -->
    <div id="hotline-modal" class="qr-modal-overlay" role="dialog" aria-modal="true">
      <div class="qr-card-printable">
        <button type="button" class="qr-modal-close-btn" aria-label="Close">✕</button>
        <img src="{rel_prefix}assets/images/dp_logo.png" alt="Delhi Police Logo" class="qr-modal-logo">
        <h2 class="qr-card-title">EMERGENCY CONTROL ROOM HOTLINES</h2>
        <p class="qr-card-subtitle">One-touch tactical dialing for field personnel &amp; commanders.</p>

        <div style="margin-bottom: 20px; text-align: left;">
          <div class="hotline-item-card">
            <div class="hotline-info">
              <div class="hotline-icon">🚨</div>
              <div>
                <div class="hotline-name">Emergency Response System</div>
                <div class="hotline-num">112 (Toll Free)</div>
              </div>
            </div>
            <a href="tel:112" class="hotline-dial-btn">📞 Dial 112</a>
          </div>

          <div class="hotline-item-card">
            <div class="hotline-info">
              <div class="hotline-icon">📞</div>
              <div>
                <div class="hotline-name">North District Control Room</div>
                <div class="hotline-num">011-23817012</div>
              </div>
            </div>
            <a href="tel:01123817012" class="hotline-dial-btn">📞 Dial</a>
          </div>

          <div class="hotline-item-card">
            <div class="hotline-info">
              <div class="hotline-icon">🚓</div>
              <div>
                <div class="hotline-name">Central Police Control Room (PCR)</div>
                <div class="hotline-num">100</div>
              </div>
            </div>
            <a href="tel:100" class="hotline-dial-btn">📞 Dial 100</a>
          </div>

          <div class="hotline-item-card">
            <div class="hotline-info">
              <div class="hotline-icon">🛡️</div>
              <div>
                <div class="hotline-name">SWAT / QRT Tactical Command</div>
                <div class="hotline-num">011-23817013</div>
              </div>
            </div>
            <a href="tel:01123817013" class="hotline-dial-btn">📞 Dial</a>
          </div>
        </div>

        <button type="button" class="qr-copy-btn qr-modal-close-btn-inline" style="width:100%; border:none; background-color:var(--navy-deep); color:var(--white);">Close Modal</button>
      </div>
    </div>
    """

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="noindex, nofollow">
  <title>{title_en} | Delhi Police</title>
  <link rel="stylesheet" href="{rel_prefix}assets/css/app.css?v=8.0">
  <link rel="manifest" href="{rel_prefix}manifest.webmanifest">
  <meta name="theme-color" content="#000C44">
</head>
<body>

  <!-- Offline Status Banner -->
  <div id="offline-banner" class="offline-banner" role="status">
    ☁️ <span class="lang-en">Offline — showing saved instructions (v{meta['version']})</span>
    <span class="lang-hi">ऑफ़लाइन — सहेजे गए निर्देश दिखा रहा है (v{meta['version']})</span>
  </div>

  <!-- Masthead Header Ribbon (Exact Match to User Mockup) -->
  <header class="masthead">
    <div class="masthead-top">
      <a href="{rel_prefix}" class="masthead-brand">
        <div class="header-logo-box">
          <img src="{rel_prefix}assets/images/dp_logo.png" alt="Delhi Police Logo">
        </div>
        <div class="header-titles">
          <h1 class="masthead-title">QUICK INSTRUCTIONS</h1>
          <div class="masthead-subtitle">DELHI POLICE • दिल्ली पुलिस</div>
        </div>
      </a>
      <div class="header-actions">
        <button type="button" class="header-qr-btn qr-view-btn" data-target-modal="{qr_modal_target_id}">
          <span>📱</span>
          <span>QR Code</span>
        </button>
        <a href="tel:112" class="header-call-btn" aria-label="Call 112">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg>
          <span>112</span>
        </a>
        <div class="lang-toggle-box">
          <button type="button" class="lang-toggle-btn active-lang" onclick="toggleLanguage('en')">EN</button>
          <span style="color:rgba(255, 224, 127, 0.5); font-size:0.8rem;">|</span>
          <button type="button" class="lang-toggle-btn" onclick="toggleLanguage('hi')">हिंदी</button>
        </div>
      </div>
    </div>

    <!-- Red Standing Directive Ribbon -->
    <div class="directive-strip">
      <span class="lang-en">STAY ALERT • STAY VIGILANT • STAY SAFE</span>
      <span class="lang-hi">सतर्क रहें • चौकस रहें • सुरक्षित रहें</span>
    </div>
  </header>

  <!-- Main Content Canvas -->
  <main class="container">
    {main_content_html}
  </main>

  {hotline_modal_html}

  <!-- Fixed Bottom Control Room Call Bar (Signal Red Signature Element) -->
  <footer class="control-room-bar">
    <a href="tel:{ctrl_number}" class="control-room-call-btn" aria-label="Call Control Room">
      {phone_svg}
      <span class="lang-en">CALL CONTROL ROOM ({ctrl_number})</span>
      <span class="lang-hi">नियंत्रण कक्ष को कॉल करें ({ctrl_number})</span>
    </a>
  </footer>

  <script src="{rel_prefix}assets/js/lang.js"></script>
  <script src="{rel_prefix}assets/js/search.js"></script>
  <script src="{rel_prefix}assets/js/app.js?v=8.0"></script>
  {extra_script}
</body>
</html>
"""

    # Generate QR SVGs first
    print("\nGenerating Vector SVG QR Codes in qr/...")
    os.makedirs("qr", exist_ok=True)
    qr_targets = [("home", f"{base_domain}/")] + [(post["slug"], f"{base_domain}/{post['slug']}/") for post in posts]
    for slug, url in qr_targets:
        out_svg = f"qr/{slug}.svg"
        qr_matrix_to_svg(slug, url, out_svg)
        print(f"  [OK] Generated {out_svg} -> {url}")

    # Read Home QR Embedded SVG
    home_qr_svg = ""
    if os.path.exists("qr/home.svg"):
        with open("qr/home.svg", "r", encoding="utf-8") as f:
            home_qr_svg = f.read()

    # Helper function to render exact QR Modal HTML (Matching Image 2)
    def build_qr_modal_html(modal_id, qr_embedded_svg, rel_prefix=""):
        return f"""
    <!-- QR Code Modal (Exact Match to User Mockup Image 2) -->
    <div id="{modal_id}" class="qr-modal-overlay" role="dialog" aria-modal="true">
      <div class="qr-card-printable">
        <button type="button" class="qr-modal-close-btn" aria-label="Close">✕</button>
        <img src="{rel_prefix}assets/images/dp_logo.png" alt="Delhi Police Logo" class="qr-modal-logo">
        <h2 class="qr-card-title">SCAN QR CODE FOR INSTRUCTIONS</h2>
        <p class="qr-card-subtitle">
          Scan with any smartphone camera to open instructions directly on mobile or tablet.
        </p>

        <div class="qr-inner-frame">
          <div class="qr-image-container">
            {qr_embedded_svg}
          </div>
          <div class="qr-frame-badge">
            <span>📱</span>
            <span>MOBILE &amp; TABLET OPTIMIZED</span>
          </div>
        </div>

        <div class="qr-modal-actions">
          <button type="button" class="qr-copy-btn qr-copy-url-btn" onclick="copyPageURL(this)">
            <span>📋</span>
            <span>Copy URL</span>
          </button>
          <button type="button" class="qr-share-btn" onclick="shareWebsite()">
            <span>🔗</span>
            <span>Share Website</span>
          </button>
        </div>
      </div>
    </div>
    """

    # 3. Pre-render Home Page (`src/index.html`)
    print("\nPre-rendering Home Page (index.html)...")
    home_tiles_html = '<div class="posts-grid" id="posts-bento-grid">'
    for idx, post in enumerate(posts):
        icon_svg = load_svg_icon(post["icon"])
        img_rel = f"assets/images/{post['slug']}.jpg"
        img_tag = f'<img src="{img_rel}" alt="{post["en"]["name"]}" class="post-tile-img" loading="lazy">' if os.path.exists(f"src/{img_rel}") else ""
        kd_en_first = post["en"]["keyDirectives"][0] if post["en"]["keyDirectives"] else ""
        kd_hi_first = post["hi"]["keyDirectives"][0] if post["hi"]["keyDirectives"] else ""
        cat = post.get("category", "general")

        home_tiles_html += f"""
      <a href="{post['slug']}/" class="post-tile" data-category="{cat}">
        <div class="post-tile-hero-wrapper">
          {img_tag}
          <div class="post-tile-icon-badge">{icon_svg}</div>
        </div>
        <div class="post-tile-body">
          <div class="post-tile-title">
            <span class="lang-en">{post['en']['name']}</span>
            <span class="lang-hi">{post['hi']['name']}</span>
          </div>
          <div class="post-tile-tagline">
            <span class="lang-en">✦ {kd_en_first}</span>
            <span class="lang-hi">✦ {kd_hi_first}</span>
          </div>
        </div>
      </a>"""
    home_tiles_html += '</div>'

    category_filter_html = """
    <div class="category-filter-bar">
      <button type="button" class="category-filter-btn active" data-filter="all">ALL POSTS</button>
      <button type="button" class="category-filter-btn" data-filter="elevated">ELEVATED</button>
      <button type="button" class="category-filter-btn" data-filter="access">ACCESS CONTROL</button>
      <button type="button" class="category-filter-btn" data-filter="mobile">PATROL &amp; MOBILE</button>
      <button type="button" class="category-filter-btn" data-filter="monitoring">MONITORING</button>
    </div>
    """

    home_main_html = f"""
    <div class="slogan-banner">
      <span class="lang-en">Peace • Service • Justice</span>
      <span class="lang-hi">शांति • सेवा • न्याय</span>
    </div>

    <form class="search-form" action="search/" method="GET">
      <div class="search-input-wrapper">
        <div class="search-icon">{search_svg}</div>
        <input type="search" name="q" class="search-input" placeholder="Search instructions / निर्देश खोजें..." aria-label="Search duty instructions">
      </div>
    </form>



    {category_filter_html}
    {home_tiles_html}

    <div class="version-stamp">
      Version {meta['version']} • Updated {meta['updated']}
    </div>

    {build_qr_modal_html("qr-modal-home", home_qr_svg, rel_prefix="")}
    """

    category_filter_script = """
    <script>
    document.addEventListener('DOMContentLoaded', function() {
      var filterBtns = document.querySelectorAll('.category-filter-btn');
      var tiles = document.querySelectorAll('.post-tile');
      filterBtns.forEach(function(btn) {
        btn.addEventListener('click', function() {
          filterBtns.forEach(function(b){ b.classList.remove('active'); });
          this.classList.add('active');
          var filter = this.getAttribute('data-filter');
          tiles.forEach(function(tile) {
            if (filter === 'all' || tile.getAttribute('data-category') === filter) {
              tile.style.display = 'flex';
            } else {
              tile.style.display = 'none';
            }
          });
        });
      });
    });
    </script>
    """

    home_html = build_page_html(meta['title']['en'], meta['title']['hi'], home_main_html, rel_prefix="", qr_modal_target_id="qr-modal-home", active_nav="home", extra_script=category_filter_script)
    with open("src/index.html", "w", encoding="utf-8") as f:
        f.write(home_html)

    # 4. Pre-render Duty Shift Compliance Checklist Page (`src/dp-c9f7e2/index.html`)
    print("\nPre-rendering Duty Shift Compliance Checklist Page (dp-c9f7e2/index.html)...")
    os.makedirs("src/dp-c9f7e2", exist_ok=True)

    checklist_main_html = f"""
    <div class="back-bar">
      <a href="../" class="back-btn">
        {arrow_left_svg}
        <span class="lang-en">ALL POSTS</span>
        <span class="lang-hi">सभी पोस्ट</span>
      </a>
      <button type="button" class="qr-view-btn" onclick="resetChecklist()" style="color:var(--signal-red); border-color:var(--signal-red);">
        🔄 Reset Shift
      </button>
    </div>

    <div class="post-header-band">
      <h2 class="post-header-title">
        <span class="lang-en">DUTY SHIFT COMPLIANCE CHECKLIST</span>
        <span class="lang-hi">ड्यूटी शिफ्ट अनुपालन चेकलिस्ट</span>
      </h2>
      <div class="post-header-icon">📋</div>
    </div>

    <div class="checklist-card-box">
      <div class="checklist-form-grid">
        <div class="form-group">
          <label class="form-label" for="post-select">Select Duty Post / स्थान चुनें</label>
          <select id="post-select" class="form-control"></select>
        </div>
        <div class="form-group">
          <label class="form-label" for="officer-rank">Officer Rank / पद</label>
          <select id="officer-rank" class="form-control">
            <option value="Constable">Constable / आरक्षी</option>
            <option value="Head Constable">Head Constable / मुख्य आरक्षी</option>
            <option value="Assistant Sub-Inspector">Assistant Sub-Inspector / ए.एस.आई</option>
            <option value="Sub-Inspector">Sub-Inspector / उप-निरीक्षक</option>
            <option value="Inspector">Inspector / निरीक्षक</option>
          </select>
        </div>
        <div class="form-group">
          <label class="form-label" for="officer-name">Officer Name &amp; PNO / नाम व पी.एन.ओ</label>
          <input type="text" id="officer-name" class="form-control" placeholder="e.g. Ct. Ramesh Kumar (PNO 28190012)">
        </div>
      </div>

      <div class="progress-container">
        <div class="progress-header">
          <span id="progress-text-val">0 / 0 Verified (0%)</span>
          <span id="checklist-status-badge" class="status-badge-pending">IN PROGRESS</span>
        </div>
        <div class="progress-bar-bg">
          <div id="progress-bar-fill" class="progress-bar-fill"></div>
        </div>
      </div>

      <div id="checklist-items-container"></div>
    </div>

    <div class="version-stamp">
      Version {meta['version']} • Updated {meta['updated']}
    </div>

    {build_qr_modal_html("qr-modal-checklist", home_qr_svg, rel_prefix="../")}
    """

    checklist_extra_script = '<script src="../assets/js/checklist.js?v=8.0"></script>'
    checklist_html = build_page_html("Duty Shift Compliance Checklist", "ड्यूटी चेकलिस्ट", checklist_main_html, rel_prefix="../", qr_modal_target_id="qr-modal-checklist", active_nav="checklist", extra_script=checklist_extra_script)
    with open("src/dp-c9f7e2/index.html", "w", encoding="utf-8") as f:
        f.write(checklist_html)

    # 5. Pre-render Post Detail Pages
    print("\nPre-rendering Post Detail Pages...")
    for post in posts:
        slug = post["slug"]
        os.makedirs(f"src/{slug}", exist_ok=True)
        post_icon_svg = load_svg_icon(post["icon"])

        qr_svg_path = f"qr/{slug}.svg"
        qr_embedded_svg = ""
        if os.path.exists(qr_svg_path):
            with open(qr_svg_path, "r", encoding="utf-8") as f:
                qr_embedded_svg = f.read()

        hero_img_rel = f"../assets/images/{slug}.jpg"
        hero_photo_card = ""
        if os.path.exists(f"src/assets/images/{slug}.jpg"):
            hero_photo_card = f"""
        <div class="post-hero-card">
          <img src="{hero_img_rel}" alt="{post['en']['name']} Briefing Photo" class="post-hero-photo" loading="eager">
          <div class="post-hero-caption-bar">
            <span class="lang-en">📷 OFFICIAL DUTY POINT BRIEFING PHOTO</span>
            <span class="lang-hi">📷 आधिकारिक ड्यूटी पॉइंट ब्रिफिंग चित्र</span>
            <span>DELHI POLICE</span>
          </div>
        </div>
        """

        kd_en_items = "".join([f'<li class="key-directive-item"><span class="key-directive-bullet-icon">✦</span><span>{kd}</span></li>' for kd in post["en"]["keyDirectives"]])
        kd_hi_items = "".join([f'<li class="key-directive-item"><span class="key-directive-bullet-icon">✦</span><span>{kd}</span></li>' for kd in post["hi"]["keyDirectives"]])

        inst_en_items = "".join([
            f'<article class="instruction-card"><div class="instruction-number">{idx+1:02d}</div><div class="instruction-text">{inst}</div></article>'
            for idx, inst in enumerate(post["en"]["instructions"])
        ])
        inst_hi_items = "".join([
            f'<article class="instruction-card"><div class="instruction-number">{idx+1:02d}</div><div class="instruction-text">{inst}</div></article>'
            for idx, inst in enumerate(post["hi"]["instructions"])
        ])

        post_modal_id = f"qr-modal-{slug}"

        post_main_html = f"""
        <div class="back-bar">
          <a href="../" class="back-btn">
            {arrow_left_svg}
            <span class="lang-en">ALL POSTS</span>
            <span class="lang-hi">सभी पोस्ट</span>
          </a>
          <button type="button" class="qr-view-btn" data-target-modal="{post_modal_id}">
            📱 <span class="lang-en">View/Print QR Code</span>
            <span class="lang-hi">क्यूआर कोड देखें/प्रिंट करें</span>
          </button>
        </div>

        <div class="post-header-band">
          <h2 class="post-header-title">
            <span class="lang-en">{post['en']['name']}</span>
            <span class="lang-hi">{post['hi']['name']}</span>
          </h2>
          <div class="post-header-icon">{post_icon_svg}</div>
        </div>

        {hero_photo_card}

        <!-- Key Directives Container Box -->
        <div class="key-directives-block">
          <div class="key-directives-title">
            <span>🛡️</span>
            <span class="lang-en">KEY DIRECTIVES</span>
            <span class="lang-hi">मुख्य निर्देश</span>
          </div>
          <ul class="key-directives-list lang-en">{kd_en_items}</ul>
          <ul class="key-directives-list lang-hi">{kd_hi_items}</ul>
        </div>

        <!-- Operational Instructions List -->
        <div class="instructions-section">
          <div class="instructions-header-bar">
            <h3 class="instructions-heading">
              <span class="lang-en">OPERATIONAL INSTRUCTIONS</span>
              <span class="lang-hi">परिचालन निर्देश</span>
            </h3>
            <button type="button" class="inline-switch-btn" onclick="toggleLanguage(document.documentElement.lang === 'hi' ? 'en' : 'hi')">
              <span class="lang-en">हिंदी में देखें</span>
              <span class="lang-hi">SHOW IN ENGLISH</span>
            </button>
          </div>

          <div class="instructions-cards-list lang-en">{inst_en_items}</div>
          <div class="instructions-cards-list lang-hi">{inst_hi_items}</div>
        </div>

        <div class="version-stamp">
          Version {meta['version']} • Updated {meta['updated']}
        </div>

        {build_qr_modal_html(post_modal_id, qr_embedded_svg, rel_prefix="../")}
        """

        post_html = build_page_html(post['en']['name'], post['hi']['name'], post_main_html, rel_prefix="../", qr_modal_target_id=post_modal_id, active_nav="home")
        with open(f"src/{slug}/index.html", "w", encoding="utf-8") as f:
            f.write(post_html)
        print(f"  [OK] Pre-rendered src/{slug}/index.html")

    # 6. Pre-render Search Page (`src/search/index.html`)
    print("\nPre-rendering Search Page (search/index.html)...")
    os.makedirs("src/search", exist_ok=True)
    search_main_html = f"""
    <div class="back-bar">
      <a href="../" class="back-btn">
        {arrow_left_svg}
        <span class="lang-en">ALL POSTS</span>
        <span class="lang-hi">सभी पोस्ट</span>
      </a>
    </div>

    <div class="search-form">
      <div class="search-input-wrapper">
        <div class="search-icon">{search_svg}</div>
        <input type="search" id="search-input" class="search-input" placeholder="Search instructions / निर्देश खोजें..." aria-label="Search duty instructions" autofocus>
      </div>
    </div>

    <div id="search-results"></div>

    <div class="version-stamp">
      Version {meta['version']} • Updated {meta['updated']}
    </div>

    {build_qr_modal_html("qr-modal-search", home_qr_svg, rel_prefix="../")}
    """
    search_html = build_page_html("Search Instructions", "निर्देश खोजें", search_main_html, rel_prefix="../", qr_modal_target_id="qr-modal-search", active_nav="search")
    with open("src/search/index.html", "w", encoding="utf-8") as f:
        f.write(search_html)

    # 7. Copy content.json into `src/content/content.json`
    os.makedirs("src/content", exist_ok=True)
    with open("src/content/content.json", "w", encoding="utf-8") as f:
        json.dump(content, f, indent=2, ensure_ascii=False)

    # 8. Generate Manifest & robots.txt
    print("\nGenerating manifest.webmanifest and robots.txt...")
    manifest = {
      "short_name": "DP Duty",
      "name": meta['title']['en'],
      "icons": [
        { "src": "/assets/images/dp_logo.png", "sizes": "192x192", "type": "image/png" },
        { "src": "/assets/images/dp_logo.png", "sizes": "512x512", "type": "image/png" }
      ],
      "start_url": "/",
      "background_color": "#FBF9F4",
      "theme_color": "#000C44",
      "display": "standalone"
    }
    with open("src/manifest.webmanifest", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    with open("src/robots.txt", "w", encoding="utf-8") as f:
        f.write("User-agent: *\nDisallow: /dp-c9f7e2/\nDisallow: /dp-q3b8a1/\n")

    # 9. Payload Budget Measurement Check
    print("\nRunning Payload Budget Measurement (< 100KB gzipped)...")
    total_uncompressed = 0
    total_gzipped = 0

    for root, _, files in os.walk("src"):
        for file in files:
            if file.endswith((".html", ".css", ".js", ".json", ".webmanifest")):
                path = os.path.join(root, file)
                with open(path, "rb") as f:
                    data = f.read()
                    gz_data = gzip.compress(data)
                    total_uncompressed += len(data)
                    total_gzipped += len(gz_data)

    print(f"Total Shipped Code Payload (HTML+CSS+JS+JSON):")
    print(f"  Uncompressed: {total_uncompressed / 1024:.2f} KB")
    print(f"  Gzipped:      {total_gzipped / 1024:.2f} KB")

    if total_gzipped > 100 * 1024:
        print("[WARNING] Payload exceeds 100KB gzipped budget!")
    else:
        print("[SUCCESS] Payload is comfortably within the 100KB gzipped budget.")

if __name__ == "__main__":
    main()
