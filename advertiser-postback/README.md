# Advertiser postback (S2S)

Call the postback URL from your **server** when the conversion happens (sign-up, sale, first deposit…). Never from the browser: the token must stay secret.

| File | Language |
|---|---|
| [`postback.sh`](postback.sh) | cURL |
| [`postback.mjs`](postback.mjs) | Node.js 18+ (built-in `fetch`) |
| [`postback.py`](postback.py) | Python 3 (standard library) |
| [`postback.php`](postback.php) | PHP 7.4+ |

All examples:

- URL-encode every value;
- send a `txn_id`, so the same order is never counted twice and its status can be changed later;
- retry on network errors and `5xx` answers, but not on `4xx` (those mean the request itself must be fixed).

Set `RASTRO_POSTBACK_URL` to the base URL shown on the advertiser's page in RastroAff, for example `https://track.rastroaff.com/postback`, and `RASTRO_TOKEN` to the advertiser token.
