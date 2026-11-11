# Verdant Capital — Studio Design System

## User-facing purpose
A decision-support workspace where judges and analysts can inspect the evidence, model limits and portfolio constraints behind an investment simulation. The system does not execute trades and makes no claims of real-world fraud detection.

## Visual direction
**Calm institutional intelligence.** A dark, slate-toned operational workspace with restrained mint accents, warm sand for reservations, and coral for risks. Dense technical evidence is presented as a readable editorial finance report, never as a wall of model JSON.

### Tokens

| Role | Color | Purpose |
|---|---|---|
| Canvas | `#0B1218` | Main app background |
| Sidebar | `#101B23` | Controls and configuration |
| Panel | `#14222B` | Important data grouping |
| Main text | `#EEF6F1` | Primary information |
| Secondary text | `#B1C4BB` | Supporting details |
| Accent | `#8CE1B6` | Interactive actions and selected state |
| Reserve | `#E9C38D` | Cash reserves, cautions |
| Risk | `#F0A8A8` | Suspicion-raising feature attribution |
| Divider | `rgba(197,222,211,.13)` | Structural separation |

- Font: Segoe UI Variable / Segoe UI / system sans. No remote webfont is required.
- Corner radius: 9–16px, based on control vs panel.
- Data numerals use tabular-nums to avoid jitter.
- Charts: Plotly dark palettes in `ui/charts.py`, transparent backgrounds.
- CSS: `ui/theme.css`, plus Streamlit dark theme in `.streamlit/config.toml`.

## Information architecture

1. **Investment boardroom** — overview, allocation weights, decision rationale, three specialist cards, material disagreements.
2. **Risk Lab (C02/C06/C13)** — class imbalance, per-seed PR metrics, confusion matrix, three held-out SHAP cases, and editable decision economics with validation-loss curve and held-out policy comparisons.
3. **Market intelligence** — time-stamped historical signals, carbon-ETF forecast and explicitly simulated feedback.
4. **Audit trail** — persisted recommendations, policy reason codes, evidence citations and reproducible commands.

## Accessibility and reliability
- Colored results always include textual labels.
- Dark/light semantic contrast uses a predominantly monochrome vocabulary plus accents.
- Real form controls stay native to Streamlit for keyboard and screen-reader compatibility.
- Visible focus rings, at least 44px primary action height, reduced-motion styling.
- Content stacks on small viewports; charts use Plotly responsivity.
- No external CDN, font dependency, JavaScript injection or third-party UI service.
- `docs/STUDIO_PREVIEW.html` is an offline, static visual specimen — **not a functional dashboard**.

## Truth-in-design
- Synthetic data and previews are labeled; there is no market-data API behind a static screenshot.
- Only optimization outputs supply weights and estimates.
- Source limitations and unverified ESG status appear near decisions, not buried in documentation.
- Real and synthetic feedback sources remain distinct.
