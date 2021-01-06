# Plugins for Bitcoin c-lightning :cactus:

## Présentation du projet :racehorse:

Ce projet a pour objectif de réaliser des plugins compatibles avec le Lightning Network Bitcoin. Nous avons commencé par étudier la structure du répertoire github du projet [Lightning](https://github.com/ElementsProject/lightning) ainsi que les ["good first issue"](https://github.com/ElementsProject/lightning/issues?q=is%3Aissue+label%3A%22good+first+issue%22+) déjà référencées.

Nous avons finalement sélectionné l'issue #3662 ["Add new notifications for plugin"](https://github.com/ElementsProject/lightning/issues/3662). L'objectif était donc d'implémenter une nouvelle notification au projet existant pour détecter lorsqu'un channel est fermé et les raisons de sa fermeture. 

Après avoir parcouru les différents fichiers écrits en C et au vu de la difficulté de ces derniers, nous avons préféré nous rediriger sur l'écriture de plugins en python à l'aide de la librairie [pylightning](https://pypi.org/project/pylightning/). Nous avons ainsi étudié la [documentation](https://lightning.readthedocs.io/_/downloads/en/master/pdf/) proposée par c-lightning sur les plugins (cf chapter 5 p31).

## Présentation de nos cas d'usage :clipboard:

Pour ce projet, nous avons défini deux cas d'usage:
1. Le premier, faire des requêtes HTTP en utilisant l'API [Coindesk]('https://api.coindesk.com/v1/bpi/currentprice.json') pour récupérer les prix du Bitcoin en temps réel et dans différentes devises (€, $ et £). L'utilisateur a ainsi aux prix du Bitcoin en direct dans son interface lightning.
2. Créer un plugin capable d'éxecuter n'importe quel jeu python dans un autre terminal puis capable de récupérer le score réalisé lpar 'utilisateur et de l'encoder avec la fonction native "signmessage" de c-lighning.

Nos résultats : 

Le premier plugin nous permet d'afficher les valeurs du Bitcoin dans différentes devises dans le terminal où est chargé lightningd.

![usecase1](https://github.com/victorlrz/LightningPlugin/blob/main/src/gameplugin.JPG)

Le deuxième usecase présenté dans la vidéo ci-dessous permet d'éxécuter un jeu python puis d'encoder le score de l'utilisateur avec la fonction native "signmessage" de c-lightning.

[![usecase2](https://github.com/victorlrz/LightningPlugin/blob/main/src/hook.png)](https://www.youtube.com/watch?v=S9FJD41cBcY&feature=youtu.be)
