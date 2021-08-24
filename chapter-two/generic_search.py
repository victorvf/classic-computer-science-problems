from __future__ import annotations
from typing import (
    TypeVar,
    Iterable,
    Sequence,
    Generic,
    List,
    Callable,
    Set,
    Deque,
    Any,
    Optional,
    Protocol,
)  # Dict

# from heapq import heappush, heappop

T = TypeVar("T")


def linear_contains(iterable: Iterable[T], key: T) -> bool:
    for item in iterable:
        if item == key:
            return True
    return False


C = TypeVar("C", bound="Comparable")


# Interface para implementar os operadores comparação em um tipo.
class Comparable(Protocol):
    def __eq__(self, other: Any) -> bool:
        ...

    def __lt__(self: C, other: C) -> bool:
        ...

    def __gt__(self: C, other: C) -> bool:
        return (not self < other) and self != other

    def __le__(self: C, other: C) -> bool:
        return self < other or self == other

    def __ge__(self: C, other: C) -> bool:
        return not self < other


def binary_contains(sequence: Sequence[C], key: C) -> bool:
    low: int = 0
    high: int = len(sequence) - 1
    while low <= high:  # enquanto ainda houver um espaço para pesquisa
        mid: int = (low + high) // 2
        if sequence[mid] < key:
            low = mid + 1
        elif sequence[mid] > key:
            high = mid - 1
        else:
            return True
    return False


class Stack(Generic[T]):
    def __init__(self) -> None:
        self._container: List[T] = []

    @property
    def empty(self) -> bool:
        return not self._container

    def push(self, item: T) -> None:
        self._container.append(item)

    def pop(self) -> T:
        return self._container.pop()

    def __repr__(self) -> str:
        return repr(self._container)


class Node(Generic[T]):
    def __init__(
        self,
        state: T,
        parent: Optional[Node],
        cost: float = 0.0,
        heuristic: float = 0.0,
    ) -> None:
        self.state: T = state
        self.parent: Optional[Node] = parent
        self.cost: float = cost
        self.heuristic: float = heuristic

    def __lt__(self, other: Node) -> bool:
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)


def dfs(
    initial: T,
    goal_test: Callable[[T], bool],
    successors: Callable[[T], List[T]],
) -> Optional[Node[T]]:
    # frontier corresponde os lugares que ainda não visitamos
    frontier: Stack[Node[T]] = Stack()
    frontier.push(Node(initial, None))

    # explored representa os lugares em que já estivemos
    explored: Set[T] = {initial}

    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        current_state: T = current_node.state

        # se encontrarmos o objetivo, terminamos
        if goal_test(current_state):
            return current_node

        # verifica para onde podemos ir em seguida e que ainda não tenha sido
        # explorado
        for child in successors(current_state):
            # ignora os filhos que já tenham sido explorados
            if child in explored:
                continue
            explored.add(child)
            frontier.push(Node(child, current_node))

    return None  # passamos por todos os lugares e não atingimos o objetivo


def node_to_path(node: Node[T]) -> List[T]:
    path: List[T] = [node.state]

    # trabalha no sentido inverso, fo final para o início
    while node.parent is not None:
        node = node.parent
        path.append(node.state)

    path.reverse()
    return path


class Queue(Generic[T]):
    def __init__(self) -> None:
        self._container: Deque[T] = Deque()

    @property
    def empty(self) -> bool:
        # negação é verdadeira para um container vazio
        return not self._container

    def push(self, item: T) -> None:
        self._container.append(item)

    def pop(self) -> T:
        return self._container.popleft()  # FIFO

    def __repr__(self) -> str:
        return repr(self._container)


def bfs(
    initial: T,
    goal_test: Callable[[T], bool],
    successors: Callable[[T], List[T]],
) -> Optional[Node[T]]:
    # Frontier corresponde aos lugares que ainda devemos visitar
    frontier: Queue[Node[T]] = Queue()
    frontier.push(Node(initial, None))

    # explored respresenta os lugares em que já estivemos
    explored: Set[T] = {initial}

    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        current_state: T = current_node.state

        if goal_test(current_state):
            return current_node

        for child in successors(current_state):
            if child in explored:
                continue
            explored.add(child)
            frontier.push(Node(child, current_node))

    return None


if __name__ == "__main__":
    print(linear_contains([1, 5, 15, 15, 15, 20], 5))
    print(binary_contains(["a", "d", "e", "f", "z"], "f"))
    print(binary_contains(["john", "mark", "ronald", "sarah"], "sheila"))
