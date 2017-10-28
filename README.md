###Artificial Intelligence Nanodegree

---
####Introductory Project: Diagonal Sudoku Solver

---
    <img src=images/sudoku-board-bare.jpg>

###Question 1 (Naked Twins)

Q: How do we use constraint propagation to solve the naked twins problem? 
A: Constraint Propagation is the repeated application of the same set of rules in order to minimize the solution space, until any further refinement is not possible/feasible. 
    
   With naked twins, the idea is to identify pair/s of boxes belonging to the same set of sudoku peers, such that the offending pairs have the same 2 numbers within their possible solutions.

    <img src=images/naked-twins.png>
    
   To do this we have to eliminate the common solution found in our naked_twin_pair from every other peer that is not in the naked_twin_pair, and has more possible solutions than our chosen pair.
    
    <img src=images/naked-twins-2.png>
    <img src=images/naked-twins-code.png>
    
###Question 2 (Diagonal Sudoku)

Q: How do we use constraint propagation to solve the diagonal sudoku problem? 

A: By including it as an additional way of counting units/peer space. Once done, all diagonal entries will have their corresponding diagonal peers. 
   Essentially making it behave similarly to the pre-existing Cartesian/Latin-Square Grid, by making it's own diagonal grid with *diagonal* rules.

    <img src=images/diagunits.png>
### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - Fill in the required functions in this file to complete the project.
* `test_solution.py` - You can test your solution by running `python -m unittest`.
* `PySudoku.py` - This is code for visualizing your solution.
* `visualize.py` - This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the `assign_value` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login) for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system.

