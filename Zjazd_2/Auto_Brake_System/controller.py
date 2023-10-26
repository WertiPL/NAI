"""

Auto Brake System Szenborn Jan, Rostkowski Wiktor,  2023


The code is designed to address a problem related to train braking control.
It uses fuzzy logic to determine the braking force required for a train based on three input parameters:
    distance to turn, angle of turn, and speed of the train.
    The goal is to provide a braking force recommendation to ensure safe and effective train control when navigating curves or turns.
    The code defines membership functions and rules for the fuzzy logic system to make these braking force recommendations,
    and it can also generate graphs to visualize the relationships between the input parameters and the recommended braking force.



"""

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt


class TrainBrakingController:

    def __init__(self):
        self.distance_to_turn = ctrl.Antecedent(np.arange(0, 800, 1), 'distance_to_turn')
        self.angle_of_turn = ctrl.Antecedent(np.arange(0, 180, 1), 'angle_of_turn')
        self.speed_of_train = ctrl.Antecedent(np.arange(0, 5, 1), 'speed_of_train')
        self.braking_force = ctrl.Consequent(np.arange(0, 2, 1), 'braking_force')
        self.rules = []
        self.controller = self.init_controller()

    def generate_distance_to_turn_mf(self):
        self.distance_to_turn.automf(number=3, names=['slight', 'moderate', 'sharp'])

    def generate_angle_of_turn_mf(self):
        self.angle_of_turn.automf(number=3, names=['small', 'medium', 'large'])

    def generate_speed_of_train_mf(self):
        self.speed_of_train.automf(number=3, names=['slow', 'moderate', 'fast'])

    def generate_braking_force_mf(self):
        self.braking_force.automf(number=3, names=['light', 'moderate', 'heavy'])

    def generate_mf(self):
        self.generate_distance_to_turn_mf()
        self.generate_angle_of_turn_mf()
        self.generate_speed_of_train_mf()
        self.generate_braking_force_mf()

    def generate_rules(self):
        return [
            ctrl.Rule(self.distance_to_turn['slight'] & self.angle_of_turn['small'] & self.speed_of_train['slow'],
                      self.braking_force['light']),
            ctrl.Rule(self.distance_to_turn['moderate'] & self.angle_of_turn['medium'] & self.speed_of_train['moderate'],
                      self.braking_force['moderate']),
            ctrl.Rule(self.distance_to_turn['sharp'] & self.angle_of_turn['large'] & self.speed_of_train['fast'],
                      self.braking_force['heavy'])]

    def init_controller(self):
        self.generate_mf()
        self.rules = self.generate_rules()
        return ctrl.ControlSystem(self.rules)

    def simulate(self):
        return ctrl.ControlSystemSimulation(self.controller)

    def compute(self, distance_to_turn, angle_of_turn, speed_of_train):
        simulation = self.simulate()
        simulation.input['distance_to_turn'] = distance_to_turn
        simulation.input['angle_of_turn'] = angle_of_turn
        simulation.input['speed_of_train'] = speed_of_train
        simulation.compute()
        return simulation.output['braking_force']

    def plot_membership_functions_and_rules(self):
        # Plot the membership functions
        self.distance_to_turn.view()
        self.angle_of_turn.view()
        self.speed_of_train.view()
        self.braking_force.view()

        # Create a rule visualization
        rule1 = ctrl.Rule(self.distance_to_turn['slight'] & self.angle_of_turn['small'] & self.speed_of_train['slow'],
                          self.braking_force['light'])
        rule2 = ctrl.Rule(self.distance_to_turn['moderate'] & self.angle_of_turn['large'] & self.speed_of_train['fast'],
                          self.braking_force['light'])
        rule3 = ctrl.Rule(self.distance_to_turn['sharp'] & self.angle_of_turn['medium'] & self.speed_of_train['slow'],
                          self.braking_force['light'])
        rule1.view()
        rule2.view()
        rule3.view()

        # Display the graphs
        plt.show()


# Create an instance of TrainBrakingController
controller = TrainBrakingController()

# Call the method to generate and display the fuzzy logic graphs
controller.plot_membership_functions_and_rules()

# Example usage of the controller
braking_force = controller.compute(400, 90, 3)
# braking_force2 = controller.compute(30, 90, 4)
print(f"Braking Force: {braking_force}")
# print(f"Braking Force: {braking_force2}")
