<?php
// Cloudways serves index.php before index.html; hand the invitation straight through.
// Short cache life so Varnish picks up new deployments within a few minutes.
header('Content-Type: text/html; charset=utf-8');
header('Cache-Control: public, max-age=300');
readfile(__DIR__ . '/index.html');
