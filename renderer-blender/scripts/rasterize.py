"""Rasterize approved SVG art to transparent PNG cards for the Blender pilot.

The approved SVG files are read, never modified. A full-size background rect
(present on pose stills) is dropped in the in-memory copy so the card is
transparent. Uses the installed Google Chrome in headless mode.

usage: python3 -I rasterize.py OUT_DIR SCALE SVG [SVG ...]
"""
import os, re, subprocess, sys, tempfile, time

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def strip_background(svg):
    m = re.search(r'viewBox="([-\d.]+) ([-\d.]+) ([-\d.]+) ([-\d.]+)"', svg)
    x, y, w, h = m.groups()
    bg = re.compile(r'<rect x="%s" y="%s" width="%s" height="%s" fill="[^"]+"/>' % (x, y, w, h))
    return bg.sub("", svg, count=1), float(w), float(h)


def main():
    out, scale, files = sys.argv[1], float(sys.argv[2]), sys.argv[3:]
    os.makedirs(out, exist_ok=True)
    for path in files:
        svg, w, h = strip_background(open(path).read())
        W, H = int(w * scale), int(h * scale)
        svg = re.sub(r'width="[\d.]+" height="[\d.]+"', f'width="{W}" height="{H}"', svg, count=1)
        html = f"<html><body style='margin:0;background:transparent'>{svg}</body></html>"
        with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as t:
            t.write(html)
        png = os.path.join(out, os.path.basename(path).replace(".svg", ".png"))
        if os.path.exists(png):
            os.unlink(png)
        # Chrome writes the screenshot but may not exit on its own; wait for the file, then stop it.
        p = subprocess.Popen([CHROME, "--headless=new", "--no-first-run", "--disable-gpu", "--hide-scrollbars",
                              f"--user-data-dir={tempfile.gettempdir()}/rasterize-chrome",
                              "--default-background-color=00000000", f"--window-size={W},{H}",
                              f"--screenshot={png}", "file://" + t.name],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(120):
            time.sleep(0.5)
            if p.poll() is not None or (os.path.exists(png) and os.path.getsize(png) > 0):
                time.sleep(1.0)
                break
        p.kill()
        p.wait()
        os.unlink(t.name)
        if not os.path.exists(png):
            sys.exit(f"no output for {path}")
        print(png, W, H)


if __name__ == "__main__":
    main()
