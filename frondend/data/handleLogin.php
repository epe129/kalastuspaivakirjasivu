<?php
session_start();
// yhteyden tietokantaan
$db = include('db_connection.php');
$name = $email = "";
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // ei aseta muuttujaa vasta kun jos tulee vastaan if lauseessa
    unset( $_SESSION['errorMessageUser'] );
    // saa arvot
    $email = htmlspecialchars($_POST["email"]);
    $password = htmlspecialchars($_POST["password"]);
    // tarkistaa ettei arvot oo tyhjiä
    if (empty($email) or empty($password)) {
        header("Location: ../login/index.php"); 
        exit;
        } else {
            // hakee sähköpostilla salasanan tietokannasta
            $stmt = $conn->prepare("SELECT pword FROM kalastaja WHERE email=?");
            $stmt->bind_param("s", $email);
            $stmt->execute();
            $stmt->store_result();
            if ($stmt->num_rows > 0) {
                $stmt->bind_result($db_password);
                $stmt->fetch();
                // tarkistaa onko salasana joka on tietokannassa ja jonka saa onko sama
                if(password_verify($password, $db_password)) {
                    // saadaan käyttäjän nimi
                    $kysely_nimi = $conn->prepare("SELECT nimi FROM kalastaja WHERE email = ?");
                    $kysely_nimi->bind_param("s", $email);
                    $kysely_nimi->execute();
                    $kysely_nimi->bind_result($_SESSION["nimi"]);
                    $kysely_nimi->fetch();
                    $kysely_nimi->close(); 
                    $_SESSION["email"] = "$email";
                    header("Location: ../main/index.php"); 
                    exit;
                }
                else {
                    // jos salasana on väärin
                    $_SESSION['errorMessageUser'] = true;
                    header("Location: ../login/index.php"); 
                    exit;
                }
            }
            else {
                // jos sähköpostia ei ole tietokannassa
                $_SESSION['errorMessageUser'] = true;
                header("Location: ../login/index.php"); 
                exit;
            }
        }
    } else {
        header("Location: ../login/index.php"); 
        exit;
    }
?>