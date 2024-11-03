import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_babel import Babel, gettext as _

from backend.user import User
from backend.machine import Machine
from backend.manager import Manager

# Inicializar o aplicativo Flask
app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.secret_key = 'qualquer_coisa_vai_funcionar'

base_dir = os.path.abspath(os.path.dirname(__file__))
translations_path = os.path.join(base_dir, 'translations')
app.config['BABEL_TRANSLATION_DIRECTORIES'] = translations_path
app.config['BABEL_DEFAULT_LOCALE'] = 'pt'

LANGUAGES = {
    'en': 'English',
    'pt': 'Português',
    'es': 'Español'
}

def get_locale():
    language = session.get('language', 'pt')
    print(f"Idioma selecionado: {language}")
    return language

babel = Babel()
babel.init_app(app, locale_selector=get_locale)

@app.context_processor
def inject_get_locale():
    return dict(get_locale=get_locale)

# Função para simular a autenticação
def simulate_authentication(email, password):
    if email == 'fabricio@fabricio.com' and password == '123':
        return User.authenticate(email, password)
    elif email == 'fabricio@gestor.com' and password == '123':
        return Manager.authenticate(email, password)
    else:
        return None
    
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

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        selected_language = request.form.get('language')
        print(f"Língua selecionada no formulário: {selected_language}")
        session['language'] = selected_language
        return redirect(url_for('home'))
    return render_template('settings.html')


@app.route('/set_language', methods=['POST'])
def set_language():
    language = request.form.get('language')
    session['language'] = language
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)