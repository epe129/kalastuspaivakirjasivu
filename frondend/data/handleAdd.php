<?php
session_start();
// yhteyden tietokantaan
include('db_connection.php');

$saatu_arvo = $laji = $pituus = $paino = $paikka = $aika = $viehe = $vapa = "";
$kalastaja_id = $viehe_id = $vapa_id = $tarppi_id = $laji_id = 0;
$tarppi_tiedot_lisaamien = false;
$saadut = array();

if ($_SERVER["REQUEST_METHOD"] == "POST") {
  
  // tarkistaa onko tokeni asetettu ja onko tokenit samatat session ja input saanissa
  if (!isset($_POST['csrf_token_li']) || !isset($_SESSION['csrf_token_li']) || !hash_equals($_SESSION['csrf_token_li'], $_POST['csrf_token_li'])) {
    die('CSRF token validation failed');
  }
  
  unset($_SESSION['csrf_token_li']);

  // ei aseta muuttujaa vasta kun jos tulee vastaan if lauseessa
  unset( $_SESSION['MessageAdd'] );
  unset( $_SESSION['Text'] );

  // saa arvot
  $laji = stripslashes(trim(htmlspecialchars($_POST["laji"])));
  $pituus = stripslashes(trim(htmlspecialchars($_POST["pituus"])));
  $paino = stripslashes(trim(htmlspecialchars($_POST["paino"])));
  $paikka = stripslashes(trim(htmlspecialchars($_POST["paikka"])));
  $aika = stripslashes(trim(htmlspecialchars($_POST["aika"])));
  $viehe = stripslashes(trim(htmlspecialchars($_POST["viehe"])));
  $vapa = stripslashes(trim(htmlspecialchars($_POST["vapa"])));

  // tarkistaa että inputit sisältää vain sille salittuja merkkejä
  if (!preg_match("/^[a-zA-ZäöåÄÖÅ]+$/u", $laji) or !preg_match("/^[0-9.]+$/u", $pituus) or !preg_match("/^[0-9.]+$/u", $paino) or !preg_match("/^[a-zA-Z0-9äöåÄÖÅ]+$/u", $paikka) or !preg_match("/^[a-zA-ZäöåÄÖÅ]+$/u", $viehe) or !preg_match("/^[a-zA-ZäöåÄÖÅ]+$/u", $vapa)) {
    $_SESSION["MessageAdd"] = true;
    $_SESSION['Text'] = "syötteessä ei saa olla erikoismerkkejä";
    header("Location: ../main/lisaa.php"); 
    exit;
  }

  // tarkistaa ettei ole tyhjä 
  if (empty($laji) or empty($pituus) or empty($paino) or empty($paikka) or empty($aika) or empty($viehe) or empty($vapa)) {
    $_SESSION["MessageAdd"] = true;
    $_SESSION['Text'] = "Jokin kohta oli tyhjä";
    header("Location: ../main/lisaa.php"); 
    exit;
  } 
  
  // saa kaikki id:t mitä tarvittee
  $selectit = array($_SESSION["email"]=>"SELECT id FROM kalastaja WHERE email = ?", $vapa=>"SELECT id FROM vapa WHERE vapa = ?", $viehe=>"SELECT id FROM viehe WHERE viehe = ?",  $laji=>"SELECT id FROM laji WHERE laji = ?");
  foreach ($selectit as $key => $value) {
    $saa_id = $conn->prepare($value);
    $saa_id->bind_param("s", $key);
    $saa_id->execute();
    $saa_id->bind_result($saatu_arvo);
    $saa_id->fetch();
    $saadut[] = "$saatu_arvo";
    $saa_id->close();
  }
  $kalastaja_id = $saadut[0];
  $vapa_id = $saadut[1];
  $viehe_id = $saadut[2];
  $laji_id = $saadut[3];

  // lisää tarppi tiedot 
  $lisaa_tarppi = $conn->prepare("INSERT INTO tarppi (aika, kalastaja_id, viehe_id, vapa_id, paikka) VALUES (?, ?, ?, ?, ?)");
  $lisaa_tarppi->bind_param("siiis", $aika, $kalastaja_id, $viehe_id, $vapa_id, $paikka);
  
  if ($lisaa_tarppi->execute() === TRUE) {
    $tarppi_tiedot_lisaamien = TRUE;
  } else {
    $_SESSION["MessageAdd"] = true;
    $_SESSION['Text'] = "Tietojen lisääminen epäonnistui";
    header("Location: ../main/lisaa.php"); 
    exit;
  }

  // saa tarppi id:n
  $tarppi_id = $lisaa_tarppi->insert_id; 
  // lisää kala tiedot
  $lisaa_kala = $conn->prepare("INSERT INTO kala (tarppi_id, pituus, paino, laji_id) VALUES (?, ?, ?, ?)");
  $lisaa_kala->bind_param("iiii", $tarppi_id, $pituus, $paino, $laji_id);
  
  // tarkistaa että molemmat syötöt onnistui
  if ($lisaa_kala->execute() === TRUE and $tarppi_tiedot_lisaamien === TRUE) {
    $_SESSION["MessageAdd"] = true;
    $_SESSION['Text'] = "Tiedot lisättiin onnistuneesti";
    header("Location: ../main/lisaa.php"); 
    exit;
    } else {
      $_SESSION["MessageAdd"] = true;
      $_SESSION['Text'] = "Tietojen lisääminen epäonnistui";
      header("Location: ../main/lisaa.php"); 
      exit;
    }
  } 
  header("Location: ../main/lisaa.php"); 
  exit;
?>