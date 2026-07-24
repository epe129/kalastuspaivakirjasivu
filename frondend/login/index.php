<?php 
session_start();
unset($_SESSION['errorTextRegister']);
// CSRF suojaus ettei voi kuka vaan tehdä pyyntojö 
if (empty($_SESSION['csrf_token_l'])) {
    $_SESSION['csrf_token_l'] = bin2hex(random_bytes(32));
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kirjaudu Sisään</title>
    <style>
        html {
            background-image: url('../kuvat/tausta.jpg'); 
            background-repeat: no-repeat;
            background-attachment: fixed;  
            background-size: cover;
        }

        body {
            font-size: 75%;
        }

        h1 {
            text-align: center;
            background-color: white; 
            width: fit-content; 
            height: fit-content; 
            margin: 0 auto; 
            border-radius: 10px;
        }
        
        .main {
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            text-align: center;
            margin: 0 auto;
            padding: 0;
            min-width: fit-content;
            max-width: 300px;
            height: auto;
        }

        /* formin css */
        form {
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            width: 100%;

        }

        label {
            font-size: 125%;
            display: block;
            margin-bottom: 8px;
            color: black;
            font-weight: bold;
            text-transform: capitalize;
        }

        input[type="text"], input[type="password"], input[type="email"] {
            width: 75%;
            padding: 12px;
            margin-bottom: 20px;
            border: 1px solid #ddd;
            border-radius: 4px;
            transition: border-color 0.3s;
            font-size: 120%;
        }
        input[type="text"]:focus, input[type="password"]:focus, input[type="email"]:focus {
            outline: none;
            border-color: #007bff;
            box-shadow: 0 0 5px rgba(0, 123, 255, 0.3);
        }

        button {
            width: 75%;
            padding: 12px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 4px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: background-color 0.3s;
        }

        button:hover {
            background-color: #0056b3;
        }

        a {
            font-size: 130%;;
            color: black;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <div class="main">
        <form action="../data/handleLogin.php" method="POST">
            <h1>Kirjaudu Sisään</h1>
            <br>
            <label>Sähköposti</label>
            <input type="email" name="email" pattern="[a-z0-9._%+\-]+@[a-z0-9.\-]+\.[a-z]{2,}$" required>
            <br>
            <label>Salasana</label>
            <input type="password" name="password" required>
            <br>
            <button type="submit">Lähetä</button>
            <br>
            <?php
            //  saa viestin jos kirjautuminen epäonnistui
            if (isset($_SESSION['errorMessageLogin']) and isset($_SESSION['errorTextLogin'])) {
                $text = ucfirst($_SESSION['errorTextLogin']);
                echo "
                <br/>
                <span>$text</span>
                <br/>
                ";
            }
            ?>
            <br>
            <a href="../rekisteroidy/index.php">Rekisteröidy</a>
            <input type="hidden" name="csrf_token_l" value="<?php echo htmlspecialchars($_SESSION['csrf_token_l']) ?>">
        </form>
    </div>
</body>
</html>