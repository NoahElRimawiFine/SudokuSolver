import pygame

# Initialize Pygame
pygame.init()

# Set the window size
size = (500, 450)
screen = pygame.display.set_mode(size)

# Set the window title
pygame.display.set_caption("Sudoku")

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# Fill the background color with white
screen.fill(white)

# Draw the 9x9 grid
for i in range(10):
    # Draw horizontal lines
    pygame.draw.line(screen, black, (i*50, 0), (i*50, 450))
    # Draw vertical lines
    pygame.draw.line(screen, black, (0, i*50), (450, i*50))

# Draw the bolder lines for the 3x3 regions
for i in range(0, 450, 150):
    for j in range(0, 450, 150):
        pygame.draw.rect(screen, black, (i, j, 150, 150), 3)

# Initialize the grid with zeroes
grid = [[0 for x in range(9)] for y in range(9)]

# Function to check if the grid is full
def check_full(grid):
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                return False
    return True

# Function to find an empty cell
def find_empty(grid):
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                return (row, col)
    return None

# function to print the board to the screen
def print_board(board):
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - -")
        
        for j in range(len(board[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end = "")
                
            if j == 8:
                print(board[i][j])
            else:
                print(str(board[i][j]) + " ", end = "")

# Function to check if the grid has a value on one of the cells
def check_if_cell_has_value(grid, row, col):
    # Check if the value is in the row
    for i in range(9):
        if grid[row][i] != 0:
            return True
    # Check if the value is in the column
    for i in range(9):
        if grid[i][col] != 0:
            return True
    # Check if the value is in the 3x3 region
    row_start = (row // 3) * 3
    col_start = (col // 3) * 3
    for i in range(row_start, row_start + 3):
        for j in range(col_start, col_start + 3):
            if grid[i][j] != 0:
                return True
    return False



# add the numbers to the grid
def draw_grid(grid):
    for row in range(9):
        for col in range(9):
            # if the grid column and row is empty draw the number in the grid
            if grid[row][col] != 0:
                # draw the number in the grid
                font = pygame.font.Font(None, 36)
                text = font.render(str(grid[row][col]), True, black)
                screen.blit(text, (col * 50 + 20, row * 50 + 15))

# use a backtracking algorithm to solve the sudoku puzzle 
def solve_sudoku(grid):
    # find an empty cell
    empty_cell = find_empty(grid)
    # if the grid is full, return True
    if not empty_cell:
        return True
    else:
        row, col = empty_cell
    # try numbers 1 to 9
    for i in range(1, 10):
        # check if the number is valid
        if check_validity(grid, row, col, i):
            # if the number is valid, assign it to the empty cell
            grid[row][col] = i
            # recursively call the function
            if solve_sudoku(grid):
                return True
            # if the number is not valid, reset the cell to 0
            grid[row][col] = 0
    return False

# add a solve button to the top right corner of the sudoku game
solve_button = pygame.Surface((50, 50))
solve_button.fill(white)
pygame.draw.rect(solve_button, black, (0, 0, 50, 50), 2)
solve_button_text = pygame.font.SysFont("Arial", 16).render("Solve", True, black)
solve_button.blit(solve_button_text, (5, 5))
screen.blit(solve_button, (500-50, 0))

# add a clear button to the top right corner of the sudoku game
clear_button = pygame.Surface((50, 50))
clear_button.fill(white)
pygame.draw.rect(clear_button, black, (0, 0, 50, 50), 2)
clear_button_text = pygame.font.SysFont("Arial", 16).render("Clear", True, black)
clear_button.blit(clear_button_text, (5, 5))
screen.blit(clear_button, (500-50, 100))

# Function to check if a number is already in the same row, column or box
def check_validity(grid, row, col, number):
    # check if the number is already in the same row
    if number in grid[row]:
        return False
    # check if the number is already in the same column
    if number in [grid[i][col] for i in range(9)]:
        return False
    # check if the number is already in the same 3x3 box
    box_row = (row // 3) * 3
    box_col = (col // 3) * 3
    for i in range(3):
        for j in range(3):
            if grid[i + box_row][j + box_col] == number:
                return False
    return True

# Function to display a pop-up message
# Function to display an error pop-up box
def display_error_box(error_message, x, y):
    # Create the error box
    error_box = pygame.Surface((200, 100))
    error_box.fill(white)
    pygame.draw.rect(error_box, black, (0, 0, 200, 100), 2)
    # Create the error message
    error_font = pygame.font.Font(None, 18)
    error_text = error_font.render(error_message, True, black)
    error_box.blit(error_text, (50, 25))
    # Blit the error box to the screen
    screen.blit(error_box, (x, y))
    pygame.display.flip()
    # Wait for user input
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

# Run the game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle mouse clicks
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Get the mouse coordinates
            x,y = pygame.mouse.get_pos()
            if solve_button.get_rect(topleft=(500-50,0)).collidepoint(x, y):
                # Solve the grid
                print("Solving...")
                solve_sudoku(grid)
                # print_board(grid)
                draw_grid(grid)
        
            if clear_button.get_rect(topleft=(500-50,100)).collidepoint(x, y):
                # Clear the grid
                print("Clearing...")
                # functionality not yet implemented     

            # Calculate the cell coordinates
            row = y // 50
            col = x // 50
            # check if user wants to delete the number, or add a new number
            if pygame.key.get_mods() & pygame.KMOD_CTRL:
                grid[row][col] = 0
                # Redraw the cell
                pygame.draw.rect(screen, white, (col * 48, row * 48, 50, 50))
            else:
                current_cell = (row, col)
        elif event.type == pygame.KEYDOWN:
            # check which number key the user typed
            if event.unicode.isnumeric():
                number = int(event.unicode)
                # check if number is already in the same row, column or box
                if check_validity(grid, current_cell[0], current_cell[1], number):
                    grid[current_cell[0]][current_cell[1]] = number
                    # write the number on the cell
                    font = pygame.font.Font(None, 36)
                    text = font.render(str(grid[current_cell[0]][current_cell[1]]), True, black)
                    screen.blit(text, (current_cell[1] * 50 + 20, current_cell[0] * 50 + 15))
                else:
                    # display an error pop-up box, currently just a print statement
                    print("Error: Number already in row, column or box")


                    
    # Update the screen
    pygame.display.flip()

# Exit Pygame
pygame.quit()

