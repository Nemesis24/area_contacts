# Area Contacts

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs) 

## Description

L'intégration **Area Contacts** permet de gérer les contacteurs d'ouverture de portes et fenêtres par zone dans Home Assistant. Vous pouvez exclure certains contacteurs de chaque zone et surveiller l'état des contacteurs dans chaque zone.

## Installation

### Via HACS (Home Assistant Community Store)

1. Ajoutez ce dépôt à HACS en tant que dépôt personnalisé.
2. Recherchez "Area Contacts" dans HACS et installez l'intégration.
3. Redémarrez Home Assistant.

### Manuel

1. Téléchargez les fichiers de ce dépôt.
2. Copiez le dossier `area_contacts` dans le répertoire `custom_components` de votre configuration Home Assistant.
3. Redémarrez Home Assistant.

## Configuration

### Via l'interface utilisateur

1. Allez dans `Configuration` > `Intégrations`.
2. Cliquez sur le bouton `+ Ajouter une intégration`.
3. Recherchez "Area Contacts" et suivez les instructions à l'écran pour configurer l'intégration.

### Via YAML

Non supporté.

## Utilisation

### Capteurs

L'intégration crée des capteurs pour chaque zone et un pour toute la maison avec les attributs suivants :

- `count`: Nombre de contacteurs ouverts.
- `total`: Nombre total de contacteurs.
- `count_of`: Nombre de contacteurs ouverts sur le total.
- `contacts_open`: Liste des contacteurs ouverts.
- `contacts_closed`: Liste des contacteurs fermés.
- `excluded_contacts`: Liste des contacteurs exclus.

### Exclusion de contacteurs

Vous pouvez exclure des contacteurs spécifiques de chaque zone via l'interface de configuration de l'intégration.

## Support

Pour toute question ou problème, veuillez utiliser le [suivi des problèmes](https://github.com//Nemesis24/area_contacts/issues).

## Contribuer

Les contributions sont les bienvenues ! Veuillez lire le fichier [CONTRIBUTING.md](https://github.com//Nemesis24/area_contacts/blob/main/CONTRIBUTING.md) pour plus d'informations.

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](https://github.com//Nemesis24/area_contacts/blob/main/LICENSE) pour plus de détails.