# esp32_coffee_screen : conception électronique

Carte porteuse pour migrer la machine à expresso (firmware : [coffee_screen](https://github.com/vivien22/coffee_screen)) de l'Arduino Nano vers un **ESP32-S3 Nano (N16R8)**, dans le boîtier plastique existant.

État : **conception de travail, rien n'est fabriqué**. Les positions sont à l'échelle mais le routage reste à faire dans un logiciel de CAO.

## Contenu
- `docs/carrier_spec.md` : spécification complète (dimensions, connecteurs, brochage, circuits, liste de composants, points à confirmer).
- `images/carrier_plan.png` : implantation à l'échelle, vue de dessus, dans le boîtier.
- `images/box_iso3.png` : vue 3D du boîtier avec la carte (les versions `box_iso`, `box_iso2` sont les itérations précédentes).
- `images/carrier_schema.png` : schéma de principe (à mettre à jour pour les connecteurs J2 2 x 4 et J7 1 x 6).
- `tools/` : scripts Python (Pillow) qui génèrent les images ; les mesures y sont en tête de fichier.

## Principes
- Carte 58 x 68 mm dans l'espace libre de 60 x 70 mm, fixée sur 4 plots de 3 mm (entraxe 45 x 50 mm), profondeur utile 25 mm.
- Uniquement des composants traversants.
- ESP32-S3 et module MAX31865 sur supports ; carte d'adaptation FPC (écran déporté) sur support 2 x 4.
- SSR conservés : commandés par transistors 2N2222A depuis le 5 V externe.
- Connecteurs : J2 2 x 4 (5 V + 3 SSR), J7 1 x 6 (bouton + encodeur), 2 x JST XH 3 broches (capteurs de débit).

## À confirmer avant fabrication
Voir la fin de `docs/carrier_spec.md` : brochage et alimentation de l'écran, ordre des broches de l'encodeur, dimensions réelles de la carte ESP32-S3 et de la carte FPC, type de sortie des capteurs de débit.
