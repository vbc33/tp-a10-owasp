from flask import Flask
import logging

app = Flask(__name__)

# --- CORRECTION A10:2025 ---
# Mode debug désactivé : aucune information technique (stack trace,
# code source, chemins serveur) n'est jamais renvoyée au client.
app.config['DEBUG'] = False

# Les erreurs détaillées sont journalisées côté serveur uniquement,
# jamais exposées au client.
logging.basicConfig(filename='app.log', level=logging.ERROR)

users = {
    "1": "Alice",
    "2": "Bob",
    "3": "Charlie",
}


@app.route('/')
def home():
    return '''
    <h1>Bienvenue sur l'API utilisateurs</h1>
    <p>Exemple valide : <a href="/user/1">/user/1</a></p>
    <p>Exemple provoquant une erreur : <a href="/user/abc">/user/abc</a></p>
    '''


@app.route('/user/<id>')
def get_user(id):
    try:
        user_id = int(id)
        name = users[str(user_id)]
        return f"Utilisateur trouvé : {name}"
    except (ValueError, KeyError) as e:
        # Exception gérée explicitement :
        # - message générique et sans détail technique renvoyé au client
        # - détail complet de l'erreur loggé côté serveur pour le débogage
        app.logger.error(f"Erreur lors de la récupération de l'utilisateur '{id}': {e}")
        return "Utilisateur introuvable.", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
