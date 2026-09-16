<?php
// Cloudways serves index.php before index.html; hand the invitation straight through.
// www.tadyjohana.com -> tadyjohana.com so guests always share one address.
$host = isset($_SERVER['HTTP_HOST']) ? strtolower($_SERVER['HTTP_HOST']) : '';
if (strpos($host, 'www.') === 0) {
  header('Location: https://' . substr($host, 4) . $_SERVER['REQUEST_URI'], true, 301);
  exit;
}
// The page is small; never cache it (Varnish and browsers), so every deployment shows at once.
// Videos and images carry a version stamp in their URLs and stay cached for a year.
header('Content-Type: text/html; charset=utf-8');
header('Cache-Control: no-cache, no-store, must-revalidate, max-age=0');
header('Pragma: no-cache');
header('Expires: 0');
readfile(__DIR__ . '/index.html');
