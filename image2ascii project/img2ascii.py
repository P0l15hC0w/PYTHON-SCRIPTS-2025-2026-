import argparse
from PIL import Image

# A gradient of characters from dark (left) to light (right).
DEFAULT_CHARSET = " @%#+=-. "  # compact, good for small outputs
# More detailed set (uncomment to use)
# DEFAULT_CHARSET = "$@B%8&WM#*oahkbdpqwmZ0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

def get_args():
    p = argparse.ArgumentParser(description="Convert image to ASCII art")
    p.add_argument("input", help="Input image path")
    p.add_argument("--width", type=int, default=100, help="Target output width in characters (default: 100)")
    p.add_argument("--outfile", default=None, help="Write ASCII art to file (default: print to stdout)")
    p.add_argument("--invert", action="store_true", help="Invert brightness mapping (optional)")
    p.add_argument("--charset", default=DEFAULT_CHARSET, help="Characters from dark->light (string)")
    p.add_argument("--scale", type=float, default=0.55, help="Height scaling factor to correct character aspect ratio (default: 0.55)")
    return p.parse_args()

def resize_image(img, new_width, scale):
    # Preserve aspect ratio but scale height for character aspect ratio
    w, h = img.size
    aspect_ratio = h / w
    new_height = max(1, int(aspect_ratio * new_width * scale))
    return img.resize((new_width, new_height))

def to_grayscale(img):
    return img.convert("L")  # L mode = (0..255) grayscale

def map_pixels_to_ascii(img_gray, charset, invert=False):
    pixels = list(img_gray.getdata())
    width, height = img_gray.size
    n_chars = len(charset)
    out_lines = []
    for y in range(height):
        row_chars = []
        for x in range(width):
            brightness = pixels[y * width + x]  # 0 (black) .. 255 (white)
            # Normalize to 0..1
            t = brightness / 255.0
            if invert:
                t = 1.0 - t
            idx = int(t * (n_chars - 1))  # index into charset
            row_chars.append(charset[idx])
        out_lines.append("".join(row_chars))
    return "\n".join(out_lines)

def main():
    args = get_args()
    try:
        img = Image.open(args.input)
    except Exception as e:
        print(f"Error opening image: {e}")
        return

    # Resize
    img_small = resize_image(img, args.width, args.scale)
    # Grayscale
    img_gray = to_grayscale(img_small)
    # Map to ASCII
    ascii_art = map_pixels_to_ascii(img_gray, args.charset, invert=args.invert)

    if args.outfile:
        try:
            with open(args.outfile, "w", encoding="utf-8") as f:
                f.write(ascii_art)
            print(f"Saved ASCII art to {args.outfile}")
        except Exception as e:
            print(f"Error writing file: {e}")
    else:
        print(ascii_art)

if __name__ == "__main__":
    main()