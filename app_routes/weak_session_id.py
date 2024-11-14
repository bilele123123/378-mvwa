import random
import string
import secrets
from flask import Blueprint, make_response, request, render_template_string
from datetime import datetime, timedelta

bp = Blueprint("weak_session_id", __name__)

def generate_weak_session_id(length=8):
    # Vulnerably short and predictable session ID
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))

def generate_secure_session_id(bits=128):
    # Generate a secure session ID with a length equivalent to 128 bits (32 characters)
    return secrets.token_hex(bits // 8)

@bp.route("/", methods=["GET", "POST"])
def login():
    # Session metadata
    session_id = request.cookies.get("session_id")
    session_start = datetime.now()
    max_session_duration = timedelta(hours=1)
    session_end = session_start + max_session_duration
    ip_address = request.remote_addr  # Get client's IP address
    user_agent = request.headers.get("User-Agent")  # Get client device info

    # Generate a secure session ID suggestion
    ideal_session_id = generate_secure_session_id()

    # Determine session status
    session_status = "Active" if session_end > datetime.now() else "Expired"

    # If session_id exists, display the current session information
    if session_id:
        response_content = f"""
            <html>
            <head>
                <title>Session Information</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        background-color: #f4f4f9;
                        margin: 0;
                    }}
                    .container {{
                        width: 100%;
                        max-width: 600px;
                        padding: 20px;
                        background-color: white;
                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                        border-radius: 8px;
                        text-align: center;
                    }}
                    h2 {{
                        color: #333;
                        margin-bottom: 20px;
                    }}
                    table {{
                        width: 100%;
                        border-collapse: collapse;
                        margin-bottom: 20px;
                    }}
                    th, td {{
                        padding: 12px;
                        border: 1px solid #ddd;
                        text-align: left;
                    }}
                    th {{
                        background-color: #007bff;
                        color: white;
                    }}
                    .session-id {{
                        font-family: monospace;
                        color: #555;
                        word-wrap: break-word;
                    }}
                    .scrollable {{
                        padding: 10px;
                        background-color: #f7f7f7;
                        border: 1px solid #ddd;
                        border-radius: 4px;
                    }}
                    .note {{
                        font-size: 0.9em;
                        color: #777;
                        text-align: left;
                        margin-top: 10px;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h2>Session Information</h2>
                    <table>
                        <tr>
                            <th>Session Detail</th>
                            <th>Value</th>
                        </tr>
                        <tr>
                            <td>Session Status</td>
                            <td>{session_status}</td>
                        </tr>
                        <tr>
                            <td>Existing Session ID</td>
                            <td class="session-id">{session_id}</td>
                        </tr>
                        <tr>
                            <td>Recommended Secure Session ID (128-bit)</td>
                            <td><div class="scrollable session-id">{ideal_session_id}</div></td>
                        </tr>
                        <tr>
                            <td>Session Start Time</td>
                            <td>{session_start.strftime("%Y-%m-%d %H:%M:%S")}</td>
                        </tr>
                        <tr>
                            <td>Session End Time</td>
                            <td>{session_end.strftime("%Y-%m-%d %H:%M:%S")}</td>
                        </tr>
                        <tr>
                            <td>Max Session Duration</td>
                            <td>1 hour</td>
                        </tr>
                        <tr>
                            <td>IP Address</td>
                            <td>{ip_address}</td>
                        </tr>
                        <tr>
                            <td>User Agent</td>
                            <td>{user_agent}</td>
                        </tr>
                    </table>
                    <p class="note">
                        Note: The existing session ID is for demonstration only. In production environments, a secure session ID, such as the recommended 128-bit version, is advised.
                    </p>
                </div>
            </body>
            </html>
        """
        return response_content, 200

    # If no session_id, create a new one and set it as a cookie
    new_session_id = generate_weak_session_id()
    response = make_response(render_template_string(f"""
        <html>
        <head>
            <title>Session Created</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    background-color: #f4f4f9;
                    margin: 0;
                }}
                .container {{
                    width: 100%;
                    max-width: 600px;
                    padding: 20px;
                    background-color: white;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    border-radius: 8px;
                    text-align: center;
                }}
                h2 {{
                    color: #333;
                    margin-bottom: 20px;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-bottom: 20px;
                }}
                th, td {{
                    padding: 12px;
                    border: 1px solid #ddd;
                    text-align: left;
                }}
                th {{
                    background-color: #007bff;
                    color: white;
                }}
                .session-id {{
                    font-family: monospace;
                    color: #555;
                    word-wrap: break-word;
                }}
                .scrollable {{
                    padding: 10px;
                    background-color: #f7f7f7;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                }}
                .note {{
                    font-size: 0.9em;
                    color: #777;
                    text-align: left;
                    margin-top: 10px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Session Created</h2>
                <table>
                    <tr>
                        <th>Session Detail</th>
                        <th>Value</th>
                    </tr>
                    <tr>
                        <td>New Session ID</td>
                        <td class="session-id">{{{{ new_session_id }}}}</td>
                    </tr>
                    <tr>
                        <td>Recommended Secure Session ID (128-bit)</td>
                        <td><div class="scrollable session-id">{{{{ ideal_session_id }}}}</div></td>
                    </tr>
                    <tr>
                        <td>Session Start Time</td>
                        <td>{{{{ session_start }}}}</td>
                    </tr>
                    <tr>
                        <td>Session End Time</td>
                        <td>{{{{ session_end }}}}</td>
                    </tr>
                    <tr>
                        <td>Max Session Duration</td>
                        <td>1 hour</td>
                    </tr>
                    <tr>
                        <td>IP Address</td>
                        <td>{{{{ ip_address }}}}</td>
                    </tr>
                    <tr>
                        <td>User Agent</td>
                        <td>{{{{ user_agent }}}}</td>
                    </tr>
                </table>
                <p class="note">
                    Note: This session ID is for demonstration purposes only. For secure production use, the recommended 128-bit session ID is advised.
                </p>
            </div>
        </body>
        </html>
    """, new_session_id=new_session_id, ideal_session_id=ideal_session_id, 
         session_start=session_start.strftime("%Y-%m-%d %H:%M:%S"), 
         session_end=session_end.strftime("%Y-%m-%d %H:%M:%S"),
         ip_address=ip_address, user_agent=user_agent))

    response.set_cookie("session_id", new_session_id)
    return response
