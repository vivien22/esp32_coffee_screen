# Carte porteuse ESP32-S3 : spécification (version de travail)

Écrit pour : toi, avant de commander la carte. Tout est en **composants traversants** (aucun CMS à souder). Documents liés : `images/carrier_plan.png` (implantation à l'échelle), `images/box_iso3.png` (vue 3D), `images/carrier_schema.png` (schéma de principe, à regénérer pour J2 / J7).

## Dimensions et fixation
- Carte : **58 x 68 mm**, deux couches, plan de masse. Zone libre du boîtier : 60 x 70 mm entre les gros plots.
- 4 trous de fixation sur les petits plots de **3 mm**, entraxe **45 x 50 mm**.
- Profondeur utile **25 mm** : plots 3 + carte 1,6 = 4,6 mm ; ESP32 sur supports de 8,5 mm (USB-C à 17,9 mm) ; carte FPC sur supports de 8,5 mm (17,7 mm) ; MAX31865 sur supports bas de 3 mm (22,6 mm, marge 2,4 mm).
- Aucun cuivre ni composant sous l'antenne de l'ESP32 (le bas de la carte ESP32).

## Connecteurs
| Repère | Type | Rôle |
|---|---|---|
| J1 | (fusionné dans J2, broches A1 / A2) | alimentation 5 V |
| J2 | barrette mâle 2 x 4 coudée, boîtiers Dupont femelles | alimentation 5 V + 3 SSR |
| J7 | barrette mâle 1 x 6 coudée | bouton + encodeur (alimenté en 5 V) |
| J8 | barrette 1 x 4 | variateur de pompe RobotDyn 4 A, en UART (alimenté en 3,3 V) |
| J9 | barrette 1 x 3 | capteur de pression 0,5 à 4,5 V, 0 à 12 bar (alimenté en 5 V) |
| J3, J4 | JST XH 3 broches (pas réel 2,5 mm) | capteurs de débit In et Out |
| J5 | support femelle 2 x 4 | ta carte d'adaptation FPC 8 broches (nappe vers l'écran déporté) |
| J6 | support femelle 1 x 8 (bas, 3 mm) | module MAX31865 |
| ESP | 2 supports femelles 1 x 20 | carte ESP32-S3 (écartement à relever) |

### J2 (2 x 4 : rangée A en haut, rangée B en bas, broche 1 à gauche)
| | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| A | +5 V | pompe + | chaudière + | vanne + |
| B | GND | pompe − | chaudière − | vanne − |

Quatre boîtiers Dupont 2P (un par colonne). Attention : un boîtier 2 x 4 n'est pas détrompé et un boîtier 2P peut être monté à l'envers ; repérer les fils (rouge sur la rangée A) ou ajouter un ergot / une barrette à boîtier détrompé.

### J7 (1 x 6)
| 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|
| bouton (GPIO 6) | GND | **+5 V** | GND | enc. A (GPIO 4) | enc. B (GPIO 5) |

Boîtiers : 2P (bouton) et 4P (encodeur : +5 V, GND, A, B). L'ordre doit suivre **ton** module d'encodeur (à vérifier).

### Protection des entrées 5 V (encodeur)
L'ESP32-S3 n'accepte que 3,3 V. Le module encodeur étant alimenté en 5 V, ses sorties (A, B, bouton) peuvent monter à 5 V si le module a des rappels vers 5 V. Chaque signal passe donc par un diviseur : 4,7 kΩ en série vers le GPIO, puis 10 kΩ du GPIO vers GND (5 V devient 3,4 V). Les rappels de 10 kΩ vers 3,3 V (R9, R10) sont alors à supprimer. **À vérifier :** si ton module est un encodeur nu sans résistances de rappel, il faut des 10 kΩ vers 5 V (à prévoir en option sur la carte).

### J8 (variateur de pompe, 1 x 4, ordre du module)
| 1 | 2 | 3 | 4 |
|---|---|---|---|
| VCC (3,3 V) | GND | TX/SDA | RX/SCL |

Module RobotDyn « 4 A Dimmer, interface DimmerLink UART / I2C » (53 x 16 mm) : pas de broche de passage par zéro ni de PWM, tout passe par le bus. **Mode retenu : UART.** Le TX de l'ESP32 (GPIO 47, **provisoire**) va vers RX/SCL du module et le RX de l'ESP32 (GPIO 48) vers TX/SDA ; le module est configuré en UART (voir sa fiche DimmerLink). Le module reste hors de la carte, côté secteur : seul le câble Dupont de commande y revient, la partie 230 V garde sa propre isolation et sa distance. Alimentation en 3,3 V pour que la logique soit au même niveau que l'ESP32.

### J9 (capteur de pression, 1 x 3)
| 1 | 2 | 3 |
|---|---|---|
| +5 V | GND | signal |

Capteur G1/4, 0 à 12 bar, sortie 0,5 à 4,5 V. Le signal passe par un diviseur 10 kΩ (série) / 20 kΩ (vers GND) qui ramène 4,5 V à 3,0 V, plus 100 nF sur le GPIO 1 (ADC1, atténuation 11 dB). Pression en bar = (tension du capteur − 0,5) x 3. Lecture à moyenner (l'ADC de l'ESP32 est bruité et peu linéaire aux extrémités).

### J3 / J4 (JST XH 3 broches)
1 = +5 V, 2 = signal, 3 = GND. L'ordre exact vient du câble du capteur (souvent rouge / jaune / noir).

