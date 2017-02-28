#!/usr/bin/env python

from random import randint


class XWingRandomizer():
    """Class to randomize some parameters of the X-Wing tabletop game."""
    def __init__(self):
        # DOC: Players names / I don't want to enter them manually each time
        self.players = ["Player 1", "Player 2", "Player 3", "Player 4",
                        "Player 5", "Player 6", "Player 7"]
        # DOC: X-Wing factions names
        self.factions = ["Imperial", "Rebels", "Scums"]

    def SetFactions(self):
        contestants = list(self.players)
        nbMatches = len(contestants)/2
        print('Number of matches: ' + str(nbMatches))
        if len(contestants)/2.0 > float(nbMatches):
            print('1 player may be screwed')
        for i in contestants:
            choice = self.Choose(self.factions)
            print(i + " should play " +
                  self.factions[choice])

    def SetBrackets(self):
        contestants = list(self.players)
        for i in range(0, len(contestants)/2):
            plChoice1 = self.Choose(contestants)
            bracket = contestants[plChoice1] + " will play against "
            del contestants[plChoice1]
            plChoice2 = self.Choose(contestants)
            bracket += contestants[plChoice2]
            del contestants[plChoice2]
            print(bracket)
        if len(contestants) > 0:
            print(contestants[0] + " will sit and watch")

    def Choose(self, plList):
        return randint(0, len(plList)-1)

if __name__ == '__main__':
    round = XWingRandomizer()
    round.SetBrackets()
