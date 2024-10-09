from figure_creator import figures, FigureAbstract
from view import View
from checker import Check


class Board:
    __board = [['   ' for _ in range(8)] for _ in range(8)]

    @staticmethod
    def get_board() -> list:
        return Board.__board

    @staticmethod
    def set_figure(figure: FigureAbstract):
        x, y = figure.get_coords()
        Board.__board[x][y] = figure.get_name()

    @staticmethod
    def update_coordinates(x: int, y: int):
        Board.__board[x][y] = '   '

    @staticmethod
    # вызывается 1 раз в начале игры
    def place_figures():
        for figure in figures.values():
            Board.set_figure(figure)


if __name__ == '__main__':
    data_dict = {}
    flag = True
    counter = 0
    # выбор игры
    while True:
        game = str(input(View.print_message('\nВведите игру, которую хотите запустить: "checkers" or "chess"')))
        key_figures = list(figures.keys())
        chess_figures = key_figures[0:32]
        checkers_figures = key_figures[32:56]
        if game == 'checkers':
            for item in chess_figures:
                remove = [key for key in figures.keys() if key == item]
                for ele in remove:
                    del figures[ele]
            break
        elif game == 'chess':
            for item in checkers_figures:
                remove = [key for key in figures.keys() if key == item]
                for ele in remove:
                    del figures[ele]
            break
        else:
            View.print_message('\nВы неверно ввели название игры')
    Board.place_figures()
    View.print_board(Board.get_board())
    View.print_counter(counter)
    death_figures_white = []
    death_figures_black = []
    while flag:
        # если метод класса Check возвращает data_dict, то меняется доска
        if data_dict := Check.input_commands(counter, game):
            current_coords = figures[data_dict['figure_name']].get_coords()
            Board.update_coordinates(current_coords[0], current_coords[1])
            # выполняется, если была рокировка
            if data_dict['add_figure'] is not None:
                current_coords_add = figures[data_dict['add_figure']].get_coords()
                Board.update_coordinates(current_coords_add[0], current_coords_add[1])
                figures[data_dict['figure_name']].set_coords(data_dict['add_coords'][0], data_dict['add_coords'][1])
                Board.set_figure(figures[data_dict['add_figure']])
            # выполняется, если была съедена какая-либо фигура
            if figure1 := data_dict['death_figure']:
                for death_figure in figures.values():
                    if death_figure == data_dict['death_figure']:
                        Board.update_coordinates(death_figure.get_coords()[0], death_figure.get_coords()[1])
                        death_figure.set_coords(8, 8)
                for figure1 in figures.values():
                    if data_dict['death_figure'] == figure1:
                        name = figure1.get_name()
                        if name.endswith('w'):
                            death_figures_white.append(name)
                        else:
                            death_figures_black.append(name)
            figures[data_dict['figure_name']].set_coords(data_dict['new_coords'][0], data_dict['new_coords'][1])
            Board.set_figure(figures[data_dict['figure_name']])
            # выполняется, если была создана новая фигура
            if figure2 := data_dict['new_figure']:
                figures[data_dict['new_figure']].set_coords(data_dict['new_coords'][0], data_dict['new_coords'][1])
                Board.set_figure(figures[data_dict['new_figure']])
            View.print_board(Board.get_board())
            # проверка на возможность съесть доп фигуры для шашек
            if data_dict.get('death_figure') is not None:
                for figure4 in figures.values():
                    if figure4.get_name() == data_dict.get('figure_name'):
                        figure = figure4
                while add_data_dict := Check.continue_eating(data_dict, figure):
                    if add_data_dict.get('stop') is True:
                        break
                    if data_dict1 := Check.turning_to_queen(data_dict):
                        data_dict.update({'figure_name': data_dict1.get('figure_name')})
                    if add_data_dict is None:
                        break
                    elif add_data_dict == 1:
                        continue
                    else:
                        current_coords = figures[data_dict['figure_name']].get_coords()
                        Board.update_coordinates(current_coords[0], current_coords[1])
                        for death_figure in figures.values():
                            if death_figure == data_dict.get('death_figure'):
                                Board.update_coordinates(death_figure.get_coords()[0], death_figure.get_coords()[1])
                                death_figure.set_coords(8, 8)
                        for figure1 in figures.values():
                            if data_dict.get('death_figure') == figure1:
                                name = figure1.get_name()
                                if name.endswith('w'):
                                    death_figures_white.append(name)
                                else:
                                    death_figures_black.append(name)
                        figures[data_dict['figure_name']].set_coords(data_dict['new_coords'][0],
                                                                     data_dict['new_coords'][1])
                        Board.set_figure(figures[data_dict['figure_name']])
                        View.print_board(Board.get_board())
                        View.print_counter(counter)
                        View.print_lists(death_figures_white, death_figures_black)
            counter += 1
            View.print_counter(counter)
            View.print_lists(death_figures_white, death_figures_black)
            # конец игры для шашек
            if len(death_figures_white) == 12:
                View.print_message('\nЧёрные выиграли')
                break
            elif len(death_figures_black) == 12:
                View.print_message('\nБелые выиграли')
                break
            else:
                continue
