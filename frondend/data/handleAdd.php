<?php
require_once __DIR__ . '/security.php';
require_fisherman();
// yhteyden tietokantaan
require_once __DIR__ . '/db_connection.php';

if ($_SERVER["REQUEST_METHOD"] == "POST") {
  verify_csrf('csrf_token_li');
  unset( $_SESSION['MessageAdd'] );
  unset( $_SESSION['Text'] );

  $laji = post_string("laji");
  $pituus = post_string("pituus");
  $paino = post_string("paino");
  $paikka = post_string("paikka");
  $aika = post_string("aika");
  $viehe = post_string("viehe");
  $vapa = post_string("vapa");

  if (
    !preg_match("/^[a-zA-ZäöåÄÖÅ]+$/u", $laji)
    || !is_numeric($pituus) || (float)$pituus <= 0 || (float)$pituus > 1000
    || !is_numeric($paino) || (float)$paino <= 0 || (float)$paino > 1000
    || !preg_match("/^[a-zA-Z0-9äöåÄÖÅ -]{1,64}$/u", $paikka)
    || !preg_match("/^[a-zA-ZäöåÄÖÅ]+$/u", $viehe)
    || !preg_match("/^[a-zA-ZäöåÄÖÅ]+$/u", $vapa)
  ) {
    $_SESSION["MessageAdd"] = true;
    $_SESSION['Text'] = "syötteessä ei saa olla erikoismerkkejä";
    header("Location: ../main/lisaa.php"); 
    exit;
  }

  if (
    $laji === '' || $pituus === '' || $paino === '' || $paikka === ''
    || $aika === '' || $viehe === '' || $vapa === ''
  ) {
    $_SESSION["MessageAdd"] = true;
    $_SESSION['Text'] = "Jokin kohta oli tyhjä";
    header("Location: ../main/lisaa.php"); 
    exit;
  } 

  $date = DateTimeImmutable::createFromFormat('!Y-m-d', $aika);
  if (
    $date === false || $date->format('Y-m-d') !== $aika
    || $date > new DateTimeImmutable('today')
  ) {
    $_SESSION["MessageAdd"] = true;
    $_SESSION['Text'] = "Päivämäärä ei ole kelvollinen";
    header("Location: ../main/lisaa.php");
    exit;
  }

  // käsittele tiedoston lataus, jos käyttäjä on valinnut kuvan
  $safeName = null;
  if (isset($_FILES['fileToUpload']) && $_FILES['fileToUpload']['error'] !== UPLOAD_ERR_NO_FILE) {
    if ($_FILES['fileToUpload']['error'] !== UPLOAD_ERR_OK) {
      $_SESSION["MessageAdd"] = true;
      $_SESSION['Text'] = "Virhe tiedoston latauksessa";
      header("Location: ../main/lisaa.php");
      exit;
    }

    $temporaryFile = $_FILES['fileToUpload']['tmp_name'];
    if (!is_uploaded_file($temporaryFile)) {
      $_SESSION["MessageAdd"] = true;
      $_SESSION['Text'] = "Virhe tiedoston latauksessa";
      header("Location: ../main/lisaa.php");
      exit;
    }
    $imageInfo = getimagesize($temporaryFile);
    $fileInfo = new finfo(FILEINFO_MIME_TYPE);
    $mimeType = $fileInfo->file($temporaryFile);
    $allowedTypes = ['image/jpeg' => 'jpg', 'image/png' => 'png', 'image/gif' => 'gif'];
    if (
      $imageInfo === false || !isset($allowedTypes[$mimeType])
      || $imageInfo['mime'] !== $mimeType
    ) {
      $_SESSION["MessageAdd"] = true;
      $_SESSION['Text'] = "Tiedosto ei ole kelvollinen kuva.";
      header("Location: ../main/lisaa.php");
      exit;
    }

    if (
      filesize($temporaryFile) > 500000
      || $imageInfo[0] * $imageInfo[1] > 20000000
    ) {
      $_SESSION["MessageAdd"] = true;
      $_SESSION['Text'] = "Kuva on liian suuri (max 500KB).";
      header("Location: ../main/lisaa.php");
      exit;
    }

    $uploadDir = private_upload_directory();
    $safeName = bin2hex(random_bytes(16)) . '.' . $allowedTypes[$mimeType];
    $targetFile = $uploadDir . $safeName;

    if (!move_uploaded_file($_FILES['fileToUpload']['tmp_name'], $targetFile)) {
      $_SESSION["MessageAdd"] = true;
      $_SESSION['Text'] = "Kuvan siirto uploads-kansioon epäonnistui.";
      header("Location: ../main/lisaa.php");
      exit;
    }
    
  }

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

  // varmistaa että valittu laji, viehe ja vapa löytyvät tietokannasta
  if (empty($vapa_id) || empty($viehe_id) || empty($laji_id)) {
    if ($safeName !== null) {
      unlink(private_upload_directory() . $safeName);
    }
    $_SESSION["MessageAdd"] = true;
    $_SESSION['Text'] = "Valittu vapa, viehe tai laji ei löydy tietokannasta";
    header("Location: ../main/lisaa.php"); 
    exit;
  }

  $transactionStarted = false;
  try {
    $conn->begin_transaction();
    $transactionStarted = true;
    $lisaa_tarppi = $conn->prepare("INSERT INTO tarppi (aika, kalastaja_id, viehe_id, vapa_id, paikka) VALUES (?, ?, ?, ?, ?)");
    $lisaa_tarppi->bind_param("siiis", $aika, $kalastaja_id, $viehe_id, $vapa_id, $paikka);
    $lisaa_tarppi->execute();

    $tarppi_id = $lisaa_tarppi->insert_id;
    $lisaa_kala = $conn->prepare("INSERT INTO kala (tarppi_id, pituus, paino, laji_id, kuva) VALUES (?, ?, ?, ?, ?)");
    $lisaa_kala->bind_param("iddis", $tarppi_id, $pituus, $paino, $laji_id, $safeName);
    $lisaa_kala->execute();
    $conn->commit();
    $transactionStarted = false;
  } catch (mysqli_sql_exception $exception) {
    if ($transactionStarted) {
      $conn->rollback();
    }
    if ($safeName !== null) {
      unlink(private_upload_directory() . $safeName);
    }
    error_log('Catch save failed: ' . $exception->getMessage());
    $_SESSION["MessageAdd"] = true;
    $_SESSION['Text'] = "Tietojen lisääminen epäonnistui";
    header("Location: ../main/lisaa.php");
    exit;
  }

  $_SESSION["MessageAdd"] = true;
  $_SESSION['Text'] = "Tiedot lisättiin onnistuneesti";
  header("Location: ../main/lisaa.php");
  exit;
}

http_response_code(405);
header('Allow: POST');
