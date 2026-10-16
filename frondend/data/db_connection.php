<?php
mysqli_report(MYSQLI_REPORT_ERROR | MYSQLI_REPORT_STRICT);
$configs = require __DIR__ . '/config.php';
$requiredSettings = ['serverinnimi', 'kayttajannimi', 'salasana', 'dbnimi'];
foreach ($requiredSettings as $setting) {
    if (!array_key_exists($setting, $configs) || !is_string($configs[$setting])) {
        throw new RuntimeException('Database configuration is incomplete.');
    }
}
$port = $configs['port'] ?? 3306;
if (!is_int($port) || $port < 1 || $port > 65535) {
    throw new RuntimeException('Database configuration has an invalid port.');
}

$conn = new mysqli(
    $configs['serverinnimi'],
    $configs['kayttajannimi'],
    $configs['salasana'],
    $configs['dbnimi'],
    $port
);
$conn->set_charset('utf8mb4');
