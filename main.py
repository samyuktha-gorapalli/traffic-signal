import matplotlib.pyplot as plt
from simulation import run_baseline_simulation, run_fuzzy_simulation


def average_wait(results, approach):
    waits = results[approach]
    return sum(waits) / len(waits) if waits else 0.0


def run_trials(sim_func, n_trials=20, **kwargs):
    totals_a, totals_b = [], []
    for _ in range(n_trials):
        results = sim_func(**kwargs)
        totals_a.append(average_wait(results, 'approach_a'))
        totals_b.append(average_wait(results, 'approach_b'))
    return sum(totals_a) / len(totals_a), sum(totals_b) / len(totals_b)


def main():
    kwargs = dict(rate_a=0.125, rate_b=0.067, total_duration=600)

    baseline_a, baseline_b = run_trials(run_baseline_simulation, **kwargs)
    fuzzy_a, fuzzy_b = run_trials(run_fuzzy_simulation, **kwargs)

    print(f"Baseline - A: {baseline_a:.2f}s, B: {baseline_b:.2f}s")
    print(f"Fuzzy    - A: {fuzzy_a:.2f}s, B: {fuzzy_b:.2f}s")
    print(f"Improvement - A: {(baseline_a - fuzzy_a) / baseline_a * 100:.1f}%, "
          f"B: {(baseline_b - fuzzy_b) / baseline_b * 100:.1f}%")

    labels = ['Approach A (busy)', 'Approach B (quiet)']
    x = range(len(labels))
    width = 0.35

    fig, ax = plt.subplots()
    ax.bar([i - width / 2 for i in x], [baseline_a, baseline_b], width, label='Fixed-Timer Baseline')
    ax.bar([i + width / 2 for i in x], [fuzzy_a, fuzzy_b], width, label='Fuzzy Controller')
    ax.set_ylabel('Average Wait Time (s)')
    ax.set_title('Average Wait Time: Baseline vs Fuzzy Controller')
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels)
    ax.legend()
    plt.tight_layout()
    plt.savefig('improvement_graph.png')
    print("Saved improvement_graph.png")


if __name__ == "__main__":
    main()