# Copyright (c) 2019 Eric Steinberger


import numpy as np
from PokerRL.cfr._CFRBase import CFRBase as _CFRBase


class DCFRPlus(_CFRBase):
    def __init__(
        self,
        name,
        chief_handle,
        game_cls,
        agent_bet_set,
        starting_stack_sizes=None,
        other_agent_bet_set=None,
        alpha=1.5,
        gamma=2,
        average=True,
    ):
        super().__init__(
            name=name,
            chief_handle=chief_handle,
            game_cls=game_cls,
            starting_stack_sizes=starting_stack_sizes,
            agent_bet_set=agent_bet_set,
            other_agent_bet_set=other_agent_bet_set,
            algo_name="DuelingCFR",
        )
        self.reset()
        self.alpha = alpha
        self.gamma = gamma
        self.average = average

    def _regret_formula_after_first_it(self, ev_all_actions, strat_ev, last_regrets):
        imm_regrets = ev_all_actions - strat_ev
        regrets = last_regrets
        T = self._iter_counter + 1

        regrets = np.maximum(
            regrets
            * np.power(T - 1, self.alpha)
            / (np.power(T - 1, self.alpha) + 1.5)
            + imm_regrets,
            0,
        )
        return regrets

    def _regret_formula_first_it(self, ev_all_actions, strat_ev):
        return ev_all_actions - strat_ev

    def _compute_new_strategy(self, p_id):
        for t_idx in range(len(self._trees)):

            def _fill(_node):
                if _node.p_id_acting_next == p_id:
                    N = len(_node.children)
                    _capped_reg = np.maximum(_node.data["regret"], 0)
                    _reg_pos_sum = np.expand_dims(
                        np.sum(_capped_reg, axis=1), axis=1
                    ).repeat(N, axis=1)

                    with np.errstate(divide="ignore", invalid="ignore"):
                        _node.strategy = np.where(
                            _reg_pos_sum > 0.0,
                            _capped_reg / _reg_pos_sum,
                            np.full(
                                shape=(
                                    self._env_bldrs[t_idx].rules.RANGE_SIZE,
                                    N,
                                ),
                                fill_value=1.0 / N,
                                dtype=np.float32,
                            ),
                        )
                for c in _node.children:
                    _fill(c)

            _fill(self._trees[t_idx].root)

    def _add_strategy_to_average(self, p_id):
        def _fill(_node):
            if _node.p_id_acting_next == p_id:
                T = self._iter_counter + 1
                contrib = _node.strategy * np.expand_dims(
                    _node.reach_probs[p_id], axis=1
                )
                if self._iter_counter > 0 and self.average is True:
                    _node.data["avg_strat_sum"] = (
                        _node.data["avg_strat_sum"] * np.power((T - 1) / T, self.gamma)
                        + contrib
                    )
                else:
                    _node.data["avg_strat_sum"] = contrib

                _s = np.expand_dims(np.sum(_node.data["avg_strat_sum"], axis=1), axis=1)

                with np.errstate(divide="ignore", invalid="ignore"):
                    _node.data["avg_strat"] = np.where(
                        _s == 0,
                        np.full(
                            shape=len(_node.allowed_actions),
                            fill_value=1.0 / len(_node.allowed_actions),
                        ),
                        _node.data["avg_strat_sum"] / _s,
                    )
                assert np.allclose(
                    np.sum(_node.data["avg_strat"], axis=1), 1, atol=0.0001
                )

            for c in _node.children:
                _fill(c)

        for t_idx in range(len(self._trees)):
            _fill(self._trees[t_idx].root)
