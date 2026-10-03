from flask import Flask

app = Flask(__name__)

# --- FAILLE A10:2025 - Mishandling of Exceptional Conditions ---
# Le mode debug est actif : en cas d'exception non gérée,
# Flask renvoie au client la stack trace complète (code source,
# variables locales, chemins serveur...) au lieu d'un message générique.
# -> CWE-209 (Generation of Error Message Containing Sensitive Information)
# -> CWE-215 (Insertion of Sensitive Information Into Debugging Code)
app.config['DEBUG'] = True

users = {
    "1": "Alice",
    "2": "Bob",
    "3": "Charlie",
}


@app.route('/')
def home():
    return '''
    <h1>Bienvenue sur l'API utilisateurs.</h1>
    <p>Exemple valide : <a href="/user/1">/user/1</a></p>
    <p>Exemple provoquant une erreur : <a href="/user/abc">/user/abc</a></p>
    '''

@app.route('/user/<id>')
def get_user(id):
    # Aucune gestion d'exception :
    # - si <id> n'est pas un nombre -> ValueError
    # - si <id> n'existe pas dans le dictionnaire -> KeyError
    # Les deux cas provoquent une erreur 500 avec la stack trace
    # complète renvoyée au client à cause du mode debug.
    user_id = int(id)
    name = users[str(user_id)]
    return f"Utilisateur trouvé : {name}"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
