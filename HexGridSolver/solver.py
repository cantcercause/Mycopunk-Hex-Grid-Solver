import random

def rotate(shape, times=1):
    for _ in range(times):
        shape = [(-q - r, q) for q, r in shape]
    return shape

def normalize(shape):
    min_q = min(q for q, r in shape)
    min_r = min(r for q, r in shape)
    return sorted((q - min_q, r - min_r) for q, r in shape)

def can_place(board, shape, anchor):
    aq, ar = anchor
    return all((aq + dq, ar + dr) in board for dq, dr in shape)

def place_shape(anchor, shape):
    aq, ar = anchor
    return {(aq + dq, ar + dr) for dq, dr in shape}

def generate_rotations(shape):
    """Return a list of all 6 unique normalized rotations."""
    rotations = set()
    current = normalize(shape)
    for _ in range(7):
        current = rotate(current)
        normalized = tuple(normalize(current))
        rotations.add(normalized)
    return [list(r) for r in rotations]

def solve_all(board, shapes, placed=None):
    if placed is None:
        placed = []

    if not shapes:
        return [placed]

    # Early pruning
    if sum(len(s) for s in shapes) > len(board):
        return []

    all_solutions = []
    shape = shapes[0]

    for rotated in generate_rotations(shape):
        for anchor in board:
            if can_place(board, rotated, anchor):
                shape_cells = place_shape(anchor, rotated)
                new_board = board - shape_cells
                result = solve_all(new_board, shapes[1:], placed + [(rotated, anchor)])
                all_solutions.extend(result)

    return all_solutions
