# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newFoodList = newFood.asList()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        # Return 0 if gonna die to ghost, never the correct choice
        for ghost in newGhostStates:
            if newPos == ghost.getPosition():
                return 0

        # return 2 if food was picked up
        if successorGameState.getNumFood() + 1 == currentGameState.getNumFood():
            return 2

        # Find the manhattan distances to all foods
        distances = []
        for food in newFoodList:
            distances.append(manhattanDistance(newPos, food))
        
        # Return the distance to the minimum
        return 1 / min(distances)

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        # Enter minimax with the depth and agentNum set to 0
        # turn = True indicates it's pacman's turn (agent = 0)
        return self.minimax(gameState, 0, 0, True)

    def minimax(self, gameState, depth, agentNum, turn):
        """Minimax search implementation

        Args:
            gameState (gameState): Object representing the game state
            depth (int): Initially 0, it represents the layer of the minimax tree we're on
            agentNum (int): Initially 0 (Pac-man), agents 1-numAgents are the ghosts
            turn (Bool): True if pacman's turn, False if ghost's turn

        Returns:
            Direction: Returns the move that is best given the minimax function
        """
        # Terminal state, return evaluation
        if depth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        # Pacman turn, agentNum = 0
        if turn:
            # Initialize max_value as -inf, and default action as stop
            max_value = float("-inf")
            best_action = Directions.STOP
            actions = gameState.getLegalActions(agentNum)
            for action in actions:
                successor = gameState.generateSuccessor(agentNum, action)
                # Don't increment depth initially, swap to min, with agentNum set to 1
                new_max_value = max(max_value, self.minimax(successor, depth, agentNum + 1, False))
                # Only update best_action if max_value is new
                if new_max_value > max_value:
                    max_value = new_max_value
                    best_action = action
            if depth == 0:
                # Return the action if it's the root node
                return best_action
            else:
                # Return value otherwise
                return max_value

        # Agent turn
        else:
            # Initial min value is infinity
            # Don't need to remember the best action for min
            min_value = float("inf")
            actions = gameState.getLegalActions(agentNum)
            for action in actions:
                # Last agent, go back to max, increment depth, agent = 0
                if agentNum + 1 == gameState.getNumAgents():
                    successor = gameState.generateSuccessor(agentNum, action)
                    # Increment depth and swap to max, agentNum set to 0
                    min_value = min(min_value, self.minimax(successor, depth + 1, 0, True))
                # Not last agent, remain in min, increment agent
                else:
                    successor = gameState.generateSuccessor(agentNum, action)
                    # Stay in min, don't increment depth since we're still on the same layer
                    min_value = min(min_value, self.minimax(successor, depth, agentNum + 1, False))
            return min_value

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        return self.expectimax(gameState, 0, 0, True)

    def expectimax(self, gameState, depth, agentNum, turn):
        # Terminal state, return evaluation
        if depth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        # Pacman turn, agentNum = 0
        if turn:
            # Initialize max_value as -inf, and best action as stop
            max_value = float("-inf")
            best_action = Directions.STOP
            actions = gameState.getLegalActions(agentNum)
            for action in actions:
                # Generate each successor 
                successor = gameState.generateSuccessor(agentNum, action)
                new_max_value = max(max_value, self.expectimax(successor, depth, agentNum + 1, False))
                # If new max_value is different, replace best_action
                if new_max_value > max_value:
                    max_value = new_max_value
                    best_action = action
            # Return action if it's the base node
            if depth == 0:
                return best_action
            # Return value otherwise
            else:
                return max_value

        # Agent turn
        else:
            # Use a list instead of a min value
            values = []
            actions = gameState.getLegalActions(agentNum)
            for action in actions:
                # Last agent, go back to max, increment depth, agent = 0
                if agentNum + 1 == gameState.getNumAgents():
                    successor = gameState.generateSuccessor(agentNum, action)
                    # Add elements to the list
                    values += [self.expectimax(successor, depth + 1, 0, True)]
                # Not last agent, remain in min, increment agent
                else:
                    successor = gameState.generateSuccessor(agentNum, action)
                    # Add elements to the list
                    values += [self.expectimax(successor, depth, agentNum + 1, False)]
            # Return the average of the list
            return sum(values) / len(values)

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    # Get current score, weigh this heavily
    score = scoreEvaluationFunction(currentGameState)
    pos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    foodList = food.asList()
    capsules = currentGameState.getCapsules()
    ghostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]

    # If its a win or lose, return an extreme bound
    if currentGameState.isWin():
        return float("inf")
    if currentGameState.isLose():
        return float("-inf")
    
    # Find the distance to all foods
    food_distances = []
    for food in foodList:
        food_distances.append(manhattanDistance(pos, food))

    # Find the distance to all ghosts
    ghost_distances = []
    for ghost in ghostStates:
        ghost_distances.append(manhattanDistance(pos, ghost.getPosition()))
        # Return an extreme if too close to a ghost, reduced number of pacman deaths 
        if manhattanDistance(pos, ghost.getPosition()) < 3:
            return float("-inf")

    # Set weights
    ghostWeight = (1000 / min(ghost_distances))
    if scaredTimes[0] == 0:
        ghostWeight *= -1 

    foodWeight = (100 / min(food_distances))
    scoreWeight = score * 100000

    # The larger this number, the better the position is currently 5/6, close to 6/6
    return scoreWeight + foodWeight + ghostWeight

# Abbreviation
better = betterEvaluationFunction
