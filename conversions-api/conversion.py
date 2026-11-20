"""Records a conversion through the RastroAff REST API. Python 3, standard library only.

    RASTRO_API_KEY=rst_... python3 conversion.py CLICK_ID ORDER_ID 49.90
"""
import json
import os
import sys
import urllib.error
import urllib.request


def record_conversion(conversion):
    req = urllib.request.Request(
        "https://rastroaff.com/api/v1/conversions",
        data=json.dumps(conversion).encode(),
        headers={"Authorization": f"Bearer {os.environ['RASTRO_API_KEY']}",
                 "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as res:
            return json.load(res)["data"]
    except urllib.error.HTTPError as err:
        raise RuntimeError(f"RastroAff API {err.code}: {err.read().decode()}") from err


if __name__ == "__main__":
    click_id, txn_id, *rest = sys.argv[1:]
    print(record_conversion({"clickId": click_id, "transactionId": txn_id,
                             "amount": rest[0] if rest else None, "status": "approved"}))
