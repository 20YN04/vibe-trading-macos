"""Strategy showcase exporter — reads run_card.json and generates HTML reports.

Usage:
    python scripts/showcase.py <run_dir> [--output report.html]
    python scripts/showcase.py portfolio/results/20260630_* --index
"""
import json
import sys
from datetime import datetime
from pathlib import Path


def load_run(run_dir: Path) -> dict:
    card = run_dir / "artifacts" / "run_card.json"
    if not card.exists():
        # Try root level
        card = run_dir / "run_card.json"
    if not card.exists():
        raise FileNotFoundError(f"No run_card.json in {run_dir}")
    return json.loads(card.read_text())


def _badge(value: float, label: str, good: bool = True) -> str:
    color = "#22c55e" if good else "#ef4444"
    return (
        f'<div style="display:inline-block;margin:8px;padding:12px 16px;'
        f'background:{color}18;border:1px solid {color}40;border-radius:8px;text-align:center">'
        f'<div style="font-size:24px;font-weight:700;color:{color}">{value}</div>'
        f'<div style="font-size:11px;color:#94a3b8;margin-top:4px">{label}</div>'
        f'</div>'
    )


def render_card(metrics: dict, title: str = "Strategy Report") -> str:
    sharpe = metrics.get("sharpe", 0)
    max_dd = metrics.get("max_drawdown", 0)
    win_rate = metrics.get("win_rate", 0)
    trades = metrics.get("trade_count", 0)
    total_return = metrics.get("total_return", 0)
    annual_return = metrics.get("annual_return", 0)

    badges = (
        _badge(f"{sharpe:.2f}", "Sharpe", sharpe > 0.5)
        + _badge(f"{max_dd*100:.1f}%", "Max DD", max_dd > -0.3)
        + _badge(f"{win_rate*100:.0f}%", "Win Rate", win_rate > 0.45)
        + _badge(f"{int(trades)}", "Trades", trades > 20)
        + _badge(f"{total_return*100:.1f}%", "Return", total_return > 0)
        + _badge(f"{annual_return*100:.1f}%", "Ann. Return", annual_return > 0.05)
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
         background: #0f172a; color: #e2e8f0; max-width: 800px; margin: 40px auto; padding: 0 20px; }}
  h1 {{ font-size: 28px; font-weight: 700; margin-bottom: 4px; }}
  .date {{ color: #64748b; font-size: 14px; margin-bottom: 24px; }}
  .badges {{ display: flex; flex-wrap: wrap; gap: 4px; margin: 24px 0; }}
  .section {{ margin: 32px 0; }}
  .section h2 {{ font-size: 18px; border-bottom: 1px solid #1e293b; padding-bottom: 8px; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 14px; }}
  th, td {{ padding: 8px 12px; text-align: left; border-bottom: 1px solid #1e293b; }}
  th {{ color: #64748b; font-weight: 600; }}
  .footer {{ margin-top: 48px; padding-top: 16px; border-top: 1px solid #1e293b;
             color: #475569; font-size: 12px; }}
</style>
</head>
<body>
<h1>{title}</h1>
<div class="date">Generated {datetime.now().strftime('%Y-%m-%d %H:%M')} · vibe-trading-macos</div>

<div class="badges">{badges}</div>

<div class="section">
<h2>Key Metrics</h2>
<table>
<tr><th>Metric</th><th>Value</th></tr>
<tr><td>Total Return</td><td>{total_return*100:.2f}%</td></tr>
<tr><td>Annual Return</td><td>{annual_return*100:.2f}%</td></tr>
<tr><td>Sharpe Ratio</td><td>{sharpe:.4f}</td></tr>
<tr><td>Max Drawdown</td><td>{max_dd*100:.2f}%</td></tr>
<tr><td>Win Rate</td><td>{win_rate*100:.1f}%</td></tr>
<tr><td>Trade Count</td><td>{int(trades)}</td></tr>
</table>
</div>

<div class="footer">
Generated with <strong>vibe-trading-macos</strong> · 
<a href="https://github.com/20YN04/vibe-trading-macos" style="color:#64748b">github.com/20YN04/vibe-trading-macos</a>
</div>
</body>
</html>"""


def generate_index(results_dir: Path) -> str:
    """Generate an index.html for all showcase reports in a directory."""
    reports = sorted(results_dir.glob("*.html"))
    if not reports:
        return "<html><body>No reports found.</body></html>"

    rows = ""
    for r in reports:
        name = r.stem.replace("-", " ").title()
        rows += f'<tr><td><a href="{r.name}">{name}</a></td><td>{datetime.fromtimestamp(r.stat().st_mtime).strftime("%Y-%m-%d %H:%M")}</td></tr>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>Portfolio Showcase</title>
<style>
  body {{ font-family: -apple-system, system-ui, sans-serif; background: #0f172a; color: #e2e8f0;
         max-width: 800px; margin: 40px auto; padding: 0 20px; }}
  h1 {{ font-size: 28px; }}
  table {{ width: 100%; border-collapse: collapse; margin-top: 24px; }}
  th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #1e293b; }}
  a {{ color: #38bdf8; text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
  .footer {{ margin-top: 48px; color: #475569; font-size: 12px; }}
</style></head>
<body>
<h1>📊 Portfolio Showcase</h1>
<p>{len(reports)} strategy reports</p>
<table>
<tr><th>Strategy</th><th>Date</th></tr>
{rows}
</table>
<div class="footer">vibe-trading-macos · github.com/20YN04/vibe-trading-macos</div>
</body></html>"""


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/showcase.py <run_dir> [--output report.html]")
        print("       python scripts/showcase.py portfolio/results/ --index")
        sys.exit(1)

    target = Path(sys.argv[1])

    if "--index" in sys.argv:
        html = generate_index(target)
        out = target / "index.html"
        out.write_text(html)
        print(f"Index written: {out}")
        return

    if "--output" in sys.argv:
        idx = sys.argv.index("--output")
        out = Path(sys.argv[idx + 1])
    else:
        out = target / "showcase.html"

    try:
        metrics = load_run(target)
    except FileNotFoundError:
        # Try nested path
        for d in target.rglob("run_card.json"):
            metrics = json.loads(d.read_text())
            break
        else:
            print(f"No run_card.json found in {target}")
            sys.exit(1)

    title = target.name if target.is_dir() else "Strategy Report"
    html = render_card(metrics, title)
    out.write_text(html)
    print(f"Report written: {out}")


if __name__ == "__main__":
    main()
