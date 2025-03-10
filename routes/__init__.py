from flask import Blueprint

# Importer tous les Blueprints
from .auth_routes import auth_bp
from .campus_routes import campus_bp
from .sortie_routes import sortie_bp
from .utilisateur_routes import utilisateur_bp

# Création d'un Blueprint principal pour tout enregistrer
main_bp = Blueprint("main", __name__)

# Enregistrement des Blueprints dans l'application
main_bp.register_blueprint(auth_bp)
main_bp.register_blueprint(campus_bp)
main_bp.register_blueprint(sortie_bp)
main_bp.register_blueprint(utilisateur_bp)
