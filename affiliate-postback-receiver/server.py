"""Minimal receiver for RastroAff affiliate postbacks. Python 3, standard library only.

Configure in RastroAff (Integration -> Postback):
    https://your-server.example/rastro/postback?conv={conversion_id}&click={click_id}&payout={payout}&currency={currency}&status={status}&sub1={sub1}&key=LONG_RANDOM_VALUE
"""
import hmac
import json
import os
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

SECRET = os.environ.get("POSTBACK_SECRET", "")
conversions = {}  # replace with your database


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlparse(self.path)
        if url.path != "/rastro/postback":
            self.send_response(404)
            self.end_headers()
            return
        q = {k: v[0] for k, v in parse_qs(url.query).items()}
        if SECRET and not hmac.compare_digest(q.get("key", ""), SECRET):
            self.send_response(403)
            self.end_headers()
            return

        conv_id = q.get("conv") or f"{q.get('click')}:{q.get('txn', '')}"
        # Idempotent: the same conversion can arrive again with a new status (e.g. reversed).
        conversions[conv_id] = {
            "click_id": q.get("click"),
            "payout": float(q.get("payout") or 0),
            "currency": q.get("currency"),
            "status": q.get("status"),
            "sub1": q.get("sub1"),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
        print("conversion", conv_id, json.dumps(conversions[conv_id]))
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"ok")


if __name__ == "__main__":
    HTTPServer(("", int(os.environ.get("PORT", "8080"))), Handler).serve_forever()
