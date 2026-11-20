# Receive RastroAff postbacks as an affiliate

As an affiliate, go to **Integration → Postback** in RastroAff and add a postback pointing to your server. RastroAff replaces the macros with each conversion's values:

```
https://your-server.example/rastro/postback?click={click_id}&txn={txn_id}&payout={payout}&currency={currency}&status={status}&offer={campaign_id}&goal={goal}&sub1={sub1}
```

| Macro | Value |
|---|---|
| `{click_id}` | The click identifier |
| `{conversion_id}` | RastroAff's conversion ID |
| `{txn_id}` | The advertiser's transaction ID |
| `{goal}` | Goal code (empty for the offer's main event) |
| `{payout}`, `{currency}` | Your earnings for this conversion |
| `{status}` | `approved`, `pending`, `rejected` or `reversed` |
| `{campaign_id}`, `{affiliate_id}` | The offer and your public ID |
| `{sub1}`, `{sub2}`, `{sub3}` | Sub IDs from the click |
| `{offer_name}`, `{payout_model}`, `{country}`, `{device}` | Offer name, payout model, country, device |

Delivery: RastroAff retries failed calls up to 5 times over 15 hours. A status change (for example a refund marked `reversed`) calls the postback again, so make your handler **idempotent**: store by `conversion_id` (or `click_id` + `txn_id`) and update, don't insert twice.

Using Keitaro, Binom, Voluum or RedTrack? You don't need a server: pick your tracker under **Template for your tracker** and pass your tracker's click ID in `sub1`.

| File | Stack |
|---|---|
| [`server.mjs`](server.mjs) | Node.js 18+, `node:http` only |
| [`server.py`](server.py) | Python 3, `http.server` only |
