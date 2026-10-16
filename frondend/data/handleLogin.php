<?php
require_once __DIR__ . '/security.php';
// yhteyden tietokantaan
require_once __DIR__ . '/db_connection.php';
$name = $email = $db_password = "";
$id = 0;

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    verify_csrf('csrf_token_l');

    // ei aseta muuttujaa vasta kun jos tulee vastaan if lauseessa
    unset( $_SESSION['errorMessageLogin'] );
    unset( $_SESSION['errorTextLogin'] );
    
    // saa arvot
    $email = post_string("email");
    $password = post_string("password");

    // tarkistaa että email on valid
    if (strlen($email) > 45 || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $_SESSION['errorMessageLogin'] = true;
        $_SESSION['errorTextLogin'] = "Sähköposti ei ole kelvollinen";
        header("Location: ../login/index.php"); 
        exit;
    }

    // tarkistaa ettei arvot oo tyhjiä
    if (empty($email) || empty($password) || strlen($password) > 72) {
        header("Location: ../login/index.php"); 
        exit;
    } 

    // hakee sähköpostilla salasanan, id ja nimen tietokannasta
    $stmt = $conn->prepare("SELECT id, nimi, pword FROM kalastaja WHERE email=?");
    $stmt->bind_param("s", $email);
    $stmt->execute();
    $stmt->store_result();

    // tarkistaa onko sähköposti tietokannssa 
    if ($stmt->num_rows > 0) {
        // saa nimen ja salasanan tietokannsata
        $stmt->bind_result($id, $name, $db_password);
        $stmt->fetch();
        // tarkistaa onko salasana joka on tietokannassa ja jonka saa sama
        if(password_verify($password, $db_password)) {
            // luodaan uusi session id käyttäjälle
            session_regenerate_id(true);
            // asettaa session muuttujat
            $_SESSION["email"] = "$email";
            $_SESSION["nimi"] = $name;
            $_SESSION["kalastaja_id"] = $id;
            $_SESSION['authenticated_at'] = time();
            $_SESSION['last_activity'] = time();
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
            $_SESSION['errorTextLogin'] = "Sähköposti tai salasanasi on väärin";
            header("Location: ../login/index.php"); 
            exit;
        }
    } 
    header("Location: ../login/index.php"); 
    exit;
