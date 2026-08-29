# hermes-plugin-backsearch

![BackSearch — search the web as it was](https://v3b.fal.media/files/b/0aa84975/CyEGZq8lccVZUWQpoxHF1_2C7j8lCa.png)

Point-in-time web search & fetch for [Hermes Agent](https://github.com/NousResearch/hermes-agent), backed by [BackSearch by General Reasoning](https://www.gr.inc/releases/introducing-backsearch).

BackSearch is a **frozen news archive**: every request carries an `as_of` date, search returns only documents *crawled* on or before it, and fetch returns the article text as archived at that time. Same query + same `as_of` = same results, forever. Built for forecasting backtests, quant research loops, RL environments, and reproducible benchmarks — any task where evidence after a cutoff date must not leak in.

The plugin registers two model tools, both gated on `OPENREWARD_API_KEY` — with no key configured they never reach the model schema, so the tool footprint is zero:

| Tool | What it does |
|---|---|
| `backsearch` | Hybrid search over the frozen corpus as of a date (`query`, `as_of`, optional `k`, `allowed_domains`/`blocked_domains`) |
| `backfetch` | Fetch a page's extracted text from the latest capture on or before the cutoff (`url`, `as_of`, optional `prompt` for a focused summary) |

## Install

```bash
# 1. Clone into the Hermes plugins dir
git clone https://github.com/NousResearch/hermes-plugin-backsearch.git ~/.hermes/plugins/backsearch

# 2. Enable
hermes plugins enable backsearch

# 3. API key — BackSearch bills against an OpenReward prepaid balance.
#    Get a key (or_...) at https://openreward.ai/
echo 'OPENREWARD_API_KEY=or_...' >> ~/.hermes/.env
```

New sessions pick the tools up automatically once the key is present.

## Semantics worth knowing

- **`as_of` gates on crawl_date**, not the article's self-reported publish date. A page first archived after the cutoff is never returned, even if it claims an earlier publish date — that's what guarantees no post-cutoff leakage into a backtest.
- **Archive window:** the current preview archive covers news domains, December 2025 – July 2026. An `as_of` outside the window returns an empty hit list (not an error).
- **Billing:** per successful request. A fetch with no capture on or before the cutoff returns a soft 404 and costs nothing; an exhausted OpenReward balance returns 402 with an actionable message.
- Fetch text is capped at 15K chars; pass a `prompt` to get a focused summary of a long article instead of the full text.
- `OPENREWARD_SEARCH_URL` overrides the base URL (`https://search.openreward.ai`) for testing/self-routing.

## Tests

```bash
# No network, no key needed — run from a hermes-agent checkout's venv so
# tools/ imports resolve (set HERMES_AGENT_REPO if not ~/.hermes/hermes-agent):
python -m pytest tests/ -q
```

## Attribution

Originally built as hermes-agent [PR #71207](https://github.com/NousResearch/hermes-agent/pull/71207); extracted to this standalone repo per the hermes-agent policy that third-party service integrations ship as plugins rather than core code.

## License

MIT
