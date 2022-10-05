# Aiyush Gupta - Tic Tac Toe

*October 2022*

---

![wer](/Users/aiyushgupta/Documents/Computer%20Science/a-level-tasks/a-level-tasks-sm-tm/noughtsCrosses/report/images/ticTacToeMockup.png)

# Specification

- [x] Single Player vs Computer
  
  - [x] Hard & Easy Mode

- [x] PvP

- [x] Random *~~Player~~* Choice of Going First or Second

- [x] GUI ~~Text Based~~

# An explanation of how the key concepts of <u>abstraction</u>, <u>algorithms</u> and <u>state</u> apply to this task.

Within this project, the key concepts are evident throughout. From the computer algorithm to the design of the GUI.

## Abstraction

Abstraction within this game of Tic-Tac-Toe allows the player(s) to make use of the game and play against the "CPU" by hiding irrelevant information of how the algorithms themselves work. It allow the game to show important information in context.

Abstraction within TicTac Toe starts from the grid itself: the player can only choose 1 of 9 positions that are cleary shown within the grid. The two player options or `X` or `O` (or in my case two different colours) abstract unneccessary information about the player away ie. name, score so far etc... and result in a clear representation of where the player is.

Abstraction is also present during the game screen: only necessary information is shown to the player. Ie. the score of P1 / P2 and whose turn it is. Information that has been abstracted away are the variables containing informations such as when each square (cell) was clicked and who by (in previous rounds). 

Within my implementation, an OOP approach makes use of my objects which are an abstraction of real world entities ie. a physical naughts / crosses board, a pen to draw where the player is etc... In my case, real world entities are represented using computational structures to highlight important information in context. 

#### Representational Abstraction

*What remains after the unnecessary information has been removed*

By employing a GUI over a text-based game alot of the information that would be displayed as text / ASCII characters has been replaced with shapes and colours that help to convey information in a more accessible and clear manner.

In the final project, even the choosing of grid position has been abstracted from the in-real-life game of drawing shapes to simply clicking a cell within the grid.

#### Abstraction by Generalisation

By grouping things by common characteristics, within the main game loop they can be referenced easily ie. the main grid contains smaller grid cells which inherits from a simple sprite class. This makes the project more easy to manage. *However, in some cases I recognise within my code additional classes could have been created to reduce the total amount of code but haven't done so to maintain readbility.*

#### Procedural Abstraction

*Makes an apperance within decomposition*

Used to abstract a procedure to make it as general as possible. Ie. The procedure for calculating the score of a game is further removed from the UI and generalised for any game where the score is increased by a certain amount.

This is further seen in the `gameState` class where large amounts of information relevant to any game are abstracted away in a single class to be made accessible to the entire scope of the game.

Ie. Procedural abstraction of whether player has won,  *would work in most / any game context*

```python
def hasWon(self, winner, incrementBy):
    gameState.won = True
    game.State.wonBy = winner
    gameState.score += incrementBy
```

Ie. Procedural abstraction of incrementing a game turn: which would work in any game.

```python
def incrementTurn(self): # State of p1 or p2
        # Swaps player turns from 1 to 2
        self.turn = 0 if self.turn else 1
```

## State

State is very relevant within this task as everything has state in context ie. the player move is simply represented as `clicked` / `unclicked` or `1`/`0` or `occupied`/`unoccupied` etc... There are two states of a single cell describing whether it has been clicked yet and a futher state describing who it is clicked by. Binary, being the mathematical application of state, could be used in noughts and crosses to represent the grid itself: the entire grid could be occupied with no winner etc... 

The difficulty ratings within the game are either `easy `/`difficult`, the number of rounds aren't a binary state but a trinary state of being selected, whether the mode is `pVp` or `1 vs Computer` is also maintined throughout. As a result of having relied heavily on the state of different items within the game, checking for certain conditions / equality is made more clear and concise.

## Algorithms

Every output within the game is a result of a process, an algorithm is a step-by-step instruction that defines what to do: this is most heavily featured within the game as the computer "*decides*" what move to make.

Algorithms are also featured within the flow of the game itself, from the menu presenting which buttons should be featured based upon user selection, to showing the game screen, to showing the end screen.

Overall, each algorithm is self-contained but the higher-level algorithms contains smaller-algorithms that help to carry out specific processes *(see top down decomposition).*

Example of *abstracted* main menu algorithm:

![wer](/Users/aiyushgupta/Documents/Computer%20Science/a-level-tasks/a-level-tasks-sm-tm/noughtsCrosses/report/images/MainMenuFlowchart.drawio.png)

# Additional Features

- Music

- Theming for the GUI
  
  - Using a basic JSON API 

- GUI
  
  - Menu
  
  - End Screen
  
  - Choose Number of rounds
