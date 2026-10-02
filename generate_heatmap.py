import json

with open('calendar_data.json') as f:
    cal = json.load(f)

weeks = cal['weeks']

start_x = 72
start_y = 190
tile_size = 11
gap = 3

def get_base_color(count):
    if count == 0:
        return '#130E24'
    elif count < 5:
        return '#4C1D95'
    elif count < 15:
        return '#7C3AED'
    elif count < 35:
        return '#A855F7'
    else:
        return '#D946EF'

active_days = []
tiles_svg = []
months_labels = []
current_month = None

days_labels = [
    f'<text x="54" y="{start_y + 1 * 14 + 9}" fill="#71717A" font-size="9" font-family="monospace" text-anchor="end">Mon</text>',
    f'<text x="54" y="{start_y + 3 * 14 + 9}" fill="#71717A" font-size="9" font-family="monospace" text-anchor="end">Wed</text>',
    f'<text x="54" y="{start_y + 5 * 14 + 9}" fill="#71717A" font-size="9" font-family="monospace" text-anchor="end">Fri</text>'
]

month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

for w_idx, week in enumerate(weeks):
    x = start_x + w_idx * (tile_size + gap)
    first_day = week['contributionDays'][0]
    month_num = int(first_day['date'].split('-')[1])
    month_name = month_names[month_num - 1]
    if month_name != current_month and w_idx % 4 == 0:
        current_month = month_name
        months_labels.append(f'<text x="{x}" y="{start_y - 8}" fill="#71717A" font-size="10" font-family="monospace">{month_name}</text>')

    for d_idx, day in enumerate(week['contributionDays']):
        y = start_y + d_idx * (tile_size + gap)
        count = day['contributionCount']
        tid = f"tile_{w_idx}_{d_idx}"
        base_color = get_base_color(count)
        
        tile_data = {
            'x': x,
            'y': y,
            'count': count,
            'date': day['date'],
            'id': tid,
            'color': base_color
        }
        
        stroke = ''
        if count >= 40:
            stroke = ' stroke="#F472B6" stroke-width="1.2"'
        elif count >= 20:
            stroke = ' stroke="#C084FC" stroke-width="0.8"'

        opacity = '0.95' if count > 0 else '0.4'
        tiles_svg.append(f'<rect id="{tid}" x="{x}" y="{y}" width="{tile_size}" height="{tile_size}" rx="2.5" fill="{base_color}" opacity="{opacity}"{stroke}><title>{day["date"]}: {count} commits</title></rect>')
        
        if count > 0:
            active_days.append(tile_data)

active_days.sort(key=lambda d: d['date'])
total_active = len(active_days)

time_per_commit = (90.0 - 4.0) / total_active

hero_keyframes = []
hero_keyframes.append("0% { transform: translate(100px, 35px) scale(0.9) rotate(-25deg); opacity: 0; }")
hero_keyframes.append("3% { transform: translate(160px, 60px) scale(0.95) rotate(-15deg); opacity: 1; }")

tile_animations_css = []
web_keyframes = []

for i, day in enumerate(active_days):
    hit_time = 4.0 + (i + 1) * time_per_commit
    pre_hit_time = hit_time - (time_per_commit * 0.45)
    
    hx = day['x'] + 5
    hy = day['y'] - 12
    
    rot = -18 if i % 2 == 0 else 18
    hero_keyframes.append(f"{hit_time:.2f}% {{ transform: translate({hx}px, {hy}px) scale(0.95) rotate({rot}deg); opacity: 1; }}")
    
    web_keyframes.append(f"{pre_hit_time:.2f}% {{ x1: {hx - 25}; y1: {hy - 45}; x2: {day['x'] + 5}; y2: {day['y'] + 5}; opacity: 0.95; stroke-dashoffset: 0; }}")
    web_keyframes.append(f"{hit_time:.2f}% {{ x1: {hx}; y1: {hy}; x2: {day['x'] + 5}; y2: {day['y'] + 5}; opacity: 0; stroke-dashoffset: 80; }}")

    anim_name = f"vaporize_{day['id']}"
    tile_keyframes = f"""
    @keyframes {anim_name} {{
      0%, {hit_time - 0.2:.2f}% {{
        opacity: 0.95;
        fill: {day['color']};
        transform: scale(1);
      }}
      {hit_time:.2f}% {{
        opacity: 1;
        fill: #FFFFFF;
        filter: url(#laser-glow);
        transform: scale(1.4);
      }}
      {hit_time + 0.5:.2f}%, 96% {{
        opacity: 0.12;
        fill: #2E1065;
        transform: scale(0.85);
      }}
      98%, 100% {{
        opacity: 0.95;
        fill: {day['color']};
        transform: scale(1);
      }}
    }}
    #{day['id']} {{
      transform-origin: {day['x'] + 5}px {day['y'] + 5}px;
      animation: {anim_name} 16s ease-out infinite;
    }}"""
    tile_animations_css.append(tile_keyframes)

