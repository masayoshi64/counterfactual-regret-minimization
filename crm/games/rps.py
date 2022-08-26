from enum import IntEnum
from typing import List

from .normal_form_game import NormalFormGame


# 列挙型の定義
class Hand(IntEnum):
    R = 0
    P = 1
    S = 2


class RPS(NormalFormGame):
    def __init__(self, players_num):
        self.players = list(range(players_num))

    def actions(self, player: int) -> List[int]:
        return [Hand.R, Hand.P, Hand.S]

    def payoff(self, actions) -> List[float]:
        u = [0.0] * len(actions)

        hands = list(set(actions))
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
            if actions[player] == win_hand:
                u[player] = 1
            else:
                u[player] = -1
        return u

    def play(self, strategy: List[List[float]]) -> List[int]:
        actions = []
        for player in self.players:
            action = self.generate_action(player, strategy[player])
            actions.append(action)
        return actions
