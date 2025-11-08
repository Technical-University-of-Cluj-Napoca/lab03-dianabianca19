from itertools import count

from utils import *
from collections import deque
from queue import PriorityQueue
from grid import Grid
from spot import Spot
import math

def reconstruct_path(came_from:dict, current:Spot, draw:callable):
    while current in came_from:
        current=came_from[current]
        current.make_path()
        draw()

def bfs(draw: callable, grid: Grid, start: Spot, end: Spot) -> bool:
    """
    Breadth-First Search (BFS) Algorithm.
    Args:
        draw (callable): A function to call to update the Pygame window.
        grid (Grid): The Grid object containing the spots.
        start (Spot): The starting spot.
        end (Spot): The ending spot.
    Returns:
        bool: True if a path is found, False otherwise.
    """
    for row in grid.grid:
        for spot in row:
            spot.update_neighbors(grid.grid)

    queue=deque([start])
    came_from={}
    visited={start}

    while queue:
        draw()
        current=queue.popleft()

        if current==end:
            reconstruct_path(came_from, end, draw)
            start.make_start()
            return True

        for neighbor in current.neighbors:
            if neighbor not in visited and not neighbor.is_barrier():
                visited.add(neighbor)
                came_from[neighbor]=current
                queue.append(neighbor)
                neighbor.make_open()

        if current!=start:
            current.make_closed()

    return False

def dfs(draw: callable, grid: Grid, start: Spot, end: Spot) -> bool:
    """
    Depdth-First Search (DFS) Algorithm.
    Args:
        draw (callable): A function to call to update the Pygame window.
        grid (Grid): The Grid object containing the spots.
        start (Spot): The starting spot.
        end (Spot): The ending spot.
    Returns:
        bool: True if a path is found, False otherwise.
    """
    for row in grid.grid:
        for spot in row:
            spot.update_neighbors(grid.grid)

    stack=[start]
    came_from={}
    visited={start}

    while stack:
        draw()
        current=stack.pop()

        if current==end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            if neighbor not in visited and not neighbor.is_barrier():
                visited.add(neighbor)
                came_from[neighbor]=current
                stack.append(neighbor)
                neighbor.make_open()

        if current!=start:
            current.make_closed()

    return False


def h_manhattan_distance(p1: tuple[int, int], p2: tuple[int, int]) -> float:
    """
    Heuristic function for A* algorithm: uses the Manhattan distance between two points.
    Args:
        p1 (tuple[int, int]): The first point (x1, y1).
        p2 (tuple[int, int]): The second point (x2, y2).
    Returns:
        float: The Manhattan distance between p1 and p2.
    """
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1-x2)+abs(y1-y2)


def h_euclidian_distance(p1: tuple[int, int], p2: tuple[int, int]) -> float:
    """
    Heuristic function for A* algorithm: uses the Euclidian distance between two points.
    Args:
        p1 (tuple[int, int]): The first point (x1, y1).
        p2 (tuple[int, int]): The second point (x2, y2).
    Returns:
        float: The Manhattan distance between p1 and p2.
    """
    x1, y1 = p1
    x2, y2 = p2
    return math.sqrt((x1-x2)**2+(y1-y2)**2)


def astar(draw: callable, grid: Grid, start: Spot, end: Spot) -> bool:
    """
    A* Pathfinding Algorithm.
    Args:
        draw (callable): A function to call to update the Pygame window.
        grid (Grid): The Grid object containing the spots.
        start (Spot): The starting spot.
        end (Spot): The ending spot.
    Returns:
        bool: True if a path is found, False otherwise.
    """
    for row in grid.grid:
        for spot in row:
            spot.update_neighbors(grid.grid)

    count=0
    open_set=PriorityQueue()
    open_set.put((0, count, start))
    came_from={}

    g_score={spot:float("inf") for row in grid.grid for spot in row}
    g_score[start]=0

    f_score={spot:float("inf") for row in grid.grid for spot in row}
    f_score[start]=h_manhattan_distance(start.get_position(), end.get_position())

    open_set_hash={start}

    while not open_set.empty():
        draw()
        current=open_set.get()[2]

        if current in open_set_hash:
            open_set_hash.remove(current)

        if current==end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            temp_g_score=g_score[current]+1

            if temp_g_score<g_score[neighbor]:
                came_from[neighbor]=current
                g_score[neighbor]=temp_g_score
                f_score[neighbor]=temp_g_score+h_manhattan_distance(neighbor.get_position(), end.get_position())

                if neighbor not in open_set_hash:
                    count=count+1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        if current!=start:
            current.make_closed()

    return False

def depth_limited_search(draw, grid: Grid, current: Spot, end: Spot, came_from: dict, limit: int, depth: int=0)->bool:

    """recursive helper function for dls"""

    draw()

    if current==end:
        reconstruct_path(came_from, end, draw)
        end.make_end()
        return True

    if depth>=limit:
        return False

    for neighbor in current.neighbors:
        if neighbor not in came_from and not neighbor.is_barrier():
            came_from[neighbor]=current
            neighbor.make_open()
            if depth_limited_search(draw, grid, neighbor, end, came_from, limit, depth+1):
                return True
            neighbor.make_closed()

    return False

def dls(draw: callable, grid: Grid, start: Spot, end: Spot, limit: int=10)->bool:
    for row in grid.grid:
        for spot in row:
            spot.update_neighbors(grid.grid)

    came_from={}
    success=depth_limited_search(draw, grid, start, end, came_from, limit)
    start.make_end()
    end.make_end()
    return success

def ucs(draw: callable, grid: Grid, start: Spot, end: Spot)->bool:
    for row in grid.grid:
        for spot in row:
            spot.update_neighbors(grid.grid)

    pq=PriorityQueue()
    pq.put((0, start))
    came_from={}
    cost={spot:float("inf") for row in grid.grid for spot in row}
    cost[start]=0
    visited=set()

    while not pq.empty():
        draw()
        current_cost, current=pq.get()
        if current in visited:
            continue

        visited.add(current)

        if current==end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            new_cost=current_cost+1
            if new_cost<cost[neighbor]:
                cost[neighbor]=new_cost
                came_from[neighbor]=current
                pq.put((new_cost, neighbor))
                neighbor.make_open()

            if current!=start:
                current.make_closed()

    return False


# Depth-Limited Search (DLS)
# ▢ Uninformed Cost Search (UCS)
# ▢ Greedy Search
# ▢ Iterative Deepening Search/Iterative Deepening Depth-First Search (IDS/IDDFS)
# ▢ Iterative Deepening A* (IDA)
# Assume that each edge (graph weight) equalss