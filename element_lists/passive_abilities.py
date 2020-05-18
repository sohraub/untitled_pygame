from game_elements.ability import PassiveAbility


calculated_strikes = PassiveAbility(name='Calculated Strikes', description='Increases your critical-hit rate.',
                                    mod_group='combat', specific_mod='crit_rate', value=5)

bloodthirst = PassiveAbility(name='Bloodthirst', description='Gain HP when you kill and enemy.',
                             mod_group='on_kill', specific_mod='gain_hp', value=2)