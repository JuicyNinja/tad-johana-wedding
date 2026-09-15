<?php
// Cloudways serves index.php before index.html; hand the invitation straight through.
header('Content-Type: text/html; charset=utf-8');
readfile(__DIR__ . '/index.html');
