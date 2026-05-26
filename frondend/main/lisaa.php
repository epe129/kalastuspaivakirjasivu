<?php
session_start();
// Saadaan yhteys tietokantaan 
include_once('../data/db_connection.php');
// tarkistetaan että käyttäjä on kirjautunut
if (!isset($_SESSION['email']) and !isset($_SESSION["kalastaja_id"])) {
    header("Location: ../index.php");
    exit();
}
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
    <link rel="stylesheet" href="main.css">
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
    <div class="main-div">
        <h1>Lisää kalastustietoja</h1>
        <!-- form lomake -->
        <form class="form" action="../data/handleAdd.php" method="post">
            <label class="label" for="pituus">Kalalaji:</label>
            <select id="KalaLaji" name="laji" required>
                <option value="">Valitse kalalaji</option>
                <?php
                    $sql = "SELECT laji FROM laji";
                    $tulos = $conn->query($sql);
                    if ($tulos->num_rows > 0) {
                        while($rivi = $tulos->fetch_assoc()) {
                            echo "
                            <option value='{$rivi['laji']}'>
                            {$rivi['laji']}   
                            </option>
                            ";
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
                    $sql = "SELECT viehe FROM viehe";
                    $tulos = $conn->query($sql);
                    if ($tulos->num_rows > 0) {
                        while($rivi = $tulos->fetch_assoc()) {
                            echo "
                            <option value='{$rivi['viehe']}'>
                            {$rivi['viehe']}   
                            </option>
                            ";
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
                    $sql = "SELECT vapa FROM vapa";
                    $tulos = $conn->query($sql);
                    if ($tulos->num_rows > 0) {
                        while($rivi = $tulos->fetch_assoc()) {
                            echo "
                            <option value='{$rivi['vapa']}'>
                            {$rivi['vapa']}   
                            </option>
                            ";
                        }
                    }
                ?>
                <option value="muu">
                    <span>muu</span>
                </option>
            </select>
            <br/>
            <button type="submit" class="button">Lähetä</button>
            <?php
            //  teksti onnistuko syöttö vai ei 
            if (isset($_SESSION['MessageAdd'])) {
                $text = ucfirst($_SESSION['Text']);
                echo "
                <br/>
                <span style='font-size: 1.5rem;'>$text</span>
                <br/>
                ";
            }
            ?>
            <input type="hidden" name="csrf_token_li" value="<?php echo htmlspecialchars($_SESSION['csrf_token_li']) ?>">   
        </form>
        <!-- jos käyttäjä valitsee muu voi lisätä uuden arvon -->
        <div class="laji_muu_div" id="laji_muu_div">
            <form class="laji_muu_form" id="laji_muu_form" action="../data/handleMuuAdd.php" method="post">
                <h2 style="margin-bottom: 10px;" id="h2_muu"></h2>
                <input type="text" id="muu" placeholder="Muu mikä" maxlength="24" style="font-size: 1.5rem;">
                <button type="submit" class="button_muu">Lähetä</button>
                <input type="hidden" name="csrf_token_li_muu" value="<?php echo htmlspecialchars($_SESSION['csrf_token_li_muu']) ?>">   
            </form>    
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>