from typing import List


class Node:
    def __init__(self, information):
        self.information = information
        self.num_actions = len(self.actions)
        self.regret_sum = [0.0] * self.num_actions
        self.strategy_sum = [0.0] * self.num_actions

    def get_strategy(self, p: float) -> List[float]:
        normalizing_sum = sum(max(0, regret) for regret in self.regret_sum)
        if normalizing_sum > 0:
            strategy = [max(0, regret) / normalizing_sum for regret in self.regret_sum]
        else:
            strategy = [1 / self.num_actions] * self.num_actions
        for action in self.actions:
            self.strategy_sum[action] += p * strategy[action]
        return strategy

    def get_average_strategy(self) -> List[float]:
        normalizing_sum = sum(self.strategy_sum)
        if normalizing_sum > 0:
            strategy = [x / normalizing_sum for x in self.strategy_sum]
        else:
            strategy = [1 / self.num_actions] * self.num_actions
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
