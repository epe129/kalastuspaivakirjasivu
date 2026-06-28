<?php
session_start();
unset($_SESSION['MessageAdd']);
// Saadaan yhteys tietokantaan 
include_once('../data/db_connection.php');
// tarkistetaan että käyttäjä on kirjautunut
if (!isset($_SESSION['email']) and !isset($_SESSION["kalastaja_id"])) {
    header("Location: ../login/index.php");
    exit();
}
// kun cookie häviää kirjaa käyttäjän ulos
if(!isset($_COOKIE["login_token"])) {
    // Poista kaikki istunnon muuttujat.
    $_SESSION = array();
    session_unset();
    // tuhoaa istunnon.
    session_destroy();
    // Ohjaa käyttäjän takaisin kirjautumissivulle.
    header("Location: ../login/index.php");
    exit;
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>kaikki data</title>
    <style>
        html {
            background-image: url('../kuvat/tausta.jpg'); 
            background-repeat: no-repeat;
            background-attachment: fixed;  
            background-size: cover;
        }
            
        /* navbar css */
        ul {
            list-style-type: none;
            margin: 0;
            padding: 0;
            background-color: #333333;
            overflow: hidden;
        }
                       
        ul li {
            float: left;
        }

        ul li a {
            display: block;
            color: white;
            text-align: center;
            padding: 14px 16px;
            text-decoration: none;
        }
            
        .a:hover {
            background-color: #232323;
        }

        .logout {
            padding: 14px 16px; 
            background-color: white;
            color: black;
            text-decoration: none;
        }

        .logout:hover {
            background-color: #dbdbdb;
        }

        h1 {
            text-align: center;
            margin: auto;
            font-size: clamp(2rem, 2.5vw, 3rem);
            color: black;
            background-color: white;
            border-radius: 5px;
            width: fit-content;
            padding: 5px;
            margin-top: 50px;
            margin-bottom: 55px;
        }
    </style>
</head>
<body>
    <!-- navbar -->
    <ul>
        <li class="li"><a class="a" href="index.php">Kalastustiedot järjestyksessä</a></li>
        <li class="li"><a class="a" href="kaikkiData.php">kaikki kalastustiedot</a></li>
        <li class="li"><a class="a" href="lisaa.php">Lisää kalastustietoja</a></li>
        <li class="li" style="float: right;">
            <div style="display: flex; flex-direction:row;">
                <?php
                echo "<a class='a'>Terve, " . $_SESSION["nimi"]."</a>";
                ?>
                <a class="logout" href="../data/handleLogout.php">Kirjaudu ulos</a>
            </div>
        </li>
    </ul>
    <h1>Kaikki sinun kalastus tiedot</h1>
    <?php 

    ?> 
</body>
</html>