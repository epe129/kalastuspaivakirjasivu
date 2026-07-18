<?php
session_start();
// yhteyden tietokantaan
include_once('db_connection.php');


// tarkistetaan että käyttäjä on kirjautunut
if (!isset($_SESSION['email']) and !isset($_SESSION["kalastaja_id"])) {
  header("Location: ../login/index.php");
  exit();
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $poista = stripslashes(trim(htmlspecialchars($_POST["poista"])));
    echo "$poista";
}