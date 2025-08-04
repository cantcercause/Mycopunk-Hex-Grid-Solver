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

def solve_shapes(board, shapes, placed=[]):
    if not shapes:
        return placed

    shape = shapes[0]
    for rot in range(6):
        rotated = normalize(rotate(shape, rot))
        for cell in board:
            if can_place(board, rotated, cell):
                shape_cells = place_shape(cell, rotated)
                new_board = board - shape_cells
                result = solve_shapes(new_board, shapes[1:], placed + [(rotated, cell)])
                if result:
                    return result
    return None
