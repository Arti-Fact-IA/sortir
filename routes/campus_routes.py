from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import Campus, db

campus_bp = Blueprint('campus', __name__, url_prefix='/api/campus')

@campus_bp.route('/', methods=['GET'])
@jwt_required()
def get_campuses():
    """Récupérer tous les campus"""
    campuses = Campus.query.all()
    return jsonify([campus.to_dict() for campus in campuses]), 200

@campus_bp.route('/', methods=['POST'])
@jwt_required()
def create_campus():
    """Créer un campus"""
    data = request.get_json()
    new_campus = Campus(nom=data['nom'], ville=data['ville'])
    db.session.add(new_campus)
    db.session.commit()
    return jsonify(new_campus.to_dict()), 201
