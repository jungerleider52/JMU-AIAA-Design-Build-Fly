"""Data stripper for xflr5 export files.

This program takes multiple .txt file in the format exported from
xflr5 and extracts the Reynolds number, angle of attack (aoa / alpha), 
cL and cD from each file. It plots aoa vs. cL/cD for each Reynolds
number, and plots it on the same 3D graph. 

Author: Joey Ungerleider
Version: 9/9/2025
"""

import numpy as np
import matplotlib.pyplot as plt
import regex as re
from pathlib import Path

def process_airfoil(airfoil, graph_switch=True):

    # OPTIONAL USER INPUT: airfoil = input("Enter Airfoil (no spaces or caps): ")
    folder = Path("xflr5data/" + airfoil)
    numRey = len(list(folder.glob("*.txt")))

    foilArray = []
    for filename in folder.glob("*.txt"):
        # import data
        try:
            dArray = np.loadtxt(filename, skiprows=11, usecols=(0, 1, 2, 3))
        except Exception as e:
            print(f"Error reading {filename.name}: {e}\n")
            continue

        # find reynolds number
        reyN = 0
        with open(filename, 'r') as file:
            for line in file:
                match = re.search(r"Re\s*=\s*([\d\.]+)\s*e\s*(\d+)", line)
                if match:
                    base = float(match.group(1))
                    exponent = int(match.group(2))
                    reyN = base * (10 ** exponent)
                    break

        # set reynolds number at fourth column
        for i in range(len(dArray)):
            dArray[i,3] = reyN

        # add this reynolds num to the airfoil array
        foilArray.append(dArray)

    # visualization

    if graph_switch:
        # aoa vs. cL
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        R = np.linspace(0.27, 0.796, numRey)
        G = np.linspace(0, 0.714, numRey)
        B = np.linspace(0.52, 0.467, numRey)

        for i in range(numRey):
            ax.plot(foilArray[i][:, 0], foilArray[i][:, 3], foilArray[i][:, 1],
                    color=[R[i], G[i], B[i]], linewidth=1.2)

        ax.set_xlabel('Angle of Attack (deg)')
        ax.set_ylabel('Reynolds Number')
        ax.set_zlabel('Coefficient of Lift')
        ax.set_title(f"AoA vs. cL at each Reynolds Number, for airfoil: {airfoil.upper()}")
        plt.grid(True)
        plt.show()

        # aoa vs. cD
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        for i in range(numRey):
            ax.plot(foilArray[i][:, 0], foilArray[i][:, 3], foilArray[i][:, 2],
                    color=[R[i], G[i], B[i]], linewidth=1.2)

        ax.set_xlabel('Angle of Attack (deg)')
        ax.set_ylabel('Reynolds Number')
        ax.set_zlabel('Coefficient of Drag')
        ax.set_title(f"AoA vs. cD at each Reynolds Number, for airfoil: {airfoil.upper()}")
        plt.grid(True)
        plt.show()

        # cL vs. cD
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        for i in range(numRey):
            ax.plot(foilArray[i][:, 1], foilArray[i][:, 3], foilArray[i][:, 2],
                    color=[R[i], G[i], B[i]], linewidth=1.2)

        ax.set_xlabel('Coefficient of Lift')
        ax.set_ylabel('Reynolds Number')
        ax.set_zlabel('Coefficient of Drag')
        ax.set_title(f"cL vs. cD at each Reynolds Number, for airfoil: {airfoil.upper()}")
        plt.grid(True)
        plt.show()

if __name__ == "__main__":
    process_airfoil("naca0012")