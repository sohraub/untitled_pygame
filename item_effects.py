def increase_hp(target, value):
    if value >= 0:
        target.hp = min(target.hp[0] + value, target.hp[1])
    else:
        target.hp = max(target.hp[0] - value, 0)

def increase_mp(target, value):
    if value >= 0:
        target.mp = min(target.mp[0] + value, target.mp[1])
    else:
        target.mp = max(target.mp[0] - value, 0)

def improve_conditions(target, conditions, values):
    for condition, value in zip(conditions, values):
        if value >= 0:
            target.conditions[condition][0] = min(target.conditions[condition][0] + value,
                                                  target.conditions[condition][1])
        else:
            target.conditions[condition][0] = max(target.conditions[condition][0] - value, 0)

