from fuzzy_sets import queue_low, queue_medium, queue_high

RULE_TABLE = {
    ('high', 'low'): 41,      # was 45
    ('high', 'medium'): 35,
    ('high', 'high'): 30,
    ('medium', 'low'): 30,
    ('medium', 'medium'): 25,
    ('medium', 'high'): 18,
    ('low', 'low'): 11,       # was 15
    ('low', 'medium'): 12,
    ('low', 'high'): 10,
}

MIN_GREEN = 10
MAX_GREEN = 45


def fuzzy_decide_green_duration(own_queue: float, other_queue: float, rule_table=None) -> float:
    if rule_table is None:
        rule_table = RULE_TABLE

    own = {'low': queue_low(own_queue), 'medium': queue_medium(own_queue), 'high': queue_high(own_queue)}
    other = {'low': queue_low(other_queue), 'medium': queue_medium(other_queue), 'high': queue_high(other_queue)}

    weighted_sum = 0.0
    total_strength = 0.0
    for (own_cat, other_cat), output_value in rule_table.items():
        strength = min(own[own_cat], other[other_cat])
        weighted_sum += strength * output_value
        total_strength += strength

    if total_strength == 0:
        return 25.0

    duration = weighted_sum / total_strength
    return max(MIN_GREEN, min(MAX_GREEN, duration))