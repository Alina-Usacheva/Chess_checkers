from figures_moves import Moves


class FigureAbstract:
    def __init__(self, name: str, colour: str, possible_moves: list, coordinates: list):
        self.__name = name
        self.__colour = colour
        self.__possible_moves = possible_moves
        self.__type = False  # используется для реализации взятия пешки на проходе и рокировки
        self.__coordinates = coordinates

    def get_coords(self) -> list:
        return self.__coordinates

    def get_name(self) -> str:
        return self.__name

    def get_colour(self) -> str:
        return self.__colour

    def get_possible_moves(self) -> list:
        return self.__possible_moves

    def get_type_figure(self) -> bool:
        return self.__type

    def set_coords(self, x, y):
        self.__coordinates = [x, y]

    def change_figure_type(self):
        if self.get_type_figure() is False:
            self.__type = True
        elif self.get_type_figure() is True:
            self.__type = False


class Queen(FigureAbstract):
    def __init__(self, name: str, colour: str, possible_moves: list, coordinates: list):
        super().__init__(name, colour, possible_moves, coordinates)


class King(FigureAbstract):
    def __init__(self, name: str, colour: str, possible_moves: list, coordinates: list):
        super().__init__(name, colour, possible_moves, coordinates)


class Knight(FigureAbstract):
    def __init__(self, name: str, colour: str, possible_moves: list, coordinates: list):
        super().__init__(name, colour, possible_moves, coordinates)


class Bishop(FigureAbstract):
    def __init__(self, name: str, colour: str, possible_moves: list, coordinates: list):
        super().__init__(name, colour, possible_moves, coordinates)


class Rook(FigureAbstract):
    def __init__(self, name: str, colour: str, possible_moves: list, coordinates: list):
        super().__init__(name, colour, possible_moves, coordinates)


class Pawn(FigureAbstract):
    def __init__(self, name: str, colour: str, possible_moves: list, coordinates: list):
        super().__init__(name, colour, possible_moves, coordinates)


class Checker(FigureAbstract):
    def __init__(self, name: str, colour: str, possible_moves: list, coordinates: list):
        super().__init__(name, colour, possible_moves, coordinates)


class QueensChecker(Checker):
    def __init__(self, name: str, colour: str, possible_moves: list, coordinates: list):
        super().__init__(name, colour, possible_moves, coordinates)


