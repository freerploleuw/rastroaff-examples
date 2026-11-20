# Keep the click_id on the landing page

RastroAff sends the visitor to your offer with the `click_id` in the URL, in the parameter you chose in the offer's destination URL (here `clickid`):

```
https://shop.example/landing?clickid=01JD3E28JT97KB6CQ643DZVMXX
```

Your site has to keep that value until the conversion, then send it back in the postback. Two common ways:

1. **Server side (recommended):** read the parameter on the first request and save it in the session, then with the lead or order in your database.
2. **Browser side:** [`capture.html`](capture.html) saves it in a first-party cookie for 30 days and copies it into a hidden form field.

Then send the postback from your server: see [`../advertiser-postback`](../advertiser-postback).
