<?php 
session_start(); 
unset($_SESSION['errorTextLogin']);
// CSRF suojaus ettei voi kuka vaan tehdä pyyntojö 
if (empty($_SESSION['csrf_token_r'])) {
    $_SESSION['csrf_token_r'] = bin2hex(random_bytes(32));
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rekisteröidy</title>
    <link rel="stylesheet" href="rekister.css">
</head>
<body>
    <br/>
    <div class="otsikko_div">
        <h1>Tervetuloa kalastus sivulle, <br/> rekisteröidy aloittaaksesi omien kala tietojen tallennus</h1>
    </div>
    <br/>
    <form action="./data/handleRegister.php" method="POST">
        <h1>Rekisteröidy</h1>
        <br>
        <label>Nimi</label>
        <input type="text" name="name" required>
        <br>
        <label>Sähköposti</label>
        <input type="email" name="email" pattern="[a-z0-9._%+\-]+@[a-z0-9.\-]+\.[a-z]{2,}$" required>
        <br>
        <label>Salasana</label>
        <input type="password" name="password" required>
        <br>
        <button type="submit">Läheta</button>
        <br>
        <?php
        //  saa viestin jos rekisteröityminen epäonnnistui
        if (isset($_SESSION['errorMessageRegister']) and isset($_SESSION['errorTextRegister'])) {
            $text = ucfirst($_SESSION['errorTextRegister']);
            echo "
            <br/>
            <span>$text</span>
            <br/>";
        }
        ?>
        <br>
        <a href="./login/index.php">Kirjaudu Sisään</a>
        <input type="hidden" name="csrf_token_r" value="<?php echo htmlspecialchars($_SESSION['csrf_token_r']) ?>">
    </form>
</body>
</html>