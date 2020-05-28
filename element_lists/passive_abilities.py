from game_elements.ability import PassiveAbility


calculated_strikes = PassiveAbility(name='Calculated Strikes', description='Increases your critical-hit rate.',
                                    mod_group='combat', specific_mod='crit_rate', value=3,
                                    details={'Additional Crit Chance': '3 * {skill_level}'})

bloodthirsty = PassiveAbility(name='Bloodthirsty', description='Gain HP when you kill an enemy.',
                              mod_group='on_kill', specific_mod='gain_hp', value=2,
                              details={'HP Gain On Kill': '2 * {skill_level}'})

deadly_momentum = PassiveAbility(name='Deadly Momentum',
                                 description='Reduce all ability cooldowns when you kill an enemy.',
                                 mod_group='on_kill', specific_mod='cooldown_reduction', value=2,
                                 details={'Cooldown Reduction On Kill': '2 * {skill_level}'})

thick_skin = PassiveAbility(name='Thick Skin', description='Increases your defense rating.', mod_group='combat',
                            specific_mod='base_def', value=2,
                            details={'Additional Defense Rating': '2 * {skill_level}'})

quiet_steps = PassiveAbility(name='Quiet Steps', mod_group='board_mods', specific_mod='enemy_aggro', value=1,
                             description='Reduce the distance at which enemies can detect you.',
                             details={'Aggro Reduction': '1 * {skill_level}'})