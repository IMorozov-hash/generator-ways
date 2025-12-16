from typing import List, Tuple, Set


class MazePathFinder:
    def __init__(self):
        self.maze = []
        self.n = 0
        self.m = 0
        self.start = None
        self.finish = None
        self.paths = []
        self.directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Вверх, вниз, влево, вправо
        self.direction_chars = ['↑', '↓', '←', '→']

    def read_maze(self) -> None:
        """Чтение лабиринта из ввода"""
        print("Введите лабиринт (пустые строки для завершения):")
        rows = []

        while True:
            try:
                line = input().strip()
                if not line:
                    break
                rows.append(line)
            except EOFError:
                break

        if not rows:
            print("Лабиринт не введен!")
            exit(1)

        self.maze = rows
        self.n = len(rows)
        self.m = len(rows[0])

        # Проверка размеров
        for i in range(self.n):
            if len(self.maze[i]) != self.m:
                print(f"Ошибка: строка {i} имеет длину {len(self.maze[i])}, ожидалось {self.m}")
                exit(1)

        # Поиск старта и финиша
        for i in range(self.n):
            for j in range(self.m):
                if self.maze[i][j] == 'S':
                    self.start = (i, j)
                elif self.maze[i][j] == 'F':
                    self.finish = (i, j)

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
        # Добавляем текущую клетку в посещенные и путь
        visited.add((x, y))
        path.append((x, y))

        # Если достигли финиша
        if (x, y) == self.finish:
            self.paths.append(path.copy())
        else:
            # Максимальная длина пути для предотвращения бесконечной рекурсии
            if len(path) < self.n * self.m:
                # Пробуем все направления
                for dx, dy in self.directions:
                    nx, ny = x + dx, y + dy
                    if self.is_passable(nx, ny) and (nx, ny) not in visited:
                        self.dfs(nx, ny, visited, path)

        # Возврат (backtracking)
        visited.remove((x, y))
        path.pop()

    def find_all_paths(self) -> None:
        """Нахождение всех путей"""
        visited = set()
        path = []
        self.dfs(self.start[0], self.start[1], visited, path)

    def get_path_length(self, path: List[Tuple[int, int]]) -> int:
        """Длина пути (количество шагов от S до F)"""
        return len(path) - 1  # -1 потому что начальная клетка не считается шагом

    def get_path_directions(self, path: List[Tuple[int, int]]) -> List[str]:
        """Получение направления движения для каждого шага"""
        directions = []
        for i in range(1, len(path)):
            x1, y1 = path[i - 1]
            x2, y2 = path[i]
            dx, dy = x2 - x1, y2 - y1

            for dir_idx, (dir_dx, dir_dy) in enumerate(self.directions):
                if dir_dx == dx and dir_dy == dy:
                    directions.append(self.direction_chars[dir_idx])
                    break

        return directions

    def format_path(self, path: List[Tuple[int, int]]) -> str:
        """Форматирование пути для вывода"""
        if not path:
            return "Путь пуст"

        # Получаем направления
        directions = self.get_path_directions(path)

        # Формируем строку пути
        result = f"S({path[0][0]},{path[0][1]})"
        for i in range(1, len(path)):
            result += f" {directions[i - 1]} "
            if (path[i][0], path[i][1]) == self.finish:
                result += f"F({path[i][0]},{path[i][1]})"
            else:
                result += f"({path[i][0]},{path[i][1]})"

        return result

    def print_maze_with_path(self, path: List[Tuple[int, int]]) -> None:
        """Вывод лабиринта с отмеченным путем"""
        # Создаем копию лабиринта для отображения
        display = [list(row) for row in self.maze]

        # Отмечаем путь (кроме старта и финиша)
        for i in range(1, len(path) - 1):
            x, y = path[i]
            display[x][y] = '*'

        # Выводим лабиринт
        print("Лабиринт с путем:")
        for row in display:
            print(''.join(row))

    def print_results(self) -> None:
        """Вывод всех результатов"""
        if not self.paths:
            print("Пути от S до F не найдены!")
            return

        # Сортируем пути по длине
        self.paths.sort(key=lambda p: self.get_path_length(p))

        print(f"\nНайдено путей: {len(self.paths)}")
        print("-" * 50)

        # Выводим все пути с их длинами
        print("Все пути от кратчайшего к самому длинному:")
        for i, path in enumerate(self.paths, 1):
            length = self.get_path_length(path)
            print(f"Путь {i} (длина {length}): {self.format_path(path)}")

        print("-" * 50)

        # Кратчайший путь
        shortest_path = self.paths[0]
        shortest_length = self.get_path_length(shortest_path)
        print(f"Кратчайший путь (длина {shortest_length}):")
        print(self.format_path(shortest_path))
        self.print_maze_with_path(shortest_path)

        print("-" * 50)

        # Самый длинный путь
        longest_path = self.paths[-1]
        longest_length = self.get_path_length(longest_path)
        print(f"Самый длинный путь (длина {longest_length}):")
        print(self.format_path(longest_path))
        self.print_maze_with_path(longest_path)

        print("-" * 50)

        # Статистика по длинам
        lengths = [self.get_path_length(path) for path in self.paths]
        print(f"Длины всех путей: {sorted(lengths)}")
        print(f"Средняя длина: {sum(lengths) / len(lengths):.2f}")

    def run(self) -> None:
        """Основной метод запуска программы"""
        print("=" * 60)
        print("ГЕНЕРАТОР ВСЕХ ПУТЕЙ В ЛАБИРИНТЕ (БЕЗ ЦИКЛОВ)")
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