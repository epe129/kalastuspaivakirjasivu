<?php
session_start();
// yhteyden tietokantaan
include_once('db_connection.php');
$name = $email = "";

if ($_SERVER["REQUEST_METHOD"] == "POST") {

    // tarkistaa onko tokeni asetettu ja onko tokenit samatat session ja input saanissa
    if (!isset($_POST['csrf_token_r']) || !isset($_SESSION['csrf_token_r']) || !hash_equals($_SESSION['csrf_token_r'], $_POST['csrf_token_r'])) {
        die('CSRF token validation failed');
    }
  
    // poistetaan tokeni
    unset($_SESSION['csrf_token_r']);

    // ei aseta muuttujaa vasta kun jos tulee vastaan if lauseessa
    unset($_SESSION['errorMessageRegister']);
    unset($_SESSION['errorTextRegister']);

    // saa arvot
    $name = stripslashes(trim(htmlspecialchars($_POST["name"])));
    $email = trim($_POST["email"]);
    $password = $_POST["password"];
    
    // hashaa salasanan
    $hash_password = password_hash($password, PASSWORD_DEFAULT);

    // tarkistaa että email on valid
    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $_SESSION["errorMessageRegister"] = true;
        $_SESSION['errorTextRegister'] = "Sähköposti ei ole kelvollinen";
        header("Location: ../rekisteroidy/index.php"); 
        exit;
    }

    // tarkistaa että nimi sisältää vaan kirjaimia ja numeroita
    if (!preg_match("/^[a-zA-Z0-9äöåÄÖÅ]+$/u",$name)) {
        $_SESSION["errorMessageRegister"] = true;
        $_SESSION['errorTextRegister'] = "Nimi ei ole kelvollinen, vain numerot ja kirjaimet ovat salittuja";
        header("Location: ../rekisteroidy/index.php"); 
        exit;
    }
    
    // tarkistaa ettei salasana ole liian lyhyt
    if (strlen($password) <=  7) {
        $_SESSION["errorMessageRegister"] = true;
        $_SESSION['errorTextRegister'] = "Salasanassa pitää olla vähintää 8 merkkiä";
        header("Location: ../rekisteroidy/index.php"); 
        exit;
    }
    
    // jos jokin arvo on tyhjä
    if (empty($name) or empty($email) or empty($password)) {
        header("Location: ../rekisteroidy/index.php"); 
        exit;
    } 

    // tarkistetaan onko sähköposti tietokannassa   
    $kysely_email = $conn->prepare("SELECT email FROM kalastaja WHERE email = ?");
    $kysely_email->bind_param("s", $email);
    $kysely_email->execute();
    $kysely_email->store_result();

    // jos sähköposti on jo olemassa
    if($kysely_email->num_rows > 0) {
        $_SESSION['errorMessageRegister'] = true;
        $_SESSION['errorTextRegister'] = "Sähköposti on jo käytössä";
        header("Location: ../rekisteroidy/index.php"); 
        exit;
    }

    // lisää arvot tietokantaan ja tarkistaa että se onnistuu
    $stmt = $conn->prepare("INSERT INTO kalastaja (nimi, email, pword) VALUES (?, ?, ?)");
    $stmt->bind_param("sss", $name, $email, $hash_password);

    if ($stmt->execute() === TRUE) {
        // jos rekisteröinti onnistuu.
        // luodaan uusi session id käyttäjälle
        session_regenerate_id();
        header("Location: ../login/index.php"); 
        exit;
        } else {
            // jos epäonnistuu saa viestin
            $_SESSION['errorMessageRegister'] = true;
            $_SESSION['errorTextRegister'] = "Jokin meni pieleen";
            header("Location: ../rekisteroidy/index.php"); 
            exit;
        }
    } 
    header("Location: ../rekisteroidy/index.php"); 
    exit;
