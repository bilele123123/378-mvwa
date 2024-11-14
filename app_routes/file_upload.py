import os
from flask import Blueprint, request, jsonify, render_template_string

bp = Blueprint("file_upload", __name__)

upload_folder = None  # Global variable for upload folder path

def init_file_upload(upload_folder_path):
    """Initialize the upload folder path."""
    global upload_folder
    upload_folder = upload_folder_path
    os.makedirs(upload_folder, exist_ok=True)  # Ensure the folder exists

@bp.route("/", methods=["GET", "POST"])
def upload_file_demo():
    """Display the file upload form (GET) and handle file upload (POST)."""
    if request.method == "GET":
        # Display a styled file upload form
        return render_template_string("""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>File Upload</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        margin: 0;
                        background-color: #f4f4f9;
                    }
                    .container {
                        max-width: 400px;
                        width: 100%;
                        padding: 20px;
                        background-color: white;
                        border-radius: 8px;
                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                        text-align: center;
                    }
                    h2 {
                        color: #333;
                        margin-bottom: 15px;
                    }
                    label {
                        display: block;
                        color: #555;
                        margin-bottom: 10px;
                        font-weight: bold;
                    }
                    input[type="file"] {
                        padding: 8px;
                        font-size: 14px;
                        border-radius: 4px;
                        border: 1px solid #ddd;
                        width: 100%;
                        margin-bottom: 20px;
                    }
                    button {
                        width: 100%;
                        padding: 12px;
                        font-size: 16px;
                        color: white;
                        background-color: #007bff;
                        border: none;
                        border-radius: 4px;
                        cursor: pointer;
                        transition: background-color 0.3s;
                    }
                    button:hover {
                        background-color: #0056b3;
                    }
                    .note {
                        font-size: 0.9em;
                        color: #777;
                        margin-top: 15px;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h2>Upload a File</h2>
                    <form action="/file_upload/" method="post" enctype="multipart/form-data">
                        <label for="file">Choose a file:</label>
                        <input type="file" id="file" name="file" required>
                        <button type="submit">Upload</button>
                    </form>
                    <p class="note">Accepted file types: .txt, .jpg, .png, etc.</p>
                </div>
            </body>
            </html>
        """)

    # Handle the POST request to upload a file
    if not upload_folder:
        return jsonify({"error": "Upload folder is not configured."}), 500

    file = request.files.get('file')
    
    if file:
        file_path = os.path.join(upload_folder, file.filename)
        try:
            file.save(file_path)
            return jsonify({"message": "File uploaded successfully", "filename": file.filename}), 200
        except Exception as e:
            return jsonify({"error": f"Failed to upload file: {str(e)}"}), 500

    return jsonify({"error": "No file uploaded"}), 400
