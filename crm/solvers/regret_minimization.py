import numpy as np
from typing import List
from tqdm import tqdm
import copy

from crm.games.normal_form_game import NormalFormGame


def regret_minimization(
    game: NormalFormGame, strategy: List[List[float]], num_epoch: int
) -> List[List[float]]:
    regret_sum = np.zeros_like(strategy, dtype=np.float32)
    strategy_sum = np.zeros_like(strategy, dtype=np.float32)
    for epoch in tqdm(range(num_epoch)):
        played_actions = game.play(strategy)
        payoff = game.payoff(played_actions)
        for player in game.players:
            counterfactual_actions = copy.deepcopy(played_actions)
            for action in game.actions(player):
                counterfactual_actions[player] = action
                counterfactual_payoff = game.payoff(counterfactual_actions)
                regret_sum[player][action] += (
                    counterfactual_payoff[player] - payoff[player]
                )  # regret（仮想的なpayoff - 実際のpayoff）
            next_probs = np.clip(regret_sum[player], 0, None)
            # 次の行動確率を計算
            if np.sum(next_probs) == 0:
                next_probs += 1 / next_probs.shape[0]
            else:
                next_probs /= np.sum(next_probs)
            # 行動確立を更新
            strategy[player] = next_probs.tolist()
        strategy_sum += strategy
    ave_strategy = (strategy_sum / num_epoch).tolist()
    return ave_strategy
