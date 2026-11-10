import os, json, urllib.request
from xml.sax.saxutils import escape

USER = os.environ.get("GH_USER", "akhilreddy59")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
PAPER, INK, ORG, MUS, RED = "#FFFBF2", "#1F1410", "#FF6B1A", "#FFB627", "#C2410C"

def get(url):
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": "langs-card"})
    if TOKEN: req.add_header("Authorization", f"Bearer {TOKEN}")
    with urllib.request.urlopen(req, timeout=30) as r: return json.load(r)

repos = get(f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner")
totals = {}
for r in repos:
    if r.get("fork"): continue
    for lang, n in get(r["languages_url"]).items():
        totals[lang] = totals.get(lang, 0) + n
top = sorted(totals.items(), key=lambda kv: -kv[1])[:6]
total = sum(totals.values()) or 1

rows, fills = "", [ORG, MUS, RED, ORG, MUS, RED]
H = 70 + len(top) * 40 + 16
for i, (lang, n) in enumerate(top):
    y = 70 + i * 40; pct = n / total * 100; w = max(8, 600 * pct / 100 * (100 / (top[0][1] / total * 100)))
    w = min(w, 600)
    rows += f'''<text x="40" y="{y+20}" font-size="16" font-weight="700" fill="{INK}" font-family="'Courier New',Courier,monospace">{escape(lang)}</text>
<rect x="230" y="{y+3}" width="600" height="24" rx="12" fill="{PAPER}" stroke="{INK}" stroke-width="2.5"/>
<rect class="b" style="animation-delay:{i*0.12:.2f}s" x="232" y="{y+5}" width="{w-4:.0f}" height="20" rx="10" fill="{fills[i]}" stroke="{INK}" stroke-width="2"/>
<text x="860" y="{y+20}" font-size="16" font-weight="700" fill="{RED}" font-family="'Courier New',Courier,monospace">{pct:.1f}%</text>'''

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 {H+8}" width="1000" height="{H+8}" role="img" aria-label="Most used languages">
<style>.b{{transform-box:fill-box;transform-origin:left center;animation:g 1.1s cubic-bezier(.2,.9,.2,1) backwards}}@keyframes g{{from{{transform:scaleX(0)}}}}@media (prefers-reduced-motion:reduce){{.b{{animation:none}}}}</style>
<rect x="11" y="11" width="984" height="{H-8}" rx="16" fill="{ORG}" stroke="{INK}" stroke-width="3"/>
<rect x="3" y="3" width="984" height="{H-8}" rx="16" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>
<text x="40" y="46" font-size="24" font-weight="900" fill="{INK}" font-family="Georgia,serif">Most used languages</text>
<text x="950" y="44" text-anchor="end" font-size="13" fill="{RED}" font-family="'Courier New',Courier,monospace">auto-updated daily</text>
{rows}</svg>'''
os.makedirs("assets", exist_ok=True)
open("assets/languages.svg", "w").write(svg)
print("wrote assets/languages.svg", top)
