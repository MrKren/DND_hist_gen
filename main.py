import numpy as np
from mpl_toolkits.mplot3d import Axes3D  # necessary for 3d plot
from matplotlib import cm
from noise import snoise2
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib.colors import LightSource


class World(object):

    def __init__(self):
        """Generates a grid of values to be used for a map"""
        self.size = (1000, 1000)
        self.elevation = np.zeros(self.size)
        self.moisture = np.zeros(self.size)
        self.sea_value = 0
        self.land_value = 0
        self.land_gen()
        self.land_value = (1 - (self.sea_value / (self.size[0] * self.size[1])))
        print("Land Mass: ", self.land_value * 100, "%")
        self.X = np.arange(0, self.size[0], 1)
        self.Y = np.arange(0, self.size[1], 1)
        self.Z_e = self.elevation
        self.Z_m = self.moisture

    def land_gen(self):
        """
        Uses simplex noise to create a random map of values that roughly resemble real life elevation values
        Uses notes from https://www.redblobgames.com/maps/terrain-from-noise/
        """
        self.sea_value = 0
        elevation_seed = np.random.randint(1, 1000)
        moisture_seed = np.random.randint(1, 1000)
        print("Elevation seed: ", elevation_seed, "\nMoisture seed: ", moisture_seed)
        for x in range(self.size[0]):
            for y in range(self.size[1]):

                elevation = snoise2(x/self.size[0], y/self.size[1], octaves=8, base=elevation_seed)/2 + 0.5
                moisture = snoise2(x/self.size[0], y/self.size[1], octaves=24, base=moisture_seed)/2 + 0.5
                sea_level = 0.4
                if elevation < sea_level:
                    self.sea_value += 1
                self.elevation[x][y] = elevation
                self.moisture[x][y] = moisture

    def plot2d(self):
        """Plots various 2d plots using the terrain data generated"""
        fig, ax = plt.subplots()
        elevation_map = ax.contourf(self.X, self.Y, self.Z_e.transpose(), cmap=cm.viridis)
        fig.colorbar(elevation_map)

        skip_val = 30
        skip = (slice(None, None, skip_val), slice(None, None, skip_val))
        V, U = np.gradient(-self.elevation[skip].transpose())
        plt.quiver(self.X[skip[0]], self.Y[skip[0]], U, V)

        plt.title("Elevation Map with Vector Field")
        plt.show()

        plt.show()

        plt.hist(self.Z_e.ravel(), bins=40, range=(0, 1))
        plt.title("Histogram of Elevation Values")
        plt.show()

        fig, ax = plt.subplots()
        moisture_map = ax.contourf(self.X, self.Y, self.Z_m.transpose(), cmap=cm.coolwarm_r)
        fig.colorbar(moisture_map)
        plt.title("Moisture Map")
        plt.show()

        ls = LightSource(azdeg=315, altdeg=45)
        fig, ax = plt.subplots()
        rgb = ls.shade(np.flipud(self.Z_e.transpose()), vert_exag=1000, blend_mode='soft', cmap=cm.gist_earth)
        ax.imshow(rgb)
        plt.show()

    def plot3d(self):
        """Plots a 3d contour graph using the elevation values"""
        # TODO change angle graph viewed from
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.plot_surface(self.X, self.Y.transpose(), self.Z_e.transpose(), antialiased=True, cmap=cm.gist_earth)
        plt.show()

    def plotmini(self):
        """Creates image using terrain gradient"""
        mini_map = np.zeros((self.size[1], self.size[0], 3), dtype=np.uint8)
        colour_map = Image.open("colour_map.jpg")
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                y = int(self.elevation[i][j] * 100)
                x = int(self.moisture[i][j] * 100)
                mini_map[-j][i] = colour_map.getpixel((x, y))
        img = Image.fromarray(mini_map, 'RGB')
        img.show()


def main():
    world_map = World()
    world_map.plot2d()
    #world_map.plot3d()
    world_map.plotmini()


if __name__ == "__main__":
    main()
