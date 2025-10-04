# Python Backend Project

A well-structured Python backend application using Flask.

## Project Structure

```
.
├── app.py                  # Main application entry point
├── requirements.txt        # Python dependencies
├── .env.example           # Example environment variables
├── .gitignore             # Git ignore file
├── README.md              # This file
├── config/                # Configuration files
│   ├── __init__.py
│   └── config.py          # Application configuration
├── src/                   # Source code
│   ├── __init__.py
│   ├── api/               # API routes
│   │   ├── __init__.py
│   │   └── routes.py      # API endpoints
│   ├── models/            # Data models
│   │   ├── __init__.py
│   │   └── example_model.py
│   ├── services/          # Business logic
│   │   ├── __init__.py
│   │   └── example_service.py
│   └── utils/             # Utility functions
│       ├── __init__.py
│       └── helpers.py
├── static/                # Static files
│   ├── css/              # Stylesheets
│   ├── js/               # JavaScript files
│   └── images/           # Images
├── templates/             # HTML templates
└── tests/                # Test files
    ├── __init__.py
    └── test_api.py

```

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Copy `.env.example` to `.env` and configure your environment variables:
   ```bash
   cp .env.example .env
   ```

5. Run the application:
   ```bash
   python app.py
   ```

## API Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check
- `GET /api/example` - Get all examples
- `POST /api/example` - Create new example
- `GET /api/example/<id>` - Get example by ID

## Testing

Run tests with pytest:
```bash
pytest tests/
```

## Development

The project follows a modular structure:
- **api/**: Contains all API route definitions
- **models/**: Data models and schemas
- **services/**: Business logic layer
- **utils/**: Helper functions and utilities
- **config/**: Configuration management
- **static/**: Static assets (CSS, JS, images)
- **templates/**: HTML templates for rendering