hero_keyframes.append("92% { transform: translate(840px, 35px) scale(0.95) rotate(-35deg); opacity: 1; }")
hero_keyframes.append("96%, 100% { transform: translate(890px, -20px) scale(0.85) rotate(-45deg); opacity: 0; }")

hero_keyframes_css = "\n      ".join(hero_keyframes)
all_tile_css = "\n".join(tile_animations_css)
web_keyframes_css = "\n      ".join(web_keyframes)

tiles_content = '\n    '.join(tiles_svg)
months_content = '\n    '.join(months_labels)
days_content = '\n    '.join(days_labels)

svg_output = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 330" width="100%" height="330">
  <defs>
    <!-- Purple Cyber Glow Filters -->
    <filter id="purple-glow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="3.5" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>

    <filter id="laser-glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="2.5" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>

    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#14092A" />
      <stop offset="100%" stop-color="#07050E" />
    </linearGradient>

    <!-- Stealth Violet Suit Gradients -->
    <linearGradient id="stealthSuit" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#A855F7" />
      <stop offset="100%" stop-color="#6B21A8" />
    </linearGradient>

    <linearGradient id="darkArmor" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1E1638" />
      <stop offset="100%" stop-color="#0A0614" />
    </linearGradient>

    <linearGradient id="laserTracer" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF" />
      <stop offset="50%" stop-color="#C084FC" />
      <stop offset="100%" stop-color="#A855F7" />
    </linearGradient>
  </defs>

  <style>
    @keyframes heroAscendingHunt {{
      {hero_keyframes_css}
    }}

    @keyframes webTracerFlight {{
      {web_keyframes_css}
    }}

    @keyframes beaconPulse {{
      0%, 100% {{ opacity: 1; transform: scale(1); }}
      50% {{ opacity: 0.35; transform: scale(0.9); }}
    }}

    @keyframes shockwaveSept8 {{
      0%, 46% {{ r: 2; opacity: 0; }}
      48% {{ r: 5; opacity: 1; stroke-width: 2.5; }}
      54% {{ r: 28; opacity: 0; stroke-width: 0.5; }}
      100% {{ opacity: 0; }}
    }}

    .hero-acrobat {{
      animation: heroAscendingHunt 16s cubic-bezier(0.4, 0.0, 0.2, 1) infinite;
    }}

    .web-tracer-line {{
      stroke: url(#laserTracer);
      stroke-width: 1.8;
      stroke-dasharray: 4, 1.5;
      animation: webTracerFlight 16s ease-out infinite;
    }}

    .pulse-beacon {{
      transform-origin: 8px 8px;
      animation: beaconPulse 2s ease-in-out infinite;
    }}

    .shockwave-burst {{
      animation: shockwaveSept8 16s ease-out infinite;
    }}

    {all_tile_css}
  </style>

  <!-- Container Box -->
  <rect x="0" y="0" width="900" height="330" rx="12" fill="url(#bgGrad)" stroke="#2E1065" stroke-width="1.2" />

  <!-- Background Cyber Mesh -->
  <g opacity="0.05" stroke="#C084FC" stroke-width="0.8">
    <line x1="0" y1="50" x2="900" y2="50" />
    <line x1="0" y1="165" x2="900" y2="165" />
    <line x1="70" y1="50" x2="70" y2="330" />
    <line x1="820" y1="50" x2="820" y2="330" />
    <path d="M0,0 L40,0 M0,0 L0,40 M0,0 L30,30" stroke-width="1.2" />
    <path d="M900,0 L860,0 M900,0 L900,40 M900,0 L870,30" stroke-width="1.2" />
  </g>

  <!-- HUD Header Section -->
  <g transform="translate(24, 28)">
    <circle cx="8" cy="8" r="4.5" fill="#A855F7" class="pulse-beacon" filter="url(#purple-glow)" />
    <circle cx="8" cy="8" r="8.5" fill="none" stroke="#A855F7" stroke-width="0.8" opacity="0.4" />

    <text x="24" y="12" fill="#F8FAFC" font-size="13" font-weight="700" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', monospace" letter-spacing="1">
      PATROL TELEMETRY // ASCENDING DISPATCH RADAR
    </text>

    <!-- Header Telemetry Tags -->
    <g transform="translate(555, -2)">
      <rect x="0" y="0" width="135" height="22" rx="4" fill="#170F2E" stroke="#3B1768" stroke-width="0.8" />
      <text x="12" y="15" fill="#C084FC" font-size="10.5" font-family="monospace" font-weight="600">⚡ 296 DISPATCHES</text>

      <rect x="145" y="0" width="145" height="22" rx="4" fill="#170F2E" stroke="#A855F7" stroke-width="0.8" />
      <text x="155" y="15" fill="#A855F7" font-size="10.5" font-family="monospace" font-weight="600">🎯 PEAK: 96 / DAY</text>
    </g>
  </g>

  <!-- Dynamic Web Tracer Line (Fires point-to-point in ascending chronological order) -->
  <line x1="0" y1="0" x2="0" y2="0" class="web-tracer-line" filter="url(#laser-glow)" />

  <!-- Sept 8 (96-commit) shockwave impact -->
  <circle cx="763" cy="223" r="2" fill="none" stroke="#D946EF" stroke-width="2" class="shockwave-burst" />
  <circle cx="763" cy="223" r="2" fill="none" stroke="#FFFFFF" stroke-width="1" class="shockwave-burst" style="animation-delay: 0.1s;" />

  <!-- Heatmap Calendar Grid -->
  <g id="heatmap-grid">
    {months_content}
    {days_content}
    {tiles_content}
  </g>

  <!-- The Acrobatic Hero (Cool, sleek, stealth-violet athletic silhouette) -->
  <g class="hero-acrobat" filter="url(#purple-glow)">
    <ellipse cx="0" cy="16" rx="12" ry="3.5" fill="#000000" opacity="0.4" />

    <g transform="translate(0, 0)">
      <!-- Right Arm (Gauntlet / Web Shooter) -->
      <path d="M5,-5 Q16,-12 22,-22" fill="none" stroke="url(#stealthSuit)" stroke-width="3.8" stroke-linecap="round" />
      <circle cx="22" cy="-22" r="2.8" fill="#FFFFFF" filter="url(#laser-glow)" />

      <!-- Left Arm (Dynamic balance) -->
      <path d="M-5,-3 Q-14,4 -20,10" fill="none" stroke="url(#darkArmor)" stroke-width="3.8" stroke-linecap="round" />
      <circle cx="-20" cy="10" r="2.5" fill="#7C3AED" />

      <!-- Athletic Legs in kinetic sprint/leap pose -->
      <path d="M-4,8 Q-14,12 -10,20" fill="none" stroke="url(#darkArmor)" stroke-width="4.2" stroke-linecap="round" />
      <path d="M-10,20 Q-7,24 -3,22" fill="none" stroke="url(#stealthSuit)" stroke-width="3.6" stroke-linecap="round" />

      <path d="M4,8 Q14,6 18,-2" fill="none" stroke="url(#darkArmor)" stroke-width="4.2" stroke-linecap="round" />
      <path d="M18,-2 Q22,-4 24,-2" fill="none" stroke="url(#stealthSuit)" stroke-width="3.6" stroke-linecap="round" />

      <!-- Torso Core -->
      <ellipse cx="0" cy="6" rx="6" ry="4.5" fill="url(#darkArmor)" />
      <path d="M-6,5 C-8,-2 -5,-9 0,-11 C5,-9 8,-2 6,5 Z" fill="url(#stealthSuit)" />

      <!-- Chest Spider Insignia (Violet neon geometric) -->
      <polygon points="0,-7 3,-3 0,-1 -3,-3" fill="#FFFFFF" opacity="0.9" />
      <path d="M-2,-5 L-6,-8 M2,-5 L6,-8 M-2,-2 L-6,-1 M2,-2 L6,-1" stroke="#FFFFFF" stroke-width="0.7" opacity="0.8" />

      <!-- Sleek Angular Mask -->
      <g transform="translate(0, -17)">
        <ellipse cx="0" cy="0" rx="7.2" ry="8.8" fill="url(#stealthSuit)" stroke="#6B21A8" stroke-width="0.7" />
        <!-- Angular Lenses (White with violet perimeter) -->
        <path d="M-1.2,-1.5 Q-4,-3.2 -5.8,-0.8 Q-3.5,3.2 -1.2,0.8 Z" fill="#FFFFFF" stroke="#07050E" stroke-width="1.4" stroke-linejoin="round" />
        <path d="M1.2,-1.5 Q4,-3.2 5.8,-0.8 Q3.5,3.2 1.2,0.8 Z" fill="#FFFFFF" stroke="#07050E" stroke-width="1.4" stroke-linejoin="round" />
      </g>
    </g>
  </g>

  <!-- Heatmap Legend -->
  <g transform="translate(680, 305)" font-family="monospace" font-size="9" fill="#71717A">
    <text x="0" y="8" text-anchor="end">Less</text>
    <rect x="8" y="0" width="8" height="8" rx="1.5" fill="#130E24" opacity="0.5" />
    <rect x="20" y="0" width="8" height="8" rx="1.5" fill="#4C1D95" opacity="0.9" />
    <rect x="32" y="0" width="8" height="8" rx="1.5" fill="#7C3AED" opacity="0.9" />
    <rect x="44" y="0" width="8" height="8" rx="1.5" fill="#A855F7" opacity="0.9" />
    <rect x="56" y="0" width="8" height="8" rx="1.5" fill="#D946EF" opacity="1" stroke="#F472B6" stroke-width="1" />
    <text x="72" y="8">Burst</text>
  </g>
</svg>'''

with open('patrol-heatmap.svg', 'w') as f:
    f.write(svg_output)

print('Generated patrol-heatmap.svg with ascending chronological commit hunt and disappearing tiles!')
