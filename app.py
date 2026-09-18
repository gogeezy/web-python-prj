import logging
import os

import psycopg
from flasgger import Swagger
from flask import Flask, request

from controllers.calculator import calculator_bp
from controllers.welcome import welcome_bp

LOG_FILE = "/var/log/web-python.log"

def create_app():
    app = Flask(__name__)

    logging.basicConfig(
	level=logging.INFO,
	format="%(asctime)s %(levelname)s %(message)s",
    )

    app.register_blueprint(welcome_bp)
    app.register_blueprint(calculator_bp, url_prefix="/calculator")
    Swagger(
        app,
        template={
            "info": {
                "title": "Web Python API",
                "description": "Приветственная страница и калькулятор (сумма)",
                "version": "1.0.0",
            }
        },
    )
    @app.before_request
    def log_request():
        app.logger.info(
            "Request: %s %s from %s",
            request.method,
            request.path,
            request.remote_addr,
        )

    @app.get("/health")
    def health():
        return {"status": "ok", "service": "web-python-prj"}, 200

    @app.get("/db-health")
    def db_health():
        try:
            with psycopg.connect(
                host=os.getenv("DB_HOST", "db"),
                port=os.getenv("DB_PORT", "5432"),
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
            ) as conn, conn.cursor() as cur:
                cur.execute("SELECT 1")
                result = cur.fetchone()

            return {"status": "ok", "database": result[0]}, 200
        except psycopg.Error as error:
            app.logger.error("Database check failed: %s", error)
            return {"status": "error", "database": "unavailable"}, 503

    return app


app = create_app()
app.logger.setLevel("INFO")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
