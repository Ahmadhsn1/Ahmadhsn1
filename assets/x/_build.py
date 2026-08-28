#!/usr/bin/env python3
"""Header / divider / language-mix / footer SVGs for the profile README.
Reference style: glowing wordmark, faint node motif, one reusable divider.
Blue/cyan theme. Minimal ambient motion — a light sweep across each wordmark,
a blinking caret, a slow drift on the node dots with one bead travelling an
edge, and a sweep + pulse on the divider. Everything freezes under
prefers-reduced-motion; the markdown body never moves."""
import os, html

def e(s):
    return html.escape(str(s), quote=True)

OUT = os.path.dirname(os.path.abspath(__file__))
os.makedirs(OUT, exist_ok=True)
W = 1200
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
MONO = "'SFMono-Regular', ui-monospace, 'JetBrains Mono', Menlo, Consolas, monospace"
BG = "#0B1220"
CY, BL = "#38BDF8", "#2563EB"
INK, MID, LO = "#EAF1FB", "#9DB2D2", "#5C6F91"


def write(name, s):
    open(os.path.join(OUT, name), "w").write(s)
    print("wrote", name, len(s))


# node dots + connecting lines that live faintly in the banner corners
_PTS = [(120, 60), (250, 120), (170, 200), (1010, 70), (1090, 150), (900, 40)]
_LINKS = [(0, 1), (1, 2), (3, 4), (3, 5)]
NODES = "".join(
    f'<circle cx="{x}" cy="{y}" r="{r}" fill="#38BDF8" fill-opacity="{o}"/>'
    for (x, y), r, o in zip(_PTS, [2.5, 2, 2, 2.5, 2, 2], [.5, .35, .3, .5, .35, .4])
)
EDGES = "".join(
    f'<line x1="{_PTS[a][0]}" y1="{_PTS[a][1]}" x2="{_PTS[b][0]}" y2="{_PTS[b][1]}" '
    f'stroke="#38BDF8" stroke-opacity="0.12" stroke-width="1" stroke-dasharray="2 6"/>'
    for a, b in _LINKS
)
# one bead travelling the first edge, via SMIL (widely supported in <img> SVG)
BEAD = (f'<circle r="2.4" fill="#BFE8FF" fill-opacity="0.9">'
        f'<animateMotion dur="6s" repeatCount="indefinite" keyPoints="0;1;1" keyTimes="0;0.55;1" '
        f'calcMode="spline" keySplines="0.4 0 0.2 1;0 0 1 1" '
        f'path="M{_PTS[3][0]},{_PTS[3][1]} L{_PTS[4][0]},{_PTS[4][1]}"/></circle>')


def banner(name, sub, h, sub2=None, caret=False):
    big = 66 if len(name) < 16 else 52
    y = h // 2 - 14
    nm, sb = e(name), e(sub)
    ls = f"{big * 0.14:.0f}"
    extra = (f'<text x="{W/2}" y="{y+62}" text-anchor="middle" font-family="{MONO}" '
             f'font-size="12" letter-spacing="1" fill="{LO}">{e(sub2)}</text>') if sub2 else ""
    cw = round(len(name) * big * 0.60 + (len(name) - 1) * float(ls))   # rough wordmark width
    caret_el = (f'<rect class="caret" x="{W/2 + cw/2 + 22:.0f}" y="{y-big*0.72:.0f}" '
                f'width="5" height="{big*0.78:.0f}" rx="1" fill="{CY}"/>') if caret else ""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}" font-family="{FONT}" role="img" aria-label="{nm} - {sb}">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0A0F1C"/><stop offset="0.5" stop-color="{BG}"/><stop offset="1" stop-color="#0A1428"/></linearGradient>
