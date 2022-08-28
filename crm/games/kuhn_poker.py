from enum import IntEnum
import random

from .game_base import Node, Game


class Action(IntEnum):
    Bet = 0
    Call = 1
    Fold = 2
    Check = 3


class Card(IntEnum):
    Q = 0
    K = 1
    A = 2


class KuhnPokerNode(Node):
    def __init__(self, information):
        super().__init__(information)

    @property
    def actions(self):
        hist = self.information[1]
        if len(hist) == 0:
            return [Action.Bet, Action.Check]
        elif hist[-1] == Action.Bet:
            return [Action.Call, Action.Fold]
        elif hist[-1] == Action.Check:
            if len(hist) >= 2 and hist[-2] == Action.Check:
                return []
            else:
                return [Action.Bet, Action.Check]
        else:
            return []


class KuhnPoker(Game):
    def __init__(self):
        self.cards = [Card.Q, Card.K, Card.A]
        super().__init__()

    def reset(self):
        random.shuffle(self.cards)

    @property
    def players(self):
        return list(range(2))

    def player(self, hist):
        return len(hist) % self.num_players

    def create_node(self, info):
        return KuhnPokerNode(info)

    def is_terminal(self, hist):
        if len(hist) == 0:
            return False
        elif hist[-1] == Action.Call or hist[-1] == Action.Fold:
            return True
        elif len(hist) >= 2 and hist[-1] == Action.Check and hist[-2] == Action.Check:
            return True
        else:
            return False

    def payoff(self, hist):
        if hist[-1] == Action.Fold:
            if len(hist) % 2 == 0:
                return [1, -1]
            else:
                return [-1, 1]
        elif hist[-1] == Action.Check:
            if self.cards[0] > self.cards[1]:
                return [1, -1]
            else:
                return [-1, 1]
        else:
            if self.cards[0] > self.cards[1]:
                return [2, -2]
            else:
                return [-2, 2]

    def information(self, hist):
        card = self.cards[self.player(hist)]
        return (card, tuple(hist))
