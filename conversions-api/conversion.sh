#!/usr/bin/env bash
# Records a conversion through the RastroAff REST API.
#   RASTRO_API_KEY=rst_... ./conversion.sh CLICK_ID ORDER_ID 49.90
set -euo pipefail

curl --fail-with-body --silent --show-error \
  -X POST "https://rastroaff.com/api/v1/conversions" \
  -H "Authorization: Bearer ${RASTRO_API_KEY}" \
  -H "Content-Type: application/json" \
  --data "$(printf '{"clickId":"%s","transactionId":"%s","amount":"%s","status":"approved"}' "$1" "$2" "${3:-0}")"
echo
