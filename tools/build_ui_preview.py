"""Build a local, noninteractive visual specimen of the Streamlit design language.

Uses representative output from the real deterministic demo engine, and is
clearly labeled a STATIC PREVIEW. The actual functional UI is app.py.
"""
from html import escape
from pathlib import Path
from orchestrator.graph import run_pipeline
from ui.presentation import hero, stat, percent, money, section, agent_header, chip

ROOT=Path(__file__).resolve().parents[1]
DATA=run_pipeline({"mode":"demo", "candidates":["SOLR","WIND","FOSS"],"capital":100000,
                   "risk_profile":"moderate","strict_esg":True,"query":"Evidence-led capital allocation"},persist=False)
portfolio=DATA['final_memo']['portfolio']
weights={r['ticker']:r['weight'] for r in portfolio}
css=(ROOT/'ui/theme.css').read_text(encoding='utf-8')
logo='''<svg viewBox="0 0 40 40" width="29" height="29" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"><path d="M7 11 17 31 32 7"/><path d="M17 16 23 25"/><path d="M23 25 33 10"/></svg>'''
stat_html=''.join(stat(*row) for row in [
    ('Mandate value',money(100000),'Capital available'),
    ('Invested in assets',money(100000*(1-weights['CASH'])),'After ESG screening','green'),
    ('Cash protection',percent(weights['CASH']),'Capital held uninvested','gold'),
    ('Conflicts reviewed',str(len(DATA['final_memo']['conflicts'])),'Documented decision tensions')])

ledger=''.join(f'<div class="vc-ledger"><div class="vc-ledger-symbol">{escape(r["ticker"])}</div><div class="vc-ledger-track"><div class="vc-ledger-fill" style="width:{r["weight"]*100:.2f}%"></div></div><div class="vc-ledger-pct">{percent(r["weight"])}</div></div>' for r in sorted(portfolio,key=lambda r:r['weight'],reverse=True))

agents=''.join(f'<div class="vc-panel">{agent_header(n,s,l)}<div class="vc-agent-metric">{v} <span style="font-size:.73rem;color:#A8BEB3">{e}</span></div><div class="vc-agent-note">{d}</div></div>' for n,s,l,v,e,d in [
   ('ESG Verifier','Source-aware screening','E','1 / 3','credible profiles','Document-cited evidence and uncertainty-aware screening.'),
   ('Market Analyst','Risk and return signals','M','2 / 3','bullish signals','Historical direction and volatility assessments.'),
   ('Portfolio Optimizer','Constraint engine','P','100%','accounted for','Long-only allocations, exposure caps and cash reserve.')])

