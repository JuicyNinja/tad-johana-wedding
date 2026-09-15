<?php
// Cloudways serves index.php before index.html; hand the invitation straight through.
// www.tadyjohana.com -> tadyjohana.com so guests always share one address.
$host = isset($_SERVER['HTTP_HOST']) ? strtolower($_SERVER['HTTP_HOST']) : '';
if (strpos($host, 'www.') === 0) {
  header('Location: https://' . substr($host, 4) . $_SERVER['REQUEST_URI'], true, 301);
  exit;
}
// Short cache life so Varnish picks up new deployments within a few minutes.
header('Content-Type: text/html; charset=utf-8');
header('Cache-Control: public, max-age=300');
readfile(__DIR__ . '/index.html');
