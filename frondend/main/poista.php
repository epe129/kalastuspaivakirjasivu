<?php
session_start();
unset($_SESSION['MessageAdd']);
if (empty($_SESSION['csrf_token_p'])) {
    $_SESSION['csrf_token_p'] = bin2hex(random_bytes(32));
}
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
$lajit = array("ahven", "harjus", "hauki", "jokirapu", "kiiski", "kirjolohi", "kolmipiikki", "kuha", "kuore", "lahna", "lohi", "made", "muikku", "pasuri", "rautu", "ruutana", "salakka", "särki", "säyne", "siika", "silakka", "sorva", "suutari", "taimen", "täplärapu");
$kysely_lajit = $conn->prepare("SELECT laji FROM laji");
$kysely_lajit->execute();
$data_lajit = $kysely_lajit->get_result();
if ($data_lajit) {
    // lisää lajit arrayhyn
    while($rivi = $data_lajit->fetch_assoc()) {
        if (in_array($rivi["laji"], $lajit))
            {
                continue;
            } else {
                array_push($lajit, $rivi["laji"]);
            }
    }
}
$kalastaja_id = $_SESSION["kalastaja_id"]; 
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Poista kalasaaliita</title>
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
        /* nayttaa css */
        .nayttaa {
            margin: 0 auto;
            position: relative;
            padding: 10px;
            font-size: 1.5rem;
            height: auto;
            min-width: fit-content;
            max-width: 600px;
            border: 1px solid gray;
            border-radius: 5px;
            box-shadow: 2px 2px 5px black;
            background-color: white;
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
    </style>
</head>
<body>
    <!-- navbar -->
    <ul>
        <li class="li"><a class="a" href="index.php">Kalastustiedot järjestyksessä</a></li>
        <li class="li"><a class="a" href="kaikkiData.php">kaikki kalastustiedot</a></li>
        <li class="li"><a class="a" href="lisaa.php">Lisää kalastustietoja</a></li>
        <li class="li"><a class="a" href="poista.php">Poista kalastustietoja</a></li>
        <li class="li" style="float: right;">
            <div style="display: flex; flex-direction:row;">
                <?php
                echo "<a class='a'>Terve, " . $_SESSION["nimi"]."</a>";
                ?>
                <a class="logout" href="../data/handleLogout.php">Kirjaudu ulos</a>
            </div>
        </li>
    </ul>
    <h1>Poista kalastustietojasi</h1>
    <?php
        //  teksti onnistuko syöttö vai ei 
        if (isset($_SESSION['MessagePoista'])) {
            $text = ucfirst($_SESSION['TextPoista']);
            echo "
            <br/>
            <span style='font-size: 1.5rem;'>$text</span>
            <br/>
            ";
        }
        ?>
    <?php
        echo "<div class='nayttaa'>";
        // haetaan dataa tietokannasta
        $rivien_maarat = 0;
        $kysely_paino = $conn->prepare("SELECT aika, laji, kuva, paino, kala.id as kala_id, tarppi.id as tarppi_id, kala.laji_id as laji_id FROM kala, laji, tarppi WHERE kala.laji_id=laji.id AND tarppi.kalastaja_id= ? AND tarppi.id=kala.tarppi_id");
        $kysely_paino->bind_param("i", $kalastaja_id);
        $kysely_paino->execute();
        $data_paino = $kysely_paino->get_result();
        // tarkistaa että dataa on
        if ($data_paino) {
            while ($rivi = $data_paino->fetch_assoc()) {
                $rivien_maarat += 1;
                $lajiKuvaHaku = $rivi["laji"];
                if (in_array($rivi["laji"], array_slice($lajit, 0,25)))
                {
                    // check if user has uplouded picture if has shows that picture
                    if ($rivi['kuva'] == null) {
                        echo "<img src='../kuvat/$lajiKuvaHaku.jpg' width='50' height='25'> ";   
                    } else {
                        echo "<img src='../data/uploads/$rivi[kuva]' width='50' height='25'> ";   
                    }
                } else {
                    echo "🐟";
                }
                $r = implode(" ",$rivi);
                $kala_id = $rivi["kala_id"];
                $tarppi_id = $rivi["tarppi_id"];
                $laji_id = $rivi["laji_id"];
                $aika = $rivi["aika"];
                
                echo "<form class='form' action='../data/handlePoista.php' method='post' enctype='multipart/form-data'>";
                echo date_format(date_create(explode(" ", $rivi["aika"])[0]), "d.m.Y")." ".$rivi["laji"]. " ".$rivi["paino"]." kg"." <button>Poista</button> <input type='hidden' name='poista' value='$kalastaja_id $kala_id $tarppi_id $laji_id $aika'/>"."<br/>";    
                echo '<input type="hidden" name="csrf_token_p" value="' . $_SESSION['csrf_token_p'] . '">';
                echo "</form>";
            }
        } 
        if ($rivien_maarat == 0) {
            echo "Mitään ei löytynyt";
        }  
        // jos tulos on nolla
        echo "</div>"
    ?>
</body>
</html>