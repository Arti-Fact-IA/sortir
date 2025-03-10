from app import db  # ✅ Assure-toi que c'est bien importé ainsi
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ENUM
from werkzeug.security import generate_password_hash, check_password_hash



# ✅ Définition propre des ENUMs
etat_enum = ENUM('En création', 'Ouverte', 'Clôturée', 'Annulée', 'Historisée', name='etat_sortie', create_type=True)
statut_enum = ENUM('Inscrit', 'Désisté', name='statut_participation', create_type=True)

class Utilisateur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    pseudo = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mot_de_passe = db.Column(db.String(255), nullable=False)  # Stocke le hash du mot de passe
    telephone = db.Column(db.String(20), nullable=True)

    @staticmethod
    def hash_password(password):
        """Hash un mot de passe"""
        return generate_password_hash(password)

    def verify_password(self, password):
        """Vérifie un mot de passe hashé"""
        return check_password_hash(self.mot_de_passe, password)

class Campus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    ville = db.Column(db.String(100), nullable=False)

class Sortie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime, nullable=False)
    lieu = db.Column(db.String(255), nullable=False)
    etat = db.Column(db.String(50), nullable=False)
    organisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), nullable=False)
    campus_id = db.Column(db.Integer, db.ForeignKey('campus.id'), nullable=False)

    def to_dict(self):
        """Convertit l'objet SQLAlchemy en dictionnaire pour JSON"""
        return {
            "id": self.id,
            "titre": self.titre,
            "description": self.description,
            "date": self.date.isoformat(),  # Convertir en format lisible
            "lieu": self.lieu,
            "etat": self.etat,
            "organisateur_id": self.organisateur_id,
            "campus_id": self.campus_id
        }


class Participation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), nullable=False)
    sortie_id = db.Column(db.Integer, db.ForeignKey('sortie.id'), nullable=False)
    statut = db.Column(statut_enum, nullable=False)
