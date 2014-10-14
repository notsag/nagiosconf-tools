# Outils d'aide à la création de configuration pour les Nagios-like

## hostnames2ip.py

Ce script permet de générer un fichier JSON de correspondances IP -> noms :

```bash
hostname2ip.py -i <liste> -o <fichier.json> [-v]
hostname2ip.py -i <fichier> -o <fichier.json> [-v]
```

## json2nagios.py

Ce script utilise les fichiers JSON générés par hostnames2ip.py pour créer des fichiers de configuration nagios. Les fichiers créés contiennent la définition du host et les services HTTP et/ou HTTPs après vérification par le script pour chacun des noms correspondant à une url.

```bash
json2nagios.py -i <fichier.json>
```

