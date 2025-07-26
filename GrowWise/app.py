import os
import logging
from flask import Flask
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix
from extensions import db  # ← Use db from extensions.py

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("SESSION_SECRET", "default-secret")
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    # DB Config
    database_url = os.environ.get("DATABASE_URL", "sqlite:///growwise.db")
    if "DATABASE_URL" not in os.environ:
        logger.warning("⚠️ No DATABASE_URL found, using SQLite fallback")

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }

    db.init_app(app)
    CORS(app)

    with app.app_context():
        from db_models import Prediction, WeatherQuery, VoiceQuery, MarketPrice
        db.create_all()
        logger.info("✅ Database tables created")

        from routes import main_bp
        app.register_blueprint(main_bp)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
