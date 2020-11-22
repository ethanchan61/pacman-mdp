# mdpAgents.py
# parsons/20-nov-2017
#
# Version 1
#
# The starting point for CW2.
#
# Intended to work with the PacMan AI projects from:
#
# http://ai.berkeley.edu/
#
# These use a simple API that allow us to control Pacman's interaction with
# the environment adding a layer on top of the AI Berkeley code.
#
# As required by the licensing agreement for the PacMan AI we have:
#
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

# The agent here is was written by Simon Parsons, based on the code in
# pacmanAgents.py

from pacman import Directions
from game import Agent
import api
import random
import game
import util

last_iterate = [[]]
class MDPAgent(Agent):
    # Constructor: this gets run when we first invoke pacman.py
    def __init__(self):
        print "Starting up MDPAgent!"
        name = "Pacman"

    # Gets run after an MDPAgent object is created and once there is
    # game state to access.
    def registerInitialState(self, state):
        print "Running registerInitialState for MDPAgent!"

        

    def createMapMatrix(self, state):
        width,height = api.corners(state)[3][0]+1,api.corners(state)[3][1]+1
        mapMatrix = [[0 for x in range(height)] for y in range(width)] 
        ghost_pos = api.ghosts(state)

        for i in api.food(state):
            mapMatrix[i[0]][i[1]]= 5
        for i in api.capsules(state):
            mapMatrix[i[0]][i[1]] = 5
        for i in api.ghostStatesWithTimes(state):

            mapMatrix[int(i[0][0])][int(i[0][1])] = -10

        for i in api.walls(state):
            mapMatrix[i[0]][i[1]] = None
        return mapMatrix



    # This is what gets run in between multiple games
    def final(self, state):
        print "Looks like the game just ended!"


    def bellman(self, state, mapMatrix, reward, gamma):
        index = 80
        while index > 0:
            corners = api.corners(state)
            old_value = mapMatrix
            for i in range(corners[3][0]):
                for j in range(corners[3][1]):
                    if old_value[i][j] != None and old_value[i][j]!=-10 and old_value[i][j]!=5:
                        if old_value[i][j+1]!=None:
                            up = old_value[i][j+1]
                        else:
                            up = old_value[i][j]
                        if old_value[i][j-1]!=None:
                            down = old_value[i][j-1]
                        else:
                            down = old_value[i][j]
                        if old_value[i+1][j]!=None:
                            right = old_value[i+1][j]
                        else:
                            right = old_value[i][j]
                        if old_value[i-1][j]!=None:
                            left = old_value[i-1][j]
                        else:
                            left = old_value[i][j]
                        mapMatrix[i][j]= reward + gamma * max((0.8*up+0.1*left+0.1*right),(0.8*down+0.1*left+0.1*right),(0.8*left+0.1*up+0.1*down),(0.8*right+0.1*up+0.1*down))
            index -= 1
            old_value  = None
        return mapMatrix



    

    def policy_selection(self, state):

        new_map = self.createMapMatrix(state)
        iterated_value = self.bellman(state,new_map,-0.04, 0.6)
        pacman = api.whereAmI(state)
        left = iterated_value[pacman[0]-1][pacman[1]]
        right = iterated_value[pacman[0]+1][pacman[1]]
        up = iterated_value[pacman[0]][pacman[1]+1]
        down = iterated_value[pacman[0]][pacman[1]-1]
        if max(left,right,up,down)==up:
            return Directions.NORTH
        if max(left,right,up,down)==down:
            return Directions.SOUTH
        if max(left,right,up,down)==left:
            return Directions.WEST
        if max(left,right,up,down)==right:
            return Directions.EAST
        




    def getAction(self, state):
        direction = self.policy_selection(state)
        legal = api.legalActions(state)

        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        actual_selected_direction = api.makeMove(direction, legal)
        return actual_selected_direction


