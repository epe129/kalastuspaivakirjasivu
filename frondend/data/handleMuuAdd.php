<?php
session_start();
// yhteyden tietokantaan
include('db_connection.php');

$laji = $viehe = $vapa = "";
$array_arvot = array("laji", "viehe", "vapa");

if ($_SERVER["REQUEST_METHOD"] == "POST") {
  
  // tarkistaa onko tokeni asetettu ja onko tokenit samatat session ja input saanissa
  if (!isset($_POST['csrf_token_li_muu']) || !isset($_SESSION['csrf_token_li_muu']) || !hash_equals($_SESSION['csrf_token_li_muu'], $_POST['csrf_token_li_muu'])) {
    die('CSRF token validation failed');
  }

  unset($_SESSION['csrf_token_li_muu']);

  // ei aseta muuttujaa vasta kun jos tulee vastaan if lauseessa
  unset( $_SESSION['MessageAdd'] );
  unset( $_SESSION['Text'] );
  
  foreach ($array_arvot as $x) {
    // hakee aina name inputin avulla ja kattoo onko tyhjä name on aina esim name="laji"
    $get_arvo = stripslashes(trim(htmlspecialchars($_POST["$x"]))); 
    // tarkistaa onko input tyhjä
    if (strlen($get_arvo) != 0) {

      // tarkistaa että syötteessä on vain kirjaimia
      if (!preg_match("/^[a-zA-ZäöåÄÖÅ]+$/u", $get_arvo)) {
        $_SESSION["MessageAdd"] = true;
        $_SESSION['Text'] = "Syötteessä saa olla vain kirjaimia";
        header("Location: ../main/lisaa.php"); 
        exit;
      }

      // tarkistaa onko arvo jo tietokannassa
      $onko_result = $conn->prepare("SELECT * FROM $x WHERE $x = ?");
      $onko_result->bind_param("s", $get_arvo);
      $onko_result->execute();
      $onko_result->store_result();
      
      // jos arvo on jo tietokannassa
      if ($onko_result->num_rows > 0) {
        $_SESSION["MessageAdd"] = true;
        $_SESSION['Text'] = "$x on jo tietokannassa";
        header("Location: ../main/lisaa.php");
        exit; 
      } 
        
      // lisää arvon jos ei oo tietokannassa
      $stmt_lisaa = $conn->prepare("INSERT INTO $x ($x) VALUES (?)");
      $stmt_lisaa->bind_param("s", $get_arvo);
      
      if ($stmt_lisaa->execute() === TRUE) {
        // jos lisääminen onnistui saa viestin ja menee takaisin samalle sivulle
        $_SESSION["MessageAdd"] = true;
        $_SESSION['Text'] = "Uusi $x lisättiin onnistuneesti";
        header("Location: ../main/lisaa.php"); 
        exit;
        } else {
          // jos lisääminen ei onnistunut saa viestin ja menee takaisin samalle sivulle
          $_SESSION["MessageAdd"] = true;
          $_SESSION['Text'] = "Uuden $x lisääminen epäonnistui";
          header("Location: ../main/lisaa.php"); 
          exit;
        }
      } else {
        continue;
      }
    }
  } 
  header("Location: ../main/lisaa.php"); 
  exit;
?>