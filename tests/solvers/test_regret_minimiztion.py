import pytest

from crm.solvers.regret_minimization import regret_minimization
from crm.games.rps import RPS


def test_regret_minimization():
    game = RPS(2)  # 二人じゃんけん
    strategy = [[1.0, 0, 0], [0, 0, 1.0]]
    nash = regret_minimization(game, strategy, 10000)
    # 出力がナッシュ均衡になっているか
    for i in range(2):
        for j in range(3):
            assert nash[i][j] == pytest.approx(1 / 3, 0.1)
