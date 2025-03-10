from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from app import db
from models import Utilisateur

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    """Authentification de l'utilisateur"""
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"msg": "❌ Email et mot de passe requis"}), 400

    # 🔹 Vérifier si l'utilisateur existe
    user = db.session.query(Utilisateur).filter_by(email=email).first()

    if not user or not user.verify_password(password):
        return jsonify({"msg": "❌ Identifiants incorrects"}), 401


    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token), 200
