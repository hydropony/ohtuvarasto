"""Flask web application for warehouse management."""
from flask import Flask, render_template, request, redirect, url_for, flash
from varasto import Warehouse

app = Flask(__name__)
app.secret_key = 'dev_secret_key_change_in_production'

# In-memory storage for warehouses (dictionary with ID as key)
warehouses = {}
next_id = 1


@app.route('/')
def index():
    """Display list of all warehouses."""
    return render_template('index.html', warehouses=warehouses)


@app.route('/create', methods=['GET', 'POST'])
def create():
    """Create a new warehouse."""
    if request.method == 'POST':
        try:
            name = request.form.get('name', '').strip()
            capacity = float(request.form.get('capacity', 0))
            initial_balance = float(request.form.get('initial_balance', 0))
            
            if not name:
                flash('Warehouse name is required', 'error')
                return redirect(url_for('create'))
            
            if capacity <= 0:
                flash('Capacity must be greater than 0', 'error')
                return redirect(url_for('create'))
            
            # Create new warehouse
            global next_id
            warehouse_id = next_id
            next_id += 1
            
            warehouses[warehouse_id] = {
                'id': warehouse_id,
                'name': name,
                'warehouse': Warehouse(capacity, initial_balance)
            }
            
            flash(f'Warehouse "{name}" created successfully', 'success')
            return redirect(url_for('index'))
        except ValueError:
            flash('Invalid capacity or initial balance. Please enter valid numbers', 'error')
            return redirect(url_for('create'))
    
    return render_template('create.html')


@app.route('/edit/<int:warehouse_id>', methods=['GET', 'POST'])
def edit(warehouse_id):
    """Edit an existing warehouse."""
    if warehouse_id not in warehouses:
        flash('Warehouse not found', 'error')
        return redirect(url_for('index'))
    
    warehouse_data = warehouses[warehouse_id]
    
    if request.method == 'POST':
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
    
    return render_template('edit.html', warehouse_data=warehouse_data)


@app.route('/add/<int:warehouse_id>', methods=['GET', 'POST'])
def add_items(warehouse_id):
    """Add items to a warehouse."""
    if warehouse_id not in warehouses:
        flash('Warehouse not found', 'error')
        return redirect(url_for('index'))
    
    warehouse_data = warehouses[warehouse_id]
    
    if request.method == 'POST':
        try:
            amount = float(request.form.get('amount', 0))
            
            if amount <= 0:
                flash('Amount must be greater than 0', 'error')
                return redirect(url_for('add_items', warehouse_id=warehouse_id))
            
            warehouse_data['warehouse'].add_to_warehouse(amount)
            flash(f'Added {amount} items to warehouse "{warehouse_data["name"]}"', 'success')
            return redirect(url_for('index'))
        except ValueError:
            flash('Invalid amount. Please enter a valid number', 'error')
            return redirect(url_for('add_items', warehouse_id=warehouse_id))
    
    return render_template('add.html', warehouse_data=warehouse_data)


@app.route('/take/<int:warehouse_id>', methods=['GET', 'POST'])
def take_items(warehouse_id):
    """Remove items from a warehouse."""
    if warehouse_id not in warehouses:
        flash('Warehouse not found', 'error')
        return redirect(url_for('index'))
    
    warehouse_data = warehouses[warehouse_id]
    
    if request.method == 'POST':
        try:
            amount = float(request.form.get('amount', 0))
            
            if amount <= 0:
                flash('Amount must be greater than 0', 'error')
                return redirect(url_for('take_items', warehouse_id=warehouse_id))
            
            taken = warehouse_data['warehouse'].take_from_warehouse(amount)
            flash(f'Took {taken} items from warehouse "{warehouse_data["name"]}"', 'success')
            return redirect(url_for('index'))
        except ValueError:
            flash('Invalid amount. Please enter a valid number', 'error')
            return redirect(url_for('take_items', warehouse_id=warehouse_id))
    
    return render_template('take.html', warehouse_data=warehouse_data)


@app.route('/delete/<int:warehouse_id>', methods=['POST'])
def delete(warehouse_id):
    """Delete a warehouse."""
    if warehouse_id not in warehouses:
        flash('Warehouse not found', 'error')
        return redirect(url_for('index'))
    
    warehouse_name = warehouses[warehouse_id]['name']
    del warehouses[warehouse_id]
    flash(f'Warehouse "{warehouse_name}" deleted successfully', 'success')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
