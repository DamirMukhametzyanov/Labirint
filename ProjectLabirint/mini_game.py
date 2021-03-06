# Фазульзянов Амир

import pygame
from random import randint

WIDTH = 1250
HEIGHT = 850
BLACK = 0
BLUE = 1
RED = 2
COLORS = ['Black', 'Blue', 'Red']


class NoughtsCrosses:
    def __init__(self, width, height, left=325, top=100, cell_size=200):
        self.width = width
        self.height = height
        self.board = [[BLACK] * width for _ in range(height)]
        self.robot = Robot(self.board)
        self.set_view(left, top, cell_size)

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        ots = 2
        for row in range(self.height):
            for col in range(self.width):
                pygame.draw.rect(screen, 'White', (self.left + col * self.cell_size,
                                 self.top + row * self.cell_size, self.cell_size, self.cell_size), 1)
                self.draw_moves(screen, row, col, ots)

    def draw_moves(self, screen, row, col, ots):
        if self.board[row][col] == BLUE:
            pygame.draw.line(screen, COLORS[self.board[row][col]],
                             (col * self.cell_size + 2 * ots + self.left, row * self.cell_size + ots + self.top),
                             ((col + 1) * self.cell_size - 2 * ots + self.left,
                              (row + 1) * self.cell_size - 2 * ots + self.top), width=7)
            pygame.draw.line(screen, COLORS[self.board[row][col]],
                             ((col + 1) * self.cell_size - 2 * ots + self.left,
                              row * self.cell_size + ots + self.top),
                             (col * self.cell_size + 2 * ots + self.left,
                              (row + 1) * self.cell_size - 2 * ots + self.top), width=7)
        if self.board[row][col] == RED:
            pygame.draw.circle(screen, COLORS[self.board[row][col]],
                               ((col + 0.5) * self.cell_size + self.left,
                                (row + 0.5) * self.cell_size + self.top),
                               self.cell_size / 2 - ots, width=7)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def get_cell(self, pos):
        if 0 <= pos[0] - self.left < self.width * self.cell_size and \
                0 <= pos[1] - self.top < self.height * self.cell_size:
            return (pos[0] - self.left) // self.cell_size, (pos[1] - self.top) // self.cell_size
        return None

    def on_click(self, cell):
        if cell:
            col, row = cell[0], cell[1]
            if self.board[row][col] == BLACK:
                self.board[row][col] = BLUE
                if not self.is_win(BLUE) and not self.is_drawn_game():
                    self.robot.set_board(self.board)
                    self.robot.move()
                    self.board = self.robot.get_board()

    def is_win(self, color):
        set_elements = set()
        i = 1
        for row in range(self.height):
            for col in range(self.width):
                if self.board[row][col] == color:
                    set_elements.add(i)
                i += 1
        if {1, 2, 3} <= set_elements or {4, 5, 6} <= set_elements or {7, 8, 9} <= set_elements:
            return True
        if {1, 4, 7} <= set_elements or {2, 5, 8} <= set_elements or {3, 6, 9} <= set_elements:
            return True
        if {1, 5, 9} <= set_elements or {3, 5, 7} <= set_elements:
            return True
        return False

    def is_drawn_game(self):
        for row in range(self.height):
            for col in range(self.width):
                if self.board[row][col] == BLACK:
                    return False
        return True


class Robot:
    def __init__(self, board):
        self.set_board(board)

    def set_board(self, board):
        self.board = board

    def move(self):
        horisontal = self.horizontal_move()
        if not horisontal:
            vertical = self.vertical_move()
            if not vertical:
                diagonal = self.diagonal_move()
                if not diagonal:
                    self.random_move()

    def horizontal_move(self):
        for row in range(len(self.board)):
            if self.board[row].count(BLUE) == 2 or self.board[row].count(RED) == 2:
                for col in range(len(self.board[row])):
                    if self.board[row][col] == BLACK:
                        self.board[row][col] = RED
                        return True
        return False

    def vertical_move(self):
        new_board = [[BLACK] * len(self.board[row]) for row in range(len(self.board))]
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                new_board[col][row] = self.board[row][col]
        for row in range(len(new_board)):
            if new_board[row].count(BLUE) == 2 or new_board[row].count(RED) == 2:
                for col in range(len(new_board[row])):
                    if new_board[row][col] == BLACK:
                        self.board[col][row] = RED
                        return True
        return False

    def diagonal_move(self):
        set_elements = self.get_elements_board()
        if {1, 5} <= set_elements or {1, 9} <= set_elements or {5, 9} <= set_elements:
            for i in range(len(self.board)):
                if self.board[i][i] == BLACK:
                    self.board[i][i] = RED
                    return True
        if {3, 5} <= set_elements or {5, 7} <= set_elements or {3, 7} <= set_elements:
            for i in range(len(self.board)):
                if self.board[i][len(self.board) - i - 1] == BLACK:
                    self.board[i][len(self.board) - i - 1] = RED
                    return True
        return False

    def random_move(self):
        while True:
            row, col = randint(0, 2), randint(0, 2)
            if self.board[row][col] == BLACK:
                self.board[row][col] = RED
                return

    def get_board(self):
        return self.board

    def get_elements_board(self):
        set_elements = set()
        i = 1
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row][col] == BLUE:
                    set_elements.add(i)
                i += 1
        return set_elements


def main_noughts_crosses():
    pygame.init()
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Мини-игра "Крестики-нолики"')
    noughts_crosses = NoughtsCrosses(3, 3)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                noughts_crosses.get_click(event.pos)
        screen.fill((0, 0, 0))
        noughts_crosses.render(screen)
        pygame.display.flip()
        if noughts_crosses.is_win(BLUE):
            pygame.time.delay(1000)
            pygame.quit()
            return True
        if noughts_crosses.is_win(RED) or noughts_crosses.is_drawn_game():
            pygame.time.delay(1000)
            pygame.quit()
            return False
    pygame.quit()
    return False


if __name__ == '__main__':
    print(main_noughts_crosses())