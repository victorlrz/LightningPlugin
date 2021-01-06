# Plugins for Bitcoin c-lightning :cactus:

## Présentation du projet :racehorse:

Ce projet a pour objectif de réaliser des plugins compatibles avec le Lightning Network Bitcoin. Nous avons commencé par étudier la structure du répertoire github du projet [Lightning](https://github.com/ElementsProject/lightning) ainsi que les ["good first issue"](https://github.com/ElementsProject/lightning/issues?q=is%3Aissue+label%3A%22good+first+issue%22+) déjà référencées.

Nous avons finalement sélectionné l'issue #3662 ["Add new notifications for plugin"](https://github.com/ElementsProject/lightning/issues/3662). L'objectif était donc d'implémenter une nouvelle notification au projet existant pour détecter lorsqu'un channel est fermé et les raisons de sa fermeture. 

Après avoir parcouru les différents fichiers écrits en C et au vu de la difficulté de ces derniers, nous avons préféré nous rediriger sur l'écriture de plugins en python à l'aide de la librairie [pylightning](https://pypi.org/project/pylightning/). Nous avons ainsi étudié la [documentation](https://lightning.readthedocs.io/_/downloads/en/master/pdf/) proposée par c-lightning sur les plugins (cf chapter 5 p31).

## Présentation de nos cas d'usage :clipboard:

Pour ce projet, nous avons défini deux cas d'usage:
1. Le premier, faire des requêtes HTTP en utilisant l'API [Coindesk]('https://api.coindesk.com/v1/bpi/currentprice.json') pour récupérer les prix du Bitcoin en temps réel et dans différentes devises (€, $ et £). L'utilisateur a ainsi accès au prix du Bitcoin, en direct, depuis son interface lightning.
2. Créer un plugin capable d'éxecuter n'importe quel jeu python dans un autre terminal et aussi capable de récupérer le score réalisé par l'utilisateur et de l'encoder avec la fonction native "signmessage" de c-lighning.

Nos résultats : 

Le premier plugin nous permet d'afficher les valeurs du Bitcoin dans différentes devises dans le terminal où est chargé lightningd.

![usecase1](https://github.com/victorlrz/LightningPlugin/blob/main/src/btcplugin.png)

Le deuxième usecase présenté dans la vidéo ci-dessous permet d'éxécuter un jeu python puis d'encoder le score de l'utilisateur avec la fonction native "signmessage" de c-lightning.

[![usecase2](https://github.com/victorlrz/LightningPlugin/blob/main/src/hook.png)](https://www.youtube.com/watch?v=S9FJD41cBcY&feature=youtu.be)

## Overview de l'environnement :runner::dash:

Nous avons installé et configuré c-lightning sur WSL2 depuis Windows 10. Le Sous-système Windows pour Linux permet aux développeurs d’exécuter un environnement GNU/Linux (et notamment la plupart des utilitaires, applications et outils en ligne de commande) directement sur Windows, sans modification et tout en évitant la surcharge d’une machine virtuelle traditionnelle ou d’une configuration à double démarrage.

Windows Terminal est aussi nécessaire pour éxecuter notre second plugin spécifiquement configué pour un environnement Windows 10. Vous pouvez installer Terminal Windows à partir du [Microsoft Store](https://www.microsoft.com/fr-fr/p/windows-terminal/9n0dx20hk701?rtc=1&activetab=pivot:overviewtab). Si vous n’avez pas accès au Microsoft Store, les builds sont publiées sur la page [Versions de GitHub](https://github.com/microsoft/terminal/releases). Si vous installez à partir de GitHub, le terminal n’est pas automatiquement mis à jour avec les nouvelles versions.

Enfin, Bitcoind et Lightningd sont configurés spécifiquement pour le testnet network.

## Overview du projet :eyes:

Nos plugins utilisent tous les deux la librairie [pylightning](https://pypi.org/project/lightning-python/). Nous importons ainsi les composants nécessaires de cette librairie pour développer nos plugins.

```from lightning import Plugin```

#### Bitcoin value plugin :chart:

Le premier plugin réalisé a pour objectif de récupérer la valeur du Bitcoin en temps réel dans différentes devises. Pour cela nous utilisons l'API mise à disposition par Coindesk. La fonction "getBTCvalue" nous permet de retourner un string contenant la valeur d'un BTC.

```
def getBTCvalue(currency):
    res = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
    resjson = res.json()
    symbol = symbols[str(currency).strip()]
    return "1 BTC = " + resjson['bpi'][currency]['rate'] + symbol
```

Cette fonction est appelée dans l'unique méthode mise à disposition à l'utilisateur. La méthode "BTCvalue" prend en paramètres deux arguments. Le premier argument "stopstr" permet à l'utilisateur de contrôler l'affichage des valeurs du BTC (afficher/arrêter l'affichage). Le deuxième paramètre "currency" permet à l'utilisateur de sélectionner dans quelle devise afficher la valeur BTC.

@plugin.method est natif à "pylightning" et permet de créer puis d'ajouter des méthodes à un plugin.

```
@plugin.method("BTCvalue")
def BTCvalue(plugin, stopstr=None, currency="USD", count=0, starttime = time.time()):
    """This plugin display BTC value for several currencies and suscribe to several RPC events"""
    global pluginRun
    
    stop = None

    if (stopstr == "True"):
        stop = True
    elif (stopstr == "False"):
        stop = False
    else:
        stop = None

    if (stop != None):
        pluginRun['running'] = stop

    if (pluginRun['running']):
        return None

    count += 1
    #plugin.log(f"tick {count}")
    plugin.log(getBTCvalue(currency))

    time.sleep(5.0 - ((time.time()) - starttime) % 5.0)
    BTCvalue(plugin, None, currency, count, starttime)
```

Enfin, @plugin.init() et @plugin.run() permettent l'initialisation de notre plugin. Pour lancer un plugin il suffit de préciser son path absolu au lancement de lightningd.

Par exemple :
> lightningd --plugin=/path/to/plugin

