#The Main File for the app
import numpy
from scipy.spatial import Voronoi, voronoi_plot_2d

num_points=10

def GenVoronoi():
    rng =numpy.random.default_rng()
    roints= rng.random((10,2))
    vor=Voronoi(roints)
    return vor


if __name__ == '__main__':
    #showing the voronoi plot
    voro=GenVoronoi()
    points=voro.points
    for p in range(0,num_points):
        print(points[p])


