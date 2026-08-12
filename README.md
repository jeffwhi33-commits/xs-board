# X$ Board — Landing page

Consumer landing page for **X$ Board**.

**Default view = Hot Tips** (long / buy calls only). Secondary tab = **Pro board · Long/Short** (full $10k leaderboard).

## Files

| Path | Purpose |
|------|---------|
| `index.html` | Free landing page (masked retail handles) |
| `paid.html` | Stub only — "Checkout required" + Stripe link (no paid data) |
| `x/<unlock_token>/index.html` | Secret paid unlock page (real @handles). Path from `stripe_config.json` |
| `x/<unlock_token>/paid_board.json` | Paid board JSON (not under public `/data/`) |
| `data/hot_tips.json` | Hot Tips: longs-only who-to-follow board |
| `data/free_teaser.json` | Pro board Top 15 (long + short, masked) |
| `stripe_config.json` | Stripe Payment Link metadata + `unlock_token` / `paid_path` (no secret API keys) |
| `robots.txt` | Disallows `/x/` and old `paid.html` |
| `sync_data.py` | Regenerates / copies free JSON into `data/` |

## Stripe checkout (test mode)

Unlock CTAs on `index.html` point **only** at the Stripe **Payment Link** in `stripe_config.json` (`payment_url`). They never link directly to the secret paid URL.

Success redirect → obscure path in `success_url` / `paid_path` (set as Payment Link `after_completion.redirect.url`).

### Test cards

Use Stripe test card:

- Card: `4242 4242 4242 4242`
- Any future expiry, any CVC, any ZIP

Other test cards: https://stripe.com/docs/testing

### MVP access gate (obfuscation only)

1. Paid content lives under an obscure `x/<token>/` path (not guessable from marketing URLs).
2. Visiting that path sets `localStorage.xs_board_unlocked=1` for return visits in the same browser.
3. Old `paid.html` is a paywall stub with **no** handles and **no** paid JSON.
4. `/data/paid_board.json` is removed from the public site root.

**This is not real security.** The GitHub repo is (or was) public, so a secret path committed to git is still discoverable by browsing the repo. Making the repo **private** raises the bar. **True entitlement checks need a backend** (Stripe webhook / Customer Portal / signed cookies). This MVP only stops casual guessing from the free marketing URL.

## Open locally

```bash
cd site
python3 -m http.server 8080
# open http://localhost:8080
# paid preview: use success_url / paid_path from stripe_config.json
```

## Refresh data

```bash
python site/sync_data.py
python site/sync_data.py --no-regen   # copy + embed only
```

After regenerating retail / hot tips boards, rebuild and copy paid JSON into `x/<token>/paid_board.json` (and re-embed in the secret HTML if you rely on the inline blob).

## Information architecture

1. **Hot Tips (default)** — who to follow by longs-only $10k P&L.
2. **Pro board** — full Top 15 long/short (`free_teaser.json` on free; real handles on paid).
3. Free masking: benchmarks show `@handles`; others `xxxxxxxx` + last 2.
4. CTA: **Unlock — $12/mo** → Stripe Payment Link → secret paid path.

## Deploy

Static host, no build step. GitHub Pages publishes site files at repo root (`jeffwhi33-commits/xs-board`). Prefer a **private** repo so the obscure path is not browsable on github.com.

## Disclaimers

Not investment advice. Simulated from public posts + market data. Past ≠ future. Hot Tips = longs-only follows; Pro board includes shorts. Checkout currently runs in Stripe **test mode**.
