import sys, os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
F = sys.argv[1]; OUT = sys.argv[2]
def text_path(fontfile, wght, text, size, x, y, tracking=0):
    f = TTFont(fontfile); gs = f.getGlyphSet(location={'wght': wght}); cmap = f.getBestCmap()
    upm = f['head'].unitsPerEm; s = size / upm; d = []; cx = x
    for ch in text:
        g = cmap.get(ord(ch))
        if ch == ' ':
            cx += gs[g].width * s + tracking; continue
        pen = SVGPathPen(gs); gs[g].draw(TransformPen(pen, (s, 0, 0, -s, cx, y))); d.append(pen.getCommands())
        cx += gs[g].width * s + tracking
    return ' '.join(d), cx - tracking
name, w1 = text_path(F + '/RobotoSlab.ttf', 160, 'SM Legal', 100, 72, 112)
# subtitle sized to span roughly the name width + a bit, like the original
sub, w2 = text_path(F + '/Raleway.ttf', 300, 'MARUSHKINA LAW FIRM', 33, 72, 178, 1.2)
scale_fix = (w1 - 70) * 1.08 / (w2 - 72)
sub, w2 = text_path(F + '/Raleway.ttf', 300, 'MARUSHKINA LAW FIRM', 33 * scale_fix, 74, 182, 1.2 * scale_fix)
W = int(max(w1, w2)) + 20; H = 220
variants = {
  'logo-dark':  ('#1e1f22', '#7d7f84', '#1e1f22', None),
  'logo-slate': ('#4e525a', '#8a8d93', '#4e525a', None),
  'logo-rose':  ('#f3c2b1', '#f3c2b1', '#f3c2b1', None),
  'logo-white': ('#ffffff', '#f3c2b1', '#f3c2b1', None),
  'logo-rose-on-slate': ('#f3c2b1', '#f3c2b1', '#f3c2b1', '#4e525a'),
}
os.makedirs(OUT, exist_ok=True)
for fn, (c1, c2, bar, bg) in variants.items():
    rect = f'<rect width="{W}" height="{H}" rx="18" fill="{bg}"/>' if bg else ''
    sub_op = ' fill-opacity=".75"' if fn == 'logo-rose' else ''
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="SM Legal — Marushkina Law Firm">'
           f'<title>SM Legal — Marushkina Law Firm</title>{rect}<rect x="30" y="12" width="4.5" height="196" fill="{bar}"/>'
           f'<path fill="{c1}" d="{name}"/><path fill="{c2}"{sub_op} d="{sub}"/></svg>')
    open(f'{OUT}/{fn}.svg', 'w').write(svg)
# monogram favicon
mono, mw = text_path(F + '/RobotoSlab.ttf', 300, 'SM', 34, 0, 0)
open(f'{OUT}/../favicon.svg', 'w').write(
  f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="12" fill="#4e525a"/>'
  f'<rect x="11" y="13" width="2.6" height="38" fill="#f3c2b1"/><g transform="translate(18 44)"><path fill="#f3c2b1" d="{mono}"/></g></svg>')
print(W, H)
