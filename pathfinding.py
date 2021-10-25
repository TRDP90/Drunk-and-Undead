from math import sqrt
from queue import PriorityQueue
from map import Map


class Node:
    def __init__(self, x_tile, y_tile, x_goal_tile, y_goal_tile):

        self.neighbours = []
        self.cost = Map().costmap
        self.x_max = 25
        self.y_max = 30
        self.x_tile = x_tile
        self.y_tile = y_tile
        self.x_goal_tile = x_goal_tile
        self.y_goal_tile = y_goal_tile

    def euclidian(self, world_node, world_goal):

        p2x = world_goal[0]

        p1x = world_node[0]

        p2y = world_goal[1]
        p1y = world_node[1]

        return sqrt((p2x - p1x) ** 2 + (p2y - p1y) ** 2)

    def heuristic(self, x_start, y_start):
        dx = abs(x_start - self.x_goal_tile)
        dy = abs(y_start - self.y_goal_tile)
        return sqrt(dx * dx + dy * dy)

    def update_neighbours(self, x_tile, y_tile):

        self.neighbours = []
        # DOWN
        lower_neighbour = (x_tile, y_tile + 1)

        if -1 < x_tile < self.x_max:
            if -1 < y_tile + 1 < self.y_max:
                if self.cost[y_tile + 1][x_tile] < 100:
                    self.neighbours.append(lower_neighbour)
        # UP
        upper_neighbour = (x_tile, y_tile - 1)

        if -1 < x_tile < self.x_max:
            if -1 < y_tile - 1 < self.y_max:
                if self.cost[y_tile - 1][x_tile] < 100:
                    self.neighbours.append(upper_neighbour)
        # LEFT
        left_neighbour = (x_tile - 1, y_tile)

        if -1 < x_tile - 1 < self.x_max:
            if -1 < y_tile < self.y_max:
                if self.cost[y_tile][x_tile - 1] < 100:
                    self.neighbours.append(left_neighbour)
        # RIGHT
        right_neighbour = (x_tile + 1, y_tile)

        if -1 < x_tile + 1 < self.x_max:
            if -1 < y_tile < self.y_max:
                if self.cost[y_tile][x_tile + 1] < 100:
                    self.neighbours.append(right_neighbour)

    def a_star_search(self, start, goal):
        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0

        while not frontier.empty():
            current_tile = frontier.get()
            self.update_neighbours(current_tile[0], current_tile[1])

            if current_tile == goal:
                break

            for next in self.neighbours:
                new_cost = cost_so_far[current_tile] + self.cost[next[1]][next[0]]
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost

                    priority = new_cost + self.heuristic(next[0], next[1])
                    frontier.put(next, priority)
                    came_from[next] = current_tile

        return self.reconstruct_path(came_from, start, goal)

    def reconstruct_path(self, came_from, start, goal):
        current = goal
        path = []
        while current != start:
            path.append(current)
            current = came_from[current]
        path.reverse()
        return path
