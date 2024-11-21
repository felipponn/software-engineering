import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_babel import Babel, gettext as _

from backend.user import User
from backend.machine import Machine
from backend.manager import Manager
from backend.product import Product

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
    if email == 'fabricio@fabricio.com':
        return User.authenticate(email, password)
    elif email == 'fabricio@gestor.com':
        return Manager.authenticate(email, password)
    else:
        return None

current_user = Manager.authenticate('fabricio@gestor.com', '123')  # Manager
# current_user = User.authenticate('fabricio@fabricio.com', '123')  # Regular user

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
    if request.method == 'GET':
        # Save the previous URL in the session
        session['previous_url'] = request.referrer
        return render_template('settings.html')
    
    if request.method == 'POST':
        selected_language = request.form.get('language')
        session['language'] = selected_language
        # Redirect to the previous URL, if available
        return redirect(session.get('previous_url', url_for('home')))


@app.route('/select_machine')
def select_machine():
    '''
    Route to render the machine selection page.
    '''
    machine_ids = Machine.get_machines()
    return render_template('select_machine.html', machine_ids=machine_ids)

@app.route('/machine_profile/<int:machine_id>')
def machine_profile(machine_id):
    '''
    Route to render the machine profile page.
    '''
    machine = Machine(machine_id=machine_id)
    
    profile, available_products, reviews_info = machine.get_profile()
    
    is_favorite = current_user.is_favorite(machine_id)
    
    return render_template('machine_profile.html', profile=profile, available_products=available_products, reviews_info=reviews_info, is_favorite=is_favorite)

@app.route('/select_product')
def select_product():
    '''
    Route to render the product selection page.
    '''
    product_ids = Product.get_products()
    return render_template('select_product.html', product_ids=product_ids)

@app.route('/product_profile/<int:product_id>')
def product_profile(product_id):
    '''
    Route to render the product profile page.
    '''
    product = Product(product_id=product_id)
    
    profile, available_machines, reviews_info = product.get_profile()
    profile["status"] = "ativo"
    
    # is_favorite = current_user.is_favorite(product_id)
    
    return render_template('product_profile.html', profile=profile, available_machines=available_machines, reviews_info=reviews_info)

@app.route('/toggle_favorite/<int:machine_id>', methods=['POST'])
def toggle_favorite(machine_id):
    '''
    API route to toggle a machine as a favorite.
    '''
    try:
        if current_user.is_favorite(machine_id):
            success = current_user.remove_favorite(machine_id)
            is_favorite = False
            message = 'Máquina removida das favoritas.'
        else:
            success = current_user.add_favorite(machine_id)
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
def manager_stock():
    '''
    Route to render the manager's stock panel.
    Only accessible if the user is a manager.
    '''
    machine_ids = Machine.get_machines()
    product_names = list(Product.get_products().values())
    quantity_categories = ['Critical', 'Low', 'Medium', 'High', 'Full']
    return render_template('stock_manager.html', machine_ids=machine_ids, product_names=product_names, quantity_categories=quantity_categories)

@app.route('/get_stock', methods=['GET'])
def get_stock():
    '''
    API route to fetch stock information based on filters.
    Only accessible if the user is a manager.
    '''
    machine_id = request.args.get('machine_id')
    product_name = request.args.get('product_name')
    quantity_category = request.args.get('quantity_category')

    if machine_id == 'all':
        machine_id = None
    if product_name == 'all':
        product_name = None
    if quantity_category == 'all':
        quantity_category = None

    stock_info = current_user.get_stock(machine_id=machine_id, product_name=product_name, quantity_category=quantity_category)

    return jsonify(stock_info)


if __name__ == '__main__':
    app.run(debug=True)