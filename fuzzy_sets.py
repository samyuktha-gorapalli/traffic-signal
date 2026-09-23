def trapezoidal_membership(x: float, a: float, b: float, c: float, d: float) -> float:
    """Degree of membership μ(x) for a trapezoidal fuzzy set, with correct
    unbounded shoulders when a==b (left) or c==d (right)."""
    if a == b and x <= a:
        return 1.0
    if c == d and x >= c:
        return 1.0
    if b <= x <= c:
        return 1.0
    if x <= a or x >= d:
        return 0.0
    if a < x < b:
        return (x - a) / (b - a)
    if c < x < d:
        return (d - x) / (d - c)
    return 0.0


def queue_low(x):
    return trapezoidal_membership(x, 0, 0, 2, 4)

def queue_medium(x):
    return trapezoidal_membership(x, 1, 3, 5, 7)

def queue_high(x):
    return trapezoidal_membership(x, 4, 6, 8, 8)


def wait_low(x):
    return trapezoidal_membership(x, 0, 0, 20, 40)

def wait_medium(x):
    return trapezoidal_membership(x, 20, 50, 80, 110)

def wait_high(x):
    return trapezoidal_membership(x, 90, 120, 200, 200)