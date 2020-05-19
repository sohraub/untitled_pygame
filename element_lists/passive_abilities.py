from game_elements.ability import PassiveAbility


calculated_strikes = PassiveAbility(name='Calculated Strikes', description='Increases your critical-hit rate by {} %.',
                                    mod_group='combat', specific_mod='crit_rate', value=3)

bloodthirst = PassiveAbility(name='Bloodthirst', description='Gain {} HP when you kill an enemy.',
                             mod_group='on_kill', specific_mod='gain_hp', value=2)

deadly_momentum = PassiveAbility(name='Deadly Momentum',
                                 description='Reduce all ability cooldowns by {} when you kill an enemy.',
                                 mod_group='on_kill', specific_mod='cooldown_reduction', value=2)

thick_skin = PassiveAbility(name='Thick Skin', description='Increases your defense rating by {}.', mod_group='combat',
                            specific_mod='base_def', value=2)