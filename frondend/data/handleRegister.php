<!-- tee että tarkistaa onko sähköposti tietokannassa -->
<?php
session_start();
// yhteyden tietokantaan
$db = include('db_connection.php');
$name = $email = "";
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // ei aseta muuttujaa vasta kun jos tulee vastaan if lauseessa
    unset( $_SESSION['errorMessage'] );
    unset( $_SESSION['AlreadyExist'] );
    // saa arvot
    $name = htmlspecialchars($_POST["name"]);
    $email = htmlspecialchars($_POST["email"]);
    // hashaa salasanan
    $hash_password = password_hash(htmlspecialchars($_POST["password"]), PASSWORD_DEFAULT);
    // tarkistetaan onko sähköposti tietokannassa   
    $kysely_email = $conn->prepare("SELECT email FROM kalastaja WHERE email = ?");
    $kysely_email->bind_param("s", $email);
    $kysely_email->execute();
    $kysely_email->store_result();

    if($kysely_email->num_rows > 0) {
        // jos sähköposti on jo olemassa
        $_SESSION['AlreadyExist'] = true;
        header("Location: ../index.php"); 
        exit;
    }
    
    if (empty($name) or empty($email) or empty(htmlspecialchars($_POST["password"]))) {
        // jos jokin arvo on tyhjä
        header("Location: ../index.php"); 
        exit;
        } else {
            // lisää arvot tietokantaan ja tarkistaa että se onnistuu
            $stmt = $conn->prepare("INSERT INTO kalastaja (nimi, email, pword) VALUES (?, ?, ?)");
            $stmt->bind_param("sss", $name, $email, $hash_password);

            if ($stmt->execute() === TRUE) {
                $_SESSION["email"] = "$email";
                $_SESSION["nimi"] = "$name";
                header("Location: ../main/index.php"); 
                exit;
            } else {
                // jos epäonnistuu saa viestin
                $_SESSION['errorMessage'] = true;
                header("Location: ../index.php"); 
                exit;
            }
        }
    } else {
        header("Location: ../index.php"); 
        exit;
    }
?>