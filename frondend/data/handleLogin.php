<?php
session_start();
// yhteyden tietokantaan
include('db_connection.php');

$name = $email = $db_password = "";

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    
    // tarkistaa onko tokeni asetettu ja onko tokenit samatat session ja input saanissa
    if (!isset($_POST['csrf_token_l']) || !isset($_SESSION['csrf_token_l']) || !hash_equals($_SESSION['csrf_token_l'], $_POST['csrf_token_l'])) {
        die('CSRF token validation failed');
    }
    
    // ei aseta muuttujaa vasta kun jos tulee vastaan if lauseessa
    unset( $_SESSION['errorMessageLogin'] );
    unset( $_SESSION['errorTextLogin'] );
    
    // saa arvot
    $email = stripslashes(trim(htmlspecialchars($_POST["email"])));
    $password = stripslashes(trim(htmlspecialchars($_POST["password"])));

    // tarkistaa että email on valid
    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $_SESSION['errorMessageLogin'] = true;
        $_SESSION['errorTextLogin'] = "Sähköposti ei ole kelvollinen";
        header("Location: ../login/index.php"); 
        exit;
    }

    // tarkistaa ettei arvot oo tyhjiä
    if (empty($email) or empty($password)) {
        header("Location: ../login/index.php"); 
        exit;
    } 

    // hakee sähköpostilla salasanan ja nimen tietokannasta
    $stmt = $conn->prepare("SELECT nimi, pword FROM kalastaja WHERE email=?");
    $stmt->bind_param("s", $email);
    $stmt->execute();
    $stmt->store_result();

    // tarkistaa onko sähköposti tietokannssa 
    if ($stmt->num_rows > 0) {
        // saa nimen ja salasanan tietokannsata
        $stmt->bind_result($_SESSION["nimi"], $db_password);
        $stmt->fetch();
        // tarkistaa onko salasana joka on tietokannassa ja jonka saa sama
        if(password_verify($password, $db_password)) {
            // luodaan uusi session id käyttäjälle
            session_regenerate_id();
            $_SESSION["email"] = "$email";
            header("Location: ../main/index.php"); 
            exit;
            }
            else {
                // jos salasana on väärin
                $_SESSION['errorMessageLogin'] = true;
                $_SESSION['errorTextLogin'] = "Sähköposti tai salasanasi on väärin";
                header("Location: ../login/index.php"); 
                exit;
                }
        }
        else {
            // jos sähköpostia ei ole tietokannassa
            $_SESSION['errorMessageLogin'] = true;
            $_SESSION['errorTextLogin'] = "Sähköposti ei ole kelvollinen";
            header("Location: ../login/index.php"); 
            exit;
        }
    } 
    header("Location: ../login/index.php"); 
    exit;
?>