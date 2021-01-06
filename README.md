# Plugins for Bitcoin c-lightning :cactus:

## Présentation du projet :racehorse:

Ce projet a pour objectif de réaliser des plugins compatibles avec le Lightning Network Bitcoin. Nous avons commencé par étudier la structure du répertoire github du projet [Lightning](https://github.com/ElementsProject/lightning) ainsi que les ["good first issue"](https://github.com/ElementsProject/lightning/issues?q=is%3Aissue+label%3A%22good+first+issue%22+) déjà référencées.

Nous avons finalement sélectionné l'issue #3662 ["Add new notifications for plugin"](https://github.com/ElementsProject/lightning/issues/3662). L'objectif était donc d'implémenter une nouvelle notification au projet existant pour détecter lorsqu'un channel est fermé et les raisons de sa fermeture. 

Après avoir parcouru les différents fichiers écrits en C et au vu de la difficulté de ces derniers, nous avons préféré nous rediriger sur l'écriture de plugins en python à l'aide de la librairie [pylightning](https://pypi.org/project/pylightning/). Nous avons ainsi étudié la [documentation](https://lightning.readthedocs.io/_/downloads/en/master/pdf/) proposée par c-lightning sur les plugins (cf chapter 5 p31).