### J5 (carte FPC, tes numéros : haut 1 3 5 7, bas 2 4 6 8)
Affectation **provisoire** (GC9A01 8 broches typique) : 1 GND, 2 3V3, 3 SCL (GPIO 12), 4 SDA (GPIO 11), 5 DC (GPIO 9), 6 CS (GPIO 10), 7 RST (GPIO 8), 8 BL (GPIO 14 par transistor). **À confirmer avec la fiche de l'écran.**

### J6 (module MAX31865)
VIN (3,3 V), 3Vo (non utilisé), GND, CLK (GPIO 12), SDO (GPIO 13), SDI (GPIO 11), CS (GPIO 7), RDY (non utilisé). Ordre à vérifier sur ton module.

## Broches de l'ESP32-S3
5V, 3V3, GND ; GPIO 17 (SSR pompe), 18 (SSR chaudière), 21 (SSR vanne) ; 15 (débit In), 16 (débit Out) ; 4 / 5 (encodeur) ; 6 (bouton) ; 11 / 12 / 13 (SPI MOSI / SCK / MISO) ; 10 (écran CS) ; 9 / 8 (écran DC / RST) ; 14 (rétroéclairage) ; 7 (MAX31865 CS) ; 47 / 48 (variateur, UART TX / RX) ; 1 (pression, ADC) ; 38 (réserve). Évitées : 0, 3, 45, 46, 19, 20, 35 à 37.

## Circuits
- **Alimentation :** J2 A1 (+5 V) → fusible réarmable 1,1 A → diode 1N5819 (contre l'inversion) → rail +5 V (470 µF + 100 nF) → broche 5V de l'ESP32. Le 3,3 V vient de la carte ESP32.
- **SSR (x3) :** GPIO → 1 kΩ → base d'un 2N2222A ; 10 kΩ base → GND ; l'entrée « + » du SSR au rail +5 V, l'entrée « − » au collecteur ; émetteur à GND. L'entrée du SSR reçoit environ 4,8 V.
- **Capteur de débit (x2) :** signal → 10 kΩ vers +5 V ; signal → 4,7 kΩ → GPIO ; GPIO → 10 kΩ → GND ; 1 nF GPIO → GND. Marche avec une sortie 5 V (le pont donne environ 3,4 V) ou à collecteur ouvert.
- **Rétroéclairage de l'écran :** GPIO 14 → 1 kΩ → base d'un 2N2222A ; le courant du rétroéclairage passe par le collecteur (à adapter à l'écran).
- **Encodeur :** pull-ups de 10 kΩ vers 3,3 V sur A et B, 100 nF contre les rebonds. **Bouton :** pull-up interne (ou 10 kΩ vers 3,3 V).

## Liste des composants (traversants)
| Qté | Composant | Prix indicatif |
|---|---|---|
| 1 | carte ESP32-S3 N16R8 (tu l'as) | 0 |
| 2 | supports femelles 1 x 20, 8,5 mm | 1 € |
| 1 | module MAX31865 (tu l'as) + support 1 x 8 bas | 0,3 € |
| 1 | carte FPC 8P (tu l'as) + barrette mâle 2 x 4 + support femelle 2 x 4 | 0,5 € |
| 1 | barrette mâle 2 x 4 coudée + 1 x 6 coudée | 0,5 € |
| 2 | embases JST XH 3 broches | 0,5 € |
| 4 | transistors 2N2222A (3 SSR + rétroéclairage) | 0,6 € |
| 20 | résistances axiales : 4 x 1 kΩ, 8 x 10 kΩ, 5 x 4,7 kΩ, 1 x 20 kΩ… (à recompter au routage) | 1 € |
| 1 | fusible réarmable 1,1 A (radial) | 0,5 € |
| 1 | diode 1N5819 | 0,2 € |
| 1 | condensateur 470 µF 10 V radial ; 3 x 100 nF ; 2 x 1 nF | 1 € |
| 4 | entretoises 3 mm (existantes) + vis M2,5 | 0 |
| | **Total composants** | **environ 6 à 8 €** |
| 5 | cartes nues, 58 x 68 mm, 2 couches (port compris) | 10 à 20 € |

## Points à confirmer avant la fabrication
1. L'ordre des broches de la nappe de ton écran (J5), son alimentation et son rétroéclairage.
2. L'ordre des broches de ton module MAX31865 et de l'encodeur.
3. L'écartement (rangées et pas) des broches de ta carte ESP32-S3, et sa vraie largeur.
4. Les dimensions de ta carte d'adaptation FPC (environ 22 x 28 mm estimés) et l'écartement de ses trous de fixation.
5. Le type de sortie des capteurs de débit (5 V ou collecteur ouvert) : le circuit prévu convient aux deux.
6. Module MAX31865 (Adafruit, relevé sur le plan du fabricant) : 25,4 x 27,9 mm, trous de fixation à 0,9" d'entraxe et 0,1" du bord côté bornier, connecteur 1 x 8 au pas de 0,1" sur le petit côté : VIN, 3Vo, GND, CLK, SDO, SDI, CS, RDY.
7. Variateur de pompe : le protocole DimmerLink (commandes, adresse I2C, vitesse UART) est à relever sur la fiche du module. Pompe : Olab Silent Green (vibrante, 230 V / 35 W / 0,33 A en version européenne ; vérifier l'étiquette). Le variateur de phase est une pratique courante sur ce type de pompe. Le variateur se place en série avec la pompe ; garder le SSR de pompe en série comme coupure franche (le variateur seul ne garantit pas l'arrêt complet). Aux faibles puissances la pompe peut vibrer sans pomper : prévoir une plage de réglage minimale à calibrer avec le capteur de pression.
8. Capteur de pression : confirmer 3 fils (+5 V, GND, signal) et le raccord G1/4 côté circuit hydraulique.
