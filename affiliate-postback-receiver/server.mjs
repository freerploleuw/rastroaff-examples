// Minimal receiver for RastroAff affiliate postbacks. Node.js 18+, no dependencies.
// Configure in RastroAff (Integration → Postback):
//   https://your-server.example/rastro/postback?conv={conversion_id}&click={click_id}&payout={payout}&currency={currency}&status={status}&sub1={sub1}
// Add a secret of your own to the URL (for example &key=LONG_RANDOM_VALUE) and check it here.
import { createServer } from "node:http";

const SECRET = process.env.POSTBACK_SECRET ?? "";
const conversions = new Map(); // replace with your database

createServer((req, res) => {
  const url = new URL(req.url, "http://localhost");
  if (url.pathname !== "/rastro/postback") return res.writeHead(404).end();
  const q = url.searchParams;
  if (SECRET && q.get("key") !== SECRET) return res.writeHead(403).end("forbidden");

  const id = q.get("conv") || `${q.get("click")}:${q.get("txn") ?? ""}`;
  // Idempotent: the same conversion can arrive again with a new status (e.g. reversed).
  conversions.set(id, {
    clickId: q.get("click"),
    payout: Number(q.get("payout") ?? 0),
    currency: q.get("currency"),
    status: q.get("status"),
    sub1: q.get("sub1"),
    updatedAt: new Date().toISOString(),
  });
  console.log("conversion", id, conversions.get(id));
  res.writeHead(200, { "Content-Type": "text/plain" }).end("ok");
}).listen(Number(process.env.PORT ?? 8080), () => console.log("listening"));
