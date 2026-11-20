# Macros: Everflow, Affise, Scaleo and Offer18 → RastroAff

When you move offers to RastroAff, the destination URLs need RastroAff's macros. The [direct migration](https://rastroaff.com/migrate) converts them for you; this table is for doing it by hand.

| Meaning | Everflow | Affise | Scaleo | Offer18 | RastroAff |
|---|---|---|---|---|---|
| Click ID | `{transaction_id}` | `{clickid}` | `{click_id}` | `{tid}` | `{click_id}` |
| Affiliate ID | `{affiliate_id}` | `{pid}` | `{aff_id}` | `{aff_id}` | `{affiliate_id}` |
| Offer ID | `{offer_id}` | `{offer_id}` | `{offer_id}` | `{offerid}` | `{campaign_id}` |
| Sub IDs | `{sub1}`…`{sub5}` | `{sub1}`…`{sub5}` | `{sub1}`…`{sub5}` | `{aff_sub1}`…`{aff_sub5}` | `{sub1}`…`{sub5}` |
| Traffic source | `{source_id}` | | | | `{source}` |

Sources: each platform's public documentation (Everflow "Parameters & Macros", Affise API docs, Scaleo's public API collection, Offer18 "Tracking URL macros").

## Example

Everflow destination URL:

```
https://shop.example/landing?clickid={transaction_id}&aff={affiliate_id}
```

In RastroAff:

```
https://shop.example/landing?clickid={click_id}&aff={affiliate_id}
```

The advertiser keeps reading `clickid` as before. Only the macro changes.

## Macros in affiliate postbacks

Postbacks that RastroAff sends to affiliates use a different set: `{click_id}`, `{conversion_id}`, `{txn_id}`, `{goal}`, `{payout}`, `{currency}`, `{status}`, `{campaign_id}`, `{affiliate_id}`, `{sub1}`–`{sub3}`, `{offer_name}`, `{payout_model}`, `{country}`, `{device}`. See [affiliate-postback-receiver](affiliate-postback-receiver).
