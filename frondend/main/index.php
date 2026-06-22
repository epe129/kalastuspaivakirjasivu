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
            
            /* navbar css */
            ul {
                list-style-type: none;
                margin: 0;
                padding: 0;
                background-color: #333333;
                /* display: flex; */
                /* border-radius: 5px; */
                /* width: 100%; */
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

            /* otsikon css */
            .title {
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

            .main {
                margin: 0 auto;
                position: relative;
                height: auto;
                width: 100%;
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

        </style>       
    </head>
<body>
    <!-- navbar -->
    <ul>
        <li class="li"><a class="a" href="index.php">Kalastustiedot</a></li>
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
    <!-- datan näyttö -->
    <?php
    echo "<h1 class='title'>Kalastustiedot</h1>";
    echo "<div class='main'>";
        echo "<div class='nayttaa'>";
            echo "<h2>Kalat painon mukaan</h2>";
            // haetaan dataa tietokannasta
            $rivien_maarat = 0;
            $kysely_paino = $conn->prepare("SELECT aika, laji, paino, kuva FROM kala, laji, tarppi WHERE kala.laji_id=laji.id AND tarppi.kalastaja_id= ? AND tarppi.id=kala.tarppi_id ORDER BY paino DESC;");
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
                        echo "<img src='../data/uploads/$rivi[kuva]' width='50' height='25'> ";   
                    } else {
                        echo "🐟";
                    }
                    if ($rivien_maarat == 1) {
                        // date_format(date_create(explode(" ", $rivi["aika"])[0]), "d.m.Y") luodaan datetime ottamalla aika ja siitä luodaan datitime joka formatoidaan suomi muotoon
                        echo " ".date_format(date_create(explode(" ", $rivi["aika"])[0]), "d.m.Y")."🥇".$rivi["laji"]. " ".$rivi["paino"]." kg"."<br/>";
                    } else if ($rivien_maarat == 2) {
                        echo " ".date_format(date_create(explode(" ", $rivi["aika"])[0]), "d.m.Y")."🥈".$rivi["laji"]. " ".$rivi["paino"]." kg"."<br/>";
                    } else if ($rivien_maarat == 3) {
                        echo " ".date_format(date_create(explode(" ", $rivi["aika"])[0]), "d.m.Y")."🥉".$rivi["laji"]. " ".$rivi["paino"]." kg"."<br/>";
                    } else {
                        echo $rivi["laji"]. " ".$rivi["paino"]." kg"."<br/>";
                    }
                }
            }    
            // jos tulos on nolla
            if ($rivien_maarat == 0) {
                echo "Mitään ei löytynyt";
            }    
            $kysely_paino->close();
        echo "</div>
        <br/>";
        echo "<div class='nayttaa'>";
            echo "<h2>Kalat pituuden mukaan</h2>";
            $rivien_maarat = 0;
            $kysely_pituus = $conn->prepare("SELECT aika, laji, pituus FROM kala, laji, tarppi WHERE kala.laji_id=laji.id AND tarppi.kalastaja_id= ? AND tarppi.id=kala.tarppi_id ORDER BY pituus DESC;");
            $kysely_pituus->bind_param("i", $kalastaja_id);
            $kysely_pituus->execute();
            $data_pituus = $kysely_pituus->get_result();
            // tarkistaa että dataa on
            if ($data_pituus) {
                while($rivi = $data_pituus->fetch_assoc()) {
                    $rivien_maarat += 1;
                    $lajiKuvaHaku = $rivi["laji"];
                    if (in_array($rivi["laji"], array_slice($lajit, 0,25)))
                    {
                        echo "<img src='../kuvat/$lajiKuvaHaku.jpg' width='50' height='25'> ";   
                    } else {
                        echo "🐟";
                    }
                    if ($rivien_maarat == 1) {
                        echo " ".date_format(date_create(explode(" ", $rivi["aika"])[0]), "d.m.Y")."🥇".$rivi["laji"]. " ".$rivi["pituus"]." cm"."<br/>";
                    } else if ($rivien_maarat == 2) {
                        echo " ".date_format(date_create(explode(" ", $rivi["aika"])[0]), "d.m.Y")."🥈".$rivi["laji"]. " ".$rivi["pituus"]." cm"."<br/>";
                    } else if ($rivien_maarat == 3) {
                        echo " ".date_format(date_create(explode(" ", $rivi["aika"])[0]), "d.m.Y")."🥉".$rivi["laji"]. " ".$rivi["pituus"]." cm"."<br/>";
                    } else {
                        echo $rivi["laji"]. " ".$rivi["pituus"]." cm"."<br/>";
                    }
                } 
            } 
            // jos tulos on nolla
            if ($rivien_maarat == 0) {
                echo "Mitään ei löytynyt";
            }           
            $kysely_pituus->close();            
        echo "</div>
        <br/>";
        echo "<div class='nayttaa'>";
            echo "<h2>Kalalajien saanti määrät</h2>";
            $kysely_saanti = $conn->prepare("SELECT laji, laji_id, COUNT(laji_id) as maara FROM kala, laji, tarppi WHERE kala.laji_id=laji.id AND tarppi.kalastaja_id=? AND tarppi.id=kala.tarppi_id GROUP BY laji_id ORDER BY maara DESC;");
            $kysely_saanti->bind_param("i", $kalastaja_id);
            $kysely_saanti->execute();
            $data_saanti = $kysely_saanti->get_result();
            // tarkistaa että dataa on
            if ($data_saanti) {
                while($rivi = $data_saanti->fetch_assoc()) {
                    $lajiKuvaHaku = $rivi["laji"];
                    if (in_array($rivi["laji"], array_slice($lajit, 0,25)))
                    {
                        echo "<img src='../kuvat/$lajiKuvaHaku.jpg' width='50' height='25'> ";   
                    } else {
                        echo "🐟";
                    }
                    echo $rivi["laji"]. " ".$rivi["maara"]." kpl"."<br/>";
                }
            }
            // jos tulos on nolla
            if ($rivien_maarat == 0) {
                echo "Mitään ei löytynyt";
            }
            $kysely_saanti->close();
        echo "</div>
        <br/>";
        echo "<div class='nayttaa'>";
            echo "<h2>Kalalajien saanti määrät eri vieheillä</h2>";
            $rivien_maarat = 0;
            $viehe = array();
            // käy lajit arraysta
            foreach ($lajit as $x) {
                $kysely_viehe = $conn->prepare("SELECT laji, viehe, viehe_id, laji_id, COUNT(laji_id) as maara FROM viehe, tarppi, kala, laji WHERE viehe.id=tarppi.viehe_id AND kala.laji_id=laji.id AND tarppi.kalastaja_id=? AND tarppi.id=kala.tarppi_id AND laji=? GROUP BY viehe_id ORDER BY maara DESC;");
                $kysely_viehe->bind_param("is", $kalastaja_id, $x);
                $kysely_viehe->execute();
                $data_viehe = $kysely_viehe->get_result();
                // tarkistaa että dataa on
                if ($data_viehe) {
                    while($rivi = $data_viehe->fetch_assoc()) {
                        // lisää rivin arrayhyn
                        array_push($viehe, array("laji"=>$rivi["laji"], "viehe"=>$rivi["viehe"], "maara"=>$rivi["maara"]));
                        $rivien_maarat += 1;
                    }
                } 
                $kysely_viehe->close();
            }
            // sorttaa arrayn määrän järjestykseen
            $maara = array_column($viehe, 'maara');
            array_multisort($maara, SORT_DESC, $viehe);
            // tulostaa datan näytille arraysta
            foreach ($viehe as $rivi) {
                $lajiKuvaHaku = $rivi["laji"];
                if (in_array($rivi["laji"], array_slice($lajit, 0,25)))
                {
                    echo "<img src='../kuvat/$lajiKuvaHaku.jpg' width='50' height='25'> ";   
                } else {
                    echo "🐟";
                }
                echo $rivi["laji"]. " ".$rivi["viehe"]. " ".$rivi["maara"]." kpl"."<br/>";
            }
            // // jos tulos on nolla
            if ($rivien_maarat == 0) {
                echo "Mitään ei löytynyt";
            }
        echo "</div>
        <br/>";
        echo "<div class='nayttaa'>";
            echo "<h2>Kalalajien saanti määrät eri vavoilla</h2>";
            $rivien_maarat = 0;
            $vapa = array();
            // käy lajit arraysta
            foreach ($lajit as $x) {
                $kysely_vapa = $conn->prepare("SELECT laji, vapa, vapa_id, laji_id, COUNT(laji_id) as maara FROM vapa, tarppi, kala, laji WHERE vapa.id=tarppi.vapa_id AND kala.laji_id=laji.id AND tarppi.kalastaja_id=? AND tarppi.id=kala.tarppi_id AND laji=? GROUP BY vapa_id ORDER BY maara DESC;");
                $kysely_vapa->bind_param("is", $kalastaja_id, $x);
                $kysely_vapa->execute();
                $data_vapa = $kysely_vapa->get_result();
                // tarkistaa että dataa on
                if ($data_vapa) {
                    while($rivi = $data_vapa->fetch_assoc()) {
                        // lisää rivin arrayhyn
                        array_push($vapa, array("laji"=>$rivi["laji"], "vapa"=>$rivi["vapa"], "maara"=>$rivi["maara"]));
                        $rivien_maarat += 1;
                    }
                } 
                $kysely_vapa->close();
            }
            // sorttaa arrayn määrän järjestykseen
            $maara = array_column($vapa, 'maara');
            array_multisort($maara, SORT_DESC, $vapa);
            // tulostaa datan näytille arraysta
            foreach ($vapa as $rivi) {
                $lajiKuvaHaku = $rivi["laji"];
                if (in_array($rivi["laji"], array_slice($lajit, 0,25)))
                {
                    echo "<img src='../kuvat/$lajiKuvaHaku.jpg' width='50' height='25'> ";   
                } else {
                    echo "🐟";
                }
                echo $rivi["laji"]. " ".$rivi["vapa"]. " ".$rivi["maara"]." kpl"."<br/>";
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