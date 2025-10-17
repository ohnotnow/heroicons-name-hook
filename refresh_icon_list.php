<?php

$url = "https://api.github.com/repos/tailwindlabs/heroicons/contents/optimized/24/outline";

// GitHub API requires a User-Agent header
$opts = [
    "http" => [
        "method" => "GET",
        "header" => "User-Agent: PHP Script\r\n"
    ]
];

$context = stream_context_create($opts);
$json = file_get_contents($url, false, $context);
$data = json_decode($json, true);

// Extract filenames
$filenames = array_filter(array_map(function($item) {
    return $item['type'] === 'file' ? $item['name'] : null;
}, $data));

// Write to file
file_put_contents('heroicon-list.txt', implode("\n", $filenames) . "\n");

echo "Written " . count($filenames) . " icon filenames to heroicon-list.txt\n";

