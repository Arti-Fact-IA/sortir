from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import Utilisateur, db

utilisateur_bp = Blueprint('utilisateur', __name__, url_prefix='/api/utilisateurs')

@utilisateur_bp.route('/', methods=['GET'])
@jwt_required()
def get_utilisateurs():
    """Récupérer tous les utilisateurs"""
    utilisateurs = Utilisateur.query.all()
    return jsonify([utilisateur.to_dict() for utilisateur in utilisateurs]), 200

@utilisateur_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_utilisateur(user_id):
    """Récupérer un utilisateur spécifique"""
    utilisateur = Utilisateur.query.get_or_404(user_id)
    return jsonify(utilisateur.to_dict()), 200

@utilisateur_bp.route('/', methods=['POST'])
def create_utilisateur():
    """Créer un nouvel utilisateur"""
    data = request.get_json()
    new_user = Utilisateur(
        nom=data['nom'],
        prenom=data['prenom'],
        pseudo=data['pseudo'],
        email=data['email'],
        mot_de_passe=data['mot_de_passe'],  # ⚠️ Doit être hashé en prod
        telephone=data['telephone']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 201

@utilisateur_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_utilisateur(user_id):
    """Supprimer un utilisateur"""
    utilisateur = Utilisateur.query.get_or_404(user_id)
    db.session.delete(utilisateur)
    db.session.commit()
    return jsonify({"message": "Utilisateur supprimé"}), 200
