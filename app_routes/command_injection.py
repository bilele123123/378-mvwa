from flask import Blueprint, request, render_template_string
import subprocess
import re
import shlex

bp = Blueprint("command_injection", __name__)

@bp.route("/", methods=["GET", "POST"])
def exec_demo():
    output = ""
    if request.method == "POST":
        # Get the user input
        ip_address = request.form.get("ip")

        # Basic filtering - removing '&&' and ';'
        filtered_ip = re.sub(r"[;&]", "", ip_address)

        # Split input based on '&' to simulate chaining
        commands = filtered_ip.split("&")

        try:
            # Execute each command separately
            for cmd in commands:
                cmd = cmd.strip()  # Clean up spaces
                if "ping" in cmd:
                    result = subprocess.check_output(f"ping -c 1 {cmd.split()[1]}", shell=True, text=True)
                else:
                    result = subprocess.check_output(cmd, shell=True, text=True)
                output += result + "\n"
                
        except subprocess.CalledProcessError as e:
            output += str(e) + "\n"

    return render_template_string("""
        <html>
        <head>
            <title>Command Injection Challenge</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f9;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    flex-direction: column;
                    padding: 20px;
                    margin: 0;
                }
                .container {
                    width: 100%;
                    max-width: 600px;
                    background-color: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                }
                h2 {
                    color: #333;
                    text-align: center;
                }
                form {
                    display: flex;
                    flex-direction: column;
                    margin-bottom: 20px;
                }
                input[type="text"] {
                    padding: 10px;
                    font-size: 16px;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    margin-bottom: 15px;
                }
                input[type="submit"] {
                    background-color: #007bff;
                    color: white;
                    font-size: 16px;
                    padding: 10px;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                    transition: background-color 0.3s;
                }
                input[type="submit"]:hover {
                    background-color: #0056b3;
                }
                .output {
                    background-color: #f9f9f9;
                    border: 1px solid #ddd;
                    padding: 10px;
                    border-radius: 4px;
                    margin-top: 20px;
                    font-family: monospace;
                    white-space: pre-wrap;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Command Injection Challenge</h2>
                <p>Enter an IP address to ping:</p>
                <form method="post">
                    <input type="text" name="ip" placeholder="127.0.0.1" required>
                    <input type="submit" value="Ping">
                </form>
                <div class="output">
                    <h3>Output:</h3>
                    <pre>{{ output }}</pre>
                </div>
            </div>
        </body>
        </html>
    """, output=output)