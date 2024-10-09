# для вывода доски, списков съеденных фигур, счётчика и текстовых сообщений
class View:
    @staticmethod
    def print_counter(counter: int):
        print(f'Количество сделанных ходов: {counter} \n')

    @staticmethod
    def print_board(board: list):
        print('     a     b     c     d     e     f     g     h   ')
        for index, row in enumerate(board):
            print(index + 1, end=" ")
            for cell in row:
                print("| {} ".format(cell), end="")
            print('|')
            print('  -------------------------------------------------')

    @staticmethod
    def print_message(string: str) -> str:
        print(f'{string}')
        return ''

    @staticmethod
    def print_lists(death_figures_white: list, death_figures_black: list):
        print(f'Списки съеденных фигур: \n{death_figures_white}\n{death_figures_black}\n')
