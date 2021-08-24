from enum import Enum
from typing import List, NamedTuple, Callable, Optional
import random
from math import sqrt
from generic_search import dfs, node_to_path, Node, bfs #astar


class Cell(str, Enum):
    EMPTY = " "
    BLOCKED = "X"
    START = "S"
    GOAL = "G"
    PATH = "*"


class MazeLocation(NamedTuple):
    row: int
    column: int


class Maze:
    def __init__(
        self,
        rows: int = 10,
        columns: int = 10,
        sparseness: float = 0.2,
        start: MazeLocation = MazeLocation(0, 0),
        goal: MazeLocation = MazeLocation(9, 9)
    ) -> None:
        self._rows: int = rows
        self._columns: int = columns
        self.start: MazeLocation = start
        self.goal: MazeLocation = goal
        # preenche a grade com células vazias
        self._grid: List[List[Cell]] = [
            [Cell.EMPTY for c in range(columns)] for r in range(rows)
        ]
        # preenche a grade com células bloqueadas
        self._randomly_fill(rows, columns, sparseness)
        # preenche as posições inicial e final
        self._grid[start.row][start.column] = Cell.START
        self._grid[goal.row][goal.column] = Cell.GOAL
    
    def _randomly_fill(self, rows: int, columns: int, sparseness: float):
        for row in range(rows):
            for column in range(columns):
                if random.uniform(0, 1.0) < sparseness:
                    self._grid[row][column] = Cell.BLOCKED
    
    def __str__(self) -> str:
        output: str = "------------\n"
        for row in self._grid:
            output += "|" + "".join([c.value for c in row]) + "|\n"
        output += "------------\n"
        return output
    
    def goal_test(self, ml: MazeLocation) -> bool:
        return ml == self.goal

    def successors(self, ml: MazeLocation) -> List[MazeLocation]:
        locations: List[MazeLocation] = []

        if (
            ml.row + 1 < self._rows
            and self._grid[ml.row + 1][ml.column] != Cell.BLOCKED
        ):
            locations.append(MazeLocation(ml.row + 1, ml.column))

        if (
            ml.row - 1 >= 0
            and self._grid[ml.row - 1][ml.column] != Cell.BLOCKED
        ):
            locations.append(MazeLocation(ml.row - 1, ml.column))

        if (
            ml.column + 1 < self._columns
            and self._grid[ml.row][ml.column + 1] != Cell.BLOCKED
        ):
            locations.append(MazeLocation(ml.row, ml.column + 1))

        if (
            ml.column - 1 >= 0
            and self._grid[ml.row][ml.column - 1] != Cell.BLOCKED
        ):
            locations.append(MazeLocation(ml.row, ml.column - 1))

        return locations
    
    def mark(self, path: List[MazeLocation]):
        for maze_location in path:
            self._grid[maze_location.row][maze_location.column] = Cell.PATH
        self._grid[self.start.row][self.start.column] = Cell.START
        self._grid[self.goal.row][self.goal.column] = Cell.GOAL
    
    def clear(self, path: List[MazeLocation]):
        for maze_location in path:
            self._grid[maze_location.row][maze_location.column] = Cell.EMPTY
        self._grid[self.start.row][self.start.column] = Cell.START
        self._grid[self.goal.row][self.goal.column] = Cell.GOAL


if __name__ == "__main__":
    # DFS - Pesquisa em profundidade
    maze: Maze = Maze()
    print(maze)

    solution_one: Optional[Node[MazeLocation]] = dfs(maze.start, maze.goal_test, maze.successors)
    if solution_one is None:
        print("No solution found using depth-first search!")
    else:
        path_one: List[MazeLocation] = node_to_path(solution_one)
        maze.mark(path_one)
        print(maze)
        maze.clear(path_one)

    solution_two: Optional[Node[MazeLocation]] = bfs(maze.start, maze.goal_test, maze.successors)
    if solution_two is None:
        print("No solution found using breadth-first search!")
    else:
        path_two: List[MazeLocation] = node_to_path(solution_two)
        maze.mark(path_two)
        print(maze)
        maze.clear(path_two)
