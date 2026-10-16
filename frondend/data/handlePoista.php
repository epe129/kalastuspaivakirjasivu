<?php
require_once __DIR__ . '/security.php';
require_fisherman();
// yhteyden tietokantaan
require_once __DIR__ . '/db_connection.php';

// tarkistetaan että käyttäjä on kirjautunut
if ($_SERVER["REQUEST_METHOD"] == "POST") {
  verify_csrf('csrf_token_p');
  $fishId = filter_var(post_string('fish_id'), FILTER_VALIDATE_INT);
  if ($fishId === false || $fishId < 1) {
    http_response_code(400);
    exit('Invalid catch selection.');
  }

  $imageName = null;
  $select = $conn->prepare(
    "SELECT kala.kuva, kala.tarppi_id FROM kala "
    . "JOIN tarppi ON tarppi.id = kala.tarppi_id "
    . "WHERE kala.id = ? AND tarppi.kalastaja_id = ?"
  );
  $select->bind_param("ii", $fishId, $_SESSION['kalastaja_id']);
  $select->execute();
  $select->bind_result($imageName, $catchId);
  $exists = $select->fetch();
  $select->close();

  if (!$exists) {
    http_response_code(404);
    exit('Catch not found.');
  }

  $conn->begin_transaction();
  $kala_delete = $conn->prepare(
    "DELETE FROM kala WHERE id = ? AND tarppi_id = ?"
  );
  $kala_delete->bind_param("ii", $fishId, $catchId);
  $kala_delete->execute();
  $tarppi_delete = $conn->prepare(
    "DELETE FROM tarppi WHERE id = ? AND kalastaja_id = ?"
  );
  $tarppi_delete->bind_param("ii", $catchId, $_SESSION["kalastaja_id"]);
  if ($kala_delete->affected_rows === 1 && $tarppi_delete->execute()) {
    $conn->commit();
    if (
      is_string($imageName)
      && preg_match('/^[a-f0-9]{32}\.(jpg|png|gif)$/', $imageName)
    ) {
      $imagePath = private_upload_directory() . $imageName;
      if (is_file($imagePath)) {
        unlink($imagePath);
      }
    }
    $_SESSION['MessagePoista'] = True;
    $_SESSION['TextPoista'] = "Saalis poistettiin onnistuneesti";
  } else {
    $conn->rollback();
    $_SESSION['MessagePoista'] = True;
    $_SESSION['TextPoista'] = "Saaliin poistaminen epännistui";
  }
} else {
  http_response_code(405);
  header('Allow: POST');
  exit;
}
header("Location: ../main/poista.php"); 
exit;