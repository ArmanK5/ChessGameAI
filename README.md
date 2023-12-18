# ChessGameAI
A Python-based chess game that utilises a minmax algorithm
If there are any mistakes or possibilities for efficiencies please send a pull request :)

Currently, the choice to play against AI or humans has to be changed within the source code. I will get onto that ASAP. For now default setting will be black as AI and white as the player

Controls:
Run the ChessMain.py file
Click on a piece with left mouse click and valid moves for the piece will be highlighted, click any of these squares to move the piece
R is to reset the board
Z is to undo the move (currently gimmicky if trying to undo an AI move)

How it works:
As I have stated previously, this utilises a minMax algorithm, processed as a zero-sum game.
Each piece has been evaluated on its strength to the player and given a point on that basis (for example, pawn receives 1, knight receives 3 and queen 5 etc)
After every move, the algorithm runs and compiles the worth of the pieces it can take at the current moment and if it can affect the score in the current player's favour.
This evaluation happens in branches and works on if the player were to make that move what would happen next, so it technically makes that move in a temporary game state, then evaluates the enemy player's next move.
It would calculate the score (based on the piece valuation earlier), and if that path processes a negative score then it would move to the next and save the highest score through a for-loop to process the algorithm for each valid move.
In effect maximise the minimum gains of the player.

After that long description, have an attempt at beating the AI and try not to lose!
