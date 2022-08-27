import copy
from typing import List, Any

from tqdm import tqdm

from ..games.game_base import Game, Node


class CRM:
    def __init__(self, game: Game):
        self.game = game
        self.node_dict: dict[Any, Node] = {}

    def cfr(self, hist: List[int], prob: List[float]) -> List[float]:
        # 終端ならpayoffをそのまま返す
        if self.game.is_terminal(hist):
            return self.game.payoff(hist)
        player = self.game.player(hist)
        info = self.game.information(hist)
        if info not in self.node_dict:
            node = self.game.create_node(info)
            self.node_dict[info] = node
        node = self.node_dict[info]
        strategy = node.get_strategy(prob[player])
        player_util = [0.0] * node.num_actions
        node_util = [0.0] * self.game.num_players
        for action in node.actions:
            next_hist = copy.deepcopy(hist)
            next_hist.append(action)
            next_prob = copy.deepcopy(prob)
            for p in self.game.players:
                if p != player:
                    next_prob[p] *= strategy[action]
            next_util = self.cfr(next_hist, next_prob)
            player_util[action] = next_util[player]
            for p in self.game.players:
                node_util[p] += strategy[action] * next_util[p]

        for action in node.actions:
            regret = player_util[action] - node_util[player]
            node.regret_sum[action] += prob[player] * regret
        return node_util

    def train(self, iterations):
        for i in tqdm(range(iterations)):
            self.cfr([], [1] * self.game.num_players)
