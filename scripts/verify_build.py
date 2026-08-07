import os
import json
import gzip

def verify():
    print("=== Law & Order App Build Verification ===")
    
    # 1. Check content.json invariant
    with open("content/content.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"Content Version: {data['meta']['version']}")
    print(f"Updated Date: {data['meta']['updated']}")

    posts = data["posts"]
    assert len(posts) == 9, f"Expected 9 posts, got {len(posts)}"

    for post in posts:
        pid = post["id"]
        en_cnt = len(post["en"]["instructions"])
        hi_cnt = len(post["hi"]["instructions"])
        assert en_cnt == hi_cnt, f"Post {pid} instruction count mismatch: EN={en_cnt}, HI={hi_cnt}"
        assert len(post["en"]["keyDirectives"]) > 0, f"Post {pid} missing EN key directives"
        assert len(post["hi"]["keyDirectives"]) > 0, f"Post {pid} missing HI key directives"
        print(f"  [PASS] Post '{pid}' EN/HI instruction parity: {en_cnt} items")

    # 2. Check 11 HTML Pages
    expected_pages = [
        "src/index.html",
        "src/rooftop/index.html",
        "src/morcha/index.html",
        "src/machan/index.html",
        "src/vehicle-checking/index.html",
        "src/dfmd/index.html",
        "src/qrt/index.html",
        "src/xray/index.html",
        "src/cctv/index.html",
        "src/medical/index.html",
        "src/search/index.html"
    ]

    for page in expected_pages:
        assert os.path.exists(page), f"Missing pre-rendered page: {page}"
        with open(page, "r", encoding="utf-8") as f:
            content = f.read()
            assert '<meta name="robots" content="noindex, nofollow">' in content, f"Missing noindex tag in {page}"
            assert 'lang-en' in content and 'lang-hi' in content, f"Missing bilingual markup in {page}"
            assert 'control-room-bar' in content, f"Missing Control Room bar in {page}"
        print(f"  [PASS] Pre-rendered HTML page verified: {page}")

    # 3. Check 10 QR SVG files
    expected_qrs = [
        "qr/home.svg", "qr/rooftop.svg", "qr/morcha.svg", "qr/machan.svg",
        "qr/vehicle-checking.svg", "qr/dfmd.svg", "qr/qrt.svg",
        "qr/xray.svg", "qr/cctv.svg", "qr/medical.svg"
    ]

    for qr in expected_qrs:
        assert os.path.exists(qr), f"Missing QR code: {qr}"
        with open(qr, "r", encoding="utf-8") as f:
            svg_data = f.read()
            assert '<svg' in svg_data and '</svg>' in svg_data, f"Invalid SVG in {qr}"
        print(f"  [PASS] Vector SVG QR code verified: {qr}")

    # 4. Measure Payload Budget
    total_uncompressed = 0
    total_gzipped = 0
    for root, _, files in os.walk("src"):
        for file in files:
            if file.endswith((".html", ".css", ".js", ".json", ".webmanifest")):
                filepath = os.path.join(root, file)
                with open(filepath, "rb") as f:
                    content_bytes = f.read()
                    total_uncompressed += len(content_bytes)
                    total_gzipped += len(gzip.compress(content_bytes))

    print(f"\nPayload Summary:")
    print(f"  Total Uncompressed Code Payload: {total_uncompressed / 1024:.2f} KB")
    print(f"  Total Gzipped Code Payload:      {total_gzipped / 1024:.2f} KB")
    assert total_gzipped < 100 * 1024, f"Payload exceeded 100KB budget: {total_gzipped} bytes"
    print("  [PASS] Gzipped payload budget < 100KB verified!")

    print("\nALL VERIFICATION CHECKS PASSED PERFECTLY!")

if __name__ == "__main__":
    verify()
