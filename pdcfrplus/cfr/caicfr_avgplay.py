from pdcfrplus.cfr.cfr import CFR, CFRState
import numpy as np

class CAICFRState(CFRState):
    def init_data(self):
        super().init_data()
        self.c_1_to_t = 0
        # self.m_t = {a: 0 for a in self.legal_actions}
        # self.V_t = {a: 0 for a in self.legal_actions}
        # self.regrets = {a: 1/self.num_actions for a in self.legal_actions}

    # sgd + momentum
    # def calculate_c_t(self, T):
    #     cumul_and_instant_regret_sum = 0
    #     c_t_minus_1 = 0
    #     for a in self.legal_actions:
    #         cumul_and_instant_regret_sum += (max(0, self.regrets[a]+self.imm_regrets[a]))**2
    #         # cumul_and_instant_regret_sum += (max(0, self.imm_regrets[a]))**2
    #         # c_t_minus_1 += (max(0, self.regrets[a])/T)**2
    #     c_t = cumul_and_instant_regret_sum**(-1/2)  if cumul_and_instant_regret_sum != 0 else 0.1
    #     return  c_t
    
    # def calculate_c_t(self, T):
    #     cumul_and_instant_regret_sum = 0
    #     c_t_minus_1 = 0
    #     for a in self.legal_actions:
    #         cumul_and_instant_regret_sum += (max(0, self.regrets[a]+self.imm_regrets[a]))**2
    #         # cumul_and_instant_regret_sum += (max(0, self.imm_regrets[a]))**2
    #         # c_t_minus_1 += (max(0, self.regrets[a])/T)**2
    #     c_t = cumul_and_instant_regret_sum**(-1/2)  if cumul_and_instant_regret_sum != 0 else 0.1
    #     return  c_t
    # def calculate_e_t(self, T):  
    #     e_t = 0
    #     instant_regret_sum = 0
    #     for a in self.legal_actions:
    #         e_t += self.regrets[a] * max(self.imm_regrets[a], 0)
    #         instant_regret_sum +=  abs(self.imm_regrets[a])
    #     if instant_regret_sum == 0:
    #         e_t = 1e-6
    #     else:
    #         e_t /= instant_regret_sum
    #     return e_t

    def calculate_e_t(self, T):  
        e_t = 0
        instant_regret_sum = 0
        max_regret = 0
        min_regret = 1000
        for a in self.legal_actions:
            e_t +=  max(self.imm_regrets[a], 0)
            # instant_regret_sum +=  abs(self.imm_regrets[a])
            max_regret = max(max_regret, self.imm_regrets[a])
            min_regret = min(min_regret, self.imm_regrets[a])
        # if instant_regret_sum == 0:
        #     e_t = 1e-6
        # else:
        #     e_t /= instant_regret_sum
        # return e_t/((max_regret-min_regret)*self.num_actions)
        return e_t

    # def calculate_c_t(self, T):
    #     instant_regret_max= 0
    #     for a in self.legal_actions:
    #         instant_regret_max = max(instant_regret_max, self.regrets[a]+self.imm_regrets[a])
    #     if instant_regret_max == 0:
    #         instant_regret_max = 0.01
    #     return 1/instant_regret_max

    def cumulate_policy(self, T, c_t):
        for a, p in self.policy.items():
            self.cum_policy[a] = self.cum_policy[a]  + c_t * self.reach * p

    def update_regret(self, alpha_t):
        for a in self.legal_actions:
            self.regrets[a] = self.regrets[a] + self.imm_regrets[a]
        # for a in self.legal_actions:
        #     self.regrets[a] /= regret_sum
    # def update_regret(self, alpha_t):
    #     regret_sum = 0
    #     # instant_regret_sum = 0
    #     # for a in self.legal_actions:
    #     #     self.imm_regrets[a] = max(0,self.imm_regrets[a])
    #     #     instant_regret_sum += self.imm_regrets[a]
    #     for a in self.legal_actions:
    #         self.regrets[a] = self.regrets[a] * np.exp(alpha_t*self.imm_regrets[a])
    #         regret_sum += self.regrets[a]
    #     # for a in self.legal_actions:
    #     #     self.regrets[a] /= regret_sum
        
    # # sgd + momentum
    # def update_regret(self):
    #     beta = 1.2
    #     for a in self.legal_actions:
    #         self.m_t[a] = (1-beta) * self.m_t[a] + beta * self.imm_regrets[a]
    #         self.regrets[a] = self.regrets[a] + self.m_t[a]
    # adagrad
    # def update_regret(self,T):
    #     beta1 = 0.9
    #     beta2 = 0.99
    #     for a in self.legal_actions:
    #         self.m_t[a] = beta1 * self.m_t[a] + (1-beta1) * self.imm_regrets[a]
    #         self.m_t[a] /= (1-beta1**T)
    #         # self.V_t[a] = ()
    #         self.regrets[a] = self.regrets[a] + self.m_t[a]

    # e
    # def update_regret(self, T):
    #     norm_regrets = {a: 0 for a in self.legal_actions}
    #     regret_sum = 0
    #     # for a in self.legal_actions:
    #     #     norm_regrets[a] = np.exp(self.imm_regrets[a])
    #     #     regret_sum += norm_regrets[a]
        
    #     for a in self.legal_actions:
    #         self.regrets[a] = np.exp(self.regrets[a] + self.imm_regrets[a])
    #         regret_sum += self.regrets[a]
    #         # print(self.regrets[a])
            
    #     for a in self.legal_actions:
    #         self.regrets[a] /= regret_sum

    def update_current_policy(self):
        regret_sum = 0
        for a, regret in self.regrets.items():
            regret_sum += max(0, regret)
        for a, regret in self.regrets.items():
            if regret_sum == 0:
                self.policy[a] = 1 / self.num_actions
            else:
                self.policy[a] = max(0, regret) / regret_sum

    def update_current_policy2(self):
        cum_sum = sum(self.cum_policy.values())
        ave_policy = {}
        for a, cum in self.cum_policy.items():
            if cum_sum == 0:
                self.policy[a] = 1 / self.num_actions
            else:
                self.policy[a] = cum / cum_sum
        return ave_policy

class CAICFR(CFR):
    def __init__(self, game_config, logger=None, gamma=0):
        super().__init__(game_config, logger, gamma)

    def init_state(self, h):
        return CAICFRState(h)

    def update_state(self, s):
        # e_t = s.calculate_e_t(self.num_iteration)

        # if s.id == 10:
        # self.logger.record("e_t"+str(s.id), e_t)
        # alpha_t = 1/2 * np.log((1-e_t)/e_t)
        # alpha_t = 1/np.log(np.e+e_t)
        # alpha_t = np.log(e_t/())
        alpha_t =1
        # self.logger.record("alpha_t"+str(s.id), alpha_t)
        s.update_regret(2)
        s.update_current_policy()
        s.cumulate_policy(self.num_iteration, alpha_t)
        s.update_current_policy2()
        # s.cumulate_policy(self.num_iteration, self.gamma)
        # s.update_current_policy(t=1)


        