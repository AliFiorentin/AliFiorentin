"""Gera assets/languages.svg com as linguagens mais usadas nos repositórios públicos."""
import json
import os
import urllib.request
from html import escape

USER = os.environ.get("GH_USER", "AliFiorentin")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
EXCLUDE = {"Jupyter Notebook"}
TOP = 6
COLORS = ["#3178c6", "#3572a5", "#198ce7", "#3d6117", "#b83998", "#e34c26", "#8250df"]


def api(path):
    req = urllib.request.Request(f"https://api.github.com{path}")
    req.add_header("Accept", "application/vnd.github+json")
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


totals = {}
for repo in api(f"/users/{USER}/repos?per_page=100&type=owner"):
    if repo["fork"]:
        continue
    for lang, size in api(f"/repos/{USER}/{repo['name']}/languages").items():
        if lang not in EXCLUDE:
            totals[lang] = totals.get(lang, 0) + size

ranked = sorted(totals.items(), key=lambda kv: kv[1], reverse=True)[:TOP]
total = sum(size for _, size in ranked) or 1

W, ROW = 420, 26
H = 56 + ROW * len(ranked)
rows = []
for i, (lang, size) in enumerate(ranked):
    y = 56 + i * ROW
    pct = 100 * size / total
    bar = max(2, 190 * pct / 100)
    rows.append(
        f'<text x="0" y="{y}" class="t">{escape(lang)}</text>'
        f'<rect x="130" y="{y - 11}" width="190" height="10" rx="5" class="bg"/>'
        f'<rect x="130" y="{y - 11}" width="{bar:.1f}" height="10" rx="5" fill="{COLORS[i % len(COLORS)]}"/>'
        f'<text x="332" y="{y}" class="t">{pct:.1f}%</text>'
    )

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Linguagens mais usadas">
<style>
.t{{font:14px -apple-system,Segoe UI,Helvetica,Arial,sans-serif;fill:#1f2328}}
.h{{font:600 16px -apple-system,Segoe UI,Helvetica,Arial,sans-serif;fill:#1f2328}}
.bg{{fill:#d0d7de}}
@media (prefers-color-scheme: dark){{.t,.h{{fill:#e6edf3}}.bg{{fill:#30363d}}}}
</style>
<text x="0" y="20" class="h">Linguagens mais usadas</text>
{''.join(rows)}
</svg>
"""
os.makedirs("assets", exist_ok=True)
with open("assets/languages.svg", "w", encoding="utf-8") as f:
    f.write(svg)
print(ranked)
