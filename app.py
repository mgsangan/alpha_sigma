from flask import Flask, request, jsonify
import pandas as pd
import requests
import io

app = Flask(__name__)

# GitHub raw file URL
GITHUB_EXCEL_URL = "hhttps://github.com/mgsangan/alpha_sigma/blob/main/Book1.xlsx"

# Load user data from GitHub Excel file
def load_users():
    try:
        response = requests.get(GITHUB_EXCEL_URL)
        if response.status_code == 200:
            excel_data = io.BytesIO(response.content)
            df = pd.read_excel(excel_data, sheet_name="Users")

            # Ensure required columns exist
            if "Username" not in df.columns or "Password" not in df.columns:
                print("Error: Missing 'Username' or 'Password' columns in Excel file!")
                return {}

            # Convert usernames to lowercase for case-insensitive login
            return {str(row["Username"]).strip().lower(): str(row["Password"]).strip() for _, row in df.iterrows()}
        else:
            print(f"Error fetching file: {response.status_code}")
            return {}
    except Exception as e:
        print(f"Error loading users: {e}")
        return {}

@app.route('/login', methods=['POST'])
def login():
    users = load_users()  # Reload users every request
    
    data = request.json
    username = data.get('username', '').strip().lower()  # Case-insensitive check
    password = data.get('password', '').strip()

    if username in users and users[username] == password:
        return jsonify({"message": "Login successful", "status": "success"})
    else:
        return jsonify({"message": "Invalid username or password", "status": "error"}), 401

if __name__ == '__main__':
    app.run(debug=True)
