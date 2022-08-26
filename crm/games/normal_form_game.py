import random
from typing import List


class NormalFormGame:
    def __init__(self, players_num: int):
        self.players = list(range(players_num))

    def generate_action(self, player, probs):
        action = random.choices(self.actions(player), weights=probs)[0]
        return action

    def play(self, strategy: List[List[float]]) -> List[int]:
        actions = []
        for player in self.players:
            action = self.generate_action(player, strategy[player])
            actions.append(action)
        return actions

    def actions(self, player: int) -> List[int]:
        raise NotImplementedError()

    def payoff(self, actions: List[int]) -> List[float]:
        raise NotImplementedError()
