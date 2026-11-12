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

rows = ""
H = 74 + len(top) * 34 + 14
for i, (lang, n) in enumerate(top):
    y = 70 + i * 34; pct = n / total * 100
    w = max(4, 700 * (n / top[0][1]))
    cls = "ac" if i == 0 else "ins2"
    rows += f'''<text class="tx" x="28" y="{y+14}" font-size="14" font-family="-apple-system,'Segoe UI',Inter,Helvetica,Arial,sans-serif">{escape(lang)}</text>
<rect x="190" y="{y+7}" width="700" height="6" rx="3" class="tr"/>
<rect class="b {cls}" style="animation-delay:{i*0.1:.1f}s" x="190" y="{y+7}" width="{w:.0f}" height="6" rx="3"/>
<text class="mu" x="972" y="{y+14}" text-anchor="end" font-size="13" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace">{pct:.1f}%</text>'''

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 {H}" width="1000" height="{H}" role="img" aria-label="Most used languages">
<style>.tx{{fill:#111}}.mu{{fill:#6B6B6B}}.ac{{fill:#E8590C}}.ins2{{fill:#111}}.tr{{fill:#EFECE6}}.cf{{fill:#FAFAF8}}.bd{{stroke:#E4E1DB}}
@media (prefers-color-scheme:dark){{.tx{{fill:#F2EFEA}}.mu{{fill:#9A9A9F}}.ac{{fill:#FF7A2E}}.ins2{{fill:#F2EFEA}}.tr{{fill:#23252B}}.cf{{fill:#12141A}}.bd{{stroke:#2B2D33}}}}
.b{{transform-box:fill-box;transform-origin:left center;animation:g 1s cubic-bezier(.2,.9,.2,1) backwards}}@keyframes g{{from{{transform:scaleX(0)}}}}@media (prefers-reduced-motion:reduce){{.b{{animation:none}}}}</style>
<rect x=".5" y=".5" width="999" height="{H-1}" rx="14" class="cf bd" stroke-width="1"/>
<text class="mu" x="28" y="40" font-size="12" letter-spacing="2.4" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace">MOST USED LANGUAGES</text>
{rows}</svg>'''
os.makedirs("assets", exist_ok=True)
open("assets/languages.svg", "w").write(svg)
print("wrote assets/languages.svg", top)
