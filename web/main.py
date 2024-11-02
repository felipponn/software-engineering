import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, render_template, request, jsonify, redirect, url_for
from backend.user import User
from backend.machine import Machine
from backend.manager import Manager

# Inicializar o aplicativo Flask
app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

# Função para simular a autenticação
def simulate_authentication(email, password):
    if email == 'fabricio@fabricio.com' and password == '123':
        return User.authenticate(email, password)
    elif email == 'fabricio@gestor.com' and password == '123':
        return Manager.authenticate(email, password)
    else:
        return None
    
    # user_id SERIAL PRIMARY KEY,  -- Automatically generates a sequential integer ID
    # name VARCHAR(255) NOT NULL,
    # email VARCHAR(255) UNIQUE NOT NULL,
    # phone_number VARCHAR(15),
    # password VARCHAR(255),
    # role VARCHAR(50) DEFAULT 'customer',  -- Can be 'customer', 'admin', etc.
    # created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    
#simular criação de usuário
# user = User(email='fabricio@fabricio.com', password='123', user_name='Fabricio', phone='1234567890')
# user.save_db()

# gestor = Manager(email='fabricio@gestor.com', password='123', user_name='Fabricio', phone='1234567890')
# gestor.save_db()

# Simular a autenticação do usuário (altere o email para testar diferentes usuários)
current_user = simulate_authentication('fabricio@gestor.com', '123')  # Gerente
# current_user = simulate_authentication('fabricio@fabricio.com', '123')  # Usuário comum

@app.route('/')
def home():
    """
    Rota para a página inicial que permite navegar entre as telas.
    A opção do painel do gestor só aparece se o usuário for um gerente.
    """
    is_manager = isinstance(current_user, Manager)
    return render_template('home.html', is_manager=is_manager)

@app.route('/report', methods=['GET', 'POST'])
def report():
    """
    Rota para submissão de reclamações.
    """
    machine_ids = Machine.get_machines()
    
    if request.method == 'POST':
        # Coletar dados do formulário para a reclamação
        destination = request.form.get('destination')
        complaint_type = request.form.get('complaintType')
        message = request.form.get('message')
        machine_id = None
        if destination == 'machine':
            machine_id = request.form.get('machineNumber')
        
        # Registrar a reclamação se o usuário estiver autenticado
        if current_user:
            current_user.report(target=destination, type=complaint_type, machine_id=machine_id, message=message)
            return render_template('report.html', success=True, machine_ids=machine_ids)
        else:
            return render_template('report.html', error="Usuário não autenticado", machine_ids=machine_ids)
    
    return render_template('report.html', machine_ids=machine_ids)

@app.route('/manager_dashboard')
def manager_dashboard():
    """
    Rota para renderizar o painel do gestor.
    Só acessível se o usuário for um gerente.
    """
    if not isinstance(current_user, Manager):
        return redirect(url_for('home'))
    machine_ids = Machine.get_machines()
    return render_template('report_manager.html', machine_ids=machine_ids)

@app.route('/get_complaints', methods=['GET'])
def get_complaints():
    """
    Rota de API para buscar reclamações com base em filtros.
    Só acessível se o usuário for um gerente.
    """
    if not isinstance(current_user, Manager):
        return jsonify({'error': 'Não autorizado'}), 403
    
    issue = request.args.get('target')
    machine_id = request.args.get('machine_id')
    issue_type = request.args.get('issue_type')
    status = request.args.get('status')

    status_map = {
        'resolved': 'resolved',
        'unresolved': 'unresolved',
        None: None
    }

    complaints = current_user.view_all_issues(
        issue=issue,
        machine=machine_id,
        type=issue_type,
        status=status_map.get(status)
    )

    return jsonify(complaints)

if __name__ == '__main__':
    # Executar o aplicativo Flask em modo de depuração
    app.run(debug=True)