"""Gera assets/contributions.svg com as contribuições por mês (últimos 12 meses)."""
import datetime
import json
import os
import urllib.request

USER = os.environ.get("GH_USER", "AliFiorentin")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
MESES = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}
"""

req = urllib.request.Request(
    "https://api.github.com/graphql",
    data=json.dumps({"query": QUERY, "variables": {"login": USER}}).encode(),
    headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"},
)
with urllib.request.urlopen(req, timeout=30) as r:
    payload = json.load(r)
weeks = payload["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]

por_mes = {}
for week in weeks:
    for day in week["contributionDays"]:
        ym = day["date"][:7]
        por_mes[ym] = por_mes.get(ym, 0) + day["contributionCount"]

hoje = datetime.date.today()
chaves = []
y, m = hoje.year, hoje.month
for _ in range(12):
    chaves.append(f"{y:04d}-{m:02d}")
    m -= 1
    if m == 0:
        y, m = y - 1, 12
chaves.reverse()
valores = [por_mes.get(k, 0) for k in chaves]
total = sum(valores)
maior = max(valores) or 1

W, H = 420, 212
BASE, TOPO = 176, 64
slot = W / 12
barras = []
for i, (k, v) in enumerate(zip(chaves, valores)):
    h = max(2, (BASE - TOPO) * v / maior) if v else 2
    x = i * slot + 4
    barras.append(
        f'<rect x="{x:.1f}" y="{BASE - h:.1f}" width="{slot - 8:.1f}" height="{h:.1f}" rx="3" class="b"/>'
        f'<text x="{x + (slot - 8) / 2:.1f}" y="{BASE - h - 5:.1f}" class="n" text-anchor="middle">{v if v else ""}</text>'
        f'<text x="{x + (slot - 8) / 2:.1f}" y="{BASE + 16}" class="l" text-anchor="middle">{MESES[int(k[5:]) - 1]}</text>'
    )

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Contribuições por mês">
<style>
.h{{font:600 16px -apple-system,Segoe UI,Helvetica,Arial,sans-serif;fill:#1f2328}}
.s{{font:13px -apple-system,Segoe UI,Helvetica,Arial,sans-serif;fill:#59636e}}
.n{{font:11px -apple-system,Segoe UI,Helvetica,Arial,sans-serif;fill:#1f2328}}
.l{{font:11px -apple-system,Segoe UI,Helvetica,Arial,sans-serif;fill:#59636e}}
.b{{fill:#2da44e}}
@media (prefers-color-scheme: dark){{.h,.n{{fill:#e6edf3}}.s,.l{{fill:#9198a1}}.b{{fill:#3fb950}}}}
</style>
<text x="0" y="20" class="h">Contribuições por mês</text>
<text x="0" y="40" class="s">{total} contribuições nos últimos 12 meses</text>
{''.join(barras)}
</svg>
"""
os.makedirs("assets", exist_ok=True)
with open("assets/contributions.svg", "w", encoding="utf-8") as f:
    f.write(svg)
print(list(zip(chaves, valores)))
