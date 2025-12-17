from typing import List, Tuple, Set, Optional
import sys


class MazePathFinder:
    def __init__(self):
        self.maze = []
        self.n = 0
        self.m = 0
        self.start = None
        self.finish = None
        self.paths = []
        self.directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        self.direction_chars = ['↑', '↓', '←', '→']

    def read_maze_recursive(self, rows: List[str] = None) -> List[str]:
        """Рекурсивное чтение лабиринта из ввода"""
        if rows is None:
            rows = []

        try:
            line = input().strip()
            if not line:
                return rows
            return self.read_maze_recursive(rows + [line])
        except EOFError:
            return rows

    def validate_row_lengths(self, index: int = 0) -> bool:
        """Рекурсивная проверка длин строк"""
        if index >= self.n:
            return True

        if len(self.maze[index]) != self.m:
            print(f"Ошибка: строка {index} имеет длину {len(self.maze[index])}, ожидалось {self.m}")
            exit(1)

        return self.validate_row_lengths(index + 1)

    def find_start_finish_recursive(self, i: int = 0, j: int = 0) -> None:
        """Рекурсивный поиск старта и финиша"""
        if i >= self.n:
            return

        cell = self.maze[i][j]
        if cell == 'S':
            self.start = (i, j)
        elif cell == 'F':
            self.finish = (i, j)

        next_j = j + 1
        next_i = i

        if next_j >= self.m:
            next_j = 0
            next_i = i + 1

        self.find_start_finish_recursive(next_i, next_j)

    def read_maze(self) -> None:
        """Чтение лабиринта из ввода"""
        print("Введите лабиринт (пустые строки для завершения):")

        self.maze = self.read_maze_recursive()

        if not self.maze:
            print("Лабиринт не введен!")
            exit(1)

        self.n = len(self.maze)
        self.m = len(self.maze[0])

        self.validate_row_lengths()
        self.find_start_finish_recursive()

        if not self.start:
            print("Ошибка: старт (S) не найден!")
            exit(1)
        if not self.finish:
            print("Ошибка: финиш (F) не найден!")
            exit(1)

    def is_valid(self, x: int, y: int) -> bool:
        """Проверка, находится ли клетка в пределах лабиринта"""
        return 0 <= x < self.n and 0 <= y < self.m

    def is_passable(self, x: int, y: int) -> bool:
        """Можно ли пройти через клетку"""
        return self.is_valid(x, y) and self.maze[x][y] != '#'

    def dfs(self, x: int, y: int, visited: Set[Tuple[int, int]], path: List[Tuple[int, int]]) -> None:
        """Поиск в глубину для нахождения всех путей"""
        visited.add((x, y))
        path.append((x, y))

        if (x, y) == self.finish:
            self.paths.append(path.copy())
        else:
            if len(path) < self.n * self.m:
                # Рекурсивная обработка направлений
                def process_direction(idx: int = 0) -> None:
                    if idx >= len(self.directions):
                        return

                    dx, dy = self.directions[idx]
                    nx, ny = x + dx, y + dy

                    if self.is_passable(nx, ny) and (nx, ny) not in visited:
                        self.dfs(nx, ny, visited, path)

                    process_direction(idx + 1)

                process_direction()

        visited.remove((x, y))
        path.pop()

    def find_all_paths(self) -> None:
        """Нахождение всех путей"""
        visited = set()
        path = []
        self.dfs(self.start[0], self.start[1], visited, path)

    def get_path_length(self, path: List[Tuple[int, int]]) -> int:
        """Длина пути"""
        return len(path) - 1

    def get_path_directions_recursive(self, path: List[Tuple[int, int]], idx: int = 1, directions: List[str] = None) -> \
    List[str]:
        """Рекурсивное получение направлений движения"""
        if directions is None:
            directions = []

        if idx >= len(path):
            return directions

        x1, y1 = path[idx - 1]
        x2, y2 = path[idx]
        dx, dy = x2 - x1, y2 - y1

        def find_direction(dir_idx: int = 0) -> str:
            if dir_idx >= len(self.directions):
                return '?'

            dir_dx, dir_dy = self.directions[dir_idx]
            if dir_dx == dx and dir_dy == dy:
                return self.direction_chars[dir_idx]

            return find_direction(dir_idx + 1)

        directions.append(find_direction())
        return self.get_path_directions_recursive(path, idx + 1, directions)

    def format_path_recursive(self, path: List[Tuple[int, int]], idx: int = 0, result: str = "") -> str:
        """Рекурсивное форматирование пути для вывода"""
        if idx >= len(path):
            return result

        x, y = path[idx]

        if idx == 0:
            current = f"S({x},{y})"
        elif (x, y) == self.finish:
            current = f"F({x},{y})"
        else:
            current = f"({x},{y})"

        if idx == 0:
            new_result = current
        else:
            # Получаем направление для этого шага
            directions = self.get_path_directions_recursive(path)
            new_result = f"{result} {directions[idx - 1]} {current}"

        return self.format_path_recursive(path, idx + 1, new_result)

    def create_maze_with_path(self, path: List[Tuple[int, int]], display: List[List[str]] = None, idx: int = 1) -> List[
        List[str]]:
        """Рекурсивное создание лабиринта с отмеченным путем"""
        if display is None:
            display = [list(row) for row in self.maze]

        if idx >= len(path) - 1:
            return display

        x, y = path[idx]
        display[x][y] = '*'

        return self.create_maze_with_path(path, display, idx + 1)

    def print_maze_row(self, display: List[List[str]], row_idx: int = 0) -> None:
        """Рекурсивный вывод строк лабиринта"""
        if row_idx >= len(display):
            return

        print(''.join(display[row_idx]))
        self.print_maze_row(display, row_idx + 1)

    def print_maze_with_path(self, path: List[Tuple[int, int]]) -> None:
        """Вывод лабиринта с отмеченным путем"""
        display = self.create_maze_with_path(path)
        print("Лабиринт с путем:")
        self.print_maze_row(display)

    def quicksort_paths(self, paths: List[List[Tuple[int, int]]]) -> List[List[Tuple[int, int]]]:
        """Быстрая сортировка путей по длине"""
        if len(paths) <= 1:
            return paths

        pivot = paths[len(paths) // 2]
        pivot_length = self.get_path_length(pivot)

        left = []
        middle = []
        right = []

        def partition(idx: int = 0):
            if idx >= len(paths):
                return

            path = paths[idx]
            length = self.get_path_length(path)

            if length < pivot_length:
                left.append(path)
            elif length == pivot_length:
                middle.append(path)
            else:
                right.append(path)

            partition(idx + 1)

        partition()

        return self.quicksort_paths(left) + middle + self.quicksort_paths(right)

    def print_path_info(self, path: List[Tuple[int, int]], path_num: int) -> None:
        """Вывод информации об одном пути"""
        length = self.get_path_length(path)
        print(f"Путь {path_num} (длина {length}): {self.format_path_recursive(path)}")

    def print_all_paths(self, paths: List[List[Tuple[int, int]]], idx: int = 1) -> None:
        """Рекурсивный вывод всех путей"""
        if idx > len(paths):
            return

        self.print_path_info(paths[idx - 1], idx)
        self.print_all_paths(paths, idx + 1)

    def calculate_lengths(self, paths: List[List[Tuple[int, int]]], idx: int = 0, lengths: List[int] = None) -> List[
        int]:
        """Рекурсивный расчет длин всех путей"""
        if lengths is None:
            lengths = []

        if idx >= len(paths):
            return lengths

        lengths.append(self.get_path_length(paths[idx]))
        return self.calculate_lengths(paths, idx + 1, lengths)

    def quicksort_lengths(self, arr: List[int]) -> List[int]:
        """Быстрая сортировка длин"""
        if len(arr) <= 1:
            return arr

        pivot = arr[len(arr) // 2]

        left = []
        middle = []
        right = []

        def partition(idx: int = 0):
            if idx >= len(arr):
                return

            if arr[idx] < pivot:
                left.append(arr[idx])
            elif arr[idx] == pivot:
                middle.append(arr[idx])
            else:
                right.append(arr[idx])

            partition(idx + 1)

        partition()

        return self.quicksort_lengths(left) + middle + self.quicksort_lengths(right)

    def sum_list(self, arr: List[int], idx: int = 0, total: int = 0) -> int:
        """Рекурсивная сумма элементов списка"""
        if idx >= len(arr):
            return total

        return self.sum_list(arr, idx + 1, total + arr[idx])

    def print_results(self) -> None:
        """Вывод всех результатов"""
        if not self.paths:
            print("Пути от S до F не найдены!")
            return

        self.paths = self.quicksort_paths(self.paths)

        print(f"\nНайдено путей: {len(self.paths)}")
        print("-" * 50)

        print("Все пути от кратчайшего к самому длинному:")
        self.print_all_paths(self.paths)

        print("-" * 50)

        shortest_path = self.paths[0]
        shortest_length = self.get_path_length(shortest_path)
        print(f"Кратчайший путь (длина {shortest_length}):")
        print(self.format_path_recursive(shortest_path))
        self.print_maze_with_path(shortest_path)

        print("-" * 50)

        longest_path = self.paths[-1]
        longest_length = self.get_path_length(longest_path)
        print(f"Самый длинный путь (длина {longest_length}):")
        print(self.format_path_recursive(longest_path))
        self.print_maze_with_path(longest_path)

        print("-" * 50)

        lengths = self.calculate_lengths(self.paths)
        sorted_lengths = self.quicksort_lengths(lengths)
        total_length = self.sum_list(lengths)

        print(f"Длины всех путей: {sorted_lengths}")
        print(f"Средняя длина: {total_length / len(lengths):.2f}")

    def run(self) -> None:
        """Основной метод запуска программы"""
        print("=" * 60)
        print("ГЕНЕРАТОР ВСЕХ ПУТЕЙ В ЛАБИРИНТЕ (РЕКУРСИВНАЯ ВЕРСИЯ)")
        print("=" * 60)

        self.read_maze()
        print("\nПоиск всех возможных путей...")

        self.find_all_paths()
        self.print_results()


def main():
    finder = MazePathFinder()
    finder.run()


if __name__ == "__main__":
    main()