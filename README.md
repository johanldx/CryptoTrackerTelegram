# CryptoTrackerTelegram

## 📖 Description
**CryptoTrackerTelegram** est un bot Telegram de suivi de transactions en cryptomonnaies avec un système d'enregistrement des transactions dans la conversation.

## 🚀 Fonctionnalités
- Enregistrement de transations en BTC, ETH, LTC
- Afficher les informations d'une transaction suivie
- Contactez les créateurs
- Supprimez toutes les données stockées sur le serveur du bot

## 📷 Captures d'écran
*À venir...*

## ⚙️ Installation
Afin d'exécuter le bot sur votre propre machine, vous devez disposer d'au moins Python 3.10. Ensuite, vous devez créer un environnement virtuel et installer les dépendances répertoriées dans le fichier ```requirements.txt```. Ensuite, il suffit de cloner le dépôt GitHub et d'exécuter le fichier ```main.py```.

## 🔧 Configuration
Afin de pouvoir lancer le bot sur votre machine, vous devez d'abord configurer les clés d'API et les identifiants des administrateurs du bot.
Les API utilisés sont Blockcypher pour le suivi des transaction et Telegram pour l'envoie des messages.
- ```ADMINISTRATORS = ['ADMINISTRATOR_ID', 'ADMINISTRATOR_ID']```, à la ligne 9
- ```API_KEY = 'BLOCKCYPHER_API_KEY'```, à la ligne 10
- ```bot = telebot.TeleBot(token='TELEGRAM_BOT_TOKEN', parse_mode=None)```, à la ligne 18

## 💡 Utilisation
L'utilisation est très simple. Il existe une seule commande qui permet de faire apparaître le menu pour générer l'ensemble du bot. Il suffit ensuite de suivre les instructions.
> /start

## 🤝 Contribution
Nous sommes ravis de recevoir des contributions pour améliorer CryptoTrackerTelegram ! Voici comment vous pouvez contribuer :
- Forker le projet depuis le repository GitHub.
- Effectuer les modifications ou les améliorations souhaitées.
- Soumettre une pull request pour proposer vos modifications.

Nous apprécions les rapports de bugs, les suggestions d'amélioration, les nouvelles fonctionnalités et les corrections de code. Rejoignez-nous pour rendre CryptoTrackerTelegram encore meilleur !
