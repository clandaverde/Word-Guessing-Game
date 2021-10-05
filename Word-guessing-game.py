# Christian Landaverde
# Word Guessing Game Lab
# 04/10/2020


from graphics import *
import random

# returns random puzzle from puzzles.txt file
def get_puzzle():
    # reads all puzzles
    input_file = open("puzzles.txt", "r")
    # makes all puzzles to a string
    s_puzzles = input_file.read()
    # splits any lines breaks
    l_puzzles = s_puzzles.split("\n")
    # closes file
    input_file.close()

    i_num_puzzles = len(l_puzzles)
    # length of puzzle is 10
    # you subtract one since 0-9 = (10 values)
    # 0 to 10 is 11 values
    i_puzzle_number = random.randint(0, i_num_puzzles - 1)
    s_puzzle = l_puzzles[i_puzzle_number]

    return s_puzzle


# shows graphical display to user
# takes the graphic window & puzzle as input
# returns entry object
def show_display(window, s_puzzle):
    window.setBackground("aliceblue")

    # Draws the upper left lines
    i_num_letters = len(s_puzzle)
    for i in range(i_num_letters):
        line = Line(Point(280 + (i * 30), 85), Point(280 + (i * 30) + 25, 85))
        line.draw(window)

    # Draw where to enter guess and available letters
    enter_letter = Text(Point(100, 300), "Enter a letter:")
    enter_letter.draw(window)
    submit_text = Text(Point(270, 300), "Submit")
    submit_text.draw(window)
    avail_letter = Text(Point(265, 320), "Letters Available : a b c d e f g h i j k l m n o p q r s t u v w x y z")
    avail_letter.draw(window)

    entry_guess = Entry(Point(185, 300), 8)
    entry_guess.draw(window)

    button_rectangle = Rectangle(Point(240, 310), Point(300, 288))
    button_rectangle.draw(window)
    
    incorrect_text = Text(Point(115, 400), "Incorrect Guesses")
    incorrect_text.draw(window)

    for i in range(6):
        icircle = Circle(Point(80 + (i * 80), 450), 30)
        icircle.draw(window)

    return entry_guess


# gets a guess from user & returns it
# needs the list of available letter, entry box
# and the window as input
# and returns the guess
def get_guess(l_available_letters, entry_box, window):
    s_guess = ""
    while validate_guess(s_guess, l_available_letters) == False:
        p_mouse_click_point = window.getMouse()
        i_x_coordinate = p_mouse_click_point.getX()
        i_y_coordinate = p_mouse_click_point.getY()
        while (i_x_coordinate < 240 or i_x_coordinate > 300) or (i_y_coordinate > 310 or i_y_coordinate < 288):
            p_mouse_click_point = window.getMouse()
            i_x_coordinate = p_mouse_click_point.getX()
            i_y_coordinate = p_mouse_click_point.getY()

        s_guess = entry_box.getText()
    
    return s_guess


# takes a guess and the list of available letters from the
# user and returns a boolean indicating whether the guess
# is valid or not
def validate_guess(s_guessed_letter, l_available_letters):
    if s_guessed_letter in l_available_letters:
        b_valid = True
    else:
        b_valid = False
    return b_valid


# takes a guess, the list of available letters, the number of wrong guesses,
# and the graphics window as input and returns a boolean indicating whether
# the guess was in the puzzle.    
def process_guess(l_available_letters, i_number_wrong_guesses, s_guess, window, s_puzzle):
    update_available_letters(l_available_letters, s_guess)
    
    if s_guess not in s_puzzle:
        i_number_wrong_guesses = i_number_wrong_guesses + 1
        
    update_display(l_available_letters, i_number_wrong_guesses, window, s_guess, s_puzzle)
    
    return i_number_wrong_guesses


# takes the list of available letters and the guessed letter and updates the
# list of available letters
def update_available_letters(l_available_letters, s_guessed_letter):
    l_available_letters.remove(s_guessed_letter)
    

# updates the display with the new list of available letters, the new number
# of incorrect guesses, and reveals any correctly guessed letter.
# Takes the graphics window, the list of available letters, the guessed
# letter, the puzzle, and the number of incorrect guesses.
def update_display(l_available_letters, i_number_wrong_guesses, window, s_guess, s_puzzle):
    
    # reveal any new letter in the puzzle that was guessed
    for i in range(len(s_puzzle)):
        if s_guess == s_puzzle[i]:
            text_reveal = Text(Point(292 + (i * 30), 75), s_guess)
            text_reveal.draw(window)
            # Point(280 + (i * 30), 85)

    # repaint list of available letters
    s_avail_letter = "Letters Available: "
    for s_letter in l_available_letters:
        s_avail_letter = s_avail_letter + s_letter + " "
    for i in range(i_number_wrong_guesses):
        s_avail_letter = s_avail_letter + " "

    rect = Rectangle(Point(0, 312), Point(500, 332))
    rect.setFill("aliceblue")
    rect.setOutline("aliceblue")
    rect.draw(window)  
    avail_letter = Text(Point(265, 320), s_avail_letter)
    avail_letter.draw(window)


    # may have to fill in circle if guess was wrong
    if s_guess not in s_puzzle:
        circle = Circle(Point(80 - 80 + (i_number_wrong_guesses * 80), 450), 30)
        circle.draw(window)
        circle.setFill("darkblue")
        circle.setOutline("darkblue")

        
# determines if a player has solved the puzzle
# takes list of available letters and the puzzle as input
# returns boolean 
def check_win(l_available_letters, s_puzzle):
    b_won = True
    for letter in s_puzzle:
        if letter in l_available_letters:
            b_won = False            

    return b_won

    
def main():
    s_puzzle = get_puzzle()
    # print(s_puzzle)
    window = GraphWin("Word guessing game", 800, 700)
    entry_box = show_display(window, s_puzzle)
    i_number_wrong_guesses = 0
    b_solved_puzzle = False
    l_available_letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
                           "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                           "u", "v", "w", "x", "y", "z"]

    while i_number_wrong_guesses < 6 and b_solved_puzzle == False:
        s_guessed_letter = get_guess(l_available_letters, entry_box, window)
        i_number_wrong_guesses = process_guess(l_available_letters, i_number_wrong_guesses, s_guessed_letter, window, s_puzzle)
        b_solved_puzzle = check_win(l_available_letters, s_puzzle)
    
    if i_number_wrong_guesses < 6:
        text_game_over = Text(Point(400, 200), "You Win!")
    else: # user lost
        text_game_over = Text(Point(400, 170), "You Lose!")
        text_game_over2 = Text(Point(400, 225), "The Puzzle Was: " + s_puzzle)
        text_game_over2.setTextColor("dodgerblue")
        text_game_over2.setSize(30)
        text_game_over2.draw(window)
        
    text_game_over.setTextColor("dodgerblue")
    text_game_over.setSize(30)
    text_game_over.draw(window)

main()
