#!/usr/bin/env bash
# Sends one conversion to RastroAff. Usage:
#   RASTRO_POSTBACK_URL=https://track.rastroaff.com/postback RASTRO_TOKEN=... \
#     ./postback.sh CLICK_ID ORDER_ID 49.90 approved
set -euo pipefail

click_id="$1"
txn_id="$2"
amount="${3:-}"
status="${4:-approved}"

curl --fail-with-body --silent --show-error --get \
  --retry 4 --retry-delay 2 --max-time 15 \
  --data-urlencode "token=${RASTRO_TOKEN}" \
  --data-urlencode "click_id=${click_id}" \
  --data-urlencode "txn_id=${txn_id}" \
  --data-urlencode "amount=${amount}" \
  --data-urlencode "status=${status}" \
  "${RASTRO_POSTBACK_URL}"
echo
