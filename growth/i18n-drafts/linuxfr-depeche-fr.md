# LinuxFr.org dépêche (FR)

**STATUS: DRAFT — needs native review before posting.** Machine-assisted
French; a native speaker must review before submission. Venue:
https://linuxfr.org — submit as a *dépêche* (goes through community
moderation/rédaction; expect edits, that's normal and good). Angle per
plan: logiciel libre + architecture substance + honest limits (paid BYOK
API, non-libre models). Disclosed-maker voice. Plan ref:
`plan-q3-distribution.md` Phase 2, language wave 1 (FR). Also per plan:
request a Journal du hacker invite separately — do not self-submit there.

---

**Titre :** nanoodle : un éditeur de graphes de nœuds pour l'IA, entièrement
dans le navigateur, sous licence MIT

**Chapô :**

nanoodle est un éditeur libre (MIT) de « graphes de nœuds » pour composer
des chaînes de traitement IA — texte, image, vidéo, audio — qui fonctionne
intégralement côté client : pas de serveur, pas de compte, zéro télémétrie.
Un graphe s'exporte en application HTML autonome d'un seul fichier, ou se
partage par une URL dont le fragment contient tout le graphe. Je suis
l'auteur du logiciel ; cette dépêche présente l'architecture, et aussi ses
limites — dont la principale : l'inférence passe par une API commerciale
tierce, avec sa propre clé, facturée à l'appel.

**Corps :**

## Le principe

Si vous connaissez ComfyUI ou Node-RED, le canevas vous sera familier : on
pose des nœuds (modèles de texte, d'image, de vidéo, d'audio, plus des
nœuds utilitaires — dessin, redimensionnement, choix, commentaire…), on les
câble, on exécute. La différence est architecturale : il n'y a rien à
installer et rien ne tourne côté serveur. La page https://nanoodle.com
(interface en français : https://nanoodle.com/fr/) *est* le produit
complet : une seule page HTML statique, sans étape de build ni bundler.

Le code est publié sous licence MIT, historique complet inclus :
https://github.com/nanoodlecom/nanoodle

## Ce que l'absence de serveur impose

C'est la contrainte qui a produit les choix techniques les plus
intéressants :

- **Authentification** : OAuth PKCE directement du navigateur vers le
  fournisseur d'API. Aucun secret côté « serveur », puisqu'il n'y en a pas.
- **Persistance** : IndexedDB, dans le navigateur de l'utilisateur.
- **Partage** : le graphe est encodé dans le **fragment** de l'URL (après
  le `#`). Le fragment n'étant jamais transmis au serveur par le
  navigateur, un lien partagé est illisible pour l'hébergeur — par
  construction, pas par promesse.
- **Export** : un graphe s'exporte en application HTML **autonome, en un
  seul fichier**, moteur d'exécution embarqué. Elle s'héberge n'importe où
  et s'ouvre même depuis le disque.
- **Vie privée vérifiable** : zéro analytics, et la Content-Security-Policy
  n'autorise aucune origine tierce (pas de CDN, pas de polices externes,
  pas de traceurs). L'affirmation se vérifie dans les en-têtes HTTP et dans
  le fichier `_headers` du dépôt — l'onglet réseau fait office de preuve.

Conséquence amusante : l'éditeur et l'application exportée sont deux
moteurs d'exécution jumeaux qui doivent se comporter identiquement. La
dérive entre les deux étant devenue la première classe de bogues, la parité
est imposée par des hooks de pré-commit (le dépôt en compte une
quarantaine).

## L'écosystème

Deux bibliothèques d'exécution **sans aucune dépendance** permettent de
rejouer un graphe hors navigateur, avec des charges utiles identiques à
l'octet près entre elles :

- JavaScript : `npm install nanoodle` —
  https://github.com/nanoodlecom/nanoodle-js
- Python : `pip install nanoodle` —
  https://github.com/nanoodlecom/nanoodle-py

## Les limites, honnêtement

- **Les modèles ne sont pas libres et ne tournent pas localement.**
  L'inférence passe par l'API de nano-gpt.com (un agrégateur de modèles),
  avec **votre propre clé, facturée à l'appel**. Vos requêtes partent donc
  chez ce fournisseur au moment de l'exécution — c'est le compromis assumé
  pour n'avoir aucune infrastructure et ne détenir aucune donnée. Une
  estimation du coût (« ~$X to run ») s'affiche avant chaque exécution.
- L'édition, le partage et l'export fonctionnent sans clé et sans compte ;
  seule l'exécution des modèles est payante, au tarif du fournisseur, sans
  marge prélevée par nanoodle. Le modèle économique est un programme de
  parrainage du fournisseur, affiché tel quel.
- Pas de modèles locaux (pas de llama.cpp ni d'API locale à ce jour) ; pour
  du 100 % local, ComfyUI et consorts restent la bonne réponse.
- Auto-hébergement : la page étant statique, servir le dépôt suffit.

## En conclusion

nanoodle explore une position particulière : tout le logiciel est libre et
côté client, la seule dépendance externe est l'API d'inférence, et chaque
affirmation de confidentialité est vérifiable dans les en-têtes. Les
retours — notamment critiques — sont bienvenus, ici ou sur le dépôt.

**Liens :**
- Site : https://nanoodle.com (FR : https://nanoodle.com/fr/)
- Dépôt (MIT) : https://github.com/nanoodlecom/nanoodle
- Exécuteurs : https://github.com/nanoodlecom/nanoodle-js ·
  https://github.com/nanoodlecom/nanoodle-py
- Fournisseur d'API (dépendance, service commercial) : https://nano-gpt.com

---

**Submission notes (EN, not part of the dépêche):**
- LinuxFr moderation may rewrite parts — accept edits gracefully, answer
  every comment, do not argue about the non-libre models point (concede
  it; it is true).
- Log in `growth/shares.md`.
