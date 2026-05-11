<?php
session_start();
// yhteyden tietokantaan
$db = include('db_connection.php');
$laji = $pituus = $paino = $paikka = $aika = $viehe = $vapa = "";
$kalastaja_id = $viehe_id = $vapa_id = $tarppi_id = $laji_id = 0;
$tarppi_tiedot_lisaamien = false;
if ($_SERVER["REQUEST_METHOD"] == "POST") {
  // ei aseta muuttujaa vasta kun jos tulee vastaan if lauseessa
  unset( $_SESSION['SuccesfullAdd'] );
  unset( $_SESSION['ErrorAdd'] );
  // saa arvot
  $laji = htmlspecialchars($_POST["laji"]);
  $pituus = htmlspecialchars($_POST["pituus"]);
  $paino = htmlspecialchars($_POST["paino"]);
  $paikka = htmlspecialchars($_POST["paikka"]);
  $aika = htmlspecialchars($_POST["aika"]);
  $viehe = htmlspecialchars($_POST["viehe"]);
  $vapa = htmlspecialchars($_POST["vapa"]);
  if (empty($laji) or empty($pituus) or empty($paino) or empty($paikka) or empty($aika) or empty($viehe) or empty($vapa)) {
    $_SESSION["ErrorAdd"] = true;
    header("Location: ../main/lisaa.php"); 
    exit;
    } else {
      // saa kaikki id:t mitä tarvittee
    $saa_kalastaja_id = $conn->prepare("SELECT id FROM kalastaja WHERE email = ?");
    $saa_kalastaja_id->bind_param("s", $_SESSION["email"]);
    $saa_kalastaja_id->execute();
    $saa_kalastaja_id->bind_result($kalastaja_id);
    $saa_kalastaja_id->fetch();
    $saa_kalastaja_id->close();
    
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

    // lisää tarppi tiedot 
    $lisaa_tarppi = $conn->prepare("INSERT INTO tarppi (aika, kalastaja_id, viehe_id, vapa_id, paikka) VALUES (?, ?, ?, ?, ?)");
    $lisaa_tarppi->bind_param("siiis", $aika, $kalastaja_id, $viehe_id, $vapa_id, $paikka);
    if ($lisaa_tarppi->execute() === TRUE) {
      $tarppi_tiedot_lisaamien = TRUE;
    } else {
      $_SESSION["ErrorAdd"] = true;
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
      $_SESSION["SuccesfullAdd"] = true;
      header("Location: ../main/lisaa.php"); 
      exit;
      } else {
        $_SESSION["ErrorAdd"] = true;
        header("Location: ../main/lisaa.php"); 
        exit;
      }
    } 
  } else {
    header("Location: ../main/lisaa.php"); 
    exit;
  }
?>