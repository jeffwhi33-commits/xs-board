# X$ Board — Landing page

Consumer landing page for **X$ Board**.

**Default view = Hot Tips** (long / buy calls only). Secondary tab = **Pro board · Long/Short** (full $10k leaderboard).

## Files

| Path | Purpose |
|------|---------|
| `index.html` | Free landing page (masked retail handles) |
| `paid.html` | Paid unlock page (real @handles) after Stripe success |
| `data/hot_tips.json` | Hot Tips: longs-only who-to-follow board |
| `data/free_teaser.json` | Pro board Top 15 (long + short, masked) |
| `data/paid_board.json` | Paid board with real handles (Hot Tips + Pro) |
| `stripe_config.json` | Stripe test Payment Link metadata (no secret keys) |
| `sync_data.py` | Regenerates / copies JSON into `data/` |

## Stripe checkout (test mode)

Unlock CTAs on `index.html` point at the Stripe **Payment Link** in `stripe_config.json` (`payment_url`).

Success URL → `paid.html?unlocked=1`

### Test cards

Use Stripe test card:

- Card: `4242 4242 4242 4242`
- Any future expiry, any CVC, any ZIP

Other test cards: https://stripe.com/docs/testing

### MVP access gate (temporary)

`paid.html` unlocks when:

1. URL has `?unlocked=1` (Stripe success redirect), **or**
2. `localStorage.xs_board_unlocked=1` from a prior unlocked visit

On `?unlocked=1`, the page sets that localStorage flag so return visits work without paying again.

**This is not a real entitlement check** — anyone with the success URL can unlock. Replace with Stripe Customer Portal / webhook-backed auth before charging real money.

## Open locally

```bash
cd site
python3 -m http.server 8080
# open http://localhost:8080
# paid preview: http://localhost:8080/paid.html?unlocked=1
```

## Refresh data

```bash
python site/sync_data.py
python site/sync_data.py --no-regen   # copy + embed only
```

Also copy / rebuild `data/paid_board.json` when regenerating retail / hot tips boards (see deploy scripts / paid page embed).

## Information architecture

1. **Hot Tips (default)** — who to follow by longs-only $10k P&L.
2. **Pro board** — full Top 15 long/short (`free_teaser.json` on free; real handles on paid).
3. Free masking: benchmarks show `@handles`; others `xxxxxxxx` + last 2.
4. CTA: **Unlock — $12/mo** → Stripe Payment Link → `paid.html?unlocked=1`.

## Deploy

Static host, no build step. GitHub Pages publishes site files at repo root (`jeffwhi33-commits/xs-board`).

## Disclaimers

Not investment advice. Simulated from public posts + market data. Past ≠ future. Hot Tips = longs-only follows; Pro board includes shorts. Checkout currently runs in Stripe **test mode**.
