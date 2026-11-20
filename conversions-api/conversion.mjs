// Records a conversion through the RastroAff REST API. Node.js 18+, no dependencies.
//   RASTRO_API_KEY=rst_... node conversion.mjs CLICK_ID ORDER_ID 49.90

export async function recordConversion(conversion) {
  const res = await fetch("https://rastroaff.com/api/v1/conversions", {
    method: "POST",
    headers: { Authorization: `Bearer ${process.env.RASTRO_API_KEY}`, "Content-Type": "application/json" },
    body: JSON.stringify(conversion),
    signal: AbortSignal.timeout(15_000),
  });
  const json = await res.json();
  if (!res.ok) throw new Error(`RastroAff API ${res.status}: ${JSON.stringify(json)}`);
  return json.data;
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const [clickId, transactionId, amount] = process.argv.slice(2);
  console.log(await recordConversion({ clickId, transactionId, amount, status: "approved" }));
}
