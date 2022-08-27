import pytest

from crm.solvers.counterfactual_regret_minimization import CRM
from crm.games.rps import RPS
from crm.games.guriko import Guriko


def test_regret_minimization():
    # 対称な二人零和ゲームのナッシュ均衡を求める
    game_list = [RPS(), Guriko()]
    nash_list = [[1 / 3, 1 / 3, 1 / 3], [0.4, 0.2, 0.4]]
    for game, nash in zip(game_list, nash_list):
        crm = CRM(game)
        crm.train(1000)
        # 出力がナッシュ均衡になっているか
        for i in range(2):
            node = crm.node_dict[i]
            strategy = node.get_average_strategy()
            for j in range(3):
                assert strategy[j] == pytest.approx(nash[j], 0.1)