<radialGradient id="glow" cx="0.5" cy="0.42" r="0.55"><stop offset="0" stop-color="{BL}" stop-opacity="0.55"/><stop offset="0.55" stop-color="{BL}" stop-opacity="0.12"/><stop offset="1" stop-color="{BL}" stop-opacity="0"/></radialGradient>
<linearGradient id="wm" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#7DD3FC"/><stop offset="0.5" stop-color="{CY}"/><stop offset="1" stop-color="#818CF8"/></linearGradient>
<linearGradient id="sheen" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/><stop offset="0.5" stop-color="#FFFFFF" stop-opacity="0.5"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>
<linearGradient id="bar" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{BL}" stop-opacity="0"/><stop offset="0.45" stop-color="{CY}"><animate attributeName="offset" values="0.30;0.62;0.30" dur="7s" repeatCount="indefinite"/></stop><stop offset="1" stop-color="{BL}" stop-opacity="0"/></linearGradient>
<filter id="soft" x="-30%" y="-60%" width="160%" height="220%"><feGaussianBlur stdDeviation="7"/></filter>
<clipPath id="clip"><rect width="{W}" height="{h}" rx="16"/></clipPath>
<clipPath id="wmclip"><text x="{W/2}" y="{y}" text-anchor="middle" font-size="{big}" font-weight="800" letter-spacing="{ls}">{nm}</text></clipPath>
<style>
@keyframes glow{{0%,100%{{opacity:.5}}50%{{opacity:.85}}}}
@keyframes sweep{{0%{{transform:translateX(-460px)}}62%,100%{{transform:translateX({W+220}px)}}}}
@keyframes blink{{0%,48%{{opacity:1}}52%,100%{{opacity:0}}}}
@keyframes drift{{0%,100%{{transform:translate(0,0)}}50%{{transform:translate(6px,-4px)}}}}
.glow{{animation:glow 7s ease-in-out infinite}}
.sheen{{animation:sweep 6s ease-in-out infinite}}
.caret{{animation:blink 1.05s step-end infinite}}
.drift{{animation:drift 16s ease-in-out infinite}}
@media(prefers-reduced-motion:reduce){{.glow,.sheen,.caret,.drift{{animation:none}}.caret{{opacity:1}}}}
</style>
</defs>
<g clip-path="url(#clip)">
<rect width="{W}" height="{h}" fill="url(#bg)"/>
<ellipse class="glow" cx="{W/2}" cy="{h*0.44}" rx="520" ry="{h*0.7}" fill="url(#glow)"/>
<g class="drift">{EDGES}{NODES}{BEAD if sub2 else ""}</g>
<text x="{W/2}" y="{y}" text-anchor="middle" font-size="{big}" font-weight="800" letter-spacing="{ls}" fill="url(#wm)" filter="url(#soft)" opacity="0.5">{nm}</text>
<text x="{W/2}" y="{y}" text-anchor="middle" font-size="{big}" font-weight="800" letter-spacing="{ls}" fill="url(#wm)">{nm}</text>
<g clip-path="url(#wmclip)"><rect class="sheen" x="-220" y="0" width="180" height="{h}" fill="url(#sheen)"/></g>
{caret_el}
<text x="{W/2}" y="{y+34}" text-anchor="middle" font-size="13.5" font-weight="600" letter-spacing="4" fill="{MID}">{sb}</text>
{extra}
<rect x="0" y="{h-3}" width="{W}" height="3" fill="url(#bar)"/>
</g>
</svg>
'''


def divider():
    h = 34
    cx = W / 2
    write("divider.svg", f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}" role="img" aria-label="">
<defs>
<linearGradient id="l" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CY}" stop-opacity="0"/><stop offset="0.5" stop-color="{CY}" stop-opacity="0.5"/><stop offset="1" stop-color="{CY}" stop-opacity="0"/></linearGradient>
<linearGradient id="hi" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CY}" stop-opacity="0"/><stop offset="0.5" stop-color="#CFEEFF" stop-opacity="0.9"/><stop offset="1" stop-color="{CY}" stop-opacity="0"/></linearGradient>
<clipPath id="band"><rect x="0" y="{h/2-1.5}" width="{W}" height="3"/></clipPath>
<style>
@keyframes dsweep{{0%{{transform:translateX(-260px)}}58%,100%{{transform:translateX({W+120}px)}}}}
@keyframes dpulse{{0%,100%{{opacity:.65;transform:scale(1)}}50%{{opacity:1;transform:scale(1.14)}}}}
.dsweep{{animation:dsweep 5.5s ease-in-out infinite}}
.dpulse{{transform-box:fill-box;transform-origin:center;animation:dpulse 4s ease-in-out infinite}}
@media(prefers-reduced-motion:reduce){{.dsweep,.dpulse{{animation:none}}}}
</style>
</defs>
<rect x="0" y="{h/2-0.5}" width="{W}" height="1" fill="url(#l)"/>
<g clip-path="url(#band)"><rect class="dsweep" x="-220" y="{h/2-1.5}" width="200" height="3" fill="url(#hi)"/></g>
<rect class="dpulse" x="{cx-4}" y="{h/2-4}" width="8" height="8" fill="{BG}" stroke="{CY}" stroke-opacity="0.8" stroke-width="1.2" transform="rotate(45 {cx} {h/2})"/>
</svg>
''')


def langmix():
    h = 148
    segs = [("TypeScript", 34, "#3178C6"), ("JavaScript", 22, "#C9B037"), ("Kotlin", 14, "#7F52FF"),
            ("Java", 14, "#E76F00"), ("Python", 12, "#4B8BBE"), ("SQL / PLpgSQL", 4, "#3ECF8E")]
    g = [f'<text x="40" y="34" font-size="13" font-weight="700" letter-spacing="2" fill="{INK}">LANGUAGE MIX</text>',
         f'<text x="{W-40}" y="34" text-anchor="end" font-size="11.5" fill="{LO}">approximate share of code across every repository</text>']
    x, total = 40, W - 80
    for _, pct, col in segs:
        w = round(total * pct / 100)
        g.append(f'<rect x="{x}" y="52" width="{w-2}" height="12" rx="2" fill="{col}"/>')
        x += w
    lx = 40
    for nm, pct, col in segs:
        g.append(f'<circle cx="{lx+4}" cy="90" r="3.5" fill="{col}"/><text x="{lx+14}" y="94" font-size="12.5" fill="{MID}">{nm} {pct}%</text>')
        lx += len(nm) * 7.3 + 58
    g.append(f'<rect x="40" y="112" width="{W-80}" height="1" fill="#1C2842"/>')
    g.append(f'<text x="40" y="134" font-size="12.5" fill="{LO}">9 projects    ·    live on the App Store &amp; Google Play    ·    10,000+ app users    ·    an AI booking assistant, 15 tools</text>')
    write("language-mix.svg", f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}" font-family="{FONT}" role="img" aria-label="Language mix and project metrics">
<defs><clipPath id="c"><rect width="{W}" height="{h}" rx="16"/></clipPath></defs>
<g clip-path="url(#c)"><rect width="{W}" height="{h}" fill="{BG}"/>{"".join(g)}</g>
<rect x="0.5" y="0.5" width="{W-1}" height="{h-1}" rx="15.5" fill="none" stroke="{CY}" stroke-opacity="0.12"/>
</svg>
''')


write("hero-banner.svg", banner("AHMAD HASSAN", "AI SYSTEMS ENGINEER", 260,
                                sub2="LLM products, end to end  ·  RAG  ·  agents  ·  multi-tenant data isolation",
                                caret=True))
write("footer-banner.svg", banner("LET’S BUILD SOMETHING",
                                  "OPEN TO AI ENGINEERING & FULL-STACK ROLES — REMOTE OR LAHORE", 150))
divider()
langmix()
print("done")
