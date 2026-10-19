# OSS Evidence Atlas

[English](README.en.md) · [Español](README.es.md)

**Relier chaque chantier à un livrable et à ses preuves ; distinguer visibilité, déclarations de dépendances et adoption.**

L’atlas présente douze nouveaux outils métier et son propre moteur de preuves : **treize projets, vingt-six chantiers**, avec plusieurs capacités distinctes dans les dépôts partagés. Il conserve les versions, empreintes, reçus de rejeu et limites. Une preuve manquante reste visible ; une inspection seule ne devient pas une amélioration.

## Essayer

Python 3.11+ ; la galerie utilise un registre enregistré, sans clé et sans rafraîchissement réseau automatique.

```sh
git clone https://github.com/gbesse/oss-evidence-atlas
cd oss-evidence-atlas
python3 -m evidence_atlas serve --lang fr
```

Ouvrir `http://127.0.0.1:8775/?lang=fr`. Parcourir les projets et leur version, filtrer par portefeuille, retirer une preuve en simulation, inspecter une déclaration de dépendance et faire évoluer un contrat de fraîcheur synthétique. Les résultats de couverture et de fraîcheur sont recalculés par le moteur, pas dessinés à l’avance.

```sh
python3 -m evidence_atlas demo
```

`pip install .` fournit aussi `evidence-atlas`. Interface, erreurs, fiches et documentation FR/EN/ES. Les noms de projets, identifiants et données citées restent inchangés.

![Galerie](docs/preview-fr.png)

## Trois preuves différentes

**Capacité reproduite.** Chaque outil métier possède un commit Git épinglé, les liens de sa CI et trois reçus frais : démonstration avec assertions de résultat, suite unitaire sans tests ignorés et parcours navigateur. Les douze démonstrations, douze suites et douze navigateurs ont été réellement rejoués. Le code SQL doit trouver son contre-exemple et retourner 1 : ce statut attendu ne devient pas une erreur arbitrairement ignorée. Les tests de chaque capacité restent dans son dépôt ; un smoke test ne prouve pas toutes les propriétés d’un produit.

Les six chantiers transversaux concernent ce même atlas : couverture exhaustive, galerie exécutable, déclarations de dépendances, rejeu enregistré, fraîcheur et accès anonyme. Ses reçus sont liés à l’empreinte SHA-256 des fichiers Python/JS/HTML/CSS du paquet, **pas à un faux commit autoréférentiel**. Modifier ces fichiers invalide les reçus intégrés ; la CI de sa propre version complète cette auto-évaluation. Le registre et les reçus sont des observations locales, pas des attestations indépendantes signées.

**Déclaration de dépendance.** Le collecteur lit `package.json` ou les dépendances PEP 621 de `pyproject.toml`, épingle d’abord le commit, conserve le chemin, l’empreinte et la version déclarée, puis distingue portée runtime/développement/optionnelle/peer, même propriétaire GitHub et fork. Il déduplique les mêmes observations. Une plage de versions n’est pas une version résolue. Alias, transitivité, fichiers dynamiques et installation réelle ne sont pas inférés.

Le registre montre un essai réel de cette méthode : `carlaiau/read-with-jev` déclare `@typesafe-ai/sdk` en version `0.6.0` dans un manifeste public épinglé. **Cela ne prouve pas l’adoption des projets gbesse**, ni le nombre de personnes utilisant le lecteur. Le champ `private` d’un manifeste npm ne signifie pas que son dépôt GitHub est privé. Les projets gbesse n’ont ici aucune preuve d’adoption humaine établie. Différents propriétaires GitHub ne prouvent pas des organisations indépendantes ; l’absence de déclaration collectée ne prouve pas l’absence d’usage.

```sh
pip install .
python3 -m evidence_atlas collect carlaiau/read-with-jev package.json npm @typesafe-ai/sdk typesafe-ai
```

**Fraîcheur et accès.** Un contrat de fraîcheur lie l’empreinte d’une source à un dépôt, un commit et un contrôle de reproduction. Source modifiée → revue requise, même si le reproducteur passe. Source identique + échec → reproduction échouée. Aucun reçu → aucun rejeu revendiqué. Un reçu d’une autre révision est refusé. Les observations sur les sources publiées sont réelles ; les deux interrupteurs de la démo manipulent un exemple synthétique et ne prétendent pas qu’un amont a changé.

```sh
python3 -m evidence_atlas freshness contrat.json source-locale receipt.json
python3 -m evidence_atlas audit fiche.json
```

L’audit anonyme télécharge le fichier source au commit et la roue de version **sans authentification**, puis compare les deux SHA-256 attendus. Les douze roues métier et leurs sources ont été vérifiées ainsi. La propre roue de l’atlas doit être auditée après sa publication ; elle n’est pas comptée dans les douze observations intégrées. Réseau explicite uniquement, TLS vérifié, hôtes GitHub autorisés, timeout et limites de taille. Aucune clé GitHub ou Jev n’est nécessaire.

## Rejouer un outil

Exporter une fiche de `cards` du registre dans `fiche.json`, préparer son checkout au commit indiqué et installer ses dépendances. Le même environnement Python doit fournir les dépendances du projet ; pour le navigateur, installer aussi ses paquets npm et Chromium.

```sh
python3 -m evidence_atlas replay fiche.json /chemin/checkout demo
python3 -m evidence_atlas replay fiche.json /chemin/checkout unit
python3 -m evidence_atlas replay fiche.json /chemin/checkout browser
```

Le moteur vérifie commit, remote et arbre propre, puis exécute **uniquement la commande codée dans son registre**. Il n’exécute aucune commande shell issue d’un document, README ou manifeste. Les identifiants de fournisseurs et secrets de l’environnement ne sont pas transmis. Les douze démos utilisent des données synthétiques et ne pilotent aucun système réel. Limite de 120 secondes par contrôle ; sorties hachées, pas réinterprétées comme instructions.

## Sources, comparaisons et limites

[GitHub construit déjà un graphe de dépendances à partir des manifestes](https://docs.github.com/en/code-security/concepts/supply-chain-security/supply-chain-security). Cet atlas ne le remplace pas : il produit une petite observation exportable, épinglée et limitée à un paquet ciblé. [GitHub expose séparément les vues et visiteurs](https://docs.github.com/en/rest/metrics/traffic). Ces compteurs, clones, étoiles, visites du propriétaire et bots ne prouvent pas une adoption humaine ; ils ne sont pas convertis en « utilisateurs ».

L’angle est **chantier → version → test → limite**, avec contrôle de fraîcheur et téléchargement sans compte. Pas de découverte exhaustive de tous les consommateurs, d’identité humaine vérifiée, de qualification opérationnelle, de benchmark SOTA ou d’attestation cryptographique indépendante. Les résultats sont des exercices bornés ; consulter les limites propres à chaque dépôt. Aucun message social, email ou contact de mainteneur n’est envoyé.

## Vérifier

```sh
python3 -m unittest discover -s tests -v
npm ci
npx playwright install chromium
npm run test:browser
npm run format:check
```

Seize tests : portées et normalisation de dépendances, doublons, forks, absence de preuve, collecte publique épinglée, URL interdites, empreintes, reçus périmés, couverture incomplète et invalidation du paquet lui-même. Navigateur FR/EN/ES : galerie, vingt-six chantiers, preuve retirée, déclaration limitée, source modifiée, reproduction échouée, export, filtres et mobile. CI Python 3.11/3.12, construction et roue hors sources. MIT ; alpha publique.
