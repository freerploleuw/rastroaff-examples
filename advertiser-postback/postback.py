"""Sends a conversion to RastroAff by S2S postback. Python 3, standard library only.

    RASTRO_POSTBACK_URL=https://track.rastroaff.com/postback RASTRO_TOKEN=... \
        python3 postback.py CLICK_ID ORDER_ID 49.90 approved
"""
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = os.environ.get("RASTRO_POSTBACK_URL", "")
TOKEN = os.environ.get("RASTRO_TOKEN", "")


def send_postback(click_id, txn_id, amount=None, status="approved", goal=None,
                  coupon=None, country=None, customer_id=None, attempts=5):
    params = {"token": TOKEN, "click_id": click_id, "txn_id": txn_id, "amount": amount,
              "status": status, "goal": goal, "coupon": coupon, "country": country,
              "customer_id": customer_id}
    query = urllib.parse.urlencode({k: v for k, v in params.items() if v not in (None, "")})
    url = f"{BASE}?{query}"

    for attempt in range(1, attempts + 1):
        try:
            with urllib.request.urlopen(url, timeout=15) as res:
                return res.read().decode()
        except urllib.error.HTTPError as err:
            body = err.read().decode()
            if err.code < 500:  # 4xx: the request must be fixed, retrying won't help
                raise RuntimeError(f"Postback refused ({err.code}): {body}") from err
            if attempt == attempts:
                raise RuntimeError(f"Postback failed ({err.code}): {body}") from err
        except urllib.error.URLError:
            if attempt == attempts:
                raise
        time.sleep(2 ** attempt)


if __name__ == "__main__":
    click, txn, *rest = sys.argv[1:]
    print(send_postback(click, txn, *(rest[:2])))
