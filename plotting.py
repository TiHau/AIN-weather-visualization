import matplotlib.pyplot as plt
import numpy as np

height = 5
elevation = [3, 4, 4, 4, 2, 2, 3, 4, 5, 4]


# arrival_time: time of arrival as last value on x-axis
# height: highest displayed point above sea level
def plotting(arrival_time):

    # NEEDED FOR VISUALIZATION
    # altitude (y-axis)
    # flight time (x axis)
    # wind speed
    # wind direction
    # elevation (separate plot)

    x = np.linspace(0, arrival_time, num=10)  # x-axis displays 50 values from start to arrival
    y = np.linspace(0, height, num=10)  # y-axis displays 50 values from 0 to 60.000 metres above sea level

    # calculate the points on the grid where the wind barbs are to be displayed later
    X, Y = np.meshgrid(x, y)
    # creating a matrix for U and V coordinates FOR TEST PURPOSES
    u, v = X, Y

    # plot barb for each grid coordinate
    plt.barbs(X, Y, u, v)
    # plot elevation
    plt.plot(elevation)
    plt.show()

if __name__ == '__main__':
    plotting(10)
