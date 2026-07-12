export default function RouteMap() {
  return (
    <svg
      viewBox="0 0 360 220"
      className="w-full max-w-sm"
      role="img"
      aria-label="Animated map showing a live vehicle route between two depots"
    >
      <path
        d="M 20 190 C 90 190 90 90 170 90 S 260 40 340 40"
        fill="none"
        stroke="#232b35"
        strokeWidth="2"
        strokeDasharray="1 9"
        strokeLinecap="round"
      />

      <g>
        <circle cx="20" cy="190" r="5" fill="#8a94a1" opacity="0.5" />
        <text x="32" y="194" fontFamily="IBM Plex Mono, monospace" fontSize="10" fill="#8a94a1">
          DEPOT-A
        </text>
      </g>

      <g>
        <circle cx="170" cy="90" r="5" fill="#8a94a1" opacity="0.5" />
        <text x="182" y="94" fontFamily="IBM Plex Mono, monospace" fontSize="10" fill="#8a94a1">
          WAYPOINT
        </text>
      </g>

      <g>
        <circle cx="340" cy="40" r="4.5" className="route-marker-ping" fill="#e8a33d" />
        <circle cx="340" cy="40" r="4.5" fill="#e8a33d" />
        <text x="300" y="28" fontFamily="IBM Plex Mono, monospace" fontSize="10" fill="#e8a33d">
          DEPOT-B
        </text>
      </g>

      <circle r="4" fill="#e8a33d" className="route-traveler">
        <title>Vehicle en route</title>
      </circle>
    </svg>
  );
}
