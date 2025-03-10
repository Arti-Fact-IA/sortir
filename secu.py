from app import create_app, db
from models import Utilisateur
from werkzeug.security import generate_password_hash

# 🔹 Créer l'application Flask et obtenir le contexte
app = create_app()

with app.app_context():  # ✅ Utilisation correcte du contexte Flask
    utilisateurs = Utilisateur.query.all()
    for user in utilisateurs:
        if not user.mot_de_passe.startswith("pbkdf2:sha256"):  # ⚠️ Vérifie si le mot de passe est déjà hashé
            print(f"🔄 Mise à jour du mot de passe pour {user.email}")
            user.mot_de_passe = generate_password_hash(user.mot_de_passe)
            db.session.commit()
    print("✅ Mots de passe mis à jour avec un hash sécurisé !")
