# Conversions through the REST API

The same as the postback, but with a JSON body and an **API key** instead of the postback token. Useful when you already call APIs from your backend.

1. Log in to RastroAff with the advertiser account, open **API** and create a key with **write** access. It starts with `rst_` and is shown only once.
2. `POST https://rastroaff.com/api/v1/conversions` with `Authorization: Bearer rst_...`.

| Field | Type | What it does |
|---|---|---|
| `clickId` | string | The `click_id` received in the destination URL |
| `transactionId` | string | Your order or lead ID |
| `amount` | number or string | Sale value, for percentage payouts |
| `status` | string | `approved`, `pending`, `rejected` or `reversed` |
| `goal` | string | Goal code, for example `first_deposit` |
| `coupon` | string | Attribute by coupon code instead of `clickId` |
| `campaignId` | string | Offer ID, needed with `coupon` when it isn't unique |
| `customerId` | string | Customer ID, for subscriptions |
| `interval` | string | `month`, `quarter` or `year` |

Answers: `201` for a new conversion, `200` for an update or a duplicate. Errors come as JSON with a code and a message. Limit: 600 requests per minute per key.

The full specification (OpenAPI 3.1) is at `https://rastroaff.com/api/v1/openapi.json`.

| File | Language |
|---|---|
| [`conversion.sh`](conversion.sh) | cURL |
| [`conversion.mjs`](conversion.mjs) | Node.js 18+ |
| [`conversion.py`](conversion.py) | Python 3 |
