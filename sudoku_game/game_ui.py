# Author: 4sushi
from __future__ import annotations
import curses
from sudoku_game.game import GameSudoku
from typing import List, Optional
import sys
from datetime import datetime, timedelta



class GameUI:

    def __init__(self):
        self.stdscr = None
        self.dt_start_game: None | datetime = None
        self.cursor_pos: None | List[int] = None
        self.game: None | GameSudoku = None
        self.height: None | int = None
        self.width: None | int = None
        self.x_center: None | int = None
        self.y_center: None | int = None
        self.KEY_QUIT: int = ord('!')
        self.KEY_RESTART: int = ord('?')
        self.KEY_ENTER: int = 10
        self.KEYS_DEL: List[int] = [127, 8, curses.KEY_DL, curses.KEY_DC, curses.KEY_BACKSPACE]
        self.ID_COLOR_RED: int = 1
        self.init_game()
        curses.wrapper(self.init_screen)

    def init_game(self, difficulty: int = 2):
        self.game = GameSudoku(difficulty)
        self.cursor_pos = [0, 0]
        self.dt_start_game = datetime.now()

    def init_screen(self, stdscr):
        self.stdscr = stdscr
        curses.curs_set(0)
        self.stdscr.keypad(True)
        # Init colors
        curses.use_default_colors()
        curses.start_color()
        curses.init_pair(self.ID_COLOR_RED, curses.COLOR_RED, -1)
        self.controller()
       
    def controller(self):
        k = 0
        while k != self.KEY_QUIT:
            try:
                if k in (curses.KEY_RIGHT, curses.KEY_LEFT, curses.KEY_DOWN, curses.KEY_UP):
                    self.controller_direction_keys(k)
                elif ord('1') <= k <= ord('9'):
                    value: int = int(chr(k))
                    self.controller_digit(value)
                elif k in self.KEYS_DEL or k == ord('0'):
                    self.controller_del()
                elif k == self.KEY_RESTART:
                    self.popup_new_game()
                self.refresh_screen()
                if self.game.is_game_won():
                    self.popup_game_won()
            except curses.error as e:
                if str(e) == 'addwstr() returned ERR':
                    self.popup_error()
                else:
                    raise e
            k = self.stdscr.getch()

    def controller_direction_keys(self, k: int):
        if k == curses.KEY_RIGHT:
            self.cursor_pos[0] = min(self.cursor_pos[0]+1, self.game.VALUE_MAX-1)
        elif k == curses.KEY_LEFT:
            self.cursor_pos[0] = max(self.cursor_pos[0]-1, 0)
        elif k == curses.KEY_UP:
            self.cursor_pos[1] = max(self.cursor_pos[1]-1, 0)
        elif k == curses.KEY_DOWN:
            self.cursor_pos[1] = min(self.cursor_pos[1]+1, self.game.VALUE_MAX-1)

    def controller_digit(self, value: int):
        i_col, i_row = self.cursor_pos
        if self.game.base_grid[i_row][i_col] == 0:
            self.game.grid[i_row][i_col] = value

    def controller_del(self):
        i_col, i_row = self.cursor_pos
        if self.game.base_grid[i_row][i_col] == 0:
            self.game.grid[i_row][i_col] = 0

    def popup_game_won(self):
        self.stdscr.clear()
        dt_now: datetime = datetime.now()
        delta: timedelta = dt_now - self.dt_start_game
        message: str = f'Victory! You have won in {delta.seconds // 60} minutes and {delta.seconds % 60} seconds.'
        self.stdscr.addstr(self.y_center-1, self.x_center - int(len(message)/2), message)
        message = f'Press [?] to replay or [!] to quit.'
        self.stdscr.addstr(self.y_center, self.x_center - int(len(message)/2), message)
        while True:
            k = self.stdscr.getch()
            if k == self.KEY_QUIT:
                sys.exit(0)
            elif k == self.KEY_RESTART:
                self.init_game()
                break

    def popup_new_game(self):
        self.stdscr.clear()
        levels: List[str] = [f'[{k}] {v}' for k, v in self.game.DIFFICULTIES.items()]
        levels_str: str = '\n'.join(levels)
        message = f'New game - Choose the difficulty:\n{levels_str}'
        self.stdscr.addstr(0, 0, message)
        while True:
            k = self.stdscr.getch()
            c = chr(k)
            if ord('1') <= k <= ord('4'):
                self.init_game(difficulty=int(c))
                break
            elif c == '!':
                sys.exit(0)

    def popup_error(self):
        self.stdscr.clear()
        error_message: str = 'Screen is to small, enlarge the window to play.'
        self.addstr(self.y_center-1, self.x_center - int(len(error_message)/2), error_message, self.ID_COLOR_RED)
    
    def refresh_screen(self):
        self.stdscr.clear()
        self.height, self.width = self.stdscr.getmaxyx()
        self.x_center = int(self.width / 2)
        self.y_center = int(self.height / 2)

        # Draw Sudoku
        lines = self.game.get_sudoku_str().split('\n')
        for i, line in enumerate(lines):
            self.addstr(1+i, 1, line)
        
        # Draw base digit in bold
        for i_row in range(self.game.SIZE*self.game.SIZE):
            for i_col in range(self.game.SIZE*self.game.SIZE):
                val = self.game.base_grid[i_row][i_col]
                if val > 0:
                    self.stdscr.addstr(2+i_row*2, 3+i_col*4, str(val), curses.A_BOLD)
        
        # Draw cursor
        i_col, i_row = self.cursor_pos
        val = str(self.game.grid[i_row][i_col]).replace('0', ' ')
        params = curses.A_STANDOUT
        if self.game.base_grid[i_row][i_col] > 0:
            params = curses.A_STANDOUT | curses.A_BOLD
        self.stdscr.addstr(2+i_row*2, 3+i_col*4 -1, f' {val} ', params)

        info_menu: str = (f'({self.game.get_difficulty()}) [←][→][↑][↓]navigate [Del←][0]delete  [1-9]set value [?]new '
                          f'game [!]quit')
        self.stdscr.addstr(self.height-1, 0, info_menu + ' '*(self.width-len(info_menu)-1), curses.A_STANDOUT)
        self.stdscr.refresh()

    def addstr(self, y: int, x: int, text: str, id_color_pair: Optional[int] = None):
        if id_color_pair:
            self.stdscr.attron(curses.color_pair(id_color_pair))
        self.stdscr.addstr(y, x, text)
        if id_color_pair:
            self.stdscr.attroff(curses.color_pair(id_color_pair))
