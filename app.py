from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load the Excel file
df = pd.read_excel('Book1.xlsx')

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    # Check if the username and password match
    if ((df['Username'] == username) & (df['Password'] == password)).any():
        return jsonify({'result': 'success'})
    else:
        return jsonify({'result': 'failure'})

if __name__ == '__main__':
    app.run(debug=True)
