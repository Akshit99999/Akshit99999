import json

with open('calendar_data.json') as f:
    cal = json.load(f)

weeks = cal['weeks']

def get_color(count):
    if count == 0:
        return '#161B22'
    elif count < 5:
        return '#0D419D'
    elif count < 15:
        return '#007ACC'
    elif count < 35:
        return '#E23636'
    else:
        return '#FF4655'

start_x = 72
start_y = 190
tile_size = 11
gap = 3

tiles_svg = []
months_labels = []
current_month = None

# Day names
days_labels = [
    f'<text x="54" y="{start_y + 1 * 14 + 9}" fill="#64748B" font-size="9" font-family="monospace" text-anchor="end">Mon</text>',
    f'<text x="54" y="{start_y + 3 * 14 + 9}" fill="#64748B" font-size="9" font-family="monospace" text-anchor="end">Wed</text>',
    f'<text x="54" y="{start_y + 5 * 14 + 9}" fill="#64748B" font-size="9" font-family="monospace" text-anchor="end">Fri</text>'
]

month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

for w_idx, week in enumerate(weeks):
    x = start_x + w_idx * (tile_size + gap)
    # Check first day of week for month label
    first_day = week['contributionDays'][0]
    month_num = int(first_day['date'].split('-')[1])
    month_name = month_names[month_num - 1]
    if month_name != current_month and w_idx % 4 == 0:
        current_month = month_name
        months_labels.append(f'<text x="{x}" y="{start_y - 8}" fill="#64748B" font-size="10" font-family="monospace">{month_name}</text>')

    for d_idx, day in enumerate(week['contributionDays']):
        y = start_y + d_idx * (tile_size + gap)
        count = day['contributionCount']
        color = get_color(count)
        opacity = '0.95' if count > 0 else '0.45'
        stroke = ''
        if count >= 40:
            stroke = ' stroke="#FFD700" stroke-width="1.2" filter="url(#gold-glow)"'
        elif count >= 20:
            stroke = ' stroke="#FF4655" stroke-width="1"'
        
        tiles_svg.append(f'<rect x="{x}" y="{y}" width="{tile_size}" height="{tile_size}" rx="2.5" fill="{color}" opacity="{opacity}"{stroke}><title>{day["date"]}: {count} commits</title></rect>')

tiles_content = '\n    '.join(tiles_svg)
months_content = '\n    '.join(months_labels)
days_content = '\n    '.join(days_labels)