html=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Verdant Capital — Static Design Specimen</title><style>{css}</style><style>
body{{margin:0}}.spec-shell{{display:grid;grid-template-columns:294px 1fr;min-height:100vh}}.spec-sidebar{{padding:18px 22px;background:#101B23;border-right:1px solid var(--vc-border)}}.spec-main{{max-width:1440px;padding:33px 40px 70px}}.spec-controls{{margin-top:26px}}.spec-input{{border:1px solid rgba(185,219,204,.18);background:#172731;border-radius:9px;color:#EAF3F0;padding:13px;margin:8px 0 21px;font-size:.81rem}}.spec-label{{color:#C6D8CF;font-weight:650;font-size:.75rem}}.spec-btn{{color:#0B1B16;background:#8CE1B6;padding:13px;border-radius:9px;font-size:.8rem;font-weight:750;text-align:center}}.spec-tabs{{display:flex;gap:33px;border-bottom:1px solid var(--vc-border);margin-bottom:24px;overflow-x:auto}}.spec-tab{{padding:17px 0;color:#ACBDB6;font-weight:700;font-size:.86rem;white-space:nowrap}}.spec-tab.active{{border-bottom:2px solid #8CE1B6;color:#8CE1B6}}.spec-stats{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:15px;margin:14px 0 25px}}.spec-panels{{display:grid;grid-template-columns:1fr 1fr;gap:18px}}.spec-agents{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:15px}}.spec-ring{{width:214px;height:214px;border-radius:50%;margin:8px auto 25px;background:conic-gradient(#8CE1B6 0% 55%,#E9C38D 55% 100%);display:grid;place-items:center}}.spec-ring-inner{{width:149px;height:149px;background:#111E27;border-radius:50%;display:flex;flex-direction:column;align-items:center;justify-content:center;color:#F0F7F2;font-size:2rem;font-weight:800}}.spec-ring-inner small{{font-size:.64rem;letter-spacing:.09em;color:#9BAFA6;font-weight:650}}.spec-keynote{{color:#B1C4BB;font-size:.8rem;line-height:1.55;margin-top:15px}}.spec-conflict{{border-top:1px solid var(--vc-border);padding:14px 0;font-size:.83rem;color:#D9E8DF}}.spec-flag{{position:fixed;right:18px;bottom:18px;border:1px solid var(--vc-border);background:#182831;padding:7px 10px;border-radius:7px;color:#C9DCD2;font-size:.64rem}}@media(max-width:1000px){{.spec-shell{{grid-template-columns:minmax(0,1fr)}}.spec-main{{min-width:0}}.spec-sidebar{{display:none}}.spec-main{{padding:22px}}.spec-stats{{grid-template-columns:repeat(2,minmax(0,1fr))}}.spec-agents{{grid-template-columns:1fr}}.spec-panels{{grid-template-columns:1fr}}}}@media(max-width:500px){{.spec-main{{padding:12px 15px}}.spec-tabs{{gap:24px}}.spec-stats{{gap:9px}}}}
</style></head><body><div class="spec-shell"><aside class="spec-sidebar">
<div class="vc-brand"><div class="vc-logo">{logo}</div><div><div class="vc-brand-name">Verdant <span style="color:#8CE1B6">Capital</span></div><div class="vc-brand-sub">Decision Intelligence</div></div></div>
<div class="vc-sidebar-title">Investment mandate</div><div class="vc-sidebar-help">Configure a portfolio scenario and invite the three specialist agents to review it.</div><div class="vc-note"><strong>SIMULATION</strong> · All entities are fictional.</div>
<div class="spec-controls"><div class="spec-label">Capital to allocate</div><div class="spec-input">$ 100,000</div><div class="spec-label">Risk appetite</div><div class="spec-input">Moderate</div><div class="spec-label">Investment universe</div><div class="spec-input">SOLR · WIND · FOSS</div><div class="spec-label">Hypothetical stress event</div><div class="spec-input">Base case</div><div class="spec-label">Investment principles</div><div class="spec-input" style="height:86px">Favor verifiable sustainability claims, manage volatility and preserve capital.</div><div class="spec-btn">Run investment review</div></div>
<div class="vc-sidebar-tail">Decision support only. No securities transactions.</div></aside>
<main class="spec-main">{hero(mode='demo',preview=True)}
<div class="spec-tabs"><div class="spec-tab active">Investment boardroom</div><div class="spec-tab">Risk lab · C02 / C06</div><div class="spec-tab">Market intelligence</div><div class="spec-tab">Audit trail</div></div>
<div class="vc-alertline"><strong>PREVIEW</strong> · Fictional assets and generated prices. No live market claims.</div>
{section('Allocation overview','Mathematically constrained, evidence-informed capital deployment.','Long-only · ESG screened')}
<div class="spec-stats">{stat_html}</div>
<div class="spec-panels"><div><div class="vc-section-top"><div><h2>Portfolio composition</h2><p class="vc-section-desc">Validated weights and cash protection.</p></div></div><div class="vc-panel"><div class="spec-ring"><div class="spec-ring-inner">100%<small>ACCOUNTED</small></div></div><div class="vc-panel-head">Allocation ledger</div>{ledger}</div></div>
<div><div class="vc-section-top"><div><h2>Investment rationale</h2><p class="vc-section-desc">What the optimizer accepted, constrained or set aside.</p></div></div><div class="vc-panel"><div class="vc-panel-head">Policy review</div><div class="vc-ledger"><div class="vc-ledger-symbol">SOLR</div><div style="flex:1">{chip('Allocated','positive')}</div><div class="vc-ledger-pct">55.0%</div></div><div class="vc-ledger"><div class="vc-ledger-symbol">FOSS</div><div style="flex:1">{chip('Excluded','negative')}</div><div class="vc-ledger-pct">0.0%</div></div><div class="vc-ledger"><div class="vc-ledger-symbol">CASH</div><div style="flex:1">{chip('Cash reserve','info')}</div><div class="vc-ledger-pct">45.0%</div></div><p class="spec-keynote">No unverified ESG evidence is treated as a verified classification. Hard constraints outrank narrative optimism.</p></div><div class="vc-note"><strong>Allocation authority:</strong> Weights are produced by the constrained optimizer, not AI prose.</div></div></div>
{section('Specialist council','Three distinct responsibilities; one transparent investment memo.')}
<div class="spec-agents">{agents}</div>
{section('The decision room','Where ESG evidence and market signals disagree.')}
<div class="vc-panel"><div class="spec-conflict"><strong>FOSS</strong> · Market opportunity versus sustainability policy &nbsp; {chip('Conflict resolved','warning')}</div><p class="spec-keynote">Market strength does not validate sustainability claims. The quantified ESG exclusion takes precedence; capital remains protected.</p></div>
<div class="vc-footer"><span><b>Verdant Capital</b> · Team Cypher</span><span>Not financial advice · Static visual preview</span></div>
</main></div></body></html>'''
out=ROOT/'docs'/'STUDIO_PREVIEW.html';out.write_text(html,encoding='utf-8')
print(out)
