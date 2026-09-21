from simulation import run_baseline_simulation


def main():
    results = run_baseline_simulation(rate_a=0.125, rate_b=0.067, total_duration=600)

    avg_wait_a = sum(results['approach_a']) / len(results['approach_a'])
    avg_wait_b = sum(results['approach_b']) / len(results['approach_b'])

    print(f"Approach A (busy)  - cars served: {len(results['approach_a'])}, avg wait: {avg_wait_a:.2f}s")
    print(f"Approach B (quiet) - cars served: {len(results['approach_b'])}, avg wait: {avg_wait_b:.2f}s")


if __name__ == "__main__":
    main()