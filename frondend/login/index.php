<?php session_start();
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
    <title>Log in</title>
    <style>
        html {
            background-image: url('../kuvat/tausta.jpg'); 
            background-repeat: no-repeat;
            background-attachment: fixed;  
            background-size: cover;
        }
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            padding: 20px;
            font-size: 1.3rem;
            min-height: 70vh;
        }
        /* formin css */
        form {
            background-color: white;
            padding: 20px 50px 40px 40px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            width: 100%;
            max-width: 400px;
        }

        label {
            display: block;
            margin-bottom: 8px;
            color: black;
            font-weight: bold;
            text-transform: capitalize;
        }

        input[type="text"], input[type="password"], input[type="email"] {
            width: 100%;
            padding: 12px;
            margin-bottom: 20px;
            border: 1px solid #ddd;
            border-radius: 4px;
            transition: border-color 0.3s;
            font-size: 1.3rem;
        }

        input[type="text"]:focus, input[type="password"]:focus, input[type="email"]:focus {
            outline: none;
            border-color: #007bff;
            box-shadow: 0 0 5px rgba(0, 123, 255, 0.3);
        }

        button {
            width: 100%;
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
            font-size: 1.5rem;
            color: black;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <form action="../data/handleLogin.php" method="POST">
        <h1>Log in</h1>
        <br>
        <label>email</label>
        <input type="email" name="email" pattern="[a-z0-9._%+\-]+@[a-z0-9.\-]+\.[a-z]{2,}$" required>
        <br>
        <label>password</label>
        <input type="password" name="password" required>
        <br>
        <button type="submit">Lähetä</button>
        <br>
        <?php
        //  saa viestin onnistuiko arvojen lisääminen 
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
        <a href="../index.php">Register</a>
        <input type="hidden" name="csrf_token_l" value="<?php echo htmlspecialchars($_SESSION['csrf_token_l']) ?>">
    </form>
</body>
</html>