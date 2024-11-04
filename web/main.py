import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from decimal import Decimal
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_babel import Babel, gettext as _

from backend.user import User
from backend.machine import Machine
from backend.manager import Manager

# Initialize the Flask application
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
    '''
    Function to get the language selected by the user.
    '''
    language = session.get('language', 'pt')
    return language

babel = Babel()
babel.init_app(app, locale_selector=get_locale)

@app.context_processor
def inject_get_locale():
    return dict(get_locale=get_locale)

def simulate_authentication(email, password):
    '''
    Function to simulate authentication.
    '''
    if email == 'fabricio@fabricio.com' and password == '123':
        return User.authenticate(email, password)
    elif email == 'fabricio@gestor.com' and password == '123':
        return Manager.authenticate(email, password)
    else:
        return None

current_user = simulate_authentication('fabricio@gestor.com', '123')  # Manager
# current_user = simulate_authentication('fabricio@fabricio.com', '123')  # Regular user

@app.route('/')
def home():
    '''
    Route for the home page that allows navigation between screens.
    The manager dashboard option only appears if the user is a manager.
    '''
    is_manager = isinstance(current_user, Manager)
    return render_template('home.html', is_manager=is_manager)

@app.route('/report', methods=['GET', 'POST'])
def report():
    '''
    Route for submitting complaints.
    '''
    machine_ids = Machine.get_machines()
    
    if request.method == 'POST':
        # Collect form data for the complaint
        destination = request.form.get('destination')
        complaint_type = request.form.get('complaintType')
        message = request.form.get('message')
        machine_id = None
        if destination == 'machine':
            machine_id = request.form.get('machineNumber')
        
        # Register the complaint if the user is authenticated
        if current_user:
            current_user.report(target=destination, type=complaint_type, machine_id=machine_id, message=message)
            return render_template('report.html', success=True, machine_ids=machine_ids)
        else:
            return render_template('report.html', error="Usuário não autenticado", machine_ids=machine_ids)
    
    return render_template('report.html', machine_ids=machine_ids)

@app.route('/manager_dashboard')
def manager_dashboard():
    '''
    Route to render the manager dashboard.
    Only accessible if the user is a manager.
    '''
    if not isinstance(current_user, Manager):
        return redirect(url_for('home'))
    machine_ids = Machine.get_machines()
    return render_template('report_manager.html', machine_ids=machine_ids)

@app.route('/get_complaints', methods=['GET'])
def get_complaints():
    '''
    API route to fetch complaints based on filters.
    Only accessible if the user is a manager.
    '''
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
    '''
    Route to change the system language.
    '''
    if request.method == 'POST':
        selected_language = request.form.get('language')
        print(f"Língua selecionada no formulário: {selected_language}")
        session['language'] = selected_language
        return redirect(url_for('home'))
    return render_template('settings.html')


@app.route('/set_language', methods=['POST'])
def set_language():
    '''
    Route to change the system language.
    '''
    language = request.form.get('language')
    session['language'] = language
    return redirect(url_for('home'))

@app.route('/select_machine')
def select_machine():
    machine_ids = Machine.get_machines()
    print(machine_ids)
    return render_template('select_machine.html', machine_ids=machine_ids)

@app.route('/machine_profile/<int:machine_id>')
def machine_profile(machine_id):
    machine = Machine(machine_id=machine_id)
    
    profile, available_products, reviews_info = machine.get_profile()
    
    profile = {
        'machine_id': profile[0],
        'location': profile[1],
        'status': profile[2],
        'last_maintenance': profile[3].strftime('%Y-%m-%d') if profile[3] else 'N/A',
        'installation_date': profile[4].strftime('%Y-%m-%d') if profile[4] else 'N/A'
    }
    
    available_products = [{'name': p[0], 'price': f"{p[1]:.2f}"} for p in available_products]
    
    return render_template('machine_profile.html', profile=profile, available_products=available_products, reviews_info=reviews_info)

if __name__ == '__main__':
    app.run(debug=True)