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

  if (!isset($_POST['csrf_token_p']) || !isset($_SESSION['csrf_token_p']) || !hash_equals($_SESSION['csrf_token_p'], $_POST['csrf_token_p'])) {
    die('CSRF token validation failed');
  }

  $poista_get = stripslashes(trim(htmlspecialchars($_POST["poista"])));
  $poistaArray = explode(" ", $poista_get);
  $k_id = $poistaArray[0];
  $aika = $poistaArray[1];
  $kala = $poistaArray[3];
  
  print_r($k_id);
  echo "<br/>";
  print_r($aika);
  echo "<br/>";
  print_r($kala);

  $poista = $conn->prepare("");
  $poista->bind_param("iss", $k_id, $aika, $kala);
  
  if ($poista->execute() === True) {

  } else {

  }

}