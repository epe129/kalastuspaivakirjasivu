<?php
session_start();
// yhteyden tietokantaan
$db= include('db_connection.php');
$laji = $viehe = $vapa = "";
if ($_SERVER["REQUEST_METHOD"] == "POST") {
  // ei aseta muuttujaa vasta kun jos tulee vastaan if lauseessa
  unset( $_SESSION['SuccesfullAddMuu'] );
  unset( $_SESSION['ErrorAddMuu'] );
  unset( $_SESSION['TextMuu'] );
  unset( $_SESSION['AlreadyExistMuu'] );
  $array_arvot = array("laji", "viehe", "vapa");
  foreach ($array_arvot as $x) {
    // hakee aina name inputin avulla ja kattoo onko tyhjä name on aina esim name="laji"
    $get_arvo = htmlspecialchars($_POST["$x"]);  
    // tarkistaa onko input tyhjä
    if (strlen($get_arvo) != 0) {
      $_SESSION["TextMuu"] = "$x";
      // tarkistaa onko arvo jo tietokannassa
      $onko_result = $conn->prepare("SELECT * FROM $x WHERE $x = ?");
      $onko_result->bind_param("s", $get_arvo);
      $onko_result->execute();
      $onko_result->store_result();
      if ($onko_result->num_rows > 0) {
        // jos arvo on jo
        $_SESSION['AlreadyExistMuu'] = true;
        header("Location: ../main/lisaa.php");
        exit; 
        } else {
          // lisää arvon jos ei oo tietokannassa
          $stmt_lisaa = $conn->prepare("INSERT INTO $x ($x) VALUES (?)");
          $stmt_lisaa->bind_param("s", $get_arvo);
          if ($stmt_lisaa->execute() === TRUE) {
            // jos lisääminen onnistui saa viestin ja menee takaisin samalle sivulle
            $_SESSION["SuccesfullAddMuu"] = true;
            header("Location: ../main/lisaa.php"); 
            exit;
    
            } else {
              // jos lisääminen ei onnistunut saa viestin ja menee takaisin samalle sivulle
              $_SESSION["ErrorAddMuu"] = true;
              header("Location: ../main/lisaa.php"); 
              exit;
              }
    
          }
        } else {
        continue;
      }
    }
  } else {
    header("Location: ../main/lisaa.php"); 
    exit;
  }
?>