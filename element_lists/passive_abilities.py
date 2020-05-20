from game_elements.ability import PassiveAbility


calculated_strikes = PassiveAbility(name='Calculated Strikes', description='Increases your critical-hit rate by {} %.',
                                    mod_group='combat', specific_mod='crit_rate', value=3)

bloodthirsty = PassiveAbility(name='Bloodthirsty', description='Gain {} HP when you kill an enemy.',
                             mod_group='on_kill', specific_mod='gain_hp', value=2)

deadly_momentum = PassiveAbility(name='Deadly Momentum',
                                 description='Reduce all ability cooldowns by {} when you kill an enemy.',
                                 mod_group='on_kill', specific_mod='cooldown_reduction', value=2)

thick_skin = PassiveAbility(name='Thick Skin', description='Increases your defense rating by {}.', mod_group='combat',
                            specific_mod='base_def', value=2)

quiet_steps = PassiveAbility(name='Quiet Steps', mod_group='board_mods', specific_mod='enemy_aggro', value=1,
                             description='Reduce the distance at which enemies can detect you by {} tile.')