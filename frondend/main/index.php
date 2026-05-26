<?php
session_start();
unset($_SESSION['MessageAdd']);
// Saadaan yhteys tietokantaan 
include_once('../data/db_connection.php');
// tarkistetaan että käyttäjä on kirjautunut
if (!isset($_SESSION['email']) and !isset($_SESSION["kalastaja_id"])) {
    header("Location: ../index.php");
    exit();
}
$lajit = array("ahven", "harjus", "hauki", "jokirapu", "kiiski", "kirjolohi", "kolmipiikki", "kuha", "kuore", "lahna", "lohi", "made", "muikku", "pasuri", "rautu", "ruutana", "salakka", "särki", "säyne", "siika", "silakka", "sorva", "suutari", "taimen", "täplärapu");
$tulos = $conn->query("SELECT laji FROM laji");
if ($tulos->num_rows > 0) {
    // lisää lajit arrayhyn
    while($rivi = $tulos->fetch_assoc()) {
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
<html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Kalastustiedot</title>
        <style>
            html {
                background-image: url('../kuvat/tausta.jpg'); 
                background-repeat: no-repeat;
                background-attachment: fixed;  
                background-size: cover;
            }
            /* otsikon css */
            .title {
                text-align: center;
                margin: auto;
                font-size: 3rem;
                color: black;
                background-color: white;
                border-radius: 5px;
                width: 350px;
                margin-top: 50px;
                margin-bottom: 55px;
            }
            .main {
                margin: 0 auto;
                position: relative;
                height: 100%;
                width: 100%;
            }
            /* nayttaa css */
            .nayttaa {
                margin: 0 auto;
                position: relative;
                padding: 20px;
                font-size: 1.5rem;
                height: 100%;
                width: 450px;
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
                display: flex;
                border-radius: 5px;
                width: 100%;
            }

            .a {
                display: block;
                color: white;
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
        <li class="li"><a class="a" href="index.php">Kalastustiedot</a></li>
        <li class="li"><a class="a" href="lisaa.php">Lisää kalastustietoja</a></li>
        <li class="li" style="margin-left: auto;">
            <div style="display: flex; flex-direction:row;">
                <?php
                echo "<a class='a'>Terve, " . $_SESSION["nimi"]."</a>";
                ?>
                <a class="logout" href="../data/handleLogout.php">Kirjaudu ulos</a>
            </div>
        </li>
    </ul>
    <!-- datan näyttö -->
    <?php
    echo "<h1 class='title'>Kalastustiedot</h1>";
    echo "<div class='main'>";
        echo "<div class='nayttaa'>";
            echo "<h2>Kalat painon mukaan</h2>";
            // haetaan dataa tietokannasta
            $rivien_maarat = 0;
            $tulos = $conn->query("SELECT laji, paino FROM kala, laji, tarppi WHERE kala.laji_id=laji.id AND tarppi.kalastaja_id='$kalastaja_id' AND tarppi.id=kala.tarppi_id ORDER BY paino DESC");
            // tarkistaa että tivejä on enemmän kuin nolla
            if ($tulos->num_rows > 0) {
                while($rivi = $tulos->fetch_assoc()) {
                    $rivien_maarat += 1;
                    $lajiKuvaHaku = $rivi["laji"];
                    if (in_array($rivi["laji"], array_slice($lajit, 0,25)))
                    {
                        echo "<img src='../kuvat/$lajiKuvaHaku.jpg' width='50' height='25'> ";   
                    } else {
                        echo "🐟";
                    }
                    if ($rivien_maarat == 1) {
                        echo "🥇".$rivi["laji"]. " ".$rivi["paino"]." kg"."<br/>";
                    } else if ($rivien_maarat == 2) {
                        echo "🥈".$rivi["laji"]. " ".$rivi["paino"]." kg"."<br/>";
                    } else if ($rivien_maarat == 3) {
                        echo"🥉".$rivi["laji"]. " ".$rivi["paino"]." kg"."<br/>";
                    } else {
                        echo $rivi["laji"]. " ".$rivi["paino"]." kg"."<br/>";
                    }
                }
            } else {
                echo "Mitään ei löytynyt";
            }            
        echo "</div>
        <br/>";
        echo "<div class='nayttaa'>";
            echo "<h2>Kalat pituuden mukaan</h2>";
            $rivien_maarat = 0;
            $tulos = $conn->query("SELECT laji, pituus FROM kala, laji, tarppi WHERE kala.laji_id=laji.id AND tarppi.kalastaja_id='$kalastaja_id' AND tarppi.id=kala.tarppi_id ORDER BY pituus DESC");
            if ($tulos->num_rows > 0) {
                while($rivi = $tulos->fetch_assoc()) {
                    $rivien_maarat += 1;
                    $lajiKuvaHaku = $rivi["laji"];
                    if (in_array($rivi["laji"], array_slice($lajit, 0,25)))
                    {
                        echo "<img src='../kuvat/$lajiKuvaHaku.jpg' width='50' height='25'> ";   
                    } else {
                        echo "🐟";
                    }
                    if ($rivien_maarat == 1) {
                        echo "🥇".$rivi["laji"]. " ".$rivi["pituus"]." cm"."<br/>";
                    } else if ($rivien_maarat == 2) {
                        echo "🥈".$rivi["laji"]. " ".$rivi["pituus"]." cm"."<br/>";
                    } else if ($rivien_maarat == 3) {
                        echo "🥉".$rivi["laji"]. " ".$rivi["pituus"]." cm"."<br/>";
                    } else {
                        echo $rivi["laji"]. " ".$rivi["pituus"]." cm"."<br/>";
                    }
                } 
            } else {
                echo "Mitään ei löytynyt";
            }
        echo "</div>
        <br/>";
        echo "<div class='nayttaa'>";
            echo "<h2>Kalalajien saanti määrät</h2>";
            $tulos = $conn->query("SELECT laji, laji_id, COUNT(laji_id) as maara FROM kala, laji, tarppi WHERE kala.laji_id=laji.id AND tarppi.kalastaja_id='$kalastaja_id' AND tarppi.id=kala.tarppi_id GROUP BY laji_id ORDER BY maara DESC");
            if ($tulos->num_rows > 0) {
                while($rivi = $tulos->fetch_assoc()) {
                    $lajiKuvaHaku = $rivi["laji"];
                    if (in_array($rivi["laji"], array_slice($lajit, 0,25)))
                    {
                        echo "<img src='../kuvat/$lajiKuvaHaku.jpg' width='50' height='25'> ";   
                    } else {
                        echo "🐟";
                    }
                    echo $rivi["laji"]. " ".$rivi["maara"]." kpl"."<br/>";
                }
            } else {
                echo "Mitään ei löytynyt";
            }
        echo "</div>
        <br/>";
        echo "<div class='nayttaa'>";
            echo "<h2>Kalalajien saanti määrät eri vieheillä</h2>";
            $rivien_maarat = 0;
            // käy lajit arraysta
            foreach ($lajit as $x) {
                $tulos = $conn->query("SELECT COUNT(laji) AS maara, laji, viehe FROM viehe, tarppi, kala, laji WHERE viehe.id=tarppi.viehe_id AND kala.laji_id=laji.id AND tarppi.kalastaja_id='$kalastaja_id' AND tarppi.id=kala.tarppi_id AND laji='$x' GROUP BY viehe ORDER BY maara DESC;");
                // tarkistaa että tivejä on enemmän kuin nolla
                if ($tulos->num_rows > 0) {
                    while($rivi = $tulos->fetch_assoc()) {
                        $lajiKuvaHaku = $rivi["laji"];
                        if (in_array($rivi["laji"], array_slice($lajit, 0,25)))
                        {
                            echo "<img src='../kuvat/$lajiKuvaHaku.jpg' width='50' height='25'> ";   
                        } else {
                            echo "🐟";
                        }
                        echo $rivi["laji"]. " ".$rivi["viehe"]. " ".$rivi["maara"]." kpl"."<br/>";
                        $rivien_maarat += 1;
                    }
                } 
            }
            // jos tulos on nolla
            if ($rivien_maarat == 0) {
                echo "Mitään ei löytynyt";
            }
        echo "</div>
        <br/>";
        echo "<div class='nayttaa'>";
            echo "<h2>Kalalajien saanti määrät eri vavoilla</h2>";
            foreach ($lajit as $x) {
                $tulos = $conn->query("SELECT COUNT(laji) AS maara, laji, vapa FROM vapa, tarppi, kala, laji WHERE vapa.id=tarppi.vapa_id AND kala.laji_id=laji.id AND tarppi.kalastaja_id='$kalastaja_id' AND tarppi.id=kala.tarppi_id AND laji='$x' GROUP BY vapa ORDER BY maara DESC;");
                if ($tulos->num_rows > 0) {
                    while($rivi = $tulos->fetch_assoc()) {
                        $lajiKuvaHaku = $rivi["laji"];
                        if (in_array($rivi["laji"], array_slice($lajit, 0,25)))
                        {
                            echo "<img src='../kuvat/$lajiKuvaHaku.jpg' width='50' height='25'> ";   
                        } else {
                            echo "🐟";
                        }
                        echo $rivi["laji"]. " ".$rivi["vapa"]. " ".$rivi["maara"]." kpl"."<br/>";
                        $rivien_maarat += 1;
                    }
                } 
            }
            // jos tulos on nolla
            if ($rivien_maarat == 0) {
                echo "Mitään ei löytynyt";
            }
        echo "</div>";
    echo "</div>";
    ?>
</body>
</html>