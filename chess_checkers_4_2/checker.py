from view import View
from figure_creator import figures, Queen, Bishop, Rook, Knight, QueensChecker, FigureAbstract
from figures_moves import Moves


class Check:
    @staticmethod
    # ввод данных и формирование словаря на их основе
    def input_commands(counter: int, game: str) -> dict | None:
        while True:
            data_dict = {'figure_name': None, 'new_coords': None, 'death_figure': None, 'isminner': False,
                         'new_figure': None, 'add_figure': None, 'draw': False}
            figure = str(input(View.print_message('\nВведите фигуру, которую хотите переместить')))
            View.print_message('\nВведите координаты клетки, куда хотите походить')
            try:
                number = int(input(View.print_message('\nВведите цифру '))) - 1
            except ValueError:
                View.print_message('\nВы неверно ввели данные')
                return None
            letter = str(input(View.print_message('\nВведите букву')))
            letters_dict = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
            if letter in letters_dict:
                letter = letters_dict[letter]
            data_dict.update({'figure_name': figure, 'new_coords': [number, letter]})
            # выбор проверрок в зависимости от игры
            if game == 'checkers':
                if Check.checkers_checks(counter, figure, data_dict) is False:
                    break
            elif game == 'chess':
                if Check.checking_process(counter, figure, data_dict) is False:
                    break
        return data_dict

    @staticmethod
    # вызов всех основных проверок для шашек
    def checkers_checks(counter: int, figure: str, data_dict: dict):
        if Check.players_turn(counter, figure) is True:
            return True
        if Check.input_check(figure, data_dict['new_coords'][0], data_dict['new_coords'][1]) is True:
            return True
        for element in figures.values():
            if element.get_name() == figure:
                figure = element
        if Check.move_figure(data_dict, figure) is True:
            return True
        if data_dict.get('figure_name')[0] == 'q':
            if Check.eating_checkers_by_queens(data_dict, figure) is True:
                return True
        else:
            if Check.eating_checkers(data_dict, figure) is True:
                return True
        Check.turning_to_queen(data_dict)
        return False

    @staticmethod
    # проверка на становление шашки дамкой
    def turning_to_queen(data_dict: dict) -> dict:
        if data_dict.get('figure_name')[0] == 'q':
            pass
        else:
            if data_dict.get('figure_name')[-1] == 'b' and data_dict.get('new_coords')[0] == 0:
                index = input(View.print_message('\nВведите индекс для дамки'))
                new_figure = 'q' + str(index) + 'b'
                Check.figure_creation(new_figure, data_dict)
                data_dict.update({'figure_name': new_figure})
                return data_dict
            elif data_dict.get('figure_name')[-1] == 'w' and data_dict.get('new_coords')[0] == 7:
                index = input(View.print_message('\nВведите индекс для дамки'))
                new_figure = 'q' + str(index) + 'w'
                Check.figure_creation(new_figure, data_dict)
                data_dict.update({'figure_name': new_figure})
                return data_dict

    @staticmethod
    # проверка на возможность поедания шашек дамками
    def eating_checkers_by_queens(data_dict: dict, figure: FigureAbstract):
        check_list = [data_dict.get('new_coords')[0] - figure.get_coords()[0],
                      data_dict.get('new_coords')[1] - figure.get_coords()[1]]
        possible_moves = figure.get_possible_moves()
        number_of_between_figures = 0
        if check_list in possible_moves:
            figure, between_coords, data_dict = Check.another_figure_way_1(data_dict, figure)
            for lst in between_coords:
                for figure1 in figures.values():
                    if figure1.get_coords() == lst:
                        number_of_between_figures += 1
                        if figure.get_colour() == figure1.get_colour():
                            View.print_message('\nФигура не может перескакивать через шашку своего цвета')
                            return True
            if number_of_between_figures == 1:
                for figure2 in figures.values():
                    if figure2.get_coords() in between_coords:
                        data_dict.update({'death_figure': figure2})
            elif number_of_between_figures > 1:
                View.print_message('\nФигура не может перескакивать через несколько фигур')
                return True

    @staticmethod
    # проверка на возможность съесть другую шашку для обычных шашек
    def eating_checkers(data_dict: dict, figure: FigureAbstract):
        check_list = [data_dict.get('new_coords')[0] - figure.get_coords()[0],
                      data_dict.get('new_coords')[1] - figure.get_coords()[1]]
        *a, b, c, d, e = figure.get_possible_moves()
        for figure1 in figures.values():
            if figure1.get_coords() == data_dict.get('new_coords'):
                View.print_message('\nХод не соответсвует правилам игры (шашка не может есть таким образом)')
                return True
        if check_list in (b, c, d, e):
            figure, between_coords, data_dict = Check.another_figure_way_1(data_dict, figure)
            for lst in between_coords:
                for figure1 in figures.values():
                    if figure1.get_coords() == lst:
                        if figure.get_colour() == figure1.get_colour():
                            View.print_message('\nФигура не может перескакивать через шашку своего цвета')
                            return True
                        else:
                            data_dict.update({'death_figure': figure1})

    @staticmethod
    # проверка на возможность продолжить поедание шашек
    def continue_eating(data_dict: dict, figure: FigureAbstract) -> dict | None:
        x = data_dict.get('new_coords')[0]
        y = data_dict.get('new_coords')[1]
        figures_coords_current = []
        empty_current_cells = []
        for figure1 in figures.values():
            figures_coords_current.append(figure1.get_coords())
        for coord1 in range(8):
            for coord2 in range(8):
                if [coord1, coord2] not in figures_coords_current:
                    empty_current_cells.append([coord1, coord2])
        if figure.get_name().startswith('q'):
            add_data_dict = Check.checking_for_add_eating(data_dict=data_dict, x=0, y=0, figure=figure)
            return add_data_dict
        else:
            if [x + 1, y + 1] in figures_coords_current and [x + 2, y + 2] in empty_current_cells:
                for item in figures.values():
                    if item.get_coords() == [x + 1, y + 1] and item.get_colour() != data_dict.get('figure_name')[-1]:
                        add_data_dict = Check.checking_for_add_eating(data_dict, x + 1, y + 1, figure)
                        return add_data_dict
            elif [x - 1, y - 1] in figures_coords_current and [x - 2, y - 2] in empty_current_cells:
                for item in figures.values():
                    if item.get_coords() == [x - 1, y - 1] and item.get_colour() != data_dict.get('figure_name')[-1]:
                        add_data_dict = Check.checking_for_add_eating(data_dict, x - 1, y - 1, figure)
                        return add_data_dict
            elif [x - 1, y + 1] in figures_coords_current and [x - 2, y + 2] in empty_current_cells:
                for item in figures.values():
                    if item.get_coords() == [x - 1, y + 1] and item.get_colour() != data_dict.get('figure_name')[-1]:
                        add_data_dict = Check.checking_for_add_eating(data_dict, x - 1, y + 1, figure)
                        return add_data_dict
            elif [x + 1, y - 1] in figures_coords_current and [x + 2, y - 2] in empty_current_cells:
                for item in figures.values():
                    if item.get_coords() == [x + 1, y - 1] and item.get_colour() != data_dict.get('figure_name')[-1]:
                        add_data_dict = Check.checking_for_add_eating(data_dict, x + 1, y - 1, figure)
                        return add_data_dict
            else:
                return None

    @staticmethod
    # ввод данных, обозначающих какую шашку хочет съесть пользователь
    def checking_for_add_eating(data_dict: dict, x: int, y: int, figure: FigureAbstract) -> dict | int:
        View.print_message(f'\nВозможно вы можете съесть ещё одну шашку шашкой {data_dict.get("figure_name")}.')
        stop = input(View.print_message('Напишите "stop", если вы не осталось фигур для поедания или вы не '
                                        'желаете дальше поедать фигуры, напишите "continue", если хотите продолжить'))
        if stop == 'stop':
            stop = True
            add_data_dict = {'stop': stop}
            return add_data_dict
        elif stop == 'continue':
            stop = False
            add_data_dict = {'stop': stop}
        else:
            View.print_message('\nВы неверно ввели команду')
            return 1
        try:
            number = int(input(View.print_message('\nВведите цифру '))) - 1
        except ValueError:
            View.print_message('\nВы неверно ввели данные')
            return 1
        letter = str(input(View.print_message('\nВведите букву')))
        letters_dict = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        if letter in letters_dict:
            letter = letters_dict[letter]
        current_coords = figure.get_coords()
        data_dict.update({'figure_name': data_dict.get("figure_name"), 'new_coords': [number, letter]})
        if Check.input_check(figure=None, number1=number, letter1=letter) is True:
            return 1
        if figure.get_name().startswith('q'):
            check_list = [data_dict.get('new_coords')[0] - figure.get_coords()[0],
                          data_dict.get('new_coords')[1] - figure.get_coords()[1]]
            possible_moves = figure.get_possible_moves()
            number_of_between_figures = 0
            if check_list in possible_moves:
                figure, between_coords, data_dict = Check.another_figure_way_1(data_dict, figure)
                for lst in between_coords:
                    for figure1 in figures.values():
                        if figure1.get_coords() == lst:
                            number_of_between_figures += 1
                            if figure.get_colour() == figure1.get_colour():
                                View.print_message('\nФигура не может перескакивать через шашку своего цвета')
                                return True
                if number_of_between_figures == 1:
                    for figure2 in figures.values():
                        if figure2.get_coords() in between_coords:
                            data_dict.update({'death_figure': figure2})
                elif number_of_between_figures > 1:
                    View.print_message('\nФигура не может перескакивать через несколько фигур')
                    return True
            add_data_dict.update({'figure_name': data_dict.get("figure_name"), 'new_coords': [number, letter],
                                  'death_figure': data_dict.get('death_figure')})
            return add_data_dict
        else:
            if Check.move_figure_checkers_add(x, y, figure, data_dict, current_coords) is True:
                return 1
            for figure2 in figures.values():
                if [x, y] == figure2.get_coords():
                    data_dict.update({'death_figure': figure2})
            add_data_dict = {'figure_name': data_dict.get("figure_name"), 'new_coords': [number, letter],
                             'death_figure': data_dict.get('death_figure'), 'stop': stop}
            return add_data_dict

    @staticmethod
    # проверка на правильность направления хода пешки при поедании дополнительных фигур
    def move_figure_checkers_add(x: int, y: int, figure: FigureAbstract, data_dict: dict, current_coords: list) -> bool:
        for figure1 in figures.values():
            if [x, y] == figure1.get_coords():
                if figure1.get_name().endswith(figure.get_name()[-1]):
                    View.print_message('\nХод не соответствует правилам игры (нельзя есть фигуру своего цвета)')
                    return True
                else:
                    check_list = [data_dict.get('new_coords')[0] - current_coords[0],
                                  data_dict.get('new_coords')[1] - current_coords[1]]
                    if check_list not in figure.get_possible_moves():
                        data_dict.update({'new_coords': [current_coords[0], current_coords[1]]})
                        View.print_message('\nХод не соответствует правилам игры (фигура не может так ходить)')
                        return True

    @staticmethod
    # вызов всех основных проверок для шахмат
    def checking_process(counter: int, figure: str, data_dict: dict) -> bool:
        if Check.players_turn(counter, figure) is True:
            return True
        if Check.input_check(figure, data_dict['new_coords'][0], data_dict['new_coords'][1]) is True:
            return True
        for element in figures.values():
            if element.get_name() == figure:
                figure = element
        if data_dict['figure_name'].startswith('K'):
            if Check.king_rules(data_dict, figure) is True:
                return True
            if figure.get_type_figure() is False:
                figure.change_figure_type()
            return False
        elif data_dict['figure_name'].startswith('p'):
            if Check.pawn_rules(data_dict, figure) is True:
                return True
        else:
            if Check.move_figure(data_dict, figure) is True:
                return True
            if Check.another_figure_way_2(data_dict, figure) is True:
                return True
            if figure.get_name().startswith('R') and figure.get_type_figure() is False:
                figure.change_figure_type()
        return False

    @staticmethod
    # проверка на очерёдность хода
    def players_turn(counter: int, figure: str) -> bool | None:
        colour = figure[-1]
        if counter % 2 == 0 and colour == 'b':
            View.print_message('\nСейчас ходят белые')
            return True
        elif counter % 2 != 0 and colour == 'w':
            View.print_message('\nСейчас ходят чёрные')
            return True

    @staticmethod
    # проверка на ввод данных пользователем
    def input_check(figure: str | None, number1: int, letter1: int) -> bool | None:
        if figure is not None:
            if figure not in figures.keys():
                View.print_message('\nНеправильное имя')
                return True
        if number1 not in (range(0, 9)) or letter1 not in (range(0, 9)):
            View.print_message('\nВы вышли за границы поля или неверно ввели данные')
            return True

    @staticmethod
    # проверка хода пешки и изменение её типа при необходимости
    def pawn_rules(data_dict: dict, figure: FigureAbstract) -> bool | None:
        check_list = [data_dict.get('new_coords')[0] - figure.get_coords()[0],
                      data_dict.get('new_coords')[1] - figure.get_coords()[1]]
        if check_list == figure.get_possible_moves()[1]:
            figure.change_figure_type()
        if data_dict['new_coords'][0] in (0, 7):
            if Check.changing_pawn(data_dict, figure) is True:
                return True
        else:
            if Check.move_pawn(data_dict, figure) is True:
                return True
        for figure1 in figures.values():
            if figure1.get_type_figure() is True:
                if figure1.get_name().endswith('w') and figure1.get_coords()[0] == 3:
                    figure1.change_figure_type()
                elif figure1.get_name().endswith('b') and figure1.get_coords()[0] == 4:
                    figure1.change_figure_type()

    @staticmethod
    # проверка на попытку съесть фигуру своего цвета и на правильность направления хода фигуры
    def move_figure(data_dict: dict, figure: FigureAbstract) -> bool | FigureAbstract:
        colour = figure.get_name()[-1]
        for figure1 in figures.values():
            if data_dict.get('new_coords') == figure1.get_coords():
                if figure1.get_name().endswith(colour):
                    View.print_message('\nХод не соответствует правилам игры (нельзя есть фигуру своего цвета)')
                    return True
                else:
                    if figure.get_name().startswith('N'):
                        data_dict.update({'death_figure': figure1})
                        break
            else:
                check_list = [data_dict.get('new_coords')[0] - figure.get_coords()[0],
                              data_dict.get('new_coords')[1] - figure.get_coords()[1]]
                if check_list not in figure.get_possible_moves():
                    View.print_message('\nХод не соответствует правилам игры (фигура не может ходить таким образом)')
                    return True
        return figure

    @staticmethod
    # проверка на возможность пешки походить на 2 клетки вперёд
    def move_pawn(data_dict: dict, figure: FigureAbstract) -> bool | None:
        if figure.get_coords()[0] not in (1, 6):
            deleting = figure.get_possible_moves()[1]
            figure.get_possible_moves().remove(deleting)
            figure.get_possible_moves().insert(1, [0, 0])
        check_list = [data_dict.get('new_coords')[0] - figure.get_coords()[0],
                      data_dict.get('new_coords')[1] - figure.get_coords()[1]]
        if check_list not in figure.get_possible_moves():
            View.print_message('\nХод не соответствует правилам игры (пешка не может ходить таким образом)')
            return True
        if Check.pawn_way(data_dict, figure, check_list) is True:
            return True

    @staticmethod
    # проверка на возможность пешки походить вперёд и наискосок
    def pawn_way(data_dict: dict, figure: FigureAbstract, check_list: list) -> bool | None:
        between_coords = []
        fl = 0
        for pere in range(check_list[0], check_list[0] + 1):
            y = figure.get_coords()[0] + pere
            lst = [y, figure.get_coords()[1]]
            between_coords.append(lst)
        if check_list in (figure.get_possible_moves()[2], figure.get_possible_moves()[3]):
            if Check.pawn_capture(data_dict, figure) is True:
                return True
            elif Check.pawn_capture(data_dict, figure) == 2:
                fl = 1
            for figure1 in figures.values():
                if data_dict['new_coords'] == figure1.get_coords():
                    data_dict.update({'death_figure': figure1})
                    fl = 1
                    break
            if fl == 0:
                View.print_message('\nХод не соответствует правилам игры (Нельзя ходить пешкой наискосок)')
                return True
        if check_list in (figure.get_possible_moves()[0], figure.get_possible_moves()[1]):
            for lst in between_coords:
                for figure1 in figures.values():
                    if lst == figure1.get_coords():
                        View.print_message('\nХод не соответствует правилам игры (пешка не может есть вперёд')
                        return True

    @staticmethod
    # проверка на возможность взять пешку врага на проходе
    def pawn_capture(data_dict: dict, figure: FigureAbstract) -> bool | int:
        x = figure.get_coords()[0]
        y = figure.get_coords()[1]
        for figure1 in figures.values():
            if figure1.get_coords() in ([x, y + 1], [x, y - 1]):
                if figure.get_name().endswith('w') and \
                   [figure1.get_coords()[0] + 1, figure1.get_coords()[1]] == data_dict['new_coords']:
                    if figure1.get_type_figure() is True:
                        data_dict.update({'death_figure': figure1})
                        return 2
                    else:
                        View.print_message('\nХод не соответствует правилам игры')
                        return True
                if figure.get_name().endswith('b') and \
                   [figure1.get_coords()[0] - 1, figure1.get_coords()[1]] == data_dict['new_coords']:
                    if figure1.get_type_figure() is True:
                        data_dict.update({'death_figure': figure1})
                        return 2
                    else:
                        View.print_message('\nХод не соответствует правилам игры')
                        return True

    @staticmethod
    # проверка на наличие фигур между текущими координаты фигуры и координатами,
    # введёнными пользователем (для всех фигур, включая короля)
    def another_figure_way_1(data_dict: dict, figure: FigureAbstract) -> tuple:
        dif = [data_dict.get('new_coords')[0] - figure.get_coords()[0],
               data_dict.get('new_coords')[1] - figure.get_coords()[1]]
        between_coords = []
        # движение по вертикали
        if abs(dif[0]) > abs(dif[1]):
            for pere in range(1, abs(dif[0])):
                # движение вниз
                if figure.get_coords()[0] < data_dict.get('new_coords')[0]:
                    y = figure.get_coords()[0] + pere
                    lst = [y, figure.get_coords()[1]]
                    between_coords.append(lst)
                # движение вверх
                elif figure.get_coords()[0] > data_dict.get('new_coords')[0]:
                    y = figure.get_coords()[0] - pere
                    lst = [y, figure.get_coords()[1]]
                    between_coords.append(lst)
        # движение по горизонтали
        elif abs(dif[0]) < abs(dif[1]):
            for pere in range(1, abs(dif[1])):
                # движение вправо
                if figure.get_coords()[1] < data_dict.get('new_coords')[1]:
                    x = figure.get_coords()[1] + pere
                    lst = [figure.get_coords()[0], x]
                    between_coords.append(lst)
                # движение влево
                elif figure.get_coords()[1] > data_dict.get('new_coords')[1]:
                    x = figure.get_coords()[1] - pere
                    lst = [figure.get_coords()[0], x]
                    between_coords.append(lst)
        # движение по диагонали
        elif abs(dif[0]) == abs(dif[1]):
            for pere in range(1, abs(dif[0])):
                # движение вверх влево
                if figure.get_coords()[0] > data_dict.get('new_coords')[0] \
                        and figure.get_coords()[1] > data_dict.get('new_coords')[1]:
                    x = figure.get_coords()[0] - pere
                    y = figure.get_coords()[1] - pere
                    lst = [x, y]
                    between_coords.append(lst)
                # движение вверх вправо
                elif figure.get_coords()[0] > data_dict.get('new_coords')[0] \
                        and figure.get_coords()[1] < data_dict.get('new_coords')[1]:
                    x = figure.get_coords()[0] - pere
                    y = figure.get_coords()[1] + pere
                    lst = [x, y]
                    between_coords.append(lst)
                # движение вниз вправо
                elif figure.get_coords()[0] < data_dict.get('new_coords')[0] \
                        and figure.get_coords()[1] < data_dict.get('new_coords')[1]:
                    x = figure.get_coords()[0] + pere
                    y = figure.get_coords()[1] + pere
                    lst = [x, y]
                    between_coords.append(lst)
                # движение вниз влево
                elif figure.get_coords()[0] < data_dict.get('new_coords')[0] \
                        and figure.get_coords()[1] > data_dict.get('new_coords')[1]:
                    x = figure.get_coords()[0] + pere
                    y = figure.get_coords()[1] - pere
                    lst = [x, y]
                    between_coords.append(lst)
        return figure, between_coords, data_dict

    @staticmethod
    # вторая часть проверки (для всех фигур, кроме короля)
    def another_figure_way_2(data_dict, figure):
        figure, between_coords, data_dict = Check.another_figure_way_1(data_dict, figure)
        if figure.get_name().startswith('N'):
            pass
        else:
            for lst in between_coords:
                for figure1 in figures.values():
                    if lst == figure1.get_coords():
                        View.print_message('\nХод не соответствует правилам игры (лишние фигуры на пути)')
                        return True
        for figure1 in figures.values():
            if data_dict.get('new_coords') == figure1.get_coords():
                data_dict.update({'death_figure': figure1})

    @staticmethod
    # получение данных о фигуре, которую хочет создать пользователь, и ограничение на создание определённых фигур
    def changing_pawn(data_dict: dict, figure: FigureAbstract) -> bool | None:
        Check.move_pawn(data_dict, figure)
        if data_dict.get('figure_name').startswith('p'):
            if data_dict.get('new_coords')[0] == 7 or data_dict.get('new_coords')[0] == 0:
                new_figure = input(View.print_message('\nКакую фигуру вы хотите создать? \n'
                                                      'Введите её имя в виде: Q1w, Q2b'))
                if new_figure.startswith(('Q', 'B', 'N', 'R')):
                    if new_figure.endswith('w') and data_dict.get('figure_name').endswith('w') or \
                            new_figure.endswith('b') and data_dict.get('figure_name').endswith('b'):
                        for figure in figures.values():
                            if figure.get_name() == new_figure:
                                View.print_message('\nТакая фигура уже существует')
                                return True
                            else:
                                Check.figure_creation(new_figure, data_dict)
                                break
                    else:
                        View.print_message('\nНельзя создать фигуру не своего цвета')
                        return True
                else:
                    View.print_message('\nНельзя создать такую фигуру')
                    return True

    @staticmethod
    # создание фигуры как экземпляра соответствующего класса
    def figure_creation(new_figure: str, data_dict: dict):
        colour = str(new_figure[-1])
        if new_figure.startswith('Q'):
            figures.update({new_figure: Queen(new_figure, colour, Moves.queen_moves(), data_dict.get('new_coords'))})
        elif new_figure.startswith('B'):
            figures.update({new_figure: Bishop(new_figure, colour, Moves.bishop_moves(), data_dict.get('new_coords'))})
        elif new_figure.startswith('N'):
            figures.update({new_figure: Knight(new_figure, colour, [[1, -2], [-1, -2], [1, 2], [-1, 2], [-2, 1],
                                               [-2, -1], [2, 1], [2, -1]], data_dict.get('new_coords'))})
        elif new_figure.startswith('R'):
            figures.update({new_figure: Rook(new_figure, colour, Moves.rook_moves(), data_dict.get('new_coords'))})
        elif new_figure.startswith('q'):
            figures.update({new_figure: QueensChecker(new_figure, colour, Moves.bishop_moves(),
                                                      data_dict.get('new_coords'))})
        data_dict.update({'new_figure': new_figure})

    @staticmethod
    # запуск проверок для короля
    def king_rules(data_dict: dict, figure: FigureAbstract) -> bool | dict:
        try:
            data_dict, fl = Check.castle(data_dict, figure)
        except TypeError:
            return True
        if fl != 1:
            if Check.move_figure(data_dict, figure) is True:
                return True
            if Check.king_threat(data_dict) is True:
                return True

    @staticmethod
    # проверка может ли король походить на выбранную клетку
    def king_threat(data_dict: dict) -> bool | None:
        possible_coords = data_dict.get('new_coords')
        for figure2 in figures.values():
            if data_dict['figure_name'][-1] == figure2.get_name()[-1]:
                pass
            else:
                dif = [possible_coords[0] - figure2.get_coords()[0],
                       possible_coords[1] - figure2.get_coords()[1]]
                if Check.dangerous_cell(dif, figure2, data_dict) is True:
                    View.print_message('\nНельзя походить сюда королём')
                    return True

    @staticmethod
    # проверка угрожают ли вражеские фигуры клетке, на которую хочет походить король
    def dangerous_cell(dif: list, figure2: FigureAbstract, data_dict: dict) -> bool | None:
        threats = []
        if dif in figure2.get_possible_moves():
            if figure2.get_name().startswith('p'):
                if dif not in (figure2.get_possible_moves()[2], figure2.get_possible_moves()[3]):
                    threats.append(False)
            else:
                figure, between_coords, data_dict = Check.another_figure_way_1(data_dict, figure2)
                # если на пути проверяемой фигуры есть другие, то она не является угрозой
                for figure3 in figures.values():
                    if figure3.get_coords() in between_coords:
                        threats.append(False)
                if False not in threats:
                    return True

    @staticmethod
    # проверка рокировки на соответствие правилам
    def castle(data_dict: dict, figure: FigureAbstract) -> bool | tuple:
        dif = [data_dict['new_coords'][0] - figure.get_coords()[0],
               data_dict['new_coords'][1] - figure.get_coords()[1]]
        between_coords = []
        for rook in figures.values():
            if rook.get_coords() == data_dict['new_coords']:
                if rook.get_name().startswith('R'):
                    for pere in range(1, abs(dif[1])):
                        # движение вправо
                        if figure.get_coords()[1] < data_dict.get('new_coords')[1]:
                            x = figure.get_coords()[1] + pere
                            lst = [figure.get_coords()[0], x]
                            between_coords.append(lst)
                        # движение влево
                        elif figure.get_coords()[1] > data_dict.get('new_coords')[1]:
                            x = figure.get_coords()[1] - pere
                            lst = [figure.get_coords()[0], x]
                            between_coords.append(lst)
                    for lst in between_coords:
                        for figure1 in figures.values():
                            if lst == figure1.get_coords():
                                View.print_message('\nХод не соответствует правилам игры (Между королём и ладьёй есть '
                                                   'другие фигуры)')
                                return True
                    for rook_king in figures.values():
                        if rook_king.get_name().startswith('R') or rook_king.get_name().startswith('K'):
                            if rook_king.get_type_figure() is True:
                                View.print_message('\nХод не соответствует правилам игры (Ладья или король уже '
                                                   'перемещались)')
                                return True
                    king_way_cells = between_coords.copy()
                    if rook.get_name()[1] == '1':
                        king_way_cells.pop(3)
                        king_way_cells.append(figure.get_coords())
                        if Check.castle_possibility(king_way_cells, data_dict) is True:
                            return True
                        data_dict = Check.long_castle(figure, data_dict)
                        fl = 1
                        return data_dict, fl
                    elif rook.get_name()[1] == '2':
                        king_way_cells.append(figure.get_coords())
                        if Check.castle_possibility(king_way_cells, data_dict) is True:
                            return True
                        data_dict = Check.short_castle(figure, data_dict)
                        fl = 1
                        return data_dict, fl

    @staticmethod
    # проверка клеток, которые проходит король, на угрозу
    def castle_possibility(king_way_cells: list, data_dict: dict):
        for cell in king_way_cells:
            for figure2 in figures.values():
                if data_dict['figure_name'][-1] == figure2.get_name()[-1]:
                    pass
                else:
                    dif = [cell[0] - figure2.get_coords()[0],
                           cell[1] - figure2.get_coords()[1]]
                    data_dict1 = {'new_coords': cell}
                    if Check.dangerous_cell(dif, figure2, data_dict1) is True:
                        View.print_message('\nХод не соответствует правилам игры (Нельзя cделать рокировку, клетки по '
                                           'которым проходит король под угрозой)')
                        return True

    @staticmethod
    # рокировка на ферзевый фланг
    def long_castle(figure: FigureAbstract, data_dict: dict) -> dict:
        data_dict_copy = data_dict.copy()
        rook = 'r'
        if figure.get_name().endswith('w'):
            for rook in figures.values():
                if rook.get_coords() == [0, 0]:
                    rook = rook.get_name()
        elif figure.get_name().endswith('b'):
            for rook in figures.values():
                if rook.get_coords() == [7, 0]:
                    rook = rook.get_name()
        new_coords = [figure.get_coords()[0], figure.get_coords()[1] - 2]
        data_dict.update({'figure_name': figure.get_name(), 'new_coords': new_coords, 'add_figure': rook.get_name(),
                          'add_coords': data_dict_copy['new_coords']})
        return data_dict

    @staticmethod
    # рокировка на королевский фланг
    def short_castle(figure: FigureAbstract, data_dict: dict) -> dict:
        data_dict_copy = data_dict.copy()
        rook = 'r'
        if figure.get_name().endswith('w'):
            for rook in figures.values():
                if rook.get_coords() == [0, 7]:
                    rook = rook.get_name()
        elif figure.get_name().endswith('b'):
            for rook in figures.values():
                if rook.get_coords() == [7, 7]:
                    rook = rook.get_name()
        new_coords = [figure.get_coords()[0], figure.get_coords()[1] + 2]
        data_dict.update({'figure_name': figure.get_name(), 'new_coords': new_coords, 'add_figure': rook.get_name(),
                          'add_coords': data_dict_copy['new_coords']})
        return data_dict
