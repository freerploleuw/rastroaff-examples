<?php
// Sends a conversion to RastroAff by S2S postback. PHP 7.4+ with the curl extension.
//
//   RASTRO_POSTBACK_URL=https://track.rastroaff.com/postback RASTRO_TOKEN=... \
//     php postback.php CLICK_ID ORDER_ID 49.90 approved

function rastro_postback(array $data, int $attempts = 5): string
{
    $params = array_filter([
        'token'       => getenv('RASTRO_TOKEN'),
        'click_id'    => $data['click_id'] ?? null,
        'txn_id'      => $data['txn_id'] ?? null,
        'amount'      => $data['amount'] ?? null,
        'status'      => $data['status'] ?? 'approved',
        'goal'        => $data['goal'] ?? null,
        'coupon'      => $data['coupon'] ?? null,
        'country'     => $data['country'] ?? null,
        'customer_id' => $data['customer_id'] ?? null,
    ], fn ($v) => $v !== null && $v !== '');
    $url = getenv('RASTRO_POSTBACK_URL') . '?' . http_build_query($params);

    for ($attempt = 1; ; $attempt++) {
        $ch = curl_init($url);
        curl_setopt_array($ch, [CURLOPT_RETURNTRANSFER => true, CURLOPT_TIMEOUT => 15]);
        $body = curl_exec($ch);
        $code = (int) curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
        curl_close($ch);

        if ($body !== false && $code >= 200 && $code < 300) {
            return $body;
        }
        if ($code >= 400 && $code < 500) {
            throw new RuntimeException("Postback refused ($code): $body");
        }
        if ($attempt >= $attempts) {
            throw new RuntimeException("Postback failed ($code)");
        }
        sleep(2 ** $attempt);
    }
}

if (PHP_SAPI === 'cli' && realpath($argv[0]) === __FILE__) {
    echo rastro_postback([
        'click_id' => $argv[1],
        'txn_id'   => $argv[2],
        'amount'   => $argv[3] ?? null,
        'status'   => $argv[4] ?? 'approved',
    ]), PHP_EOL;
}
