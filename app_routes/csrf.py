from flask import Blueprint, request, render_template_string

bp = Blueprint("csrf", __name__)

# Simulated balance for demonstration
balance = 1000

@bp.route("/", methods=["GET", "POST"])
def csrf_demo():
    global balance
    if request.method == "POST":
        amount = int(request.form.get("amount"))
        balance -= amount
        return render_template_string("""
            <div class="container">
                <div class="card">
                    <h2>Transfer Successful</h2>
                    <p>${{ amount }} transferred! New balance: ${{ balance }}</p>
                    <a href="/">Make another transfer</a>
                </div>
            </div>
            """, amount=amount, balance=balance)
    
    return render_template_string("""
        <html>
        <head>
            <title>Bank Transfer - CSRF Demo</title>
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
                    padding: 20px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    background-color: white;
                    border-radius: 8px;
                    text-align: left;
                }
                .card, .explanation {
                    margin-top: 20px;
                }
                h2 {
                    color: #333;
                    font-size: 24px;
                    margin-bottom: 10px;
                }
                h3 {
                    color: #007bff;
                    font-size: 20px;
                    margin-bottom: 10px;
                }
                p {
                    font-size: 16px;
                    color: #555;
                }
                form {
                    display: flex;
                    flex-direction: column;
                    margin-top: 20px;
                }
                input[type="text"] {
                    padding: 10px;
                    font-size: 16px;
                    margin-bottom: 15px;
                    border: 1px solid #ddd;
                    border-radius: 4px;
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
                .balance {
                    font-size: 20px;
                    color: #007bff;
                    margin-bottom: 20px;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Bank Transfer - CSRF Demo</h2>
                <p class="balance">Your balance: ${{ balance }}</p>

                <!-- Explanation of CSRF Vulnerability -->
                <div class="explanation">
                    <h3>Understanding the CSRF Vulnerability</h3>
                    <p><strong>CSRF (Cross-Site Request Forgery)</strong> is a type of attack that tricks a user into submitting a request they did not intend. This usually happens when a user is authenticated with the vulnerable site (e.g., through a session or cookies). Here’s how the CSRF vulnerability occurs in this code:</p>
                    <ul>
                        <li><strong>No Verification for Requests:</strong> The POST request in the code does not include a CSRF token or any verification mechanism to check if the request was intentionally made by the user.</li>
                        <li><strong>Global Balance Modification:</strong> When a POST request is made to the endpoint with an amount, the code subtracts that amount from the balance, assuming it’s a valid request from the user.</li>
                        <li><strong>Open to External Requests:</strong> Since the form does not require any specific authentication or authorization checks within the request itself, a malicious site can submit a request on behalf of the user.</li>
                    </ul>

                    <h3>Simulating a CSRF Attack</h3>
                    <p>Let’s go through an example to see how an attacker could exploit this setup:</p>
                    <ol>
                        <li><strong>User Visits the Vulnerable Site:</strong> Suppose the user visits this Flask application (running locally or in a sandboxed environment) and has an open session.</li>
                        <li><strong>Malicious Site:</strong> The attacker creates a fake webpage (e.g., <code>evil-site.com</code>) that contains a hidden form targeting the Flask application’s endpoint. Here’s what the malicious form might look like:</li>
                    </ol>
                    <pre></pre>
                    <p>When the user visits this malicious page, the hidden form is automatically submitted to the Flask app, transferring $500 from the user's balance without their consent. This demonstrates the potential impact of a CSRF attack.</p>
                </div>

                <!-- Bank Transfer Form -->
                <form method="post">
                    <label for="amount">Amount:</label>
                    <input type="text" name="amount" id="amount" placeholder="Enter amount">
                    <input type="submit" value="Transfer">
                </form>
            </div>
        </body>
        </html>
    """, balance=balance)
