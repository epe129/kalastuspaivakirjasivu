<?php
session_start();
// yhteyden tietokantaan
include_once('db_connection.php');

$saatu_arvo = $laji = $pituus = $paino = $paikka = $aika = $viehe = $vapa = "";
$kalastaja_id = $viehe_id = $vapa_id = $tarppi_id = $laji_id = 0;
$tarppi_tiedot_lisaamien = false;
$saadut = array();

// tarkistetaan että käyttäjä on kirjautunut
if (!isset($_SESSION['email']) and !isset($_SESSION["kalastaja_id"])) {
  header("Location: ../login/index.php");
  exit();
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {

  // tarkistaa onko tokeni asetettu ja onko tokenit samatat session ja input saanissa
  if (!isset($_POST['csrf_token_li']) || !isset($_SESSION['csrf_token_li']) || !hash_equals($_SESSION['csrf_token_li'], $_POST['csrf_token_li'])) {
    die('CSRF token validation failed');
  }
  
  // poistetaan tokeni
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
  $kalastaja_id = $_SESSION["kalastaja_id"];
    
  $saa_vapa_id = $conn->prepare("SELECT id FROM vapa WHERE vapa = ?");
  $saa_vapa_id->bind_param("s", $vapa);
  $saa_vapa_id->execute();
  $saa_vapa_id->bind_result($vapa_id);
  $saa_vapa_id->fetch();
  $saa_vapa_id->close();
  
  $saa_viehe_id = $conn->prepare("SELECT id FROM viehe WHERE viehe = ?");
  $saa_viehe_id->bind_param("s", $viehe);
  $saa_viehe_id->execute();
  $saa_viehe_id->bind_result($viehe_id);
  $saa_viehe_id->fetch();
  $saa_viehe_id->close();
    
  $saa_laji_id = $conn->prepare("SELECT id FROM laji WHERE laji = ?");
  $saa_laji_id->bind_param("s", $laji);
  $saa_laji_id->execute();
  $saa_laji_id->bind_result($laji_id);
  $saa_laji_id->fetch();
  $saa_laji_id->close();

  // varmista että valittu laji, viehe ja vapa löytyvät tietokannasta
  if (empty($vapa_id) || empty($viehe_id) || empty($laji_id)) {
    $_SESSION["MessageAdd"] = true;
    $_SESSION['Text'] = "Valittu vapa, viehe tai laji ei löydy tietokannasta";
    header("Location: ../main/lisaa.php"); 
    exit;
  }

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
  $lisaa_kala->bind_param("iddi", $tarppi_id, $pituus, $paino, $laji_id);
  
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
