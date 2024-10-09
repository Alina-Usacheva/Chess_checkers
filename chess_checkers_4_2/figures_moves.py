# для проверки направления хода фигуры
class Moves:
    @staticmethod
    def queen_moves() -> list:
        lst = []
        for i in range(-7, 8):
            lst.append([i, i])
            lst.append([i, -i])
            lst.append([i, 0])
            lst.append([0, i])
        return lst

    @staticmethod
    def bishop_moves() -> list:
        lst = []
        for i in range(-7, 8):
            lst.append([i, -i])
            lst.append([i, i])
        return lst

    @staticmethod
    def rook_moves() -> list:
        lst = []
        for i in range(-7, 8):
            lst.append([i, 0])
            lst.append([0, i])
        return lst
