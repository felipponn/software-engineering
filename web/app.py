import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.user import User
from utils.connect_db import execute_query_fetchall

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')


# user = User("Fabricio", "123", "fabricio@fabricio.com", "83999999999")
# user.save_db()

current_user = User.authenticate('fabricio@fabricio.com', '123')

@app.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        # Get form data
        destination = request.form.get('destination')
        complaint_type = request.form.get('complaintType')
        message = request.form.get('message')
        machine_id = None
        if destination == 'machine':
            machine_id = request.form.get('machineNumber')
        
        # Check if the user is authenticated
        if current_user:
            # Use current_user to send a report
            current_user.report(target=destination, type=complaint_type, machine_id=machine_id, message=message)
            return redirect(url_for('report_success'))
        else:
            return "User not authenticated", 401
    else:
        # Render the report form
        return render_template('report.html')
    
@app.route('/report_success')
def report_success():
    return "Report sent successfully!"

if __name__ == '__main__':
    app.run(debug=True)