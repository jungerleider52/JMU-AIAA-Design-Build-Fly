"""NACA Airfoil Dimensions Calculator.
https://en.wikipedia.org/wiki/NACA_airfoil

Author: Joey Ungerleider
Version: 11-21-24
"""
import numpy as np
import math
import matplotlib.pyplot as plt

def symmetric_airfoil(chord, thickness):
    """
    Generate a curve for a symmetrical NACA airfoil

    Args:
        chord: desired chord length of the wing
        thickness: percent of chord length, max thickness of the wing
    Return:
        filename: local filename to save the dims to
    """
    if not 0 < thickness < 1:
        print("Error: Thickness must be a value between 0 and 1")
        return None
    elif chord <= 0:
        print("Error: Chord length must be greater than 0")
        return None
    thickness = round(thickness, 2)

    # calculate n position points from 0 to 1.0
    n = 1000
    x = np.linspace(start=0, stop=1, num=n)

    # generate half-thickness values at a given x position (centerline to outer edge)
    filename = f"NACA-00{int(thickness*100)}_CHORD-{chord}"
    filename = 'Wing_Design/NACA_Wings/' + filename
    with open(filename, 'w') as file:
        for i in range(len(x)):
            yt = 5*thickness*(0.2969*math.sqrt(x[i]) - 0.126*x[i] - 0.3516*math.pow(x[i],2) + 0.2843*math.pow(x[i],3) - 0.1015*math.pow(x[i],4))
            x_actual = x[i] * chord
            y_actual = yt * chord
            file.write(f"{x_actual} {y_actual} 0\n")
        file.write(f"{chord} 0 0\n")

    print(f"\n~~ Generated a NACA 00{int(thickness*100)} airfoil; chord length {chord}. Saved to: {filename} ~~\n")
    return filename


def cambered_airfoil(chord, thickness, filename):
    """
    Generate a curve for a cambered NACA airfoil

    Args:
        chord: desired chord length of the wing
        thickness: percent of chord length, max thickness of the wing
        filename: local filename to save the dims to
    """
    pass


def plot_airfoil_2D(filename):
    """
    Plot an airfoil cross section.

    Args:
        filename: name of airfoil file to plot
        NACA_code: NACA code of the airfoil
    """
    x = []
    y = []
    for line in np.loadtxt(filename, delimiter=' '):
        x.append(line[0])
        y.append(line[1])
    y_i = [num*(-1) for num in y]

    plt.gca().set_aspect('equal', adjustable='box')
    plt.grid()
    plt.plot(x, y, c='k')
    plt.plot(x, y_i, c='k')
    plt.show()


if __name__ == "__main__":
    # airfoil = symmetric_airfoil(5, 0.15)
    # plot_airfoil_2D(airfoil)
