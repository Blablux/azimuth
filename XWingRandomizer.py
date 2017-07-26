#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import randint
from random import shuffle


class XWingRandomizer():
    """Class to randomize some parameters of the X-Wing tabletop game."""
    def __init__(self):
        # DOC: Players names / I don't want to enter them manually each time
        self.bracket = {'Player F': {'opponent': "", 'faction': "",
                                     'ship': "", 'pilot': ""},
                        'Player B': {'opponent': "", 'faction': "",
                                     'ship': "", 'pilot': ""},
                        'Player M': {'opponent': "", 'faction': "",
                                     'ship': "", 'pilot': ""},
                        'Player S': {'opponent': "", 'faction': "",
                                     'ship': "", 'pilot': ""}
                        }
        self.players = self.bracket.keys()
        # TODO: reverse the process (players > bracket)
        # DOC: X-Wing factions names
        self.Database = {'Scums': {"Aggressor": ["·IG-88A",
                                                 "·IG-88B",
                                                 "·IG-88C",
                                                 "·IG-88D"],
                                   "Lancer-class Pursuit Craft": [
                                   "·Ketsu Onyo",
                                   "·Asajj Ventress",
                                   "·Sabine Wren",
                                   "Shadowport Hunter"
                                   ],
                                   "G-1A Starfighter": ["·Zuckuss",
                                                        "·4-LOM",
                                                        "Gand Findsman",
                                                        "Ruthless Freelancer"],
                                   "Kihraxz Fighter": ["·Talonbane Cobra",
                                                       "·Graz The Huter",
                                                       "Blacks Sun ace",
                                                       "Cartel Marauder"],
                                   "Protectorate Starfighter": [
                                   "·Fenn Rau",
                                   "·Old Teroch",
                                   "·Kad Solus",
                                   "Concord Dawn Ace",
                                   "Concord Dawn Veteran",
                                   "Zealous Recruit"
                                   ],
                                   "Firespray": ["·Boba Fett",
                                                 "·Kath Sarlet",
                                                 "·Emon Assameen",
                                                 "Mandalorian Mercenary"],
                                   "HWK-290": ["·Dace Bonearm",
                                               "·Palob Godhali",
                                               "·Torkil Mux",
                                               "Spice Runner"],
                                   "M3-A Interceptor": [
                                   "·Serissu",
                                   "·Genesis Red",
                                   "·Laetin A'Shera",
                                   "·Quinn Jast",
                                   "Tansarii Point Veteran",
                                   "·Inaldra",
                                   "Cartel Spacer"
                                   "·Sunny Bounder",
                                   ],
                                   "Jumpmaster": ["·Dengar",
                                                  "·Tel Trevura",
                                                  "·Manaroo",
                                                  "Contracted Scout)"],
                                   "Quadjumper": ["·Constable Zuvio",
                                                  "·Sarco Plank",
                                                  "·Unkar Plutt",
                                                  "Jakku Gunrunner"],
                                   "StarViper": ["·Xizor",
                                                 "·Guri",
                                                 "Black Sun Vigo",
                                                 "Black Sun Enforcer"],
                                   "Y-Wing": ["·Kavil",
                                              "·Drea Renthal",
                                              "Hired Gun",
                                              "Syndicate Thug"],
                                   "YV-666": ["·Bossk",
                                              "·Moralo Eval",
                                              "·Latts Razzi",
                                              "Trandoshan slaver"],
                                   "Scurrg H-6 Bomber": ["·Captain Nym",
                                                         "·Sol Sixxa",
                                                         "Lok Revenant",
                                                         "Karthakk Pirate"],
                                   "Z-95": ["·N'dru Suhlak",
                                            "·Kaa'to Leeachos",
                                            "Black Sun Soldier",
                                            "Binayre Pirate"]},
                         'Imperial': {"TIE-Bomber": [
                                      "·Tomax Bren",
                                      "·Major Rhymer",
                                      "·Captain Jonus",
                                      "Gamma Squadron Veteran",
                                      "Gamma Squadron Pilot",
                                      "·Deathfire",
                                      "Scimitar Squadron Pilot"
                                      ],
                                      "TIE-Fighter": [
                                      "·Howlrunner",
                                      "·Mauler Mithel",
                                      "·Scourge",
                                      "·Backstabber",
                                      "·Dark Curse",
                                      "·Youngster",
                                      "·Night Beast",
                                      "·Winged Gundark",
                                      "·Wampa",
                                      "Black Squadron Pilot",
                                      "·Chaser",
                                      "Obsidian Squadron Pilot",
                                      "Academy Pilot"
                                      ],
                                      "TIE-Fighter/FO": [
                                      "·Omega leader",
                                      "·Omega Ace",
                                      "·Zeta Leader",
                                      "·Epsilon Leader",
                                      "·Zeta Ace",
                                      "·Epsilon Ace",
                                      "Omega Squadron Pilot",
                                      "Zeta Squadron Pilot",
                                      "Espilon Squadron Pilot"
                                      ],
                                      "TIE-Fighter/FS": ["·Quickdraw",
                                                         "·Backdraft",
                                                         "Omega Specialist",
                                                         "Zeta Specialist"],
                                      "TIE-Defender": ["·Rexler Brath",
                                                       "·Maarek Stele",
                                                       "·Colonel Vessery",
                                                       "Glaive Squadron Pilot",
                                                       "·Ryad",
                                                       "Onyx Squadron Pilot",
                                                       "Delta Squadron Pilot"],
                                      "Firespray": ["·Boba fett",
                                                    "·Kath Scarlet",
                                                    "·Krassis Trelix",
                                                    "Bounty Hunter"],
                                      "TIE-Interceptor": [
                                      "·Soontir Fell",
                                      "·Carnor Jax",
                                      "·Tetran Cowall",
                                      "·Turr Phennir",
                                      "·Kir Kanos",
                                      "Royal Guard Pilot",
                                      "·Fel's Wrath",
                                      "·Lieutenant Lorrir",
                                      "Sabre Squadron Pilot",
                                      "Avenger Squadron Pilot",
                                      "Alpha Squadron Pilot"
                                      ],
                                      "Lambda-class Shuttle": [
                                      "·Captain Kagi",
                                      "·Colonel Jendon",
                                      "·Captain Yorr",
                                      "Omicron Group Pilot"
                                      ],
                                      "Upsilon-class Shuttle": [
                                      "·Kylo Ren",
                                      "·Major Stridan",
                                      "·Lieutenant Dormitz",
                                      "Starkiller Base Pilot"
                                      ],
                                      "TIE-Adv. Prototype": [
                                      "·The Inquisitor",
                                      "·Valen Rudor",
                                      "Baron of the Empire",
                                      "Sienar Test Pilot"
                                      ],
                                      "TIE-Advanced": [
                                      "·Darth vader",
                                      "·Juno Eclipse",
                                      "·Maarek Stele",
                                      "·Zerik Strom",
                                      "·Commander Alozen",
                                      "Storm Squadron Pilot",
                                      "·Lieutenant Colzet",
                                      "Tempest Squadron Pilot"
                                      ],
                                      "TIE-Fantom": ["·Whisper",
                                                     "·Echo",
                                                     "Shadow Squadron Pilot",
                                                     "Sigma Squadron Pilot"],
                                      "TIE-Punisher": [
                                      "·Redline",
                                      "·Deathrain",
                                      "Black Eight Squadron Pilot",
                                      "Cutlass Squadron Pilot"],
                                      "TIE-Striker": ["·Duchess",
                                                      "·Pure Sabacc",
                                                      "·Countdown",
                                                      "Black Squadron Scout",
                                                      "Scarif Defender",
                                                      "Imperial Trainee"],
                                      "TIE-Aggressor": ["·Lieutenant Kestal",
                                                        "Onyx Squadron Escort",
                                                        "·Double Edge",
                                                        "Sienar Specialist"],
                                      "VT-49 Decimator": [
                                      "·Rear Admiral Chiraneau",
                                      "·Commander Kenkirk",
                                      "·Captain Oicunn",
                                      "Patrol Leader"]},
                         'Rebels': {"A-Wing": ["·Tycho Celchu",
                                               "·Jake Farrell",
                                               "·Arvel Crynd",
                                               "·Gemmer Sojan",
                                               "Green Squadron Pilot",
                                               "Prototype Pilot"],
                                    "ARC-170": ["·Norra Wexley",
                                                "·Shara Bey",
                                                "·Thane Kyrell",
                                                "·Braylen Stramm"],
                                    "B-Wing": ["·Ten Numb",
                                               "·Keyan Farlander",
                                               "·Ibistam",
                                               "·Near Dantels",
                                               "Dagger Squadron Pilot",
                                               "Blue Squadron Pilot"],
                                    "TIE-Fighter": ["·Ahsoka Tano",
                                                    "·Sabine Wren",
                                                    "·Captain Rex",
                                                    "·Zeb Orrelios"],
                                    "E-Wing": ["·Corran Horn",
                                               "·Etahn A'Baht",
                                               "Blackmoon Squadron Pilot",
                                               "Knave Squadron Pilot"],
                                    "HWK-290": ["·Jan Ors",
                                                "·Kyle Katarn",
                                                "·Roark Garnet",
                                                "Rebel Operative"],
                                    "K-Wing": ["·Miranda Doni",
                                               "·Esege Tuketu",
                                               "Guardian Squadron Pilot",
                                               "Warden Squadron Pilot"],
                                    "Auzituck Gunship": [
                                    "·Wullffwarro",
                                    "·Lowhhrick",
                                    "Wookie Liberator",
                                    "Kashyyyk Defender"],
                                    "Scurrg H-6 Bomber": ["·Captain Nym"],
                                    "Attack Shuttle": ["·Hera Syndula",
                                                       "·Sabine Wren",
                                                       "·Ezra Bridger",
                                                       "·Zeb Orrelios"],
                                    "U-wing": ["·Cassian Andor",
                                               "·Bohdi Rook",
                                               "·Heff Tober",
                                               "Blue Squadron Pathfinder"],
                                    "VCX-100": ["·Hera Syndulla",
                                                "·Kanan Jarrus",
                                                "·Chopper",
                                                "Lothal Rebel"],
                                    "X-Wing": ["·Wedge Antilles",
                                               "·Luke Skywalker",
                                               "·Wes Janson",
                                               "·Jek Porkins",
                                               "·Garven Dreis",
                                               "·Hobbie Klivian",
                                               "·Biggs Darklighter",
                                               "Red Squadron Pilot",
                                               "·Tarn Mison",
                                               "Rookie Pilot"],
                                    "X-Wing T70": ["·Poe Dameron (HotR)",
                                                   "·Poe Dameron (TFA)",
                                                   "·Ello Asty",
                                                   "·Nien Numb",
                                                   "·Red Ace",
                                                   "·Snap Wexley",
                                                   "·Blue Ace",
                                                   "Red Squadron Veteran",
                                                   "·Jess Pava",
                                                   "Blue Squadron Novice"],
                                    "Y-Wing": ["·Horton Salm",
                                               "·Dutch Vander",
                                               "Gray Squadron Pilot",
                                               "Gold Squadron Pilot"],
                                    "YT-1300": ["·Han Solo (Mill)",
                                                "·Han Solo (HotR)",
                                                "·Rey",
                                                "·Lando Calrissian",
                                                "·Chewbacca (Mill)",
                                                "·Chewbacca (HotR)",
                                                "Resistance Sympathizer",
                                                "Outer Rim Smuggler"],
                                    "YT-2400": ["·Dash Rendar",
                                                "·Leebo",
                                                "·Eaden Vrill",
                                                "Wild Space Fringer"],
                                    "Z-95": ["·Airen Cracken",
                                             "·Lieutenant Blount",
                                             "Tala Squadron Pilot",
                                             "Bandit Squadron Pilot"]}
                         }
        self.factions = self.Database.keys()
        # DOC: Various data for maths
        self.nbOfPlayers = len(self.players)
        self.nbOfMatches = self.nbOfPlayers / 2
        self.factionRatio = self.nbOfPlayers / len(self.factions)
        self.factionModulus = self.nbOfPlayers % len(self.factions)
        # DOC: Random list of factions assignables based on players number
        self.distribution = [i for i in self.factions for r in
                             range(self.factionRatio)]
        if self.factionModulus == 1:
            self.distribution.append(self.factions[self.Choose(self.factions)])
        elif self.factionModulus == 2:
            templist = list(self.factions)
            del templist[self.Choose(self.factions)]
            self.distribution.extend(templist)
        shuffle(self.distribution)
        self.SetBrackets()
        self.SetFactions()

    def SetFactions(self):
        # DOC: On duplique la liste des joueurs, parce qu'on va taper dedans
        contestants = list(self.players)
        # if self.nbOfMatches > float(self.nbOfMatches):
        #     print('1 player may be screwed')
        for i in contestants:
            choice = self.Choose(self.distribution)
            faction = self.distribution[choice]
            self.bracket[i]["faction"] = faction
            shipList = self.Database[faction].keys()
            ship = shipList[self.Choose(shipList)]
            self.bracket[i]["ship"] = ship
            pilotList = self.Database[faction][ship]
            pilot = self.Database[faction][ship][self.Choose(pilotList)]
            self.bracket[i]["pilot"] = pilot
            del self.distribution[choice]
            shuffle(self.distribution)

    def SetBrackets(self):
        contestants = list(self.players)
        for i in range(0, self.nbOfMatches):
            plNb1 = self.Choose(contestants)
            plChoice1 = contestants[plNb1]
            del contestants[plNb1]
            plNb2 = self.Choose(contestants)
            plChoice2 = contestants[plNb2]
            del contestants[plNb2]
            self.bracket[plChoice1]["opponent"] = plChoice2
            self.bracket[plChoice2]["opponent"] = plChoice1
        if len(contestants) > 0:
            self.bracket[contestants[0]]["opponent"] = False
        # DEBUG: print(self.bracket)

    def Choose(self, list):
        return randint(0, len(list)-1)

    def PrintBracket(self):
        for i in self.players:
            print(i + " will play against " + self.bracket[i]["opponent"]
                  + " and must use " + self.bracket[i]["pilot"] + " ("
                  + self.bracket[i]["faction"] + " / "
                  + self.bracket[i]["ship"] + ")")


if __name__ == '__main__':
    round = XWingRandomizer()
    round.PrintBracket()
