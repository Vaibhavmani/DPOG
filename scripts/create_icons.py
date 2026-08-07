import os

ICONS_DIR = "src/assets/icons"
os.makedirs(ICONS_DIR, exist_ok=True)

icons = {
    "emblem.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-5.45 9-12V5l-9-4zm0 6a3 3 0 110 6 3 3 0 010-6zm-4.5 9.5c.34-2.36 2.37-4.5 4.5-4.5s4.16 2.14 4.5 4.5H7.5z"/></svg>''',
    
    "building-watch.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm-5 11v-1c0-2 4-3.1 5-3.1s5 1.1 5 3.1v1H7z"/></svg>''',
    
    "barricade.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M19 7h-2V5c0-.55-.45-1-1-1s-1 .45-1 1v2H9V5c0-.55-.45-1-1-1s-1 .45-1 1v2H5c-1.1 0-2 .9-2 2v6c0 1.1.9 2 2 2h2v2c0 .55.45 1 1 1s1-.45 1-1v-2h6v2c0 .55.45 1 1 1s1-.45 1-1v-2h2c1.1 0 2-.9 2-2V9c0-1.1-.9-2-2-2zm0 6H5V9h14v4z"/></svg>''',
    
    "watchtower.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 2L4 5v3h16V5l-8-3zm-6 7l1.5 11h9L18 9H6zm6 2a2 2 0 110 4 2 2 0 010-4z"/></svg>''',
    
    "vehicle-check.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M18.92 6.01C18.72 5.42 18.16 5 17.5 5h-11c-.66 0-1.21.42-1.42 1.01L3 12v8c0 .55.45 1 1 1h1c.55 0 1-.45 1-1v-1h12v1c0 .55.45 1 1 1h1c.55 0 1-.45 1-1v-8l-2.08-5.99zM6.5 16c-.83 0-1.5-.67-1.5-1.5S5.67 13 6.5 13s1.5.67 1.5 1.5S7.33 16 6.5 16zm11 0c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5zM5 11l1.5-4.5h11L19 11H5z"/></svg>''',
    
    "door-frame-detector.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M19 2H5c-1.1 0-2 .9-2 2v18h3V5h12v17h3V4c0-1.1-.9-2-2-2zm-7 6c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"/></svg>''',
    
    "rapid-response.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M7 2v11h3v9l7-12h-4l4-8H7z"/></svg>''',
    
    "baggage-scanner.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M19 6h-4V4c0-1.1-.9-2-2-2h-2c-1.1 0-2 .9-2 2v2H5c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2zm-8-2h2v2h-2V4zm8 14H5V8h14v10zm-7-1h2v-8h-2v8z"/></svg>''',
    
    "camera-monitor.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M20 3H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h4v2h8v-2h4c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 14H4V5h16v12zm-6-6c0 1.1-.9 2-2 2s-2-.9-2-2 .9-2 2-2 2 .9 2 2z"/></svg>''',
    
    "ambulance.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-2 10h-4v4h-2v-4H7v-2h4V7h2v4h4v2z"/></svg>''',
    
    "phone.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg>''',
    
    "search.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg>''',
    
    "arrow-left.svg": '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"/></svg>'''
}

for name, svg in icons.items():
    filepath = os.path.join(ICONS_DIR, name)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(svg)

print(f"Created {len(icons)} SVG icons in {ICONS_DIR}")
