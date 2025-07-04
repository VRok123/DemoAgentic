import csv
import os
from flask import Flask, render_template, request, send_file, redirect, url_for

app = Flask(__name__)

# List of Indian states for the dropdown
INDIAN_STATES = [
    'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh',
    'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand',
    'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur',
    'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab',
    'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura',
    'Uttar Pradesh', 'Uttarakhand', 'West Bengal',
    'Andaman and Nicobar Islands', 'Chandigarh', 'Dadra and Nagar Haveli and Daman and Diu',
    'Delhi', 'Jammu and Kashmir', 'Ladakh', 'Lakshadweep', 'Puducherry'
]


# List of branches for the dropdown
BRANCHES = [
    'Computer Engineering',
    'Information Technology',
    'Artificial Intelligence and Data Science',
    'Electronics and Telecommunications Engineering',
    'Chemical Engineering'
]


import pathlib
REGISTRATION_FILE = str(pathlib.Path(__file__).parent / 'registrations.csv')

@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = {
            'name': request.form['name'],
            'branch': request.form['branch'],
            'state': request.form['state'],
            'email': request.form['email'],
            'phone': request.form['phone']
        }
        save_registration(data)
        return render_template('result.html', data=data)
    return render_template('register.html', states=INDIAN_STATES, branches=BRANCHES)

def save_registration(data):
    file_exists = os.path.isfile(REGISTRATION_FILE)
    with open(REGISTRATION_FILE, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['name', 'branch', 'state', 'email', 'phone']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

@app.route('/download')
def download_registrations():
    if not os.path.isfile(REGISTRATION_FILE):
        return redirect(url_for('register'))
    return send_file(REGISTRATION_FILE, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
