# Utilisation de mkdocs

## I Créer la documentation

### 1. Installer les librairies pythons mkdocs, mkdocstrings et mkdocstrings-python

### 2. Créer un fichier mkdocs.yml à la racine du projet pour configurer la doc

```yml
site_name: "Nom de votre projet"
nav: # on définit l'architecture de la doc en faisant les liens vers les fichiers dans docs
  - Accueil: index.md
  - Documentation:
      - Introduction: introduction.md
      - API:
          - Module1: api/module1.md
          - Module2: api/module2.md
theme:
  name: readthedocs #on peut utiliser d'autre theme de doc

plugins:
  - search
  - mkdocstrings: #ce la permet d'intégrer directement les docstrings
      handlers:
        python:
          options:
            docstring_style: google
            rendering:
              show_source: true
```

### 3. Créer le dossier docs et ajouter toutes les docs

### 4. On peut inclure directement les docstings comme cela

```md
# Documentation du Module1

::: src.module1
    handler: python
    rendering:
      show_source: true
``` 

### 5. Pour ajouter des fichiers md en dehors du répertoire docs, il faut créer des liens symboliques dans docs:

#### Création des liens symboliques :

Supposons que vous ayez un fichier Markdown situé dans ../external_docs/intro.md que vous voulez inclure dans la documentation. Créez un lien symbolique dans le répertoire docs :

```bash
ln -s ../external_docs/intro.md docs/intro.md
```

Cette commande crée un lien symbolique nommé intro.md dans le répertoire docs pointant vers ../external_docs/intro.md.

## II Publier la documentation sur github pages

### 1. En local créer la branche qui va accueillir la doc (le html et css générés automatiquement notamment)

```bash
git branch -M gh-pages
git push -f origin gh-pages
 ```

### 2. Configurer GitHub Pages

- Accédez à votre dépôt sur GitHub.
- Allez dans "Settings".
- Dans la section "Pages", sélectionnez la branche gh-pages comme source et roots Cliquez sur "Save".

### 3. Construisez votre doc et déployer votre code sur la branch:

```bash
 mkdocs build    
 mkdocs gh-deploy --force
 ```