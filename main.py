import numpy as np
from mpl_toolkits.mplot3d import Axes3D  # necessary for 3d plot
from matplotlib import cm
from opensimplex import OpenSimplex
import matplotlib.pyplot as plt
from random import randint
import math


class World(object):

    def __init__(self):
        """Generates a grid of values to be used for a map"""
        self.size = (100, 100)
        self.tiles = np.zeros(self.size)
        self.octaves = 7
        self.sea_value = 0
        self.land_value = 0
        attempts = 1
        while True:
            self.land_gen()
            self.land_value = (1 - (self.sea_value / (self.size[0] * self.size[1])))
            print("attempt:", attempts)
            print("Land Mass: ", self.land_value * 100, "%")
            attempts += 1
            if 0.75 < self.land_value < 0.9:
                break
        self.X = np.arange(0, self.size[0], 1)
        self.Y = np.arange(0, self.size[1], 1)
        self.Z = self.tiles

    def land_gen(self):
        """
        Uses simplex noise to create a random map of values that roughly resemble real life elevation values
        Uses notes from https://www.redblobgames.com/maps/terrain-from-noise/
        """
        # TODO add moisture generation and create climate gradient
        noise_gen = OpenSimplex(seed=randint(0, 10e7))
        self.sea_value = 0
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                elevation = 0
                for octave in range(self.octaves):
                    nx = x/self.size[0]
                    ny = y/self.size[1]
                    elevation += 1/(2**octave) * noise_gen.noise2d(nx*2**octave, ny*2**octave)
                elevation = 1/(1+math.pow(math.e, elevation))
                sea_level = 0.5
                if elevation < sea_level:
                    elevation = sea_level
                    self.sea_value += 1
                self.tiles[x][y] = elevation

    def plot2d(self):
        """Plots a 2d contour graph using the elevation values"""
        fig, ax = plt.subplots()
        ax.contourf(self.X, self.Y, self.Z)
        plt.show()

    def plot3d(self):
        """Plots a 3d contour graph using the elevation values"""
        # TODO change angle graph viewed from
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.plot_surface(self.X, self.Y, self.Z, cmap=cm.coolwarm, linewidth=0, antialiased=False)
        plt.show()


def main():
    world_map = World()
    world_map.plot2d()


if __name__ == "__main__":
    main()
