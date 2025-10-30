from flask import Flask, request
import requests
import os,sys,random
import subprocess


key = ''.join(random.choices('0123456789abcdefghijklmnopqrstuvwxyz', k=20))
prt = int(random.randint(5000,9000))
if sys.platform.startswith('win'):
    os.system('cls')
else:
    os.system('clear')
print("""[~]=========================================[~]
[~]         Cloudfire Captcha Bypass                 [~]
[~]         youtube :- cryptowithAryan               [~]
[~]         TG Channel : @cryptowitharyanog          [~]
[~]=========================================         [~]
""".strip())
print(f'Web url : \033[0;32mhttp://localhost:{prt}\033[0m')
print("=============================================")
print(" Note:\033[0;32m copy web url and browse it any browser\nfor getting captcha token. if you want more token \nuse multiple tab on your browser.\033[0m")
print("=============================================")
app = Flask(__name__)
template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cloudflare CAPTCHA</title>
    <!-- Cloudflare Turnstile Script -->
    <script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>
    <style>
        .class1 {
          font-family: 'Arial', sans-serif;
          font-size: 24px;
          margin: 20px auto;
          text-align: center;
          color: white;
       }
       div {
          margin: 20px auto; 
          width: fit-content;
       }
       body {
       background-color: black;
       }
       p {
          margin: 20px auto;
          width: fit-content;
       }
       .hclass2 {
          font-family: 'Arial', sans-serif;
          font-size: 20px;
          color: white;
          width: fit-content;
          text-decoration: none;
          text-align: center;
          margin: 20px auto;
        }
    </style>
</head>
<body>
    <h2 class='class1'>Captcha Bypass By Crypto With Aryan </h2>
    <h2 class='hclass2'>Join telegram channel : @cryptowitharyanog </h2>
    <!-- Cloudflare CAPTCHA widget -->
    <div class="cf-turnstile" data-sitekey="0x4AAAAAAA4PZrjDa5PcluqN" data-callback="onCaptchaVerified"></div>
    <p id="status" style="color: green; font-weight: bold;"></p>
    <script>
        let captchaSolved = false;
        document.getElementById("status").textContent = "Captcha is verifying, please wait...";
        // Callback when CAPTCHA is completed
        function onCaptchaVerified(token) {
            captchaSolved = true; // Mark CAPTCHA as solved
            document.getElementById("status").textContent = "Verification successful. Sending in 0.1 seconds...";
            
            // Wait 0.1 seconds before sending the token
            setTimeout(() => {
                sendToken(token);
            }, 100);
        }

        // Function to send the token
        async function sendToken(token) {
            try {
                const response = await fetch(`/reserve_token?token=${token}`);
                if (response.ok) {
                    document.getElementById("status").textContent = "Token sent successfully!";
                } else {
                    document.getElementById("status").textContent = "Failed to send token.";
                }
            } catch (error) {
                document.getElementById("status").textContent = "Error while sending the token.";
            }
            location.reload()
        }

        // Refresh the page if CAPTCHA not solved in 15 seconds
        setTimeout(() => {
            if (!captchaSolved) {
                document.getElementById("status").textContent = "CAPTCHA not solved. Refreshing the page...";
                setTimeout(() => {
                    location.reload(); // Refresh the page
                }, 1000); // Give a 1-second notice before refreshing
            }
        }, 10000); // 10 seconds
    </script>
</body>
</html>
"""
tokens=[]
@app.route('/reserve_token')
def reserve_token():
    global tokens
    token = request.args.get('token')
    tokens.append(str(token))
    return 'ok'

@app.route('/get')
def getone():
     try:
        letest_token = tokens.pop(int(len(tokens)) -1)
        return str(letest_token)
     except:
        return 'No tokens available'

@app.route('/')
def webpage():
    return template

app.run(port=prt)
