import pymupdf
import os
from PIL import Image
import io

pdf_path = "d:/VVIP/Draft Instructions 01.pdf"
output_dir = "src/assets/images"
os.makedirs(output_dir, exist_ok=True)

# Post slug mapping for the 10 PDF pages
page_slug_map = {
    0: "cover",
    1: "rooftop",
    2: "morcha",
    3: "machan",
    4: "vehicle-checking",
    5: "dfmd",
    6: "qrt",
    7: "xray",
    8: "cctv",
    9: "medical"
}

doc = pymupdf.open(pdf_path)
print(f"Opened PDF '{pdf_path}' with {len(doc)} pages.")

extracted_count = 0

for page_num in range(len(doc)):
    page = doc[page_num]
    slug = page_slug_map.get(page_num, f"page_{page_num}")
    
    # 1. First extract embedded images from page
    image_list = page.get_images(full=True)
    
    if image_list:
        img_idx = 0
        for img_info in image_list:
            xref = img_info[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            
            try:
                img = Image.open(io.BytesIO(image_bytes))
                if img.mode in ("RGBA", "P", "CMYK"):
                    img = img.convert("RGB")
                    
                # Skip tiny icon images (e.g. smaller than 100x100)
                if img.width < 100 or img.height < 100:
                    continue
                    
                # Downscale large images for mobile web performance (max 800px width)
                max_w = 800
                if img.width > max_w:
                    h = int((max_w / img.width) * img.height)
                    img = img.resize((max_w, h), Image.Resampling.LANCZOS)
                    
                out_name = f"{slug}.jpg" if img_idx == 0 else f"{slug}_{img_idx}.jpg"
                out_path = os.path.join(output_dir, out_name)
                img.save(out_path, "JPEG", quality=85, optimize=True)
                print(f"  [OK] Saved embedded image: {out_path} ({img.width}x{img.height})")
                extracted_count += 1
                img_idx += 1
            except Exception as e:
                print(f"  [ERROR] Page {page_num} xref {xref}: {e}")
                
    # 2. If no large embedded image extracted, render the page region as high-res banner image
    if img_idx == 0 if 'img_idx' in locals() else True:
        pix = page.get_pixmap(dpi=150)
        img = Image.open(io.BytesIO(pix.tobytes("jpeg")))
        max_w = 800
        if img.width > max_w:
            h = int((max_w / img.width) * img.height)
            img = img.resize((max_w, h), Image.Resampling.LANCZOS)
        out_path = os.path.join(output_dir, f"{slug}.jpg")
        img.save(out_path, "JPEG", quality=85, optimize=True)
        print(f"  [OK] Rendered page image: {out_path} ({img.width}x{img.height})")
        extracted_count += 1

print(f"\nSuccessfully extracted & optimized {extracted_count} web-ready images into {output_dir}")
