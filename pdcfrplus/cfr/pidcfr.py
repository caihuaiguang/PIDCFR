from pdcfrplus.cfr.cfr import CFR, CFRState
import copy
import numpy as np

class PIDCFRState(CFRState):
    def init_data(self):
        super().init_data()
        self.pre_imm_regrets = {a: 0 for a in self.legal_actions}

    def update_regret(self):
        for a in self.legal_actions:
            self.regrets[a] = max(self.regrets[a] + self.imm_regrets[a], 0)

    def update_current_policy(self):
        self.pred_regrets = {
            # a: max(self.regrets[a] + self.imm_regrets[a], 0) for a in self.legal_actions  (1 - 1 / np.exp(2))
            # a: 1 * max(0, self.imm_regrets[a]) + (1 - 1 / np.exp(2)) * self.regrets[a] + 0* (max(0, self.imm_regrets[a]) - max(0, self.pre_imm_regrets[a])) for a in self.legal_actions
            a: np.exp(1) * self.imm_regrets[a] + 1 * self.regrets[a] + 0* (max(0, self.imm_regrets[a]) - max(0, self.pre_imm_regrets[a])) for a in self.legal_actions
        }
        regret_sum = 0
        for regret in self.pred_regrets.values():
            regret_sum += max(0, regret)
        for a, regret in self.pred_regrets.items():
            if regret_sum == 0:
                self.policy[a] = 1 / self.num_actions
            else:
                self.policy[a] = max(0, regret) / regret_sum
        self.pre_imm_regrets = copy.deepcopy(self.imm_regrets)


class PIDCFR(CFR):
    def __init__(self, game_config, logger=None, average = True):
        super().__init__(game_config, logger, average=average)

    def init_state(self, h):
        return PIDCFRState(h)
