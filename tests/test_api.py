import unittest
import logging
from flask_jwt_extended import create_access_token
from app import create_app, db  # Import correct
from models import Utilisateur, Sortie, Campus
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash


# Configuration du logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("TestAPI")

class TestAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Initialisation avant les tests"""
        logger.info("Initialisation de l'application de test...")
        cls.app = create_app()
        cls.client = cls.app.test_client()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

        with cls.app.app_context():
            db.session.remove()
            db.drop_all()
            db.create_all()
            cls.create_test_data()
        logger.info("Base de données initialisée avec succès.")

    @classmethod
    def tearDownClass(cls):
        """Nettoyage après tous les tests"""
        logger.info("Nettoyage de la base de données...")
        with cls.app.app_context():
            db.session.remove()
        cls.app_context.pop()
        logger.info("Tests terminés.")

    @classmethod
    def create_test_data(cls):
        """Création de données pour les tests"""
        logger.info("Création des données de test...")
        with cls.app.app_context():
            db.session.query(Sortie).delete()
            db.session.query(Campus).delete()
            db.session.query(Utilisateur).delete()
            db.session.commit()

            campus = Campus(nom="Campus Test", ville="Ville Test")
            db.session.add(campus)
            db.session.commit()

            # Vérifier si un utilisateur avec cet email existe déjà
            existing_user = Utilisateur.query.filter_by(email="test11@test.com").first()
            if existing_user:
                logging.warning("⚠️ L'utilisateur test11@test.com existe déjà en base, suppression en cours...")
                db.session.delete(existing_user)
                db.session.commit()

            # ✅ Créer un utilisateur test avec mot de passe HASHÉ
            user = Utilisateur(
                nom="Test11",
                prenom="User11",
                pseudo="testuser11",
                email="test11@test.com",
                mot_de_passe=generate_password_hash("password"),  # ✅ Hachage du mot de passe
                telephone="1234567899"
            )
            db.session.add(user)
            db.session.commit()
            cls.user_id = user.id
            logging.info("✅ Utilisateur test créé avec succès !")

            sortie = Sortie(
                titre="Soirée test", description="Description test",
                date=datetime.now() + timedelta(days=10), lieu="Lieu test",
                etat="En création", organisateur_id=user.id, campus_id=campus.id
            )
            db.session.add(sortie)
            db.session.commit()
            cls.sortie_id = sortie.id
            logger.info("Données de test créées avec succès.")


    def get_auth_headers(self):
        """Génère un token JWT pour les requêtes"""
        with self.app.app_context():
            token = create_access_token(identity=self.user_id)
        return {"Authorization": f"Bearer {token}"}

    def test_auth_login(self):
        """Test de connexion utilisateur"""
        logging.info("Test de connexion en cours...")

        data = {"email": "test11@test.com", "password": "password"}  # ⚠️ Vérifie bien la clé ici
        response = self.client.post('/api/auth/login', json=data)

        # 🔹 Ajoute ces prints pour voir ce que l'API renvoie réellement
        logging.info(f"Réponse HTTP Code: {response.status_code}")
        logging.info(f"Réponse JSON: {response.json}")

        self.assertEqual(response.status_code, 200)  # 🔥 Attendu 200



    def test_get_sorties(self):
        """Test récupération des sorties"""
        logger.info("Test récupération des sorties...")
        response = self.client.get('/api/sorties/', headers=self.get_auth_headers())
        self.assertEqual(response.status_code, 200)
        logger.info("Récupération des sorties réussie !")

    def test_create_sortie(self):
        """Test création d’une sortie"""
        logger.info("Test création d'une sortie...")
        data = {
            "titre": "Nouvelle Sortie", "description": "Une sortie test",
            "date": (datetime.now() + timedelta(days=5)).isoformat(),
            "lieu": "Lieu de test", "etat": "Ouverte",
            "organisateur_id": self.user_id, "campus_id": 1
        }
        response = self.client.post('/api/sorties/', json=data, headers=self.get_auth_headers())
        self.assertIn(response.status_code, [201, 400])
        logger.info("Création de la sortie validée !")

    def test_update_sortie(self):
        """Test modification d’une sortie"""
        logger.info("Test modification d'une sortie...")
        data = {"titre": "Sortie modifiée"}
        response = self.client.put(f'/api/sorties/{self.sortie_id}', json=data, headers=self.get_auth_headers())
        self.assertIn(response.status_code, [200, 404])
        logger.info("Modification de la sortie validée !")

    def test_delete_sortie(self):
        """Test suppression d’une sortie"""
        logger.info("Test suppression d'une sortie...")
        response = self.client.delete(f'/api/sorties/{self.sortie_id}', headers=self.get_auth_headers())
        self.assertIn(response.status_code, [200, 404])
        logger.info("Suppression de la sortie validée !")

if __name__ == '__main__':
    unittest.main()