from collections import deque
from heapq import heappop, heappush
from typing import Optional

from campus_map import CAMPUS_GRAPH, COORDS, GRAPH_TYPE, HEURISTIC_AVAILABLE
from models.response import SEARCH_OUTPUT_TEMPLATE


def estimate_distance(source: Optional[str], destination: Optional[str]) -> int:
    # Estimate Manhattan distance using coordinates for heuristic use.
    # Returns 0 when inputs are missing or unknown.
    if not source or not destination:
        return 0
    if source not in COORDS or destination not in COORDS:
        return 0
    sx, sy = COORDS[source]
    dx, dy = COORDS[destination]
    return abs(sx - dx) + abs(sy - dy)


def select_algorithm(graph_type: str, heuristic_available: bool) -> str:
    # Select the operational search algorithm based on graph properties.
    # Follows the project policy for unweighted and weighted graphs.
    if graph_type == "unweighted":
        return "BFS"
    if heuristic_available:
        return "A*"
    return "UCS"


def reconstruct_path(came_from: dict, start: str, goal: str) -> list:
    # Reconstruct a path from a came_from map.
    # Returns an empty list when no path exists.
    if goal not in came_from:
        return []
    path = [goal]
    current = goal
    while current != start:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path


def bfs(graph: dict, start: str, goal: str) -> tuple[list, int]:
    # Run BFS for unweighted shortest path search.
    # Returns the path and hop-count cost.
    queue = deque([start])
    came_from = {start: None}

    while queue:
        current = queue.popleft()
        if current == goal:
            break
        for neighbor in graph.get(current, {}):
            if neighbor not in came_from:
                came_from[neighbor] = current
                queue.append(neighbor)

    path = reconstruct_path(came_from, start, goal)
    cost = len(path) - 1 if path else 0
    return path, cost


def ucs(graph: dict, start: str, goal: str) -> tuple[list, int]:
    # Run Uniform Cost Search on a weighted graph.
    # Returns the lowest-cost path and total cost.
    frontier = [(0, start)]
    came_from = {start: None}
    cost_so_far = {start: 0}

    while frontier:
        current_cost, current = heappop(frontier)
        if current == goal:
            break
        for neighbor, edge_cost in graph.get(current, {}).items():
            new_cost = current_cost + edge_cost
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                came_from[neighbor] = current
                heappush(frontier, (new_cost, neighbor))

    path = reconstruct_path(came_from, start, goal)
    cost = cost_so_far.get(goal, 0) if path else 0
    return path, cost


def a_star(graph: dict, start: str, goal: str) -> tuple[list, int]:
    # Run A* search using Manhattan distance as a heuristic.
    # Returns the lowest-cost path and total cost.
    frontier = [(0, start)]
    came_from = {start: None}
    cost_so_far = {start: 0}

    while frontier:
        _, current = heappop(frontier)
        if current == goal:
            break
        for neighbor, edge_cost in graph.get(current, {}).items():
            new_cost = cost_so_far[current] + edge_cost
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + estimate_distance(neighbor, goal)
                came_from[neighbor] = current
                heappush(frontier, (priority, neighbor))

    path = reconstruct_path(came_from, start, goal)
    cost = cost_so_far.get(goal, 0) if path else 0
    return path, cost


def find_route(
    source: Optional[str],
    destination: Optional[str],
    graph_type: Optional[str] = None,
) -> dict:
    # Compute a route using the operational algorithm policy.
    # Returns a standard search output object.
    output = SEARCH_OUTPUT_TEMPLATE.copy()

    if not source or not destination:
        return output
    if source not in CAMPUS_GRAPH or destination not in CAMPUS_GRAPH:
        return output

    graph_type = graph_type or GRAPH_TYPE
    algorithm = select_algorithm(graph_type, HEURISTIC_AVAILABLE)

    if algorithm == "BFS":
        path, cost = bfs(CAMPUS_GRAPH, source, destination)
    elif algorithm == "A*":
        path, cost = a_star(CAMPUS_GRAPH, source, destination)
    else:
        path, cost = ucs(CAMPUS_GRAPH, source, destination)

    output["algorithm_used"] = algorithm
    output["path"] = path
    output["cost"] = cost
    output["steps"] = len(path) - 1 if path else 0
    return output
