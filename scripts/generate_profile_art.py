#!/usr/bin/env python3
import json, os, urllib.request, datetime
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
USERNAME = os.environ.get("USERNAME", "NIKHIL2K5")
TOKEN = os.environ.get("GITHUB_TOKEN")
if not TOKEN:
    raise SystemExit("GITHUB_TOKEN is required.")

query = '''
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { contributionCount date weekday } }
      }
    }
  }
}
'''
today = datetime.date.today()
start = datetime.date(today.year, 1, 1)
payload = {"query": query, "variables": {
    "login": USERNAME,
    "from": start.isoformat() + "T00:00:00Z",
    "to": today.isoformat() + "T23:59:59Z",
}}
req = urllib.request.Request("https://api.github.com/graphql",
    data=json.dumps(payload).encode(),
    headers={"Authorization": "Bearer " + TOKEN, "Content-Type": "application/json",
             "User-Agent": "Nikhil-GitHub-Profile-Art"})
with urllib.request.urlopen(req, timeout=30) as response:
    result = json.loads(response.read().decode())
if result.get("errors"):
    raise SystemExit(json.dumps(result["errors"], indent=2))
user = result["data"]["user"]
if not user:
    raise SystemExit("GitHub user not found: " + USERNAME)
calendar = user["contributionsCollection"]["contributionCalendar"]
weeks = calendar["weeks"]
days = [d for week in weeks for d in week["contributionDays"]]
total = calendar["totalContributions"]

day_map = {datetime.date.fromisoformat(d["date"]): d["contributionCount"] for d in days}
cursor = today
if day_map.get(cursor, 0) == 0:
    cursor -= datetime.timedelta(days=1)
streak = 0
while day_map.get(cursor, 0) > 0:
    streak += 1
    cursor -= datetime.timedelta(days=1)

cell, gap, left, top = 11, 4, 26, 45
width, height = left * 2 + len(weeks) * (cell + gap), 145
svg = [
 f'<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 {width} {height}" role="img" aria-label="GitHub contributions for {escape(USERNAME)}">',
 '<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#071426"/><stop offset="1" stop-color="#0d1117"/></linearGradient></defs>',
 f'<rect width="{width}" height="{height}" rx="12" fill="url(#bg)" stroke="#173451"/>',
 f'<text x="{left}" y="24" fill="#e6edf3" font-family="monospace" font-size="13" font-weight="bold">{escape(USERNAME)}@github:~$ contributions --year {today.year}</text>'
]
seen = set()
for col, week in enumerate(weeks):
    for day in week["contributionDays"]:
        date = datetime.date.fromisoformat(day["date"])
        if date.month not in seen and date.day <= 7:
            svg.append(f'<text x="{left+col*(cell+gap)}" y="39" fill="#79c0ff" font-family="monospace" font-size="9">{date.strftime("%b")}</text>')
            seen.add(date.month)
        count, weekday = day["contributionCount"], int(day["weekday"])
        palette = ["#101b2b", "#123b68", "#075ea8", "#1687d9", "#4cc9ff"]
        level = 0 if count == 0 else min(4, 1 + (count >= 2) + (count >= 5) + (count >= 10))
        x, y = left + col*(cell+gap), top + weekday*(cell+gap)
        delay = col * 10 + weekday * 20
        svg.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2" fill="{palette[level]}" stroke="#1c3856" stroke-width=".4"><title>{escape(day["date"])}: {count} contributions</title><animate attributeName="opacity" values="0.25;1;1" dur="1.2s" begin="{delay}ms" fill="freeze"/></rect>')
svg += [f'<text x="{left}" y="{height-8}" fill="#8b949e" font-family="monospace" font-size="10">{total:,} contributions this year</text>', '</svg>']
(ROOT / "contrib-heatmap.svg").write_text("\n".join(svg), encoding="utf-8")

stats = f'''<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 520 210" role="img" aria-label="GitHub stats for {escape(USERNAME)}">
<defs><linearGradient id="card" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#08192b"/><stop offset="1" stop-color="#111827"/></linearGradient><linearGradient id="cyan"><stop stop-color="#00d9ff"/><stop offset="1" stop-color="#7c3aed"/></linearGradient></defs>
<rect x="1" y="1" width="518" height="208" rx="14" fill="url(#card)" stroke="#164e73"/>
<text x="24" y="34" fill="#00d9ff" font-family="monospace" font-size="14">nikhil@github ~ $ stats --year {today.year}</text>
<text x="24" y="82" fill="#8b949e" font-family="monospace" font-size="12">CONTRIBUTIONS THIS YEAR</text>
<text x="24" y="122" fill="#f0f6fc" font-family="monospace" font-size="34" font-weight="bold">{total:,}</text>
<rect x="24" y="140" width="472" height="3" rx="2" fill="#1f2937"/>
<rect x="24" y="140" width="{max(4,min(472,int(472*min(total,2000)/2000)))}" height="3" rx="2" fill="url(#cyan)"/>
<text x="24" y="174" fill="#8b949e" font-family="monospace" font-size="12">CURRENT STREAK</text>
<text x="24" y="197" fill="#00d9ff" font-family="monospace" font-size="19" font-weight="bold">{streak} day{'s' if streak != 1 else ''}</text>
<text x="496" y="197" fill="#8b949e" font-family="monospace" font-size="10" text-anchor="end">AUTO-UPDATED DAILY</text></svg>'''
(ROOT / "stats.svg").write_text(stats, encoding="utf-8")

try:
    from PIL import Image
    photo = Image.open(ROOT / "nikhil-cyber-portrait-blue.png").convert("L").resize((72, 44))
    chars = " .:-=+*#%@"
    pixels = list(photo.getdata())
    rows = []
    for r in range(44):
        line = "".join(chars[min(len(chars)-1, pixels[r*72+c]*len(chars)//256)] for c in range(72))
        rows.append(f'<text x="10" y="{22+r*10}" fill="#42d9ff" font-family="monospace" font-size="8" xml:space="preserve">{escape(line)}</text>')
    (ROOT / "nikhil-ascii.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" width="100%" viewBox="0 0 600 470"><rect width="600" height="470" rx="12" fill="#07111f" stroke="#164e73"/>' + "".join(rows) + '</svg>', encoding="utf-8")
except ImportError:
    print("Pillow unavailable; skipping ASCII portrait.")
