import pygame
import time
import traceback
import copy
pygame.font.init()

##Working of this Sudoku Game
'''
1. Working is same as of normal sudoku puzzle.
2. Buttons:
    1. RESET: Reset the entire playboard to initial setting for the player to start again
    2. Toggle Rough Cell: Toggles the cell from normal vell to rough cell where the player can jot down the possible values for the
        cell without being loosing a chance. One has to gain press the button to go back to the normal state where the player can
        mark the desired value. This button only toggles the current selected cell marked by a blue bounding square.
3. Time: Player can asses how much time it is taing him/her to finish the puzzle.
4. Space Bar: The Sudoku Solver comes into picture and let you visualize how the computer solves the problem using backtraking algorithm.
5. If you enter a value that defys the sudoku rule, a red bounding box will be showed till the value is not rectified.
4. X: Close the Sudoku Game.
'''

##Initializing the Sudoku Board
board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]

class Grid:
    
    def __init__(self, rows, cols, width, height, win, board):
        self.rows = rows
        self.cols = cols
        self.board = board
        self.solved_model = copy.deepcopy(board)
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.solve_gui = False
        self.height = height
        self.model = None
        self.win = win
        self.selected_cube = None

        self.solve_cubes() 
    
    def select_cube(self, index):
        if self.selected_cube:
            self.selected_cube.selected = False
        self.cubes[index[0]][index[1]].selected = True
        self.selected_cube = self.cubes[index[0]][index[1]]
    
    def get_board_index(self, pos):
        gap = self.width/9
        if pos[0]<self.width and pos[1]<self.height:
            x = int(pos[0]//gap)
            y = int(pos[1]//gap)
            return (y,x)
        return False
        
    def reset_board(self):
        print("Resetting board to original Matrix...")
        self.solve_gui = False
        self.selected_cube = None
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].reset(self.board[i][j])
        print("RESET successful")
        
    def reset_solved_board(self):
        self.solved_model = copy.deepcopy(self.board)
        
    def find_empty(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return i,j
        return False
        
    def solve_cubes(self):
        find = self.find_empty()
        
        if not find:
            return True
        else:
            print("next => %s,%s"%(find))
            row,col = find
        for num in range(1, 10):
            if self.is_number_position_valid(num, row, col):
                self.solved_model[row][col] = num
                self.cubes[row][col].set_value(num)
                if self.solve_gui:
                    self.cubes[row][col].update_cell(self.win, True)
                    pygame.display.update()
                    pygame.time.delay(10)
                    
                if self.solve_cubes():
                    return True
                
                self.solved_model[row][col] = 0
                self.cubes[row][col].set_value(0)
                if self.solve_gui:
                    self.cubes[row][col].update_cell(self.win, False)
                    pygame.display.update()
                    pygame.time.delay(10)
                
        return False
    
    def is_number_position_valid(self, num, row, col):
        ##checking the row
        for j in range(self.cols):
            if self.cubes[row][j].value == num and col != j:
                return False
        
        ##checking row
        for i in range(self.rows):
            if self.cubes[i][col].value == num and row != i:
                return False
        
        ##Checking 3x3 Cube
        start_row = (row//3)*3
        start_col = (col//3)*3
        for i in range(start_row, start_row+3):
            for j in range(start_col, start_col+3):
                if self.cubes[i][j].value == num and row!=i and col!=j:
                    return False
    
        ##Everything OK => Valid
        return True
        
    ##Draw Grid Thick and Thin Linings
    def draw(self):
        # Draw Grid Lines
        gap = self.width / 9
        for i in range(self.rows+1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(self.win, (0,0,0), (0, i*gap), (self.width, i*gap), thick)
            pygame.draw.line(self.win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] == 0:
                    self.cubes[i][j].wrong_filled = not(self.is_number_position_valid(self.cubes[i][j].value, i, j)) if self.cubes[i][j].value!=0 else False
                    self.cubes[i][j].draw(self.win)
                else:
                    ##Passing the base cube bool to fill the cell with base colour
                    self.cubes[i][j].draw(self.win, base_cube = True)
        
class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = [[0 for i in range(3)] for j in range(3)]
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False
        self.rough_cell = False
        self.wrong_filled = False
    
    #reset the cell to its initial configuration
    def reset(self, value):
        self.rough_cell = False
        self.temp = [[0 for i in range(3)] for j in range(3)]
        self.value = value
        self.selected = False
        self.wrong_filled = False
    
    #Set value to the cell or update the rough number matrix
    def set_value(self, value):
        if self.rough_cell:
            number = 1
            for i in range(3):
                for j in range(3):
                    if number == value:
                        self.temp[i][j] = 1
                        return
                    number+=1
        else:
            self.value = value

    #Maitain every required detail inside the cube. Like Rough Cell Text and Colour, Normal Cell Text and Colour, etc.
    def draw(self, win, base_cube = False):
        
        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap
        
        if self.rough_cell:
            pygame.draw.rect(win, (240, 240, 240, 0.5), (x,y,gap,gap), 0)
            pygame.draw.rect(win, (0, 0, 0), (x,y,gap,gap), 1)
            fnt = pygame.font.SysFont("comicsans", int(gap/3))
            rough_number = 1
            for i in range(3):
                for j in range(3):
                    if self.temp[i][j] == 1:
                        text = fnt.render(str(rough_number), 1, (0,0,0))
                        win.blit(text, (x+((j+1)*gap/4 - text.get_width()/2), y+((i+1)*gap/4 - text.get_height()/2)))
                    rough_number+=1
        
        elif not self.rough_cell and not(self.value == 0):
            if base_cube:
                pygame.draw.rect(win, (255,218,185), (x,y,gap,gap))
                pygame.draw.rect(win, (0, 0, 0), (x,y,gap,gap), 1)
            fnt = pygame.font.SysFont("comicsans", 40)
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))
            
        if self.wrong_filled:
            pygame.draw.rect(win, (255,0,0), (x,y, gap ,gap), 3)

        if self.selected:
            pygame.draw.rect(win, (0,0,255), (x,y, gap ,gap), 3)
    
    ##This cell is used when visualizing the backtracking solution to the Grid
    def update_cell(self, win, b):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        pygame.draw.rect(win, (255, 255, 255), (x, y, gap, gap), 0)

        text = fnt.render(str(self.value), 1, (0, 0, 0))
        win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))
        if b:
            pygame.draw.rect(win, (0, 255, 0), (x, y, gap, gap), 3)
        else:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)
            
