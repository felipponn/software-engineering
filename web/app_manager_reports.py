import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, render_template, request, jsonify
from backend.manager import Manager  
from backend.machine import Machine

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

# current_manager = Manager('Fabrício Gestor', '123', 'fabricio@gestor.com', '12345678')
# current_manager.save_db()

current_manager = Manager.authenticate('fabricio@gestor.com', '123')

@app.route('/manager_dashboard')
def manager_dashboard():
    machine_ids = Machine.get_machines()
    return render_template('report_manager.html', machine_ids=machine_ids)

@app.route('/get_complaints', methods=['GET'])
def get_complaints():
    # Obter os parâmetros de filtro da requisição
    target = request.args.get('target')
    machine_id = request.args.get('machine_id')
    issue_type = request.args.get('issue_type')
    status = request.args.get('status')

    # Mapear status para os valores correspondentes no banco de dados
    status_map = {
        'resolved': 'resolved',
        'unresolved': 'unresolved',
        None: None
    }

    # Chamar o método do Manager para obter as reclamações
    complaints = current_manager.view_all_issues(
        target=target,
        machine=machine_id,
        type=issue_type,
        status=status_map.get(status)
    )

    return jsonify(complaints)


if __name__ == '__main__':
    app.run(debug=True)
