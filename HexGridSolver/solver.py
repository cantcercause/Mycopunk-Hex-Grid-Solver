def rotate(shape, times=1):
    for _ in range(times):
        shape = [(-q - r, q) for q, r in shape]
    return shape

def normalize(shape):
    min_q = min(q for q, r in shape)
    min_r = min(r for q, r in shape)
    return sorted([(q - min_q, r - min_r) for q, r in shape])

def can_place(board, shape, anchor):
    aq, ar = anchor
    positions = [(aq + dq, ar + dr) for dq, dr in shape]
    return all((q, r) in board for q, r in positions)

def place_shape(anchor, shape):
    aq, ar = anchor
    return {(aq + dq, ar + dr) for dq, dr in shape}

def solve_all(board, shapes, placed=None):
    if placed is None:
        placed = []

    if not shapes:
        return [placed]

    all_solutions = []
    shape = shapes[0]
    normalized_base = normalize(shape)
    tried = set()

    for rot in range(6):
        rotated = rotate(normalized_base, rot)
        norm_rotated = normalize(rotated)
        rot_key = tuple(norm_rotated)
        if rot_key in tried:
            continue
        tried.add(rot_key)

        for cell in board:
            if can_place(board, norm_rotated, cell):
                shape_cells = place_shape(cell, norm_rotated)
                new_board = board - shape_cells
                result = solve_all(new_board, shapes[1:], placed + [(norm_rotated, cell)])
                all_solutions.extend(result)

    return all_solutions
