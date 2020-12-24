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

Sudoku Game Layout
![Base](https://user-images.githubusercontent.com/7936928/103102807-cfeb7580-4643-11eb-8937-66769d1d77fb.JPG)

Rough Cell Working
![WithRoughCells](https://user-images.githubusercontent.com/7936928/103102817-e265af00-4643-11eb-803f-189b7628a79c.JPG)

 Right Wrong Population of Numbers
![Wrong-Right](https://user-images.githubusercontent.com/7936928/103102819-e5f93600-4643-11eb-930e-14d9ec5b87a8.JPG)


