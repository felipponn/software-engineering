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
        # Obter dados do formulário
        destination = request.form.get('destination')
        complaint_type = request.form.get('complaintType')
        message = request.form.get('message')
        machine_id = None
        if destination == 'machine':
            machine_id = request.form.get('machineNumber')
        
        # Verificar se o usuário está autenticado
        if current_user:
            # Usar o current_user para enviar um relatório
            current_user.report(target=destination, type=complaint_type, machine_id=machine_id, message=message)
            return redirect(url_for('report_success'))
        else:
            return "Usuário não autenticado", 401
    else:
        # Renderizar o formulário de relatório
        return render_template('report.html')
    
@app.route('/report_success')
def report_success():
    return "Relatório enviado com sucesso!"

if __name__ == '__main__':
    app.run(debug=True)