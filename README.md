# ohtuvarasto

[![GHA workflow badge](https://github.com/hydropony/ohtuvarasto/actions/workflows/main.yml/badge.svg)](https://github.com/hydropony/ohtuvarasto/actions)
[![codecov](https://codecov.io/github/hydropony/ohtuvarasto/graph/badge.svg?token=S3HECRX47U)](https://codecov.io/github/hydropony/ohtuvarasto)

## Warehouse Management Web Interface

A Flask-based web application for managing multiple warehouses.

### Features

- **Create warehouses** with custom capacity and initial balance
- **View all warehouses** in a table with real-time status indicators
- **Edit warehouse** names
- **Add items** to warehouses (with automatic capacity limiting)
- **Remove items** from warehouses
- **Delete warehouses** with confirmation
- **Flash messages** for user feedback
- **Responsive design** with modern CSS styling

### Running the Web Interface

1. Install dependencies:
```bash
poetry install
```

2. Run the Flask application:
```bash
cd src
FLASK_APP=app.py poetry run flask run
```

3. Open your browser and navigate to `http://127.0.0.1:5000`

### Environment Variables

- `SECRET_KEY`: Flask secret key for session management (defaults to development key)
- `FLASK_DEBUG`: Set to `true` to enable debug mode (defaults to `false`)