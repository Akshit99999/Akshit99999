import json

with open('calendar_data.json') as f:
    cal = json.load(f)

weeks = cal['weeks']

# Dynamically compute stats from the data
total_contributions = cal.get('totalContributions', 0)
peak_day = max(
    (day['contributionCount'] for week in weeks for day in week['contributionDays']),
    default=0
)

start_x = 72
start_y = 75
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
        base_color = get_base_color(count)
        
        stroke = ''
        filter_attr = ''
        if count >= 40:
            stroke = ' stroke="#F472B6" stroke-width="1.2"'
            filter_attr = ' filter="url(#glow-magenta)"'
        elif count >= 20:
            stroke = ' stroke="#C084FC" stroke-width="0.8"'

        opacity = '0.95' if count > 0 else '0.45'
        tiles_svg.append(f'<rect x="{x}" y="{y}" width="{tile_size}" height="{tile_size}" rx="2.5" fill="{base_color}" opacity="{opacity}"{stroke}{filter_attr}><title>{day["date"]}: {count} contributions</title></rect>')

tiles_content = '\n    '.join(tiles_svg)
months_content = '\n    '.join(months_labels)
days_content = '\n    '.join(days_labels)

# SVG with clean, compact height (215px instead of 330px since moving hero is on hold)
svg_output = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 215" width="100%" height="215">
  <defs>
    <filter id="purple-glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>

    <filter id="glow-magenta" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="2.5" result="blur" />
      <feMerge>
        <feMergeNode in="blur" />
        <feMergeNode in="SourceGraphic" />
      </feMerge>
    </filter>

    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#120A22" />
      <stop offset="100%" stop-color="#07050E" />
    </linearGradient>
  </defs>

  <style>
    @keyframes beaconPulse {{
      0%, 100% {{ opacity: 1; transform: scale(1); }}
      50% {{ opacity: 0.35; transform: scale(0.9); }}
    }}
    .pulse-beacon {{
      transform-origin: 8px 8px;
      animation: beaconPulse 2.2s ease-in-out infinite;
    }}
  </style>

  <!-- Container Box -->
  <rect x="0" y="0" width="900" height="215" rx="10" fill="url(#bgGrad)" stroke="#2E1065" stroke-width="1.2" />

  <!-- Subtle Corner Geometry / Web Strands -->
  <g opacity="0.08" stroke="#C084FC" stroke-width="0.8">
    <line x1="0" y1="42" x2="900" y2="42" />
    <path d="M0,0 L35,0 M0,0 L0,35 M0,0 L25,25" stroke-width="1.2" />
    <path d="M900,0 L865,0 M900,0 L900,35 M900,0 L875,25" stroke-width="1.2" />
  </g>

  <!-- Header Section -->
  <g transform="translate(24, 22)">
    <circle cx="8" cy="8" r="4" fill="#A855F7" class="pulse-beacon" filter="url(#purple-glow)" />
    <circle cx="8" cy="8" r="8" fill="none" stroke="#A855F7" stroke-width="0.8" opacity="0.4" />

    <text x="24" y="12" fill="#F8FAFC" font-size="12.5" font-weight="700" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', monospace" letter-spacing="1">
      CONTRIBUTION TELEMETRY // ANNUAL DISPATCH RADAR
    </text>

    <!-- Header Badges -->
    <g transform="translate(560, -3)">
      <rect x="0" y="0" width="130" height="22" rx="4" fill="#170F2E" stroke="#3B1768" stroke-width="0.8" />
      <text x="12" y="15" fill="#C084FC" font-size="10.5" font-family="monospace" font-weight="600">⚡ {total_contributions} DISPATCHES</text>

      <rect x="140" y="0" width="145" height="22" rx="4" fill="#170F2E" stroke="#A855F7" stroke-width="0.8" />
      <text x="150" y="15" fill="#A855F7" font-size="10.5" font-family="monospace" font-weight="600">🎯 PEAK: {peak_day} IN A DAY</text>
    </g>
  </g>

  <!-- Heatmap Calendar Grid -->
  <g id="heatmap-grid">
    {months_content}
    {days_content}
    {tiles_content}
  </g>

  <!-- Heatmap Legend Bottom Right -->
  <g transform="translate(685, 195)" font-family="monospace" font-size="9" fill="#71717A">
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

print('Generated clean, elegant patrol-heatmap.svg successfully!')
