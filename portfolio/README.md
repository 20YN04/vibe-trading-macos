# Portfolio Project Templates

Ready-to-run research prompts for the 8 projects from [@macroglide](https://www.instagram.com/p/DZtFyvpjoHz/):
*"Projects that actually get you hired."*

Each template is a one-command prompt you can paste into `vibe-trading run`.
Results include backtest metrics, trade attribution, and a run card you can
put in your portfolio.

## Quick start

```bash
source ~/activate-vibe-trading.sh
vibe-trading run -p "$(cat portfolio/ml-alpha-model.txt)" --max-iter 15
```

## Templates

| # | Project | Template |
|---|---------|----------|
| 1 | ML Alpha Model | [`portfolio/ml-alpha-model.txt`](ml-alpha-model.txt) |
| 2 | Options Pricing Engine | [`portfolio/options-pricing.txt`](options-pricing.txt) |
| 3 | Statistical Arbitrage | [`portfolio/stat-arb.txt`](stat-arb.txt) |
| 4 | Factor Model Builder | [`portfolio/factor-model.txt`](factor-model.txt) |
| 5 | Risk Management System | [`portfolio/risk-engine.txt`](risk-engine.txt) |
| 6 | Crypto Arbitrage Bot | [`portfolio/crypto-arb.txt`](crypto-arb.txt) |
| 7 | HFT Market Simulator | [`portfolio/hft-simulator.txt`](hft-simulator.txt) |
| 8 | Portfolio Optimizer | [`portfolio/portfolio-optimizer.txt`](portfolio-optimizer.txt) |
