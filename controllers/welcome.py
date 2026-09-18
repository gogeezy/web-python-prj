from flask import Blueprint

welcome_bp = Blueprint("welcome", __name__)


@welcome_bp.route("/")
def index():
    """Приветственная страница
    ---
    responses:
      200:
        description: HTML-страница с приветствием
    """
    return """
    <!DOCTYPE html>
    <html>
    <head><meta charset="utf-8"><title>Главная</title></head>
    <body>
        <h1>Добро пожаловать</h1>
    </body>
    </html>
    """