def get_reset_button_position():
    return (10,560,60,580)

def get_toggle_button_position():
    return (70,560,195,580)
        
def is_pressed_reset_button(pos):
    res_pos = get_reset_button_position()
    if pos[0] >=res_pos[0] and pos[0]<res_pos[2] and pos[1]>=res_pos[1] and pos[1]<res_pos[3]:
        return True
    return False

def is_pressed_toggle_button(pos):
    toggle_pos = get_toggle_button_position()
    if pos[0] >=toggle_pos[0] and pos[0]<toggle_pos[2] and pos[1]>=toggle_pos[1] and pos[1]<toggle_pos[3]:
        return True
    return False

def get_time(time):
    minutes = time//60
    seconds = time%60
    return str(minutes)+":"+str(seconds)
    
def redraw_window(win, board, time):
    win.fill((255,255,255))
    # Draw time
    fnt = pygame.font.SysFont("comicsans", 20)
    text = fnt.render("Time: " + str(get_time(time)), 1, (0,0,0))
    win.blit(text, (540 - 160, 560))
    
    #Draw Button
    pos = get_reset_button_position()
    pygame.draw.rect(win, (255,218,185), (pos[0], pos[1], pos[2]-pos[0], pos[3]-pos[1]), 0)
    pygame.draw.rect(win, (0, 0, 0), (pos[0], pos[1], pos[2]-pos[0], pos[3]-pos[1]), 2)
    text = fnt.render("RESET", 1, (0, 0, 0))
    win.blit(text, (13, 565))
    
    #Draw Button
    pos = get_toggle_button_position()
    pygame.draw.rect(win, (255,218,185), (pos[0], pos[1], pos[2]-pos[0], pos[3]-pos[1]), 0)
    pygame.draw.rect(win, (0, 0, 0), (pos[0], pos[1], pos[2]-pos[0], pos[3]-pos[1]), 2)
    text = fnt.render("Toggle Rough Cell", 1, (0, 0, 0))
    win.blit(text, (73, 565))
    
    # Draw grid and board
    board.draw()
        
def start_sudoku(window, board):
    start_time = time.time()
    run = True
    key = None
    while run:
        play_time = round(time.time() - start_time)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    key = 1
                if event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    key = 2
                if event.key == pygame.K_3 or event.key == pygame.K_KP3:
                    key = 3
                if event.key == pygame.K_4 or event.key == pygame.K_KP4:
                    key = 4
                if event.key == pygame.K_5 or event.key == pygame.K_KP5:
                    key = 5
                if event.key == pygame.K_6 or event.key == pygame.K_KP6:
                    key = 6
                if event.key == pygame.K_7 or event.key == pygame.K_KP7:
                    key = 7
                if event.key == pygame.K_8 or event.key == pygame.K_KP8:
                    key = 8
                if event.key == pygame.K_9 or event.key == pygame.K_KP9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None
                if event.key == pygame.K_SPACE:
                    board.reset_board()
                    board.reset_solved_board()
                    print(board.solved_model)
                    board.solve_gui = True
                    redraw_window(window, board, play_time)
                    board.solve_cubes()
                    key = None
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if is_pressed_reset_button(pos):
                    board.reset_board()
                    start_time = time.time()
                elif is_pressed_toggle_button(pos):
                    if board.selected_cube and board.board[board.selected_cube.row][board.selected_cube.col] == 0:
                        selected_cube = board.selected_cube
                        selected_cube.rough_cell = True if selected_cube.rough_cell == False else False
                        print("Toggled rough cell for %s,%s"%(selected_cube.row,selected_cube.col))
                else:
                    board_index = board.get_board_index(pos)
                    if board_index:
                        board.select_cube(board_index)
                key = None
        if board.selected_cube and key!=None and board.board[board.selected_cube.row][board.selected_cube.col] == 0:
            board.selected_cube.set_value(key)
        redraw_window(window, board, play_time)
        pygame.display.update()

window = pygame.display.set_mode((540, 600))
pygame.display.set_caption("Sudoku Visualizer/Game")
try:
    board_obj = Grid(9, 9, 540, 540, window, board)
    print(board_obj.solved_model)
    ##Reseting the board to original before the start of game
    board_obj.reset_board()
    start_sudoku(window, board_obj)
except Exception as e:
    print(traceback.format_exc())
    print("The exception is %s" % (str(e)))
    pygame.quit()
pygame.quit()
