import urllib.request
import re
import os

FONTS_DIR = "src/assets/fonts"
os.makedirs(FONTS_DIR, exist_ok=True)

UA_WOFF2 = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

font_queries = [
    ("Barlow+Condensed:wght@600;700", "barlow-condensed"),
    ("Inter:wght@400;600;700", "inter"),
    ("Noto+Sans+Devanagari:wght@400;600;700", "noto-sans-devanagari")
]

generated_css = ["/* Self-Hosted Fonts for Offline Law & Order Deployment Quick Instructions */\n"]

for query, prefix in font_queries:
    url = f"https://fonts.googleapis.com/css2?family={query}&display=swap"
    req = urllib.request.Request(url, headers={"User-Agent": UA_WOFF2})
    try:
        content = urllib.request.urlopen(req).read().decode("utf-8")
        blocks = re.findall(r"@font-face\s*\{[^}]+\}", content)
        for idx, block in enumerate(blocks):
            src_match = re.search(r"src:\s*url\((https://[^)]+)\)\s*format\(['\"]?([^'\"]+)['\"]?\)", block)
            if src_match:
                font_url, font_format = src_match.groups()
                ext = "woff2" if "woff2" in font_format else "ttf"
                filename = f"{prefix}-{idx+1}.{ext}"
                filepath = os.path.join(FONTS_DIR, filename)
                
                if not os.path.exists(filepath):
                    print(f"Downloading {font_url} -> {filepath}")
                    font_data = urllib.request.urlopen(font_url).read()
                    with open(filepath, "wb") as f:
                        f.write(font_data)
                
                local_block = block.replace(src_match.group(1), f"../fonts/{filename}")
                generated_css.append(local_block + "\n")
    except Exception as e:
        print(f"Error fetching font {query}: {e}")

css_path = "src/assets/css/fonts.css"
os.makedirs("src/assets/css", exist_ok=True)
with open(css_path, "w", encoding="utf-8") as f:
    f.write("\n".join(generated_css))

print(f"Successfully generated {css_path} with {len(generated_css)-1} font declarations.")
