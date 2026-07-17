<?php
session_start();
unset($_SESSION['MessageAdd']);
// Saadaan yhteys tietokantaan 
include_once('../data/db_connection.php');
// tarkistetaan että käyttäjä on kirjautunut
if (!isset($_SESSION['email']) and !isset($_SESSION["kalastaja_id"])) {
    header("Location: ../login/index.php");
    exit();
}
// kun cookie häviää kirjaa käyttäjän ulos
if(!isset($_COOKIE["login_token"])) {
    // Poista kaikki istunnon muuttujat.
    $_SESSION = array();
    session_unset();
    // tuhoaa istunnon.
    session_destroy();
    // Ohjaa käyttäjän takaisin kirjautumissivulle.
    header("Location: ../login/index.php");
    exit;
}
$kalastaja_id = $_SESSION["kalastaja_id"]; 
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Poista kalasaaliita</title>
</head>
<body>
    <?php

    ?>
</body>
</html>