#!/usr/bin/env python

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
        # DOC: X-Wing factions names
        self.Database = {'Scums': ["Aggressor", "Lancer", "G-1A", "Kihraxz",
                                   "Protectorate", "Firespray", "HWK-290",
                                   "M3-A", "Jumpmaster", "Quadjumber",
                                   "StarViper", "Y-Wing", "YV-666", "Z-95"],
                         'Imperial': ["Bomber", "Fighter", "Fighter/FO",
                                      "Fighter/FS", "Defender", "Firespray",
                                      "Interceptor", "Lambda", "Upsilon",
                                      "Adv. Prototype", "Advanced", "Fantom",
                                      "Punisher", "Striker", "Decimator"],
                         'Rebels': ["A-Wing", "ARC-170", "B-Wing", "TIE",
                                    "E-Wing", "HWK-290", "K-Wing", "Shuttle",
                                    "U-wing", "VCX-100", "X-Wing",
                                    "X-Wing T70", "Y-Wing", "YT-1300",
                                    "YT-2400", "Z-95"]}
        # TODO: Add pilots for much more randomness
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

    def SetFactions(self):
        # DOC: On duplique la liste des joueurs, parce qu'on va taper dedans
        contestants = list(self.players)
        if self.nbOfMatches > float(self.nbOfMatches):
            print('1 player may be screwed')
        for i in contestants:
            choice = self.Choose(self.distribution)
            self.bracket[i]["faction"] = self.distribution[choice]
            shipNb = self.Choose(self.Database[self.distribution[choice]])
            ship = self.Database[self.distribution[choice]][shipNb]
            self.bracket[i]["ship"] = ship
            del self.distribution[choice]

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

    def Choose(self, plList):
        return randint(0, len(plList)-1)

    def PrintBracket(self):
        for i in self.players:
            print(i + " will play against " + self.bracket[i]["opponent"]
                  + " using " + self.bracket[i]["faction"] + "("
                  + self.bracket[i]["ship"] + ")")

if __name__ == '__main__':
    round = XWingRandomizer()
    round.SetFactions()
    round.SetBrackets()
    round.PrintBracket()
