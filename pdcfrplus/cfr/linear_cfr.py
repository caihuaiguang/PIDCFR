from pdcfrplus.cfr.cfr import CFR, CFRState


class LinearCFRState(CFRState):
    def update_regret(self, T):
        for a in self.legal_actions:
            self.regrets[a] = self.regrets[a] + self.imm_regrets[a] * T


class LinearCFR(CFR):
    def __init__(self, game_config, logger=None, gamma=1, average = True):
        super().__init__(game_config, logger, gamma=gamma, average=average)

    def init_state(self, h):
        return LinearCFRState(h)

    def update_state(self, s):
        s.update_regret(self.num_iteration)

        s.cumulate_policy(self.num_iteration, self.gamma, self.average)

        s.update_current_policy()
