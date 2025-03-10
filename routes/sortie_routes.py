from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import Sortie, db

sortie_bp = Blueprint('sortie', __name__, url_prefix='/api/sorties')

@sortie_bp.route('/', methods=['GET'])
@jwt_required()
def get_sorties():
    """Récupérer toutes les sorties"""
    sorties = Sortie.query.all()
    return jsonify([sortie.to_dict() for sortie in sorties]), 200

@sortie_bp.route('/<int:sortie_id>', methods=['GET'])
@jwt_required()
def get_sortie(sortie_id):
    """Récupérer une sortie spécifique"""
    sortie = Sortie.query.get_or_404(sortie_id)
    return jsonify(sortie.to_dict()), 200

@sortie_bp.route('/', methods=['POST'])
@jwt_required()
def create_sortie():
    """Créer une nouvelle sortie"""
    data = request.get_json()
    new_sortie = Sortie(
        titre=data['titre'],
        description=data['description'],
        date=data['date'],
        lieu=data['lieu'],
        etat=data['etat'],
        organisateur_id=data['organisateur_id'],
        campus_id=data['campus_id']
    )
    db.session.add(new_sortie)
    db.session.commit()
    return jsonify(new_sortie.to_dict()), 201

@sortie_bp.route('/<int:sortie_id>', methods=['PUT'])
@jwt_required()
def update_sortie(sortie_id):
    """Modifier une sortie"""
    sortie = Sortie.query.get_or_404(sortie_id)
    data = request.get_json()
    sortie.titre = data.get('titre', sortie.titre)
    sortie.description = data.get('description', sortie.description)
    sortie.date = data.get('date', sortie.date)
    sortie.lieu = data.get('lieu', sortie.lieu)
    sortie.etat = data.get('etat', sortie.etat)
    db.session.commit()
    return jsonify(sortie.to_dict()), 200

@sortie_bp.route('/<int:sortie_id>', methods=['DELETE'])
@jwt_required()
def delete_sortie(sortie_id):
    """Supprimer une sortie"""
    sortie = Sortie.query.get_or_404(sortie_id)
    db.session.delete(sortie)
    db.session.commit()
    return jsonify({"message": "Sortie supprimée"}), 200
