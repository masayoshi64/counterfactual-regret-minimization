from enum import IntEnum

from .game_base import Node, Game


class Hand(IntEnum):
    R = 0
    P = 1
    S = 2


class RPSNode(Node):
    def __init__(self, information):
        super().__init__(information)

    @property
    def actions(self):
        return [Hand.R, Hand.P, Hand.S]


class RPS(Game):
    def __init__(self, num_players=2):
        self.num_players = num_players
        super().__init__()

    @property
    def players(self):
        return list(range(self.num_players))

    def player(self, hist):
        return len(hist) % self.num_players

    def create_node(self, info):
        return RPSNode(info)

    def is_terminal(self, hist):
        return len(hist) == self.num_players

    def payoff(self, hist):
        u = [0.0] * self.num_players

        hands = list(set(hist))
        if len(hands) != 2:  # あいこなら全員利得0
            return u

        win_hand, lose_hand = hands
        # 勝ち負けが逆ならswap
        if win_hand == Hand.R and lose_hand == Hand.P:
            win_hand, lose_hand = lose_hand, win_hand
        elif win_hand == Hand.P and lose_hand == Hand.S:
            win_hand, lose_hand = lose_hand, win_hand
        elif win_hand == Hand.S and lose_hand == Hand.R:
            win_hand, lose_hand = lose_hand, win_hand

        for player in self.players:
            if hist[player] == win_hand:
                u[player] = 1
            else:
                u[player] = -1
        return u

    def information(self, hist):
        return self.player(hist)
