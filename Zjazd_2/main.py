#!/usr/bin/python3

from map import Map
from simulation import Simulation
from train import Train

MAP_WIDTH = 800
MAP_HEIGHT = 800

if __name__ == '__main__':
    game_map = Map((MAP_WIDTH, MAP_HEIGHT), turns=3)
    train = Train()

    simulation = Simulation(game_map, train)

    simulation.run()
