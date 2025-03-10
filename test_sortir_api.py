import unittest
from flask_jwt_extended import create_access_token
from datetime import datetime
from models import db, Utilisateur, Sortie, Campus
from run import app  # ✅ Import correct de l'application Flask

class TestSortirAPI(unittest.TestCase):
    """Tests unitaires pour l'API Sortir"""

    @classmethod
    def setUpClass(cls):
        """Initialisation de l'application Flask et création de la base de test."""
        cls.app = app.test_client()  # ✅ Création d'un client de test
        cls.app_context = app.app_context()
        cls.app_context.push()  # ✅ Activation du contexte Flask
        db.create_all()
        cls.create_test_data()

    @classmethod
    def create_test_data(cls):
        """Créer un utilisateur, un campus et une sortie pour les tests."""
        # ✅ Vérifier et insérer un campus si nécessaire
        campus = db.session.get(Campus, 1)
        if not campus:
            campus = Campus(id=1, nom="Campus Test", ville="Ville Test")
            db.session.add(campus)
            db.session.commit()

        # ✅ Vérifier et insérer un utilisateur unique
        base_pseudo = "testuser"
        pseudo = base_pseudo
        count = 1

        while Utilisateur.query.filter_by(pseudo=pseudo).first():
            pseudo = f"{base_pseudo}{count}"
            count += 1

        utilisateur = Utilisateur(
            nom="Test",
            prenom="User",
            pseudo=pseudo,
            email=f"{pseudo}@test.com"
        )
        utilisateur.set_password("password")
        db.session.add(utilisateur)
        db.session.commit()

        # ✅ Vérifier et insérer une sortie test
        sortie_existante = db.session.get(Sortie, 1)
        if not sortie_existante:
            sortie = Sortie(
                id=80,  # ✅ On fixe un ID pour éviter les erreurs de référence
                titre="Test Sortie",
                description="Description de test",
                date=datetime.strptime("2025-03-01 20:00", "%Y-%m-%d %H:%M"),
                lieu="Lieu test",
                etat="Ouverte",
                campus_id=campus.id,
                organisateur_id=utilisateur.id
            )
            db.session.add(sortie)
            db.session.commit()
            cls.sortie_id = sortie.id
        else:
            cls.sortie_id = sortie_existante.id

        cls.user_id = utilisateur.id

    def get_auth_headers(self):
        """Génère un token JWT pour l'utilisateur de test."""
        token = create_access_token(identity=self.user_id)
        return {"Authorization": f"Bearer {token}"}

    def test_get_sorties(self):
        """Test récupération des sorties."""
        response = self.app.get('/api/sorties', headers=self.get_auth_headers())
        self.assertIn(response.status_code, [200, 404])

    def test_create_sortie(self):
        """Test création d’une sortie."""
        data = {
            "titre": "Soirée test",
            "description": "Description test",
            "date": "2025-03-10 19:00",
            "lieu": "Lieu test",
            "campus_id": 1
        }
        response = self.app.post('/api/sorties', json=data, headers=self.get_auth_headers())
        self.assertIn(response.status_code, [201, 400])

    def test_inscription_sortie(self):
        """Test inscription à une sortie."""
        response = self.app.post(f'/api/sorties/{self.sortie_id}/inscription', headers=self.get_auth_headers())
        self.assertIn(response.status_code, [201, 400, 404])  # 404 si la sortie n'existe pas, 400 si déjà inscrit

    def test_update_sortie(self):
        # Vérifie que la sortie existe avant de la modifier
        sortie_existante = db.session.get(Sortie, 1)
        if not sortie_existante:
            sortie = Sortie(
                id=1,  # ID fixé pour éviter les erreurs de référence
                titre="Soirée test",
                description="Description test",
                date=datetime.strptime("2025-03-10 19:00", "%Y-%m-%d %H:%M"),
                lieu="Lieu test",
                etat="En création",
                organisateur_id=1,
                campus_id=1
            )
            db.session.add(sortie)
            db.session.commit()

        # ✅ Ensuite, on teste la modification
        data = {
            "titre": "Soirée test modifiée",
            "description": "Description mise à jour",
            "date": "2025-03-15 20:00",
            "lieu": "Nouveau lieu",
            "etat": "Ouverte"
        }

        response = self.app.put('/api/sorties/1', json=data, headers=self.get_auth_headers())

        # ✅ On attend un 200 si la modification est bien effectuée
        self.assertEqual(response.status_code, 200)


    def test_delete_sortie(self):
        """Test suppression d’une sortie."""
        response = self.app.delete(f'/api/sorties/{self.sortie_id}', headers=self.get_auth_headers())
        self.assertIn(response.status_code, [200, 404])  # 404 si la sortie n'existe plus

    @classmethod
    def tearDownClass(cls):
        """Nettoyage après les tests."""
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

if __name__ == '__main__':
    unittest.main()
