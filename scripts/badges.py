"""Gera assets/badges/*.svg (estilo flat-square) a partir dos logos em assets/logos."""
import os
import re
from html import escape

# slug: (nome, cor de fundo, cor do texto, cor do logo)
W, D, REACT = "#ffffff", "#1f2328", "#61dafb"
BADGES = {
    "r": ("R", "#276dc3", W, W),
    "matlab": ("MATLAB", "#e16737", W, None),
    "stata": ("Stata", "#1a5f91", W, None),
    "python": ("Python", "#3776ab", W, W),
    "sql": ("SQL", "#475569", W, None),
    "pandas": ("pandas", "#150458", W, W),
    "geopandas": ("GeoPandas", "#139c5a", W, W),
    "qgis": ("QGIS", "#589632", W, W),
    "webgis": ("WebGIS", "#475569", W, None),
    "googleearth": ("Google Earth", "#4285f4", W, W),
    "maplibre": ("MapLibre GL", "#396cb2", W, W),
    "typescript": ("TypeScript", "#3178c6", W, W),
    "nextdotjs": ("Next.js", "#000000", W, W),
    "react": ("React", "#20232a", W, REACT),
    "supabase": ("Supabase", "#3fcf8e", D, D),
    "firebase": ("Firebase", "#dd2c00", W, W),
    "googlecloud": ("Google Cloud", "#4285f4", W, W),
    "powerbi": ("Power BI", "#f2c811", D, D),
    "microsoftexcel": ("Excel", "#217346", W, W),
    "claude": ("Claude", "#d97757", W, W),
    "googlegemini": ("Gemini", "#8e75b2", W, W),
    "latex": ("LaTeX", "#008080", W, W),
    "git": ("Git", "#f05032", W, W),
    "vercel": ("Vercel", "#000000", W, W),
    "orcid": ("ORCID", "#a6ce39", D, D),
    "site": ("Site e artigos", "#1f6feb", W, None),
    "linkedin": ("LinkedIn", "#0a66c2", W, W),
}
H, PAD, ICON, GAP = 28, 12, 14, 7

os.makedirs("assets/badges", exist_ok=True)
for slug, (name, bg, fg, logo_color) in BADGES.items():
    text_w = round(6.9 * len(name) + 2)
    path = None
    if logo_color:
        svg = open(f"assets/logos/{slug}.svg", encoding="utf-8").read()
        path = re.search(r'<path d="([^"]+)"', svg).group(1)
    left = PAD + (ICON + GAP if path else 0)
    width = left + text_w + PAD
    icon = (
        f'<g transform="translate({PAD} {(H - ICON) / 2}) scale({ICON / 24})" fill="{logo_color}"><path d="{path}"/></g>'
        if path
        else ""
    )
    out = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{H}" viewBox="0 0 {width} {H}" role="img" aria-label="{escape(name)}">'
        f'<rect width="{width}" height="{H}" rx="4" fill="{bg}"/>{icon}'
        f'<text x="{left}" y="18" fill="{fg}" font-family="Verdana,DejaVu Sans,Segoe UI,sans-serif" font-size="11" font-weight="700" '
        f'textLength="{text_w}" lengthAdjust="spacingAndGlyphs">{escape(name)}</text></svg>'
    )
    with open(f"assets/badges/{slug}.svg", "w", encoding="utf-8") as f:
        f.write(out)
print(len(BADGES), "badges")
