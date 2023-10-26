"""
    Auto Brake Simulation Szenborn Jan, Rostkowski Wiktor,  2023

    The code initializes a simulation environment in Pygame, which simulates a train moving along a track with the help of an automatic braking system.

    It uses the Pygame library to create a graphical user interface for the simulation.

    The simulation consists of a train (represented as a red circle) and a track (a set of connected line segments).

    The train can move along the track and its position is updated over time.

    The simulation continuously runs a loop to handle events, update the train's position, and draw the current state of the simulation.

    The train's position is updated based on its speed and the time elapsed since the last update.

    The code calculates the distance between the train and the closest point on the track and the remaining distance to the turn using mathematical calculations.

    The simulation also allows for user interactions, such as restarting the train's position or reinitializing the track.

    The graphical user interface displays the track, the train, and the current speed of the train.

    The simulation loop continues until the user closes the application or presses the 'R' key to reset the simulation.

    The simulation loop can restart any time and create new triangle just  presses the 'R' key to reset the simulation
"""
from Auto_Brake_System.controller import TrainBrakingController
#!/usr/bin/python3

from map import Map
from simulation import Simulation
from train import Train

MAP_WIDTH = 800
MAP_HEIGHT = 800

if __name__ == '__main__':
    controller = TrainBrakingController()
    game_map = Map((MAP_WIDTH, MAP_HEIGHT), turns=3)
    train = Train()

    simulation = Simulation(game_map, train, controller)

    simulation.run()
