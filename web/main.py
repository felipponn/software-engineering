import sys
import os
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, g
from datetime import timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask_babel import Babel, gettext as _

from backend.users.regular_user import RegularUserFactory
from backend.machine import Machine
from backend.users.manager import ManagerFactory, Manager
from backend.product import Product

# Initialize the Flask application
app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.secret_key = 'qualquer_coisa_vai_funcionar'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

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
    return dict(get_locale=get_locale, current_user=g.get('current_user', None))

def simulate_authentication(email, password):
    """
    Function to authenticate a user based on their role.
    """
    regular_user_factory = RegularUserFactory()
    manager_factory = ManagerFactory()

    user = regular_user_factory.authenticate(email, password)
    if user and user.role == 'customer':
        return user

    manager = manager_factory.authenticate(email, password)
    if manager and manager.role == 'manager':
        return manager

    return None


def login_required(f):
    """
    Decorator to require authentication for the login.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)

@app.before_request
def load_current_user():
    """
    Loads the current user based on the session data.
    """
    user_id = session.get('user_id')
    regular_user_factory = RegularUserFactory()
    manager_factory = ManagerFactory()
    if user_id:
        role = session.get('role')
        email = session.get('email')
        password = session.get('password')
        
        if role == 'manager':
            user = manager_factory.authenticate(email, password)
        elif role == 'customer':
            user = regular_user_factory.authenticate(email, password)
        else:
            user = None
    
        if user:
            g.current_user = user
        else:
            g.current_user = None
    else:
        g.current_user = None


@app.route('/')
def index():
    '''
    Root route that redirects to login or home based on authentication.
    '''
    if g.current_user:
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Route for user login.
    """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = simulate_authentication(email, password)
        
        if user:
            session['user_id'] = user.user_id
            session['email'] = user.email
            session['role'] = user.role 
            session['password'] = user.password
            return redirect(url_for('home'))
        else:
            error = _("Credenciais inválidas. Tente novamente.")
            return render_template('login.html', error=error)
    return render_template('login.html')


@app.route('/home')
@login_required
def home():
    """
    Rota para a página inicial após login.
    """
    return render_template('home.html')

@app.route('/report_menu')
@login_required
def report_menu():
    """
    Route for the report menu page after login.
    """
    is_manager = g.current_user.role == 'manager'
    return render_template('report_menu.html')

@app.route('/report', methods=['GET', 'POST'])
@login_required
def report():
    """
    Route for sending complaints.
    """
    machine_ids = Machine.get_machines()
    
    if request.method == 'POST':
        # Collects form data
        destination = request.form.get('destination')
        complaint_type = request.form.get('complaintType')
        message = request.form.get('message')
        machine_id = None
        if destination == 'machine':
            machine_id = request.form.get('machineNumber')
        
        # Registers the complaint if the user is authenticated
        if g.current_user:
            g.current_user.report(target=destination, type=complaint_type, machine_id=machine_id, message=message)
            return render_template('report.html', success=True, machine_ids=machine_ids)
        else:
            return render_template('report.html', error=_("Usuário não autenticado"), machine_ids=machine_ids)
    
    return render_template('report.html', machine_ids=machine_ids)

@app.route('/manager_dashboard')
@login_required
def manager_dashboard():
    """
    Route for rendering the manager's dashboard.
    Only accessible if the user is a manager.
    """
    if not isinstance(g.current_user, Manager):
        return redirect(url_for('home'))
    machine_ids = Machine.get_machines()
    return render_template('report_manager.html', machine_ids=machine_ids)

@app.route('/get_complaints', methods=['GET'])
@login_required
def get_complaints():
    """
    API to search complaints based on filters.
    Only accessible if the user is a manager.
    """
    if not isinstance(g.current_user, Manager):
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

    complaints = g.current_user.view_all_issues(
        issue=issue,
        machine=machine_id,
        type=issue_type,
        status=status_map.get(status)
    )

    return jsonify(complaints)

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    """
    Route to change the system language.
    """
    if request.method == 'GET':
        # Saves the previous URL in the session
        session['previous_url'] = request.referrer
        return render_template('settings.html')
    
    if request.method == 'POST':
        selected_language = request.form.get('language')
        session['language'] = selected_language
        # Redirects to the previous URL, if available
        return redirect(session.get('previous_url', url_for('home')))

@app.route('/select_machine')
@login_required
def select_machine():
    """
    Route to render the machine selection page.
    """
    machine_ids = Machine.get_machines()
    return render_template('select_machine.html', machine_ids=machine_ids)

@app.route('/machine_profile/<int:machine_id>')
@login_required
def machine_profile(machine_id):
    """
    Route to render the machine profile page.
    """
    machine = Machine(machine_id=machine_id)
    
    profile, available_products, reviews_info = machine.get_profile()
    
    is_favorite = g.current_user.is_favorite(machine_id)
    
    return render_template('machine_profile.html', profile=profile, available_products=available_products, reviews_info=reviews_info, is_favorite=is_favorite)

@app.route('/select_product')
@login_required
def select_product():
    """
    Route to render the product selection page.
    """
    product_ids = Product.get_products()
    return render_template('select_product.html', product_ids=product_ids)

@app.route('/product_profile/<int:product_id>')
@login_required
def product_profile(product_id):
    """
    Route to render the product profile page.
    """
    product = Product(product_id=product_id)
    
    profile, available_machines, reviews_info = product.get_profile()
    
    return render_template('product_profile.html', profile=profile, available_machines=available_machines, reviews_info=reviews_info)

@app.route('/toggle_favorite/<int:machine_id>', methods=['POST'])
@login_required
def toggle_favorite(machine_id):
    """
    API to toggle a machine as a favorite.
    """
    try:
        if g.current_user.is_favorite(machine_id):
            success = g.current_user.remove_favorite(machine_id)
            is_favorite = False
            message = 'Máquina removida das favoritas.'
        else:
            success = g.current_user.add_favorite(machine_id)
            is_favorite = True
            message = 'Máquina adicionada às favoritas.'
        
        if success:
            return jsonify({'success': True, 'is_favorite': is_favorite, 'message': message}), 200
        else:
            return jsonify({'success': False, 'message': 'Operação falhou.'}), 400
    except Exception as e:
        print(f"Erro no toggle_favorite: {e}")
        return jsonify({'success': False, 'message': 'Ocorreu um erro no servidor.'}), 500

@app.route('/manager_stock')
@login_required
def manager_stock():
    """
    Route to render the manager's stock dashboard.
    Only accessible if the user is a manager.
    """
    machine_ids = Machine.get_machines()
    product_names = [name for id, name in Product.get_products()]
    quantity_categories = ['Critical', 'Low', 'Medium', 'High', 'Full']
    return render_template('stock_manager.html', machine_ids=machine_ids, product_names=product_names, quantity_categories=quantity_categories)

@app.route('/get_stock', methods=['GET'])
@login_required
def get_stock():
    """
    API to search stock information based on filters.
    Only accessible if the user is a manager.
    """
    machine_id = request.args.get('machine_id')
    product_name = request.args.get('product_name')
    quantity_category = request.args.get('quantity_category')

    if machine_id == 'all':
        machine_id = None
    if product_name == 'all':
        product_name = None
    if quantity_category == 'all':
        quantity_category = None

    stock_info = g.current_user.get_stock(machine_id=machine_id, product_name=product_name, quantity_category=quantity_category)

    return jsonify(stock_info)

if __name__ == '__main__':
    app.run(debug=True)