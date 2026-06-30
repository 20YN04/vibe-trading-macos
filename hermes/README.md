# Hermes Agent Integration

Use Vibe-Trading from inside Hermes Agent via MCP (Model Context Protocol).

## Quick setup

```bash
# Start Vibe-Trading MCP server
source ~/activate-vibe-trading.sh
vibe-trading-mcp    # stdio transport — Hermes connects to this

# OR HTTP transport
vibe-trading serve  # starts API + MCP on localhost:8899
```

## Hermes config

Add to `~/.hermes/config.yaml`:

```yaml
mcp_servers:
  vibe-trading:
    transport: stdio
    command: "vibe-trading-mcp"
    workdir: "~/Projects/vibe-trading-macos"
    env:
      VECLIB_MAXIMUM_THREADS: "1"
      ACCELERATE_NEW_LAPACK: "0"
```

Restart Hermes Agent — Vibe-Trading tools appear automatically.

## Available tools (68 MCP tools)

| Category | Tools |
|----------|-------|
| Market Data | `get_market_data`, `get_stock_profile`, `web_search` |
| Backtesting | `run_backtest`, `generate_backtest_config` |
| Alpha Research | `alpha_list`, `alpha_show`, `alpha_bench`, `alpha_compare` |
| Portfolio | `run_portfolio_analysis`, `portfolio_optimize` |
| Research | `run_research_autopilot`, `create_hypothesis` |
| Trading | `trading_account`, `trading_positions`, `trading_place_order` |
| Export | Export to Pine Script, TDX, MT5, vnpy |

## Hermes Skill

Load this skill in Hermes:

```
/skill vibe-trading
```

Or install permanently: copy `hermes/vibe-trading-skill.md` to `~/.hermes/skills/`.

## Prompt library

See [`prompts/`](prompts/) for curated research prompts organized by category.
