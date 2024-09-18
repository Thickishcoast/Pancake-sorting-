import sys
from collections import deque
import heapq

# Define the goal state
GOAL_STATE = "1w2w3w4w"

def parse_input(input_str):
    
    try:
        state_part, algo = input_str.strip().split('-')
        # Validate the algorithm choice
        if algo not in ['b', 'a']:
            raise ValueError("Algorithm must be 'b' for BFS or 'a' for A*.")
        # Validate the state length
        if len(state_part) != 8:
            raise ValueError("State must be 8 characters long (e.g., '1w2b3w4b').")
        # Validate each pancake part
        for i in range(0, 8, 2):
            if not state_part[i].isdigit() or state_part[i+1] not in ['w', 'b']:
                raise ValueError("Each pancake must have an ID followed by 'w' or 'b'.")
        return state_part, algo
    except ValueError as ve:
        print(f"Invalid input format: {ve}")
        sys.exit(1)

def flip(state, position):
    
    # Extract pancakes as list of tuples (id, side)
    pancakes = [state[i:i+2] for i in range(0, len(state), 2)]
    # Flip the top 'position' pancakes
    flipped = pancakes[:position]
    flipped = flipped[::-1]  # Reverse the order
    # Flip the side of each pancake
    flipped = [pancake[0] + ('w' if pancake[1] == 'b' else 'b') for pancake in flipped]
    new_pancakes = flipped + pancakes[position:]
    return ''.join(new_pancakes)

def heuristic(state):
    
    # Extract the pancake IDs by ignoring orientation
    ids = [int(state[i*2]) for i in range(4)]
    # Iterate from largest to smallest pancake
    for i in range(3, -1, -1):
        if ids[i] != i+1:
            return i+1  # ID of the largest out-of-order pancake
    return 0  # All pancakes are in correct order

def tie_breaker(state):
    
    num = ''
    for i in range(4):
        num += state[i*2]
        num += '1' if state[i*2+1] == 'w' else '0'
    return int(num)

def bfs(initial_state):
    
    queue = deque()
    queue.append((initial_state, []))
    visited = set()
    visited.add(initial_state)
    
    while queue:
        current, path = queue.popleft()
        
        if current == GOAL_STATE:
            return path + [current]
        
        for pos in range(1, 5):
            next_state = flip(current, pos)
            if next_state not in visited:
                visited.add(next_state)
                queue.append((next_state, path + [current]))
    return []  # No solution found

def a_star(initial_state):
    
    # Initialize the fringe as a priority queue (min-heap)
    fringe = []
    # Heap elements are tuples: (f, tie_breaker, g, state)
    g_costs = {initial_state: 0}
    h = heuristic(initial_state)
    heapq.heappush(fringe, (h, tie_breaker(initial_state), 0, initial_state))
    # Dictionary to keep track of parent states and the flip that led to the state
    parent = {initial_state: (None, None)}  # state: (parent_state, flip_position)

    while fringe:
        f, tb, g, current = heapq.heappop(fringe)

        if current == GOAL_STATE:
            # Reconstruct the path with g and h values
            path = []
            state = current
            while state:
                current_g = g_costs[state]
                current_h = heuristic(state)
                path.append((state, current_g, current_h))
                parent_info = parent[state]
                state = parent_info[0]
            return path[::-1]  # Reverse to get path from start to goal

        # If this state has already been expanded with a lower g, skip
        if g > g_costs.get(current, float('inf')):
            continue

        # Explore all possible flips (positions 1 to 4)
        for pos in range(1, 5):
            next_state = flip(current, pos)
            flip_cost = pos  # Cost is equal to the number of pancakes flipped
            tentative_g = g + flip_cost

            # If this path to next_state is better, or next_state not seen before
            if tentative_g < g_costs.get(next_state, float('inf')):
                g_costs[next_state] = tentative_g
                h = heuristic(next_state)
                f_new = tentative_g + h
                heapq.heappush(fringe, (f_new, tie_breaker(next_state), tentative_g, next_state))
                parent[next_state] = (current, pos)

    return []  # No solution found

def reconstruct_a_star_path(path):
    
    output = []
    for i in range(len(path)-1):
        current, g, h = path[i]
        next_state, _, _ = path[i+1]
        flip_pos = determine_flip_position(current, next_state)
        formatted_state = insert_flip_marker(current, flip_pos)
        output.append(f"{formatted_state} g:{g}, h:{h}")
    # Add the goal state with its g and h
    goal_state, final_g, final_h = path[-1]
    output.append(f"{goal_state} g:{final_g}, h:{final_h}")
    return output

def reconstruct_bfs_path(path):
    
    output = []
    for i in range(len(path)-1):
        current = path[i]
        next_state = path[i+1]
        # Find the flip position by comparing the two states
        for pos in range(1,5):
            if flip(current, pos) == next_state:
                # Insert '|' at the flip position
                output_state = current[:2*pos] + '|' + current[2*pos:]
                output.append(output_state)
                break
    output.append(path[-1])  # Goal state
    return output

def determine_flip_position(current, next_state):
   
    # To accurately determine the flip position, compare the two states and find the position where
    # the next_state has the top 'flip_pos' pancakes flipped from current
    for pos in range(1, 5):
        flipped = flip(current, pos)
        if flipped == next_state:
            return pos
    return 4  # Default to flipping all if no difference found

def insert_flip_marker(state, flip_position):
    
    pos = flip_position * 2
    return state[:pos] + '|' + state[pos:]
