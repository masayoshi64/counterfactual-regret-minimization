from collections import defaultdict
from typing import List


class Node:
    def __init__(self, information):
        self.information = information
        self.num_actions = len(self.actions)
        self.regret_sum = defaultdict(float)
        self.strategy_sum = defaultdict(float)

    def get_strategy(self, p: float) -> dict:
        normalizing_sum = sum(
            max(0, self.regret_sum[action]) for action in self.actions
        )
        if normalizing_sum > 0:
            strategy = {
                action: max(0, self.regret_sum[action]) / normalizing_sum
                for action in self.actions
            }
        else:
            strategy = {action: 1 / self.num_actions for action in self.actions}
        for action in self.actions:
            self.strategy_sum[action] += p * strategy[action]
        return strategy

    def get_average_strategy(self) -> dict:
        normalizing_sum = sum(p for p in self.strategy_sum.values())
        if normalizing_sum > 0:
            strategy = {
                action: self.strategy_sum[action] / normalizing_sum
                for action in self.actions
            }
        else:
            strategy = {action: 1 / self.num_actions for action in self.actions}
        return strategy

    def __str__(self) -> str:
        return str(self.information)

    @property
    def actions(self) -> List[int]:
        raise NotImplementedError()


class Game:
    def __init__(self):
        self.num_players = len(self.players)

    @property
    def players(self) -> List[int]:
        raise NotImplementedError()

    def player(self, hist: List[int]) -> int:
        raise NotImplementedError()

    def create_node(self, info) -> Node:
        raise NotImplementedError()

    def is_terminal(self, hist: List[int]) -> bool:
        raise NotImplementedError()

    def payoff(self, hist: List[int]) -> List[float]:
        raise NotImplementedError()

    def information(self, hist: List[int]):
        raise NotImplementedError()
