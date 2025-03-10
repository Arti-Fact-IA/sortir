import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Initialisation des extensions
db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    """Créer et configurer l'application Flask"""
    app = Flask(__name__)

    # Vérification et configuration de la base de données
    database_url = os.getenv("DATABASE_URL", "postgresql://sortir_user_adm:1793@localhost/sortir_db")
    if not database_url:
        raise RuntimeError("La variable d'environnement DATABASE_URL est manquante !")
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY", "super-secret-key")

    # Initialisation des extensions avec l'application
    db.init_app(app)
    jwt.init_app(app)

    # Importation et enregistrement des routes
    from routes import main_bp
    app.register_blueprint(main_bp)

    return app
