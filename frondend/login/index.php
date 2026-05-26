<?php 
session_start();
unset($_SESSION['errorTextRegister']);
// CSRF suojaus ettei voi kuka vaan tehdä pyyntojö 
if (empty($_SESSION['csrf_token_l'])) {
    $_SESSION['csrf_token_l'] = bin2hex(random_bytes(32));
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kirjaudu Sisään</title>
    <link rel="stylesheet" href="login.css">
</head>
<body>
    <form action="../data/handleLogin.php" method="POST">
        <h1>Kirjaudu Sisään</h1>
        <br>
        <label>Sähköposti</label>
        <input type="email" name="email" pattern="[a-z0-9._%+\-]+@[a-z0-9.\-]+\.[a-z]{2,}$" required>
        <br>
        <label>Salasana</label>
        <input type="password" name="password" required>
        <br>
        <button type="submit">Lähetä</button>
        <br>
        <?php
        //  saa viestin jos kirjautuminen epäonnistui
        if (isset($_SESSION['errorMessageLogin']) and isset($_SESSION['errorTextLogin'])) {
            $text = ucfirst($_SESSION['errorTextLogin']);
            echo "
            <br/>
            <span>$text</span>
            <br/>
            ";
        }
        ?>
        <br>
        <a href="../index.php">Rekisteröidy</a>
        <input type="hidden" name="csrf_token_l" value="<?php echo htmlspecialchars($_SESSION['csrf_token_l']) ?>">
    </form>
</body>
</html>