# Procédure — A10:2025 Mishandling of Exceptional Conditions

## 1. Contexte

Vulnérabilité traitée : **A10:2025 – Mishandling of Exceptional Conditions**
(CWE-209 / CWE-215 : exposition d'informations sensibles via des messages
d'erreur détaillés).

Le site de test est une petite API Flask avec une route `/user/<id>` :
si l'identifiant fourni n'est pas valide, l'application lève une exception
non gérée. En mode debug, Flask renvoie alors au client la stack trace
complète (code source, variables, chemin serveur).

Outil de détection : **OWASP ZAP** (scan passif, mode baseline).

## 2. Prérequis

- Docker et Docker Compose installés (`docker --version`,
  `docker compose version`)

- Création du dossier `rapports` dans le dossier du projet

```bash
mkdir -p rapports
chmod 777 rapports
```

## 3. Étape "AVANT" — détecter la faille

Depuis le dossier du projet :

```bash
docker compose -f docker-compose.vulnerable.yml up --build
```

Cela lance :
- le site vulnérable sur `http://localhost:5000`
- un scan ZAP baseline automatique contre ce site

Une fois le scan terminé, ouvrez le rapport généré :

```
rapports/rapport_avant.html
```

**Vérification manuelle complémentaire** (pour la capture d'écran) :
dans un navigateur, ouvrez `http://localhost:5000/user/abc`
→ la stack trace complète de Flask s'affiche directement dans le navigateur.

Dans le rapport ZAP, repérer l'alerte de type 
**"Application ErrorDisclosure"**.

📸 Capture 1 "capture/stacktrace.avant.png" : capture de la page `/user/abc` affichant la stack trace.
📸 Capture 2 "capture/rapport.avant.png : rapport ZAP montrant l'alerte.


## 4. Étape correction

La version corrigée (`app-corrige/app.py`) :
- désactive le mode debug (`app.config['DEBUG'] = False`)
- entoure le code sensible d'un `try/except`
- renvoie un message générique au client (`"Utilisateur introuvable."`, 404)
- journalise le détail de l'erreur côté serveur uniquement (`app.log`)

## 5. Étape "APRÈS" — vérifier la correction

Arrêter l'environnement précédent puis lancer la version corrigée :

```bash
docker compose -f docker-compose.vulnerable.yml down
docker compose -f docker-compose.corrige.yml up --build
```

Ouvrir le nouveau rapport :

```
rapports/rapport_apres.html
```

Vérifier dans le navigateur que `http://localhost:5000/user/abc` renvoie
désormais un message générique ("Utilisateur introuvable.") sans aucune
information technique.

📸 Capture 3 "message_generique.apres.png" :  capture de la page `/user/abc` affichant le message générique.
📸 Capture 4 "rapport.apres.png" : rapport ZAP ne montrant plus l'alerte.

## 6. Nettoyage

```bash
docker compose -f docker-compose.corrige.yml down
```

## 7. Résumé

|         Élément                   |             Avant correction             |          Après correction           |
----------------------------------------------------------------------------------------------------------------------
| Mode debug                        |                Activé                    |             Désactivé               |
| Gestion des exceptions            |               Aucune                     |       `try/except` explicite        |
| Réponse au client en cas d'erreur |          Stack trace complète            |    Message générique + code 404     |
| Détail de l'erreur                |        Visible par l'utilisateur         |    Loggé côté serveur uniquement    |
| Alerte ZAP                        |              Présente                    |               Absente               |
