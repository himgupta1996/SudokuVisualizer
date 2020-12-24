# SudokuVisualizer

Here is a Python implementation of a popular puzzle game - SUDOKU. In this project, I have tried to build a interactive sudoku puzzle using pygame module and 
visualizer of the backtracking algorithm used to solve it. This SUDOKU has the following functionalities:
1. Working is same as of the normal sudoku puzzle.
2. Buttons:
    1. RESET: Reset the entire playboard to initial setting for the player to start again
    2. Toggle Rough Cell: Toggles the cell from normal cell to rough cell where the player can jot down the possible values for the
        cell without loosing a chance. One has to again press the button to go back to the normal state where the player can
        mark the desired value. This button only toggles the current selected cell marked by a blue bounding square.
3. Time: Player can asses how much time it is taing him/her to finish the puzzle.
4. Space Bar: The Sudoku Solver comes into picture and let you visualize how the computer solves the problem using backtraking algorithm.
5. If you enter a value that defys the sudoku rule, a red bounding box will be showed till the value is not rectified.
4. X: Close the Sudoku Game.

![image](https://user-images.githubusercontent.com/7936928/103102754-77b47380-4643-11eb-94f5-8f29ecdc42d1.png)
