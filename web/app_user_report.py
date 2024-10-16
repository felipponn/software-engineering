"""
This script initializes a Flask application for submitting complaints related to vending machines or other targets. 
The application allows authenticated users to submit complaints through a form, specifying details like the type 
of complaint, the machine (if applicable), and a message.

The Flask application contains one main route:
1. /report: Handles both GET and POST requests for submitting complaints. If a POST request is made, 
   the user's complaint is registered, and success or error feedback is returned.

Dependencies:
- Flask for handling web routes and rendering templates.
- A backend module (`User` and `Machine`) for managing user authentication and machine information retrieval.
- Utility module for connecting to the database.

Assumptions:
- User authentication is simulated, and a user is automatically authenticated for testing purposes.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.user import User 
from backend.machine import Machine
from flask import Flask, render_template, request

# Initialize Flask app
app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

# Simulating login
current_user = User.authenticate('fabricio@fabricio.com', '123')

@app.route('/report', methods=['GET', 'POST'])
def report():
    """
    Handles the complaint submission route.

    If the request method is POST, collects form data and registers the complaint for the authenticated user.
    If the request method is GET, renders the complaint submission page.

    Returns:
        str: The rendered HTML page with a success or error message, depending on the outcome of the operation.
    """

    machine_ids = Machine.get_machines()
    
    if request.method == 'POST':
        # Collect form data for complaint
        destination = request.form.get('destination')
        complaint_type = request.form.get('complaintType')
        message = request.form.get('message')
        machine_id = None
        if destination == 'machine':
            machine_id = request.form.get('machineNumber')
        
        # If the user is authenticated, register the complaint
        if current_user:
            current_user.report(target=destination, type=complaint_type, machine_id=machine_id, message=message)
            return render_template('report.html', success=True, machine_ids=machine_ids)
        else:
            return render_template('report.html', error="Usuário não autenticado", machine_ids=machine_ids)
    
    # If GET request, render the report form
    return render_template('report.html', machine_ids=machine_ids)

if __name__ == '__main__':
    # Run the Flask app in debug mode
    app.run(debug=True)
