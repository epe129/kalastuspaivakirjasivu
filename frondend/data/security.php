<?php
ini_set('session.use_strict_mode', '1');
ini_set('session.use_only_cookies', '1');
ini_set('session.cookie_httponly', '1');
ini_set('session.cookie_samesite', 'Lax');
ini_set('session.gc_maxlifetime', '3600');

$https = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off')
    || getenv('APP_HTTPS') === '1';
header('X-Content-Type-Options: nosniff');
header('X-Frame-Options: DENY');
header('Referrer-Policy: strict-origin-when-cross-origin');
header(
    "Content-Security-Policy: default-src 'self'; img-src 'self'; "
    . "style-src 'self' 'unsafe-inline'; script-src 'self'; "
    . "object-src 'none'; base-uri 'self'; frame-ancestors 'none'; form-action 'self'"
);
if ($https) {
    header('Strict-Transport-Security: max-age=31536000');
}
session_set_cookie_params([
    'lifetime' => 0,
    'path' => '/',
    'secure' => $https,
    'httponly' => true,
    'samesite' => 'Lax',
]);

if (session_status() !== PHP_SESSION_ACTIVE) {
    session_start();
}

function require_fisherman(): void
{
    $userId = filter_var($_SESSION['kalastaja_id'] ?? null, FILTER_VALIDATE_INT);
    $email = $_SESSION['email'] ?? null;
    $authenticatedAt = $_SESSION['authenticated_at'] ?? null;
    $lastActivity = $_SESSION['last_activity'] ?? null;
    $now = time();

    if (
        $userId === false || $userId < 1 || !is_string($email) || $email === ''
        || !is_int($authenticatedAt) || !is_int($lastActivity)
        || $now - $lastActivity > 1800 || $now - $authenticatedAt > 28800
    ) {
        $_SESSION = [];
        session_destroy();
        header('Location: ../login/index.php');
        exit;
    }

    $_SESSION['last_activity'] = $now;
    if (empty($_SESSION['csrf_logout'])) {
        $_SESSION['csrf_logout'] = bin2hex(random_bytes(32));
    }
}

function verify_csrf(string $key): void
{
    $expected = $_SESSION[$key] ?? null;
    $provided = $_POST[$key] ?? null;
    if (
        !is_string($expected) || !is_string($provided)
        || !hash_equals($expected, $provided)
    ) {
        http_response_code(403);
        exit('Request could not be verified.');
    }
    unset($_SESSION[$key]);
}

function post_string(string $key): string
{
    $value = $_POST[$key] ?? null;
    return is_string($value) ? trim($value) : '';
}

function html($value): string
{
    return htmlspecialchars((string)$value, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
}

function private_upload_directory(): string
{
    $documentRoot = realpath($_SERVER['DOCUMENT_ROOT'] ?? '');
    if ($documentRoot === false) {
        throw new RuntimeException('The web document root is not configured.');
    }

    $directory = getenv('APP_UPLOAD_DIR');
    if ($directory === false || $directory === '') {
        throw new RuntimeException('APP_UPLOAD_DIR is not configured.');
    }
    $isAbsolutePath = DIRECTORY_SEPARATOR === '\\'
        ? (
            (
                strlen($directory) >= 3
                && ctype_alpha($directory[0])
                && $directory[1] === ':'
                && ($directory[2] === '\\' || $directory[2] === '/')
            )
            || str_starts_with($directory, '\\\\')
        )
        : str_starts_with($directory, DIRECTORY_SEPARATOR);
    if (!$isAbsolutePath) {
        throw new RuntimeException('APP_UPLOAD_DIR must be an absolute path.');
    }

    if (!is_dir($directory) && !mkdir($directory, 0770, true) && !is_dir($directory)) {
        throw new RuntimeException('Could not create the private upload directory.');
    }

    $realDirectory = realpath($directory);
    $documentPrefix = rtrim($documentRoot, DIRECTORY_SEPARATOR) . DIRECTORY_SEPARATOR;
    if (
        $realDirectory === false
        || strncasecmp($realDirectory . DIRECTORY_SEPARATOR, $documentPrefix, strlen($documentPrefix)) === 0
    ) {
        throw new RuntimeException('Uploaded images must be stored outside the web root.');
    }

    return $realDirectory . DIRECTORY_SEPARATOR;
}
