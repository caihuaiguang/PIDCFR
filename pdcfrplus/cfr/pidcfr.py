from pdcfrplus.cfr.cfr import CFR, CFRState
import copy
import numpy as np

class PIDCFRState(CFRState):
    def init_data(self):
        super().init_data()
        self.pre_regrets = {a: 0 for a in self.legal_actions}
        self.predict_v = {a: 0 for a in self.legal_actions}

    def update_regret(self, T):
        for a in self.legal_actions:
            self.regrets[a] = max(self.regrets[a] + self.imm_regrets[a], 0)

    # online gradient descent, failed
    def update_current_policy(self, T):
        if T == 1:
            self.predict_v = {a: self.imm_regrets[a] for a in self.legal_actions}
        else:
            # self.predict_v = {a: 2 * self.imm_regrets[a] - self.predict_v[a] for a in self.legal_actions}
            self.predict_v = {a: self.imm_regrets[a] for a in self.legal_actions}
        self.pred_regrets = {
            a: max(self.regrets[a] + 1/6*self.predict_v[a], 0) for a in self.legal_actions
        }        
        # self.pred_regrets = {
        #     a: max(self.regrets[a] + self.imm_regrets[a], 0) for a in self.legal_actions
        # }
        regret_sum = 0
        for regret in self.pred_regrets.values():
            regret_sum += max(0, regret)
        for a, regret in self.pred_regrets.items():
            if regret_sum == 0:
                self.policy[a] = 1 / self.num_actions
            else:
                self.policy[a] = max(0, regret) / regret_sum

    # # extragradient algorithm, failed
    # def update_regret(self, T):
    #     if T % 2 == 0:
    #         for a in self.legal_actions:
    #             self.pre_regrets[a] = self.regrets[a]
    #             self.regrets[a] = max(self.regrets[a] + self.imm_regrets[a], 0)
    #     else:
    #         for a in self.legal_actions:
    #             self.regrets[a] = max(self.pre_regrets[a] + self.imm_regrets[a], 0)

    # def update_current_policy(self):
    #     self.pred_regrets = {
    #         a: max(self.regrets[a] + self.imm_regrets[a], 0) for a in self.legal_actions
    #     }
    #     regret_sum = 0
    #     for regret in self.pred_regrets.values():
    #         regret_sum += max(0, regret)
    #     for a, regret in self.pred_regrets.items():
    #         if regret_sum == 0:
    #             self.policy[a] = 1 / self.num_actions
    #         else:
    #             self.policy[a] = max(0, regret) / regret_sum

    # def update_current_policy(self):
    #     self.pred_regrets = {
    #         # a: max(self.regrets[a] + self.imm_regrets[a], 0) for a in self.legal_actions  (1 - 1 / np.exp(2))
    #         # a: 1 * max(0, self.imm_regrets[a]) + (1 - 1 / np.exp(2)) * self.regrets[a] + 0* (max(0, self.imm_regrets[a]) - max(0, self.pre_imm_regrets[a])) for a in self.legal_actions
    #         a: np.exp(1) * self.imm_regrets[a] + 1 * self.regrets[a] + 0* (max(0, self.imm_regrets[a]) - max(0, self.pre_imm_regrets[a])) for a in self.legal_actions
    #     }
    #     regret_sum = 0
    #     for regret in self.pred_regrets.values():
    #         regret_sum += max(0, regret)
    #     for a, regret in self.pred_regrets.items():
    #         if regret_sum == 0:
    #             self.policy[a] = 1 / self.num_actions
    #         else:
    #             self.policy[a] = max(0, regret) / regret_sum
    #     self.pre_imm_regrets = copy.deepcopy(self.imm_regrets)

    # def update_current_policy(self, T):
    #     self.pred_regrets = {
    #         a: max(self.regrets[a] + self.imm_regrets[a], 0) for a in self.legal_actions
    #     }
    #     regret_sum = 0
    #     for regret in self.pred_regrets.values():
    #         regret_sum += max(0, regret)
    #     for a, regret in self.pred_regrets.items():
    #         if regret_sum == 0:
    #             self.policy[a] = 1 / self.num_actions
    #         else:
    #             self.policy[a] = max(0, regret) / regret_sum

class PIDCFR(CFR):
    def __init__(self, game_config, logger=None, gamma = 2, average = True, PID = False):
        super().__init__(game_config, logger,  gamma=gamma, average=average,PID=PID)

    def init_state(self, h):
        return PIDCFRState(h)

    def update_state(self, s):
        # self.logger.record("self.num_iteration", self.num_iteration)
        s.update_regret(self.num_iteration)

        s.cumulate_policy(self.num_iteration, self.gamma, self.average)

        s.update_current_policy(self.num_iteration)