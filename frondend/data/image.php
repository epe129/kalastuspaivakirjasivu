<?php
require_once __DIR__ . '/security.php';
require_fisherman();
require_once __DIR__ . '/db_connection.php';

$imageId = $_GET['id'] ?? null;
$fishId = filter_var(is_string($imageId) ? $imageId : '', FILTER_VALIDATE_INT);
if ($fishId === false || $fishId < 1) {
    http_response_code(404);
    exit;
}

$statement = $conn->prepare(
    'SELECT kala.kuva FROM kala '
    . 'JOIN tarppi ON tarppi.id = kala.tarppi_id '
    . 'WHERE kala.id = ? AND tarppi.kalastaja_id = ?'
);
$statement->bind_param('ii', $fishId, $_SESSION['kalastaja_id']);
$statement->execute();
$statement->bind_result($imageName);
if (!$statement->fetch()) {
    http_response_code(404);
    exit;
}
$statement->close();

if (!is_string($imageName) || !preg_match('/^[a-f0-9]{32}\.(jpg|png|gif)$/', $imageName)) {
    http_response_code(404);
    exit;
}

$imagePath = private_upload_directory() . $imageName;
if (!is_file($imagePath)) {
    http_response_code(404);
    exit;
}

$fileInfo = new finfo(FILEINFO_MIME_TYPE);
$mimeType = $fileInfo->file($imagePath);
$allowedTypes = ['image/jpeg', 'image/png', 'image/gif'];
if (!in_array($mimeType, $allowedTypes, true)) {
    http_response_code(404);
    exit;
}

header('Content-Type: ' . $mimeType);
header('Content-Length: ' . filesize($imagePath));
header('Cache-Control: private, no-store');
header('Content-Disposition: inline');
readfile($imagePath);
