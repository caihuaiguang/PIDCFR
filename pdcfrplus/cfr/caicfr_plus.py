from pdcfrplus.cfr.cfr import CFR, CFRState
import random


class CAICFRPlusState(CFRState):
    def update_regret(self):
        for a in self.legal_actions:
            self.regrets[a] = max(self.regrets[a] + self.imm_regrets[a], 0)

    def update_current_policy(self):
        # print(self.player)
        if self.player == 1:
            self.pred_regrets = {
                a: max(self.regrets[a] + 1*self.imm_regrets[a], 0) for a in self.legal_actions
            }
            regret_sum = 0
            for regret in self.pred_regrets.values():
                regret_sum += max(0, regret)
            for a, regret in self.pred_regrets.items():
                if regret_sum == 0:
                    self.policy[a] = 1 / self.num_actions
                else:
                    self.policy[a] = max(0, regret) / regret_sum
        else:
            regret_sum = 0
            for regret in self.regrets.values():
                regret_sum += max(0, regret)
            for a, regret in self.regrets.items():
                if regret_sum == 0:
                    self.policy[a] = 1 / self.num_actions
                else:
                    self.policy[a] = max(0, regret) / regret_sum


class CAICFRPlus(CFR):
    def __init__(self, game_config, logger=None, gamma=2):
        super().__init__(game_config, logger, gamma)

    def init_state(self, h):
        return CAICFRPlusState(h)
        
       

        