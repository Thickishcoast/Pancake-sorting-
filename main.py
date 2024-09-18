# main.py

from pancake_solver import parse_input, bfs, a_star, reconstruct_bfs_path, reconstruct_a_star_path

def main():
    input_str = input().strip()
    initial_state, algo = parse_input(input_str)

    if algo == 'b':
        solution_path = bfs(initial_state)
        if not solution_path:
            print("No solution found using BFS.")
            return
        formatted_output = reconstruct_bfs_path(solution_path)
    elif algo == 'a':
        solution_path = a_star(initial_state)
        if not solution_path:
            print("No solution found using A* Search.")
            return
        formatted_output = reconstruct_a_star_path(solution_path)
    else:
        print("Invalid algorithm choice. Use 'b' for BFS or 'a' for A*.")
        return

    for line in formatted_output:
        print(line)

if __name__ == "__main__":
    main()
