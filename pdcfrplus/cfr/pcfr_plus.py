from pdcfrplus.cfr.cfr import CFR, CFRState


class PCFRPlusState(CFRState):
    def update_regret(self):
        for a in self.legal_actions:
            self.regrets[a] = max(self.regrets[a] + self.imm_regrets[a], 0)

    def update_current_policy(self):
        self.pred_regrets = {
            a: max(self.regrets[a] + self.imm_regrets[a], 0) for a in self.legal_actions
        }
        regret_sum = 0
        for regret in self.pred_regrets.values():
            regret_sum += max(0, regret)
        for a, regret in self.pred_regrets.items():
            if regret_sum == 0:
                self.policy[a] = 1 / self.num_actions
            else:
                self.policy[a] = max(0, regret) / regret_sum


    # def cumulate_policy(self, T, gamma):
    #     for a, p in self.policy.items():
    #         if T == 1:
    #             self.cum_policy[a] = self.reach * p
    #             continue
    #         self.cum_policy[a] = self.reach * p
class PCFRPlus(CFR):
    def __init__(self, game_config, logger=None, gamma=2, average = True):
        super().__init__(game_config, logger, gamma=gamma, average=average)

    def init_state(self, h):
        return PCFRPlusState(h)
