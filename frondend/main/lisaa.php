<?php
require_once __DIR__ . '/../data/security.php';
require_fisherman();
unset($_SESSION['MessagePoista']);
// Saadaan yhteys tietokantaan 
require_once __DIR__ . '/../data/db_connection.php';
// tarkistetaan että käyttäjä on kirjautunut
// CSRF suojaus ettei voi kuka vaan tehdä pyyntojö 
if (empty($_SESSION['csrf_token_li'])) {
    $_SESSION['csrf_token_li'] = bin2hex(random_bytes(32));
}
if (empty($_SESSION['csrf_token_li_muu'])) {
    $_SESSION['csrf_token_li_muu'] = bin2hex(random_bytes(32));
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lisää kalastustietoja</title>
    <style>
        /* molemmilla sivuilla on samat html ja navbar css */
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
        
        /* div css */
        .main-div {
            margin: 0 auto;
            position: relative;
            padding: 10px;
            height: auto;
            min-width: fit-content;
            max-width: 500px;
        }

        h1 {
            width: fit-content;
            text-align: center;
            background-color: white;
            border-radius: 5px;
            padding: 5px;
            font-size: clamp(2rem, 2.5vw, 3rem);
            margin: auto;
            margin-top: 40px;
            margin-bottom: 45px;
        }

        /* form, input ja label css */
        .form {
            background-color: white;
            padding: 20px;
            border: 1px solid rgb(101, 100, 100);
            border-radius: 5px;
            box-shadow: 2px 2px 2px rgb(101, 100, 100);
            min-height: fit-content;
            height: 575px;
        }

        .label {
            font-size: 125%;
            display: block;
            text-transform: capitalize;
        }

        .input {
            width: 100%;
            padding: 2px;
        }

        /* laji muu form ja div css */
        .laji_muu_div {
            background-color: rgba(255, 255, 255, 0.4);
            -webkit-backdrop-filter: blur(5px);
            backdrop-filter: blur(5px);
            display: none;
            position: absolute;
            justify-content: center;
            align-items: center;
            text-align: center;
            padding: 0;
            width: 100%;
            height: 100%;
            color: black;
            font-size: 2rem;
            /* margin-top: -50vh; */
        }

        .laji_muu_form {
            margin-top: -400px;
            flex-direction: column;
        }

        .button_muu {
            margin-top: 5px;
            float: right;
            background-color: white;
            border: 1px solid black;
            border-radius: 5px;
            cursor: pointer;
            font-size: 1.2rem;
            padding: 5px;
        }

        /* form button css */
        .button {
            margin-top: 5px;
            margin-right: -10px;
            float: right;
            background-color: white;
            border: 1px solid black;
            border-radius: 5px;
            cursor: pointer;
            font-size: 1.2rem;
            padding: 5px;
        }

        #kuvaBt {
            margin-top: 5px;
            background-color: white;
            border: 1px solid black;
            border-radius: 5px;
            cursor: pointer;
            font-size: 1.2rem;
            padding: 5px;
        }

        /* select css eli valikon css */
            select {
            border: 1px solid #a9a9a9;
            background: #eeeeee;
            padding: 2px;
            transition: 0.4s;
            width: 100%;
            text-align: center;
        }

        select:hover, select:focus {
            background: #dddddd;
        }

        select, input {
            margin: 8px 0px;
            font-size: 1.1rem;
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
                echo "<a class='a'>Terve, " . html($_SESSION["nimi"])."</a>";
                ?>
                <form action="../data/handleLogout.php" method="post">
                    <input type="hidden" name="csrf_logout" value="<?php echo html($_SESSION['csrf_logout']) ?>">
                    <button class="logout" type="submit">Kirjaudu ulos</button>
                </form>
            </div>
        </li>
    </ul>
    
    <!-- jos käyttäjä valitsee muu voi lisätä uuden arvon -->
    <div class="laji_muu_div" id="laji_muu_div">
        <form class="laji_muu_form" id="laji_muu_form" action="../data/handleMuuAdd.php" method="post">
            <h2 style="margin-bottom: 10px;" id="h2_muu"></h2>
            <input type="text" id="muu" placeholder="Muu mikä" maxlength="24" style="font-size: 1.5rem;">
            <button type="submit" class="button_muu">Lähetä</button>
            <input type="hidden" name="csrf_token_li_muu" value="<?php echo htmlspecialchars($_SESSION['csrf_token_li_muu']) ?>">   
        </form>    
    </div>

    <h1>Lisää kalastustietoja</h1>
    <div class="main-div" id="main-div">
        <!-- form lomake -->
        <form class="form" action="../data/handleAdd.php" method="post" enctype="multipart/form-data">
            <label class="label" for="pituus">Kalalaji:</label>
            <select id="KalaLaji" name="laji" required>
                <option value="">Valitse kalalaji</option>
                <?php
                    $kysely_lajit_select = $conn->prepare("SELECT laji FROM laji");
                    $kysely_lajit_select->execute();
                    $data_lajit = $kysely_lajit_select->get_result();
                    if ($data_lajit) {
                        while($rivi = $data_lajit->fetch_assoc()) {
                            echo '<option value="' . html($rivi['laji']) . '">'
                                . html($rivi['laji']) . '</option>';
                        }
                    }
                ?>
                <option value="muu">
                    <span>muu</span>
                </option>
                <!-- jotta muu on viimeinen arvo -->
            </select>
            <br/>
            <label class="label" for="pituus">Pituus (cm):</label>
            <input type="number" oninput="if (this.value.length > this.maxLength) this.value = this.value.slice(0, 6);" maxlength="6" step="0.001" id="pituus" name="pituus" placeholder="Kalan pituus" class="input" required>
            <br/>        
            <label class="label" for="paino">Paino (kg):</label>
            <input type="number" oninput="if (this.value.length > this.maxLength) this.value = this.value.slice(0, 6);" maxlength="6" step="0.001" id="paino" name="paino" placeholder="Kalan paino" class="input" required>                 
            <br/>
            <label class="label" for="paikka">Paikka:</label>
            <input type="text" id="paikka" name="paikka" placeholder="Kalansaanti paikka" class="input" maxlength="24" required>
            <br/>
            <label class="label" for="aika">Aika:</label>
            <input type="date" id="aika" name="aika" class="input" required>
            <br/>
            <label class="label" for="viehe">Viehe:</label>
            <select id="viehe" name="viehe" required>
                <option>Valitse viehe</option>
                <!-- saa viehe vaihto ehdot tietokannasta -->
                <?php
                    $kysely_viehe_select = $conn->prepare("SELECT viehe FROM viehe");
                    $kysely_viehe_select->execute();
                    $data_viehe = $kysely_viehe_select->get_result();
                    if ($data_viehe) {
                        while($rivi = $data_viehe->fetch_assoc()) {
                            echo '<option value="' . html($rivi['viehe']) . '">'
                                . html($rivi['viehe']) . '</option>';
                        }
                    }
                ?>
                <option value="muu">
                    <span>muu</span>
                </option>
            </select>
            <br/>
            <label class="label" for="vapa">Vapa:</label>
            <select id="vapa" name="vapa" required>
                <option value="">Valitse vapa</option>
                <!-- saa vapa vaihto ehdot tietokannasta -->
                <?php
                    $kysely_vapa_select = $conn->prepare("SELECT vapa FROM vapa");
                    $kysely_vapa_select->execute();
                    $data_vapa = $kysely_vapa_select->get_result();
                    if ($data_vapa) {
                        while($rivi = $data_vapa->fetch_assoc()) {
                            echo '<option value="' . html($rivi['vapa']) . '">'
                                . html($rivi['vapa']) . '</option>';
                        }
                    }
                ?>
                <option value="muu">
                    <span>muu</span>
                </option>
            </select>
            <br/>
            <label class="label" for="kuva">Valitse kuva:</label> 
            <input type="file" name="fileToUpload" id="fileToUpload" accept="image/*" style="display: none;">
            <button id="kuvaBt" type="button">
                Valitse kuva
            </button>
            <br/>
            <button type="submit" name="submit" class="button">Lähetä</button>
            <?php
            //  teksti onnistuko syöttö vai ei 
            if (isset($_SESSION['MessageAdd'])) {
                $text = ucfirst(html($_SESSION['Text']));
                echo "
                <br/>
                <span style='font-size: 1.5rem;'>$text</span>
                <br/>
                ";
            }
            ?>
            <input type="hidden" name="csrf_token_li" value="<?php echo htmlspecialchars($_SESSION['csrf_token_li']) ?>">   
        </form>
    </div>
    <script src="lisaa.js" defer></script>
</body>
</html>