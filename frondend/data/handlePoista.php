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
  $kala_id = $poistaArray[1];
  $tarppi_id = $poistaArray[2];
  $laji_id = $poistaArray[3];
  $aika = $poistaArray[4];

  print_r($poistaArray);  
  echo "<br/>";  
  print_r($k_id);
  echo "<br/>";
  print_r($kala_id);
  echo "<br/>";
  print_r($tarppi_id);
  echo "<br/>";
  print_r($laji_id);
  echo "<br/>";
  print_r($aika);

  $kala_delete = $conn->prepare("DELETE FROM kala WHERE kala.id = ? AND kala.tarppi_id = ? and kala.laji_id = ?");
  $kala_delete->bind_param("iii", $kala_id, $tarppi_id, $laji_id);

  $tarppi_delete = $conn->prepare("");
  $tarppi_delete->bind_param("iii", $kala_id, $tarppi_id, $laji_id);
  

  // if ($poista->execute() === True) {

  // } else {

  // }

}

// header("Location: ../main/poista.php"); 
// exit;
