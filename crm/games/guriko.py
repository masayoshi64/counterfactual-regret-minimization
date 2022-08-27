from .rps import RPS, Hand


class Guriko(RPS):
    def __init__(self, num_players=2):
        super().__init__(num_players)
        self.value = [3, 6, 6]

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
                u[player] = self.value[win_hand]
            else:
                u[player] = -self.value[win_hand]
        return u
