"""Flask web application for warehouse management."""
import os
from flask import Flask, render_template
from flask import request, redirect, url_for, flash
from warehouse import Warehouse

app = Flask(__name__)
app.secret_key = os.environ.get(
    'SECRET_KEY', 'dev_secret_key_change_in_production'
)


class WarehouseStore:
    """Storage class for warehouses to avoid global statements."""

    def __init__(self):
        self.warehouses = {}
        self.next_id = 1

    def add(self, name, warehouse):
        """Add a new warehouse and return its ID."""
        warehouse_id = self.next_id
        self.next_id += 1
        self.warehouses[warehouse_id] = {
            'id': warehouse_id,
            'name': name,
            'warehouse': warehouse
        }
        return warehouse_id

    def get(self, warehouse_id):
        """Get warehouse data by ID."""
        return self.warehouses.get(warehouse_id)

    def remove(self, warehouse_id):
        """Remove a warehouse by ID."""
        if warehouse_id in self.warehouses:
            del self.warehouses[warehouse_id]

    def all(self):
        """Get all warehouses."""
        return self.warehouses


store = WarehouseStore()


def get_warehouse_or_redirect(warehouse_id):
    """Get warehouse data or None if not found."""
    warehouse_data = store.get(warehouse_id)
    if warehouse_data is None:
        flash('Warehouse not found', 'error')
    return warehouse_data


def handle_create_post():
    """Handle POST request for creating a warehouse."""
    name = request.form.get('name', '').strip()
    capacity = float(request.form.get('capacity', 0))
    initial_balance = float(request.form.get('initial_balance', 0))

    if not name:
        flash('Warehouse name is required', 'error')
        return redirect(url_for('create'))

    if capacity <= 0:
        flash('Capacity must be greater than 0', 'error')
        return redirect(url_for('create'))

    store.add(name, Warehouse(capacity, initial_balance))
    flash(f'Warehouse "{name}" created successfully', 'success')
    return redirect(url_for('index'))


@app.route('/')
def index():
    """Display list of all warehouses."""
    return render_template('index.html', warehouses=store.all())


@app.route('/create', methods=['GET', 'POST'])
def create():
    """Create a new warehouse."""
    if request.method == 'POST':
        try:
            return handle_create_post()
        except ValueError:
            flash('Invalid capacity or initial balance', 'error')
            return redirect(url_for('create'))

    return render_template('create.html')


@app.route('/edit/<int:warehouse_id>', methods=['GET', 'POST'])
def edit(warehouse_id):
    """Edit an existing warehouse."""
    warehouse_data = get_warehouse_or_redirect(warehouse_id)
    if warehouse_data is None:
        return redirect(url_for('index'))

    if request.method == 'POST':
        return handle_edit_post(warehouse_id, warehouse_data)

    return render_template('edit.html', warehouse_data=warehouse_data)


def handle_edit_post(warehouse_id, warehouse_data):
    """Handle POST request for editing a warehouse."""
    try:
        name = request.form.get('name', '').strip()
        if not name:
            flash('Warehouse name is required', 'error')
            return redirect(url_for('edit', warehouse_id=warehouse_id))

        warehouse_data['name'] = name
        flash(f'Warehouse "{name}" updated successfully', 'success')
        return redirect(url_for('index'))
    except ValueError:
        flash('Invalid input. Please try again', 'error')
        return redirect(url_for('edit', warehouse_id=warehouse_id))


@app.route('/add/<int:warehouse_id>', methods=['GET', 'POST'])
def add_items(warehouse_id):
    """Add items to a warehouse."""
    warehouse_data = get_warehouse_or_redirect(warehouse_id)
    if warehouse_data is None:
        return redirect(url_for('index'))

    if request.method == 'POST':
        return handle_add_post(warehouse_id, warehouse_data)

    return render_template('add.html', warehouse_data=warehouse_data)


def handle_add_post(warehouse_id, warehouse_data):
    """Handle POST request for adding items to a warehouse."""
    try:
        amount = float(request.form.get('amount', 0))
        if amount <= 0:
            flash('Amount must be greater than 0', 'error')
            return redirect(url_for('add_items', warehouse_id=warehouse_id))

        warehouse_data['warehouse'].add_to_warehouse(amount)
        name = warehouse_data["name"]
        flash(f'Added {amount} items to warehouse "{name}"', 'success')
        return redirect(url_for('index'))
    except ValueError:
        flash('Invalid amount. Please enter a valid number', 'error')
        return redirect(url_for('add_items', warehouse_id=warehouse_id))


@app.route('/take/<int:warehouse_id>', methods=['GET', 'POST'])
def take_items(warehouse_id):
    """Remove items from a warehouse."""
    warehouse_data = get_warehouse_or_redirect(warehouse_id)
    if warehouse_data is None:
        return redirect(url_for('index'))

    if request.method == 'POST':
        return handle_take_post(warehouse_id, warehouse_data)

    return render_template('take.html', warehouse_data=warehouse_data)


def handle_take_post(warehouse_id, warehouse_data):
    """Handle POST request for taking items from a warehouse."""
    try:
        amount = float(request.form.get('amount', 0))
        if amount <= 0:
            flash('Amount must be greater than 0', 'error')
            return redirect(url_for('take_items', warehouse_id=warehouse_id))

        taken = warehouse_data['warehouse'].take_from_warehouse(amount)
        name = warehouse_data["name"]
        flash(f'Took {taken} items from warehouse "{name}"', 'success')
        return redirect(url_for('index'))
    except ValueError:
        flash('Invalid amount. Please enter a valid number', 'error')
        return redirect(url_for('take_items', warehouse_id=warehouse_id))


@app.route('/delete/<int:warehouse_id>', methods=['POST'])
def delete(warehouse_id):
    """Delete a warehouse."""
    warehouse_data = store.get(warehouse_id)
    if warehouse_data is None:
        flash('Warehouse not found', 'error')
        return redirect(url_for('index'))

    warehouse_name = warehouse_data['name']
    store.remove(warehouse_id)
    flash(f'Warehouse "{warehouse_name}" deleted successfully', 'success')
    return redirect(url_for('index'))


if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode)
