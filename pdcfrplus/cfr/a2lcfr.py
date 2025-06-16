from pdcfrplus.cfr.cfr import CFR, CFRState
import copy
import numpy as np

class A2LCFRState(CFRState):
    def init_data(self):
        super().init_data()

    def update_regret(self, T):
        for a in self.legal_actions:
            self.regrets[a] = self.regrets[a] + self.imm_regrets[a]


    # def cumulate_policy(self, T, gamma, average):
    #     for a, p in self.policy.items():
    #         self.cum_policy[a] = (
    #             self.cum_policy[a] * np.power((T - 1), 2) / T + self.reach * p
    #         )
    
    def update_current_policy(self, T):
        regret_sum = 0
        for regret in self.regrets.values():
            regret_sum += max(0, regret)
        for a, regret in self.regrets.items():
            if regret_sum == 0:
                self.policy[a] = 1 / self.num_actions
            else:
                self.policy[a] += max(0, regret) / regret_sum

        # self.cum_policy = self.get_average_policy()
        # for a, p in self.policy.items():
        #     self.policy[a] +=  self.reach * p 


class A2LCFR(CFR):
    def __init__(self, game_config, logger=None, average = False, A2L = True):
        super().__init__(game_config, logger, average=average)

    def init_state(self, h):
        return A2LCFRState(h)


    def update_state(self, s):
        # self.logger.record("self.num_iteration", self.num_iteration)
        s.update_regret(self.num_iteration)

        s.cumulate_policy(self.num_iteration, self.gamma, self.average)

        s.update_current_policy(self.num_iteration)
