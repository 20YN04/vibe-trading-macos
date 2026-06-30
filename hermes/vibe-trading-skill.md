# Vibe-Trading Skill for Hermes Agent

Trigger: user asks about trading, backtesting, market data, crypto prices, quant research, alpha factors, portfolio optimization, risk analysis.

## Quick commands

```
# Market data
"Get latest BTC price from Binance"
"Show me AAPL OHLCV for last 30 days"
"What's the ETH/BTC ratio trend?"

# Backtesting
"Backtest a 20/50 SMA crossover on BTC for 2024"
"Test mean-reversion strategy on ETH with 2σ bands"

# Alpha research
"Benchmark GTJA191 factors on S&P 500 for 2023-2025"
"Which academic alphas are alive on NASDAQ 100?"

# Portfolio
"Build a minimum-variance portfolio from top 10 crypto"
"Run risk analysis: VaR and stress test on my portfolio"

# Research
"Research autopilot: find momentum factors on crypto"
"Analyze trading journal for disposition effect"
```

## Tool selection

| User intent | Use tool |
|-------------|----------|
| Price, OHLCV data | `get_market_data` → source=ccxt (crypto) or auto (equities) |
| Strategy test | `run_backtest` after `generate_backtest_config` |
| Factor discovery | `alpha_bench` or `run_research_autopilot` |
| Portfolio construction | `portfolio_optimize` |
| Trade journal analysis | Upload CSV → Shadow Account tools |

## macOS ARM note

This fork includes Apple Silicon BLAS fixes. If tools crash with "Bus error", restart with:
```bash
source ~/activate-vibe-trading.sh
```

## Portfolio projects

8 ready-to-run prompts in `portfolio/`. Use them to build a quant portfolio:
```
vibe-trading run -p "$(cat portfolio/ml-alpha-model.txt)"
```
