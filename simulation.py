import random
from collections import deque


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

    # 1. Process arrivals occurring during this 1-second window [t, t + 1)
    for approach, schedule in arrival_schedules.items():
        idx = arrival_indices[approach]
        while idx < len(schedule) and t <= schedule[idx] < t + 1:
            queues[approach].append(schedule[idx])
            idx += 1
        arrival_indices[approach] = idx

    # 2. Process discharge every 3rd second of active green
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

    queues = {
        'approach_a': deque(),
        'approach_b': deque()
    }
    arrival_indices = {
        'approach_a': 0,
        'approach_b': 0
    }
    all_wait_times = {
        'approach_a': [],
        'approach_b': []
    }

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

def trapezoidal_membership(x: float, a: float, b: float, c: float, d: float) -> float:
    # 1. Flat top / Shoulders get priority so boundary points aren't swallowed
    if b <= x <= c:
        return 1.0
    
    # 2. Outside the support window (zero membership)
    if x <= a or x >= d:
        return 0.0
    
    # 3. Rising edge (a < x < b)
    if a < x < b:
        return (x - a) / (b - a) if b > a else 1.0
    
    # 4. Falling edge (c < x < d)
    if c < x < d:
        return (d - x) / (d - c) if d > c else 1.0
        
    return 0.0