import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.user import User
from utils.connect_db import execute_query_fetchall

from flask import Flask, render_template, request

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

# simulating login
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
    if request.method == 'POST':
        destination = request.form.get('destination')
        complaint_type = request.form.get('complaintType')
        message = request.form.get('message')
        machine_id = None
        if destination == 'machine':
            machine_id = request.form.get('machineNumber')
        
        if current_user:
            current_user.report(target=destination, type=complaint_type, machine_id=machine_id, message=message)
            return render_template('report.html', success=True)
        else:
            return render_template('report.html', error="Usuário não autenticado")
    else:
        return render_template('report.html')

if __name__ == '__main__':
    app.run(debug=True)
