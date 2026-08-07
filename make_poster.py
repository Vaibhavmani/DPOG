"""
Generate the dpog.vercel.app QR code and composite it into the Delhi Police poster.
The poster has a white QR placeholder in the upper-right area.
"""
import qrcode
from PIL import Image, ImageDraw

# --- 1. Generate high-resolution QR code PNG ---
qr = qrcode.QRCode(
    version=None,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=14,
    border=2,
)
qr.add_data("https://dpog.vercel.app/")
qr.make(fit=True)

# Navy deep blue modules on white background
qr_img = qr.make_image(fill_color="#000C44", back_color="white")
qr_img = qr_img.convert("RGBA")

# Save standalone QR PNG for delivery
qr_img.save(r"d:\VVIP\dpog_home_qr.png")
print(f"[OK] Saved standalone QR: d:\\VVIP\\dpog_home_qr.png  ({qr_img.width}x{qr_img.height}px)")

# --- 2. Load poster and identify placeholder region ---
poster_path = r"d:\VVIP\WhatsApp Image 2026-08-08 at 2.24.28 AM.jpeg"

# The user shared this poster — it's a portrait flyer.
# Looking at it: poster is ~525x676 (approx from screen).
# QR placeholder is upper-right white box, visually around:
#   left: ~320px, top: ~295px, right: ~480px, bottom: ~445px
# We'll open the actual image to get real dimensions, then scale proportionally.

poster = Image.open(poster_path).convert("RGBA")
w, h = poster.size
print(f"[INFO] Poster size: {w}x{h}")

# Proportional placement based on visual inspection of poster:
# QR box appears at approx 61% from left, 44% from top, about 30% of width wide
qr_left   = int(w * 0.608)
qr_top    = int(h * 0.435)
qr_right  = int(w * 0.930)
qr_bottom = int(h * 0.620)

qr_w = qr_right - qr_left
qr_h = qr_bottom - qr_top
print(f"[INFO] Placing QR at: ({qr_left},{qr_top}) size {qr_w}x{qr_h}")

# Add white padding around QR (6px)
pad = 6
qr_inner_size = min(qr_w - pad*2, qr_h - pad*2)
qr_resized = qr_img.resize((qr_inner_size, qr_inner_size), Image.LANCZOS)

# Create a white box with the QR centred inside it
qr_box = Image.new("RGBA", (qr_w, qr_h), (255, 255, 255, 255))
offset_x = (qr_w - qr_inner_size) // 2
offset_y = (qr_h - qr_inner_size) // 2
qr_box.paste(qr_resized, (offset_x, offset_y), qr_resized)

# Composite onto poster
poster.paste(qr_box, (qr_left, qr_top))
poster_rgb = poster.convert("RGB")

out_path = r"d:\VVIP\delhi_police_poster_with_qr.jpg"
poster_rgb.save(out_path, "JPEG", quality=95)
print(f"[OK] Saved poster with QR: {out_path}")