figures = {
    'Q_w': Queen('Q_w', 'w', Moves.queen_moves(), [0, 3]),
    'K_w': King('K_w', 'w', [[0, -1], [0, 1], [-1, 0], [1, 0], [1, 1], [-1, -1], [-1, 1], [1, -1]], [0, 4]),
    'R1w': Rook('R1w', 'w', Moves.rook_moves(), [0, 0]),
    'R2w': Rook('R2w', 'w', Moves.rook_moves(), [0, 7]),
    'B1w': Bishop('B1w', 'w', Moves.bishop_moves(), [0, 2]),
    'B2w': Bishop('B2w', 'w', Moves.bishop_moves(), [0, 5]),
    'N1w': Knight('N1w', 'w', [[1, -2], [-1, -2], [1, 2], [-1, 2], [-2, 1], [-2, -1], [2, 1], [2, -1]], [0, 1]),
    'N2w': Knight('N2w', 'w', [[1, -2], [-1, -2], [1, 2], [-1, 2], [-2, 1], [-2, -1], [2, 1], [2, -1]], [0, 6]),
    'Q_b': Queen('Q_b', 'b', Moves.queen_moves(), [7, 3]),
    'K_b': King('K_b', 'b', [[0, -1], [0, 1], [-1, 0], [1, 0], [1, 1], [-1, -1], [-1, 1], [1, -1]], [7, 4]),
    'R1b': Rook('R1b', 'b', Moves.rook_moves(), [7, 0]),
    'R2b': Rook('R2b', 'b', Moves.rook_moves(), [7, 7]),
    'B1b': Bishop('B1b', 'b', Moves.bishop_moves(), [7, 2]),
    'B2b': Bishop('B2b', 'b', Moves.bishop_moves(), [7, 5]),
    'N1b': Knight('N1b', 'b', [[1, -2], [-1, -2], [1, 2], [-1, 2], [-2, 1], [-2, -1], [2, 1], [2, -1]], [7, 1]),
    'N2b': Knight('N2b', 'b', [[1, -2], [-1, -2], [1, 2], [-1, 2], [-2, 1], [-2, -1], [2, 1], [2, -1]], [7, 6]),
    'p1w': Pawn('p1w', 'w', [[1, 0], [2, 0], [1, 1], [1, -1]], [1, 0]),
    'p2w': Pawn('p2w', 'w', [[1, 0], [2, 0], [1, 1], [1, -1]], [1, 1]),
    'p3w': Pawn('p3w', 'w', [[1, 0], [2, 0], [1, 1], [1, -1]], [1, 2]),
    'p4w': Pawn('p4w', 'w', [[1, 0], [2, 0], [1, 1], [1, -1]], [1, 3]),
    'p5w': Pawn('p5w', 'w', [[1, 0], [2, 0], [1, 1], [1, -1]], [1, 4]),
    'p6w': Pawn('p6w', 'w', [[1, 0], [2, 0], [1, 1], [1, -1]], [1, 5]),
    'p7w': Pawn('p7w', 'w', [[1, 0], [2, 0], [1, 1], [1, -1]], [1, 6]),
    'p8w': Pawn('p8w', 'w', [[1, 0], [2, 0], [1, 1], [1, -1]], [1, 7]),
    'p1b': Pawn('p1b', 'b', [[-1, 0], [-2, 0], [-1, 1], [-1, -1]], [6, 0]),
    'p2b': Pawn('p2b', 'b', [[-1, 0], [-2, 0], [-1, 1], [-1, -1]], [6, 1]),
    'p3b': Pawn('p3b', 'b', [[-1, 0], [-2, 0], [-1, 1], [-1, -1]], [6, 2]),
    'p4b': Pawn('p4b', 'b', [[-1, 0], [-2, 0], [-1, 1], [-1, -1]], [6, 3]),
    'p5b': Pawn('p5b', 'b', [[-1, 0], [-2, 0], [-1, 1], [-1, -1]], [6, 4]),
    'p6b': Pawn('p6b', 'b', [[-1, 0], [-2, 0], [-1, 1], [-1, -1]], [6, 5]),
    'p7b': Pawn('p7b', 'b', [[-1, 0], [-2, 0], [-1, 1], [-1, -1]], [6, 6]),
    'p8b': Pawn('p8b', 'b', [[-1, 0], [-2, 0], [-1, 1], [-1, -1]], [6, 7]),
    '01w': Checker('01w', 'w', [[1, 1], [1, -1], [2, 2], [2, -2], [-2, -2], [-2, 2]], [0, 0]),
    '02w': Checker('02w', 'w', [[1, 1], [1, -1], [2, 2], [2, -2], [-2, -2], [-2, 2]], [0, 2]),
    '03w': Checker('03w', 'w', [[1, 1], [1, -1], [2, 2], [2, -2], [-2, -2], [-2, 2]], [0, 4]),
    '04w': Checker('04w', 'w', [[1, 1], [1, -1], [2, 2], [2, -2], [-2, -2], [-2, 2]], [0, 6]),
    '05w': Checker('05w', 'w', [[1, 1], [1, -1], [2, 2], [2, -2], [-2, -2], [-2, 2]], [1, 1]),
    '06w': Checker('06w', 'w', [[1, 1], [1, -1], [2, 2], [2, -2], [-2, -2], [-2, 2]], [1, 3]),
    '07w': Checker('07w', 'w', [[1, 1], [1, -1], [2, 2], [2, -2], [-2, -2], [-2, 2]], [1, 5]),
    '08w': Checker('08w', 'w', [[1, 1], [1, -1], [2, 2], [2, -2], [-2, -2], [-2, 2]], [1, 7]),
    '09w': Checker('09w', 'w', [[1, 1], [1, -1], [2, 2], [2, -2], [-2, -2], [-2, 2]], [2, 0]),
    '10w': Checker('10w', 'w', [[1, 1], [1, -1], [2, 2], [2, -2], [-2, -2], [-2, 2]], [2, 2]),
    '11w': Checker('11w', 'w', [[1, 1], [1, -1], [2, 2], [2, -2], [-2, -2], [-2, 2]], [2, 4]),
    '12w': Checker('12w', 'w', [[1, 1], [1, -1], [2, 2], [2, -2], [-2, -2], [-2, 2]], [2, 6]),
    '01b': Checker('01b', 'b', [[-1, -1], [-1, 1], [2, 2], [2, -2], [-2, -2], [-2, 2]], [5, 1]),
    '02b': Checker('02b', 'b', [[-1, -1], [-1, 1], [2, 2], [2, -2], [-2, -2], [-2, 2]], [5, 3]),
    '03b': Checker('03b', 'b', [[-1, -1], [-1, 1], [2, 2], [2, -2], [-2, -2], [-2, 2]], [5, 5]),
    '04b': Checker('04b', 'b', [[-1, -1], [-1, 1], [2, 2], [2, -2], [-2, -2], [-2, 2]], [5, 7]),
    '05b': Checker('05b', 'b', [[-1, -1], [-1, 1], [2, 2], [2, -2], [-2, -2], [-2, 2]], [6, 0]),
    '06b': Checker('06b', 'b', [[-1, -1], [-1, 1], [2, 2], [2, -2], [-2, -2], [-2, 2]], [6, 2]),
    '07b': Checker('07b', 'b', [[-1, -1], [-1, 1], [2, 2], [2, -2], [-2, -2], [-2, 2]], [6, 4]),
    '08b': Checker('08b', 'b', [[-1, -1], [-1, 1], [2, 2], [2, -2], [-2, -2], [-2, 2]], [6, 6]),
    '09b': Checker('09b', 'b', [[-1, -1], [-1, 1], [2, 2], [2, -2], [-2, -2], [-2, 2]], [7, 1]),
    '10b': Checker('10b', 'b', [[-1, -1], [-1, 1], [2, 2], [2, -2], [-2, -2], [-2, 2]], [7, 3]),
    '11b': Checker('11b', 'b', [[-1, -1], [-1, 1], [2, 2], [2, -2], [-2, -2], [-2, 2]], [7, 5]),
    '12b': Checker('12b', 'b', [[-1, -1], [-1, 1], [2, 2], [2, -2], [-2, -2], [-2, 2]], [7, 7])}
