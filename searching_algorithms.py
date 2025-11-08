from itertools import count
from utils import *
from collections import deque
from queue import PriorityQueue
from grid import Grid
from spot import Spot
import math


def reconstruct_path(came_from: dict, current: Spot, draw: callable):
    while current in came_from:
        current=came_from[current]
        current.make_path()
        draw()


def bfs(draw: callable, grid: Grid, start: Spot, end: Spot) -> bool:
    if start==end:
        return True

    for row in grid.grid:
        for spot in row:
            spot.update_neighbors(grid.grid)

    queue=deque([start])
    came_from ={}
    visited={start}

    while queue:
        draw()
        current=queue.popleft()

        if current==end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
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
    if start==end:
        return True

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
    x1, y1=p1
    x2, y2=p2
    return abs(x1-x2)+abs(y1-y2)


def h_euclidian_distance(p1: tuple[int, int], p2: tuple[int, int]) -> float:
    x1, y1=p1
    x2, y2=p2
    return math.sqrt((x1-x2)**2+(y1-y2)**2)


def astar(draw: callable, grid: Grid, start: Spot, end: Spot) -> bool:
    if start==end:
        return True

    for row in grid.grid:
        for spot in row:
            spot.update_neighbors(grid.grid)

    counter=count()
    open_set=PriorityQueue()
    open_set.put((0, next(counter), start))
    came_from={}

    g_score={spot: float("inf") for row in grid.grid for spot in row}
    g_score[start]=0

    f_score={spot: float("inf") for row in grid.grid for spot in row}
    f_score[start]=h_manhattan_distance(start.get_position(), end.get_position())

    open_set_hash={start}

    while not open_set.empty():
        draw()
        current=open_set.get()[2]
        open_set_hash.discard(current)

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
                    open_set.put((f_score[neighbor], next(counter), neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        if current!=start:
            current.make_closed()

    return False


def depth_limited_search(draw, grid: Grid, current: Spot, end: Spot, came_from: dict, limit: int, depth: int = 0) -> bool:
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


def dls(draw: callable, grid: Grid, start: Spot, end: Spot, limit: int=100) -> bool:
    for row in grid.grid:
        for spot in row:
            spot.update_neighbors(grid.grid)

    came_from={}
    success=depth_limited_search(draw, grid, start, end, came_from, limit)
    start.make_start()
    end.make_end()
    return success


def ucs(draw: callable, grid: Grid, start: Spot, end: Spot) -> bool:
    if start==end:
        return True

    for row in grid.grid:
        for spot in row:
            spot.update_neighbors(grid.grid)

    pq=PriorityQueue()
    tie=count()
    pq.put((0, next(tie), start))
    came_from={}
    cost={spot: float("inf") for row in grid.grid for spot in row}
    cost[start]=0
    visited=set()

    while not pq.empty():
        draw()
        current_cost, _, current=pq.get()
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
                pq.put((new_cost, next(tie), neighbor))
                neighbor.make_open()

        if current!=start:
            current.make_closed()

    return False


def greedy(draw: callable, grid: Grid, start: Spot, end: Spot, heuristic=h_euclidian_distance) -> bool:
    if start==end:
        return True

    for row in grid.grid:
        for spot in row:
            spot.update_neighbors(grid.grid)

    pq=PriorityQueue()
    tie=count()
    pq.put((heuristic(start.get_position(), end.get_position()), next(tie), start))
    came_from={}
    visited={start}

    while not pq.empty():
        draw()
        _, _, current=pq.get()

        if current==end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            if neighbor not in visited and not neighbor.is_barrier():
                visited.add(neighbor)
                came_from[neighbor]=current
                priority=heuristic(neighbor.get_position(), end.get_position())
                pq.put((priority, next(tie), neighbor))
                neighbor.make_open()

        if current!=start:
            current.make_closed()

    return False


def iddfs(draw: callable, grid: Grid, start: Spot, end: Spot, max_depth: int=200) -> bool:
    for depth in range(max_depth+1):
        for row in grid.grid:
            for spot in row:
                spot.update_neighbors(grid.grid)
        came_from={}
        if depth_limited_search(draw, grid, start, end, came_from, depth):
            start.make_start()
            end.make_end()
            return True
    return False


def ida(draw: callable, grid: Grid, start: Spot, end: Spot, heuristic=h_manhattan_distance) -> bool:
    if start==end:
        return True

    for row in grid.grid:
        for spot in row:
            spot.update_neighbors(grid.grid)

    def search(current, g, bound, came_from):
        f=g+heuristic(current.get_position(), end.get_position())
        if f>bound:
            return f
        if current==end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True

        min_bound=float("inf")
        for neighbor in current.neighbors:
            if neighbor.is_barrier() or neighbor in came_from:
                continue
            came_from[neighbor]=current
            neighbor.make_open()
            draw()
            result=search(neighbor, g+1, bound, came_from)
            if result is True:
                return True
            if isinstance(result, (int, float)) and result<min_bound:
                min_bound=result
            neighbor.make_closed()
            came_from.pop(neighbor, None)
        return min_bound

    bound=heuristic(start.get_position(), end.get_position())
    while True:
        came_from={start: None}
        result=search(start, 0, bound, came_from)
        if result is True:
            return True
        if result==float("inf"):
            return False
        bound=result
