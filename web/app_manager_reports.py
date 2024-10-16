"""
This script initializes a Flask application for managing a dashboard that handles vending machine complaints. 
It interacts with the backend to allow a manager to view machine-related complaints, filter them by various criteria, 
and display the results on a web page.

The Flask application contains two main routes:
1. /manager_dashboard: Renders the manager dashboard with a list of machine IDs.
2. /get_complaints: Fetches complaints based on filters such as machine ID, issue type, and complaint status, 
   then returns them in JSON format.

Dependencies:
- Flask for handling web routes and rendering templates.
- A backend module (`Manager` and `Machine`) for managing the business logic, such as retrieving complaints and machine information.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, render_template, request, jsonify
from backend.manager import Manager  
from backend.machine import Machine

# Initialize Flask app
app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

# Authenticate the current manager using predefined credentials
current_manager = Manager.authenticate('fabricio@gestor.com', '123')

@app.route('/manager_dashboard')
def manager_dashboard():
    """
    Route to render the manager dashboard page. It retrieves the list of machine IDs
    to be displayed on the page where the manager can view reports and complaints.
    
    Returns:
        HTML page: The rendered manager dashboard with machine IDs for selection.
    """
    machine_ids = Machine.get_machines()
    return render_template('report_manager.html', machine_ids=machine_ids)

@app.route('/get_complaints', methods=['GET'])
def get_complaints():
    """
    API route to fetch complaints based on filters such as machine ID, issue type, and status.
    This function retrieves the filter parameters from the request and calls the Manager's method
    to query the database and return the complaints in JSON format.
    
    Returns:
        JSON response: List of complaints matching the filter criteria.
    """
    # Get filter parameters from the request
    issue = request.args.get('target')
    machine_id = request.args.get('machine_id')
    issue_type = request.args.get('issue_type')
    status = request.args.get('status')

    # Map status to corresponding values in the database
    status_map = {
        'resolved': 'resolved',
        'unresolved': 'unresolved',
        None: None
    }

    # Fetch complaints using the manager's method
    complaints = current_manager.view_all_issues(
        issue=issue,
        machine=machine_id,
        type=issue_type,
        status=status_map.get(status)
    )

    return jsonify(complaints)

if __name__ == '__main__':
    # Run the Flask app in debug mode
    app.run(debug=True)
