// Sends a conversion to RastroAff by S2S postback. Node.js 18+, no dependencies.
//
//   RASTRO_POSTBACK_URL=https://track.rastroaff.com/postback RASTRO_TOKEN=... \
//     node postback.mjs CLICK_ID ORDER_ID 49.90 approved

const BASE = process.env.RASTRO_POSTBACK_URL;
const TOKEN = process.env.RASTRO_TOKEN;

export async function sendPostback({ clickId, txnId, amount, status = "approved", goal, coupon, country, customerId }) {
  const url = new URL(BASE);
  const params = { token: TOKEN, click_id: clickId, txn_id: txnId, amount, status, goal, coupon, country, customer_id: customerId };
  for (const [key, value] of Object.entries(params)) {
    if (value !== undefined && value !== null && value !== "") url.searchParams.set(key, String(value));
  }

  // Retry network errors and 5xx with growing waits; 4xx means the request must be fixed.
  for (let attempt = 1; ; attempt++) {
    try {
      const res = await fetch(url, { signal: AbortSignal.timeout(15_000) });
      const body = await res.text();
      if (res.ok) return body;
      if (res.status < 500) throw Object.assign(new Error(`Postback refused (${res.status}): ${body}`), { final: true });
      if (attempt >= 5) throw new Error(`Postback failed (${res.status}): ${body}`);
    } catch (err) {
      if (err.final || attempt >= 5) throw err;
    }
    await new Promise((r) => setTimeout(r, 1000 * 2 ** attempt));
  }
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const [clickId, txnId, amount, status] = process.argv.slice(2);
  console.log(await sendPostback({ clickId, txnId, amount, status }));
}
