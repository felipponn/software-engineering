import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, render_template, request, jsonify
from backend.user import User
from backend.manager import Manager  # Importe a classe Manager
from backend.machine import Machine

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

# current_manager = Manager('Fabrício Gestor', '123', 'fabricio@gestor.com', '12345678')
# current_manager.save_db()

current_manager = Manager.authenticate('fabricio@gestor.com', '123')
print(current_manager)  

# @app.route('/manager_dashboard')
# def manager_dashboard():
#     machine_ids = Machine.get_machines()
#     return render_template('manager_dashboard.html', machine_ids=machine_ids)

# @app.route('/get_complaints', methods=['GET'])
# def get_complaints():
#     target = request.args.get('target')
#     machine_id = request.args.get('machine_id')
#     issue_type = request.args.get('issue_type')
#     status = request.args.get('status')

#     status_map = {
#         'resolved': 'resolved',
#         'unresolved': 'unresolved',
#         'all': None
#     }

#     complaints = current_manager.view_all_issues(
#         target=target if target != 'all' else None,
#         machine=machine_id if machine_id != 'all' else None,
#         type=issue_type if issue_type != 'all' else None,
#         status=status_map.get(status)
#     )

#     return jsonify(complaints)

# if __name__ == '__main__':
#     app.run(debug=True)
