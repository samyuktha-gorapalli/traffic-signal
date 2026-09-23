import random
from collections import deque
from fuzzy_controller import fuzzy_decide_green_duration


def generate_arrival_times(rate: float, total_duration: float) -> list[float]:
    arrival_times = []
    current_time = 0.0
    while True:
        gap = random.expovariate(rate)
        current_time += gap
        if current_time > total_duration:
            break
        arrival_times.append(current_time)
    return arrival_times


def step(t, queues, arrival_schedules, arrival_indices, current_phase, discharge_counter):
    recorded_wait_times = []

    for approach, schedule in arrival_schedules.items():
        idx = arrival_indices[approach]
        while idx < len(schedule) and t <= schedule[idx] < t + 1:
            queues[approach].append(schedule[idx])
            idx += 1
        arrival_indices[approach] = idx

    discharge_counter += 1
    if discharge_counter % 3 == 0:
        active_queue = queues.get(current_phase)
        if active_queue:
            arrival_time = active_queue.popleft()
            wait_time = (t + 1) - arrival_time
            recorded_wait_times.append(wait_time)

    return recorded_wait_times, discharge_counter


def run_baseline_simulation(rate_a: float, rate_b: float, total_duration: int, green_duration: int = 30):
    arrival_schedules = {
        'approach_a': generate_arrival_times(rate_a, total_duration),
        'approach_b': generate_arrival_times(rate_b, total_duration)
    }
    queues = {'approach_a': deque(), 'approach_b': deque()}
    arrival_indices = {'approach_a': 0, 'approach_b': 0}
    all_wait_times = {'approach_a': [], 'approach_b': []}

    current_phase = 'approach_a'
    discharge_counter = 0

    for t in range(total_duration):
        if t > 0 and t % green_duration == 0:
            current_phase = 'approach_b' if current_phase == 'approach_a' else 'approach_a'
            discharge_counter = 0

        departed_waits, discharge_counter = step(
            t, queues, arrival_schedules, arrival_indices, current_phase, discharge_counter
        )
        if departed_waits:
            all_wait_times[current_phase].extend(departed_waits)

    return all_wait_times


def run_fuzzy_simulation(rate_a: float, rate_b: float, total_duration: int, rule_table=None):
    arrival_schedules = {
        'approach_a': generate_arrival_times(rate_a, total_duration),
        'approach_b': generate_arrival_times(rate_b, total_duration)
    }
    queues = {'approach_a': deque(), 'approach_b': deque()}
    arrival_indices = {'approach_a': 0, 'approach_b': 0}
    all_wait_times = {'approach_a': [], 'approach_b': []}

    current_phase = 'approach_a'
    other_phase = 'approach_b'
    discharge_counter = 0
    phase_start = 0
    current_green_duration = fuzzy_decide_green_duration(
        len(queues[current_phase]), len(queues[other_phase]), rule_table
    )

    for t in range(total_duration):
        if t - phase_start >= current_green_duration:
            current_phase, other_phase = other_phase, current_phase
            discharge_counter = 0
            phase_start = t
            current_green_duration = fuzzy_decide_green_duration(
                len(queues[current_phase]), len(queues[other_phase]), rule_table
            )

        departed_waits, discharge_counter = step(
            t, queues, arrival_schedules, arrival_indices, current_phase, discharge_counter
        )
        if departed_waits:
            all_wait_times[current_phase].extend(departed_waits)

    return all_wait_times