svg_template = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 330" width="100%" height="330">
  <defs>
    <!-- Glowing filters -->
    <filter id="crimson-glow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="3" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>

    <filter id="gold-glow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="2.5" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>

    <filter id="web-glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="1.5" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>

    <!-- Linear Gradients -->
    <linearGradient id="panelGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#0F172A" />
      <stop offset="100%" stop-color="#0A0D14" />
    </linearGradient>

    <linearGradient id="suitRed" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FF4655" />
      <stop offset="100%" stop-color="#B81424" />
    </linearGradient>

    <linearGradient id="suitBlue" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0F4C81" />
      <stop offset="100%" stop-color="#0A2540" />
    </linearGradient>

    <linearGradient id="laserWeb" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF" />
      <stop offset="40%" stop-color="#00E5FF" />
      <stop offset="100%" stop-color="#FF4655" />
    </linearGradient>
  </defs>

  <style>
    /* Hero acrobatic swing choreography */
    @keyframes heroMasterRoutine {{
      0% {{
        transform: translate(60px, 35px) rotate(-35deg) scale(0.95);
        opacity: 0;
      }}
      4% {{
        opacity: 1;
      }}
      22% {{
        /* Bottom of first swing */
        transform: translate(280px, 125px) rotate(15deg) scale(1);
      }}
      32% {{
        /* Airborne release & apex */
        transform: translate(440px, 50px) rotate(180deg) scale(1.05);
      }}
      42% {{
        /* 360 flip in mid-air */
        transform: translate(560px, 65px) rotate(360deg) scale(1);
      }}
      52% {{
        /* Web shot anchor pull towards Sept 8 spike (x:756, y:213) */
        transform: translate(660px, 115px) rotate(390deg) scale(1);
      }}
      66% {{
        /* Superhero crouch touchdown on the commit peak */
        transform: translate(756px, 168px) rotate(360deg) scale(0.9);
      }}
      78% {{
        /* Scuttle/slide across the active days to Sept 30 spike */
        transform: translate(798px, 172px) rotate(355deg) scale(0.9);
      }}
      88% {{
        /* Launch upwards into the ceiling */
        transform: translate(840px, 30px) rotate(320deg) scale(1);
        opacity: 1;
      }}
      94%, 100% {{
        transform: translate(890px, -20px) rotate(310deg) scale(0.85);
        opacity: 0;
      }}
    }}

    /* Web 1: Ceiling to Hero hand during first swing */
    @keyframes webStrand1 {{
      0% {{
        x1: 220; y1: 0;
        x2: 60; y2: 35;
        opacity: 0;
      }}
      4% {{
        opacity: 0.9;
      }}
      22% {{
        x1: 220; y1: 0;
        x2: 280; y2: 125;
        opacity: 0.9;
      }}
      26%, 100% {{
        x1: 220; y1: 0;
        x2: 320; y2: 110;
        opacity: 0;
      }}
    }}

    /* Web 2: Fired at Sept 8 peak (756, 213) */
    @keyframes webStrand2 {{
      0%, 41% {{
        opacity: 0;
        stroke-dashoffset: 400;
      }}
      43% {{
        x1: 560; y1: 65;
        x2: 756; y2: 213;
        opacity: 1;
        stroke-dashoffset: 0;
      }}
      52% {{
        x1: 660; y1: 115;
        x2: 756; y2: 213;
        opacity: 1;
      }}
      65% {{
        x1: 750; y1: 165;
        x2: 756; y2: 213;
        opacity: 0.8;
      }}
      68%, 100% {{
        opacity: 0;
      }}
    }}

    /* Web 3: Vault zip-line off the Sept 30 spike into the night */
    @keyframes webStrand3 {{
      0%, 78% {{
        opacity: 0;
      }}
      80% {{
        x1: 798; y1: 172;
        x2: 870; y2: 0;
        opacity: 1;
      }}
      88% {{
        x1: 840; y1: 30;
        x2: 870; y2: 0;
        opacity: 1;
      }}
      92%, 100% {{
        opacity: 0;
      }}
    }}

    /* Shockwave ring at 96-commit spike on impact */
    @keyframes shockwavePulse {{
      0%, 50% {{
        r: 2;
        opacity: 0;
      }}
      52% {{
        r: 4;
        opacity: 1;
        stroke-width: 2.5;
      }}
      66% {{
        r: 24;
        opacity: 0;
        stroke-width: 0.5;
      }}
      100% {{
        opacity: 0;
      }}
    }}

    /* Kinetic Snake slithering along the contribution floor */
    @keyframes snakeRoam {{
      0% {{
        transform: translate(75px, 205px);
      }}
      25% {{
        transform: translate(250px, 218px);
      }}
      50% {{
        transform: translate(450px, 205px);
      }}
      75% {{
        transform: translate(650px, 233px);
      }}
      90% {{
        transform: translate(800px, 218px);
      }}
      100% {{
        transform: translate(75px, 205px);
      }}
    }}

    /* Pulsing status beacon */
    @keyframes radarBlink {{
      0%, 100% {{ opacity: 1; }}
      50% {{ opacity: 0.3; }}
    }}

    .hero-rig {{
      animation: heroMasterRoutine 9s cubic-bezier(0.42, 0, 0.58, 1) infinite;
    }}
    .web-line-1 {{
      stroke: url(#laserWeb);
      stroke-width: 1.5;
      stroke-dasharray: 4, 1.5;
      animation: webStrand1 9s ease-in-out infinite;
    }}
    .web-line-2 {{
      stroke: url(#laserWeb);
      stroke-width: 2;
      stroke-dasharray: 300;
      animation: webStrand2 9s cubic-bezier(0.2, 0.8, 0.4, 1) infinite;
    }}
    .web-line-3 {{
      stroke: url(#laserWeb);
      stroke-width: 1.8;
      stroke-dasharray: 4, 1.5;
      animation: webStrand3 9s ease-out infinite;
    }}
    .spike-shockwave {{
      animation: shockwavePulse 9s ease-out infinite;
    }}
    .snake-rig {{
      animation: snakeRoam 14s linear infinite;
    }}
    .radar-dot {{
      animation: radarBlink 1.8s ease-in-out infinite;
    }}
  </style>

  <!-- Main Background Container -->
  <rect x="0" y="0" width="900" height="330" rx="12" fill="url(#panelGrad)" stroke="#1E293B" stroke-width="1.2" />

  <!-- Subtle High-Tech HUD Grid in Background -->
  <g opacity="0.06" stroke="#FFFFFF" stroke-width="0.8">
    <line x1="0" y1="50" x2="900" y2="50" />
    <line x1="0" y1="165" x2="900" y2="165" />
    <line x1="70" y1="50" x2="70" y2="330" />
    <line x1="820" y1="50" x2="820" y2="330" />
    <!-- Subtle corner webs -->
    <path d="M0,0 L40,0 M0,0 L0,40 M0,0 L30,30" stroke-width="1" />
    <path d="M900,0 L860,0 M900,0 L900,40 M900,0 L870,30" stroke-width="1" />
  </g>

  <!-- HUD Header Section -->
  <g transform="translate(24, 28)">
    <!-- Radar Status Dot -->
    <circle cx="8" cy="8" r="4.5" fill="#FF4655" class="radar-dot" filter="url(#crimson-glow)" />
    <circle cx="8" cy="8" r="8" fill="none" stroke="#FF4655" stroke-width="0.8" opacity="0.4" />

    <!-- Header Titles -->
    <text x="24" y="12" fill="#F8FAFC" font-size="13" font-weight="700" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', monospace" letter-spacing="1">
      PATROL TELEMETRY // REAL-TIME DISPATCH HEATMAP
    </text>

    <!-- Telemetry Badges Right -->
    <g transform="translate(560, -2)">
      <rect x="0" y="0" width="130" height="22" rx="4" fill="#161B22" stroke="#30363D" stroke-width="0.8" />
      <text x="10" y="15" fill="#38BDF8" font-size="10.5" font-family="monospace" font-weight="600">⚡ 296 DISPATCHES</text>

      <rect x="140" y="0" width="145" height="22" rx="4" fill="#161B22" stroke="#FF4655" stroke-width="0.8" />
      <text x="150" y="15" fill="#FF4655" font-size="10.5" font-family="monospace" font-weight="600">🎯 PEAK: 96 IN A DAY</text>
    </g>
  </g>

  <!-- Dynamic Animated Web Lines -->
  <line x1="0" y1="0" x2="0" y2="0" class="web-line-1" filter="url(#web-glow)" />
  <line x1="0" y1="0" x2="0" y2="0" class="web-line-2" filter="url(#web-glow)" />
  <line x1="0" y1="0" x2="0" y2="0" class="web-line-3" filter="url(#web-glow)" />

  <!-- Shockwave ripple on the 96-commit spike (756, 213) -->
  <circle cx="762" cy="218" r="2" fill="none" stroke="#FF4655" stroke-width="2" class="spike-shockwave" />
  <circle cx="762" cy="218" r="2" fill="none" stroke="#FFD700" stroke-width="1.5" class="spike-shockwave" style="animation-delay: 0.15s;" />

  <!-- Heatmap Calendar Grid (Real Data: 53 weeks x 7 days) -->
  <g id="heatmap-grid">
    <!-- Month Labels -->
    {months_content}

    <!-- Day of Week Labels -->
    {days_content}

    <!-- Tiles -->
    {tiles_content}
  </g>

  <!-- Kinetic Snake Roaming along the Heatmap Grid -->
  <g class="snake-rig" opacity="0.95">
    <!-- Tail segments -->
    <rect x="-30" y="0" width="8" height="8" rx="2" fill="#0D419D" opacity="0.4" />
    <rect x="-18" y="0" width="9" height="9" rx="2" fill="#007ACC" opacity="0.6" />
    <rect x="-6" y="-0.5" width="10" height="10" rx="2.5" fill="#E23636" opacity="0.85" />
    <!-- Snake Head -->
    <rect x="6" y="-1.5" width="12" height="12" rx="3" fill="#FF4655" stroke="#FFFFFF" stroke-width="1.2" filter="url(#crimson-glow)" />
    <!-- Eyes -->
    <circle cx="14" cy="2" r="1.2" fill="#FFFFFF" />
    <circle cx="14" cy="7" r="1.2" fill="#FFFFFF" />
  </g>

  <!-- The Agile Hero Vector Acrobat Rig -->
  <g class="hero-rig" filter="url(#crimson-glow)">
    <!-- Suit shadow -->
    <ellipse cx="0" cy="18" rx="14" ry="4" fill="#000000" opacity="0.3" />

    <!-- Hero Acrobat Body Group -->
    <g transform="translate(0, 0)">
      <!-- Right Arm (holding/shooting web) -->
      <path d="M6,-6 Q18,-14 24,-24" fill="none" stroke="url(#suitRed)" stroke-width="4.2" stroke-linecap="round" />
      <circle cx="24" cy="-24" r="3.2" fill="#FF4655" stroke="#FFFFFF" stroke-width="0.8" />

      <!-- Left Arm (balance/acrobatics) -->
      <path d="M-6,-4 Q-16,4 -22,12" fill="none" stroke="url(#suitRed)" stroke-width="4.2" stroke-linecap="round" />
      <circle cx="-22" cy="12" r="3" fill="#B81424" />

      <!-- Left Leg (tucked athletic pose) -->
      <path d="M-5,10 Q-16,14 -12,22" fill="none" stroke="url(#suitBlue)" stroke-width="4.8" stroke-linecap="round" />
      <path d="M-12,22 Q-8,26 -4,24" fill="none" stroke="url(#suitRed)" stroke-width="4.2" stroke-linecap="round" />

      <!-- Right Leg (extended sprint/swing posture) -->
      <path d="M5,10 Q16,8 20,-2" fill="none" stroke="url(#suitBlue)" stroke-width="4.8" stroke-linecap="round" />
      <path d="M20,-2 Q24,-4 26,-2" fill="none" stroke="url(#suitRed)" stroke-width="4.2" stroke-linecap="round" />

      <!-- Torso / Suit Core -->
      <ellipse cx="0" cy="8" rx="7" ry="5" fill="url(#suitBlue)" />
      <path d="M-7,6 C-9,-2 -6,-10 0,-12 C6,-10 9,-2 7,6 Z" fill="url(#suitRed)" />

      <!-- Lateral blue suit flanks -->
      <path d="M-7,6 C-8,0 -6,-6 -3,-9 C-5,-4 -6,0 -5,6 Z" fill="url(#suitBlue)" />
      <path d="M7,6 C8,0 6,-6 3,-9 C5,-4 6,0 5,6 Z" fill="url(#suitBlue)" />

      <!-- Chest Emblem -->
      <ellipse cx="0" cy="-3" rx="2" ry="3" fill="#0A0D14" />
      <path d="M-2,-4 L-5,-7 M2,-4 L5,-7 M-2,-2 L-6,-1 M2,-2 L6,-1 M-2,0 L-5,3 M2,0 L5,3" stroke="#0A0D14" stroke-width="0.8" />

      <!-- Mask / Head -->
      <g transform="translate(0, -18)">
        <ellipse cx="0" cy="0" rx="8" ry="9.5" fill="url(#suitRed)" stroke="#B81424" stroke-width="0.7" />
        <!-- Mask web mesh -->
        <path d="M-7,-2 Q0,-5 7,-2 M-7,2 Q0,5 7,2" stroke="#0A0D14" stroke-width="0.5" opacity="0.4" fill="none" />
        <line x1="0" y1="-9" x2="0" y2="9" stroke="#0A0D14" stroke-width="0.5" opacity="0.4" />

        <!-- Iconic Large White Angular Mask Lenses -->
        <path d="M-1.5,-2 Q-4.5,-4 -6.5,-1 Q-4,4 -1.5,1 Z" fill="#FFFFFF" stroke="#0A0D14" stroke-width="1.6" stroke-linejoin="round" />
        <path d="M1.5,-2 Q4.5,-4 6.5,-1 Q4,4 1.5,1 Z" fill="#FFFFFF" stroke="#0A0D14" stroke-width="1.6" stroke-linejoin="round" />
      </g>
    </g>
  </g>

  <!-- Heatmap Legend Bottom Right -->
  <g transform="translate(670, 305)" font-family="monospace" font-size="9" fill="#64748B">
    <text x="0" y="8" text-anchor="end">Less</text>
    <rect x="8" y="0" width="8" height="8" rx="1.5" fill="#161B22" opacity="0.4" />
    <rect x="20" y="0" width="8" height="8" rx="1.5" fill="#0D419D" opacity="0.9" />
    <rect x="32" y="0" width="8" height="8" rx="1.5" fill="#007ACC" opacity="0.9" />
    <rect x="44" y="0" width="8" height="8" rx="1.5" fill="#E23636" opacity="0.9" />
    <rect x="56" y="0" width="8" height="8" rx="1.5" fill="#FF4655" opacity="1" stroke="#FFD700" stroke-width="1" />
    <text x="72" y="8">Burst</text>
  </g>
</svg>'''

with open('patrol-heatmap.svg', 'w') as f:
    f.write(svg_template)

print('Generated patrol-heatmap.svg successfully!')
