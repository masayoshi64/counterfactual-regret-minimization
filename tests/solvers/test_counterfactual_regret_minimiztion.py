import pytest

from crm.solvers.counterfactual_regret_minimization import CRM
from crm.games.rps import RPS
from crm.games.guriko import Guriko
from crm.games.kuhn_poker import KuhnPoker, Action


def test_regret_minimization():
    tol = 0.1
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
                assert strategy[j] == pytest.approx(nash[j], abs=tol)

    # Kuhn Pokerのナッシュ均衡を求める
    kuhn_poker = KuhnPoker()
    crm = CRM(kuhn_poker)
    crm.train(10000)
    # プレイヤー1の戦略
    alpha = crm.node_dict[(0, ())].get_average_strategy()[Action.Bet]
    assert crm.node_dict[(1, ())].get_average_strategy()[Action.Bet] == pytest.approx(
        0, abs=tol
    )
    assert crm.node_dict[(2, ())].get_average_strategy()[Action.Bet] == pytest.approx(
        3 * alpha, abs=tol
    )
    assert crm.node_dict[(1, (Action.Check, Action.Bet))].get_average_strategy()[
        Action.Call
    ] == pytest.approx(alpha + 1 / 3, abs=tol)
    # プレイヤー2の戦略
    assert crm.node_dict[(0, (Action.Check,))].get_average_strategy()[
        Action.Bet
    ] == pytest.approx(1 / 3, abs=tol)
    assert crm.node_dict[(0, (Action.Bet,))].get_average_strategy()[
        Action.Call
    ] == pytest.approx(0, abs=tol)
    assert crm.node_dict[(1, (Action.Bet,))].get_average_strategy()[
        Action.Call
    ] == pytest.approx(1 / 3, abs=tol)
    assert crm.node_dict[(2, (Action.Bet,))].get_average_strategy()[
        Action.Call
    ] == pytest.approx(1, abs=tol)
