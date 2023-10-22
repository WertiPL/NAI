#!/usr/bin/python3

from map import Map
from simulation import Simulation

MAP_WIDTH = 800
MAP_HEIGHT = 800

if __name__ == '__main__':
    game_map = Map((MAP_WIDTH, MAP_HEIGHT), turns=3)
    simulation = Simulation(game_map)

    simulation.run()
