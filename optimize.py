import random
from simulation import run_fuzzy_simulation
from fuzzy_controller import RULE_TABLE, MIN_GREEN, MAX_GREEN


def evaluate(rule_table, trials=5, rate_a=0.125, rate_b=0.067, total_duration=600):
    """Average combined wait time (both approaches) over a few trials —
    fewer than main.py's 20, to keep each evaluation fast during search."""
    total = 0.0
    for _ in range(trials):
        results = run_fuzzy_simulation(rate_a, rate_b, total_duration, rule_table=rule_table)
        a_wait = sum(results['approach_a']) / len(results['approach_a']) if results['approach_a'] else 0
        b_wait = sum(results['approach_b']) / len(results['approach_b']) if results['approach_b'] else 0
        total += (a_wait + b_wait)
    return total / trials


def hill_climb(iterations=30, step_size=4):
    current_table = dict(RULE_TABLE)
    current_score = evaluate(current_table)
    print(f"Starting score (avg combined wait): {current_score:.2f}s")

    for i in range(iterations):
        candidate = dict(current_table)
        key = random.choice(list(candidate.keys()))
        delta = random.choice([-step_size, step_size])
        candidate[key] = max(MIN_GREEN, min(MAX_GREEN, candidate[key] + delta))

        candidate_score = evaluate(candidate)
        if candidate_score < current_score:
            current_table = candidate
            current_score = candidate_score
            print(f"Iteration {i+1}: improved to {current_score:.2f}s (changed {key} -> {candidate[key]})")

    return current_table, current_score


if __name__ == "__main__":
    best_table, best_score = hill_climb()
    print("\nBest rule table found:")
    for k, v in best_table.items():
        print(f"  {k}: {v}")
    print(f"Final avg combined wait: {best_score:.2f}s")