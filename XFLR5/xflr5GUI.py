"""Data stripper for xflr5 export files.

This program takes multiple .txt file in the format exported from
xflr5 and extracts the Reynolds number, angle of attack (aoa / alpha), 
cL and cD from each file. It plots aoa vs. cL/cD for each Reynolds
number, and plots it on the same 3D graph. 

Author: Joey Ungerleider
Version: 9/9/2025
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import re

def process_files(folder_path, graph_switch, output_box):
    txt_files = list(Path(folder_path).glob("*.txt"))
    numRey = len(txt_files)
    foilArray = []

    for filename in txt_files:
        try:
            dArray = np.loadtxt(filename, skiprows=11, usecols=(0, 1, 2, 3))
        except Exception as e:
            output_box.insert(tk.END, f"Error reading {filename.name}: {e}\n")
            continue

        # Extract Reynolds number
        reyN = 0
        with open(filename, 'r') as file:
            for line in file:
                match = re.search(r"Re\s*=\s*([\d\.]+)\s*e\s*(\d+)", line)
                if match:
                    base = float(match.group(1))
                    exponent = int(match.group(2))
                    reyN = base * (10 ** exponent)
                    break

        output_box.insert(tk.END, f"{filename.name}: Re = {reyN:.1f}\n")

        # Add Reynolds number to array
        rey_column = np.full((dArray.shape[0], 1), reyN)
        dArray = np.hstack((dArray, rey_column))
        foilArray.append(dArray)

    if graph_switch:
        R = np.linspace(0.27, 0.796, numRey)
        G = np.linspace(0, 0.714, numRey)
        B = np.linspace(0.52, 0.467, numRey)

        # Plot AoA vs cL
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        for i in range(numRey):
            ax.plot(foilArray[i][:, 0], foilArray[i][:, 4], foilArray[i][:, 1],
                    color=[R[i], G[i], B[i]], linewidth=1.2)
        ax.set_xlabel('Angle of Attack (deg)')
        ax.set_ylabel('Reynolds Number')
        ax.set_zlabel('Coefficient of Lift')
        ax.set_title("AoA vs. cL")
        plt.show()

        # Plot AoA vs cD
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        for i in range(numRey):
            ax.plot(foilArray[i][:, 0], foilArray[i][:, 4], foilArray[i][:, 2],
                    color=[R[i], G[i], B[i]], linewidth=1.2)
        ax.set_xlabel('Angle of Attack (deg)')
        ax.set_ylabel('Reynolds Number')
        ax.set_zlabel('Coefficient of Drag')
        ax.set_title("AoA vs. cD")
        plt.show()

        # Plot cL vs cD
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        for i in range(numRey):
            ax.plot(foilArray[i][:, 1], foilArray[i][:, 4], foilArray[i][:, 2],
                    color=[R[i], G[i], B[i]], linewidth=1.2)
        ax.set_xlabel('Coefficient of Lift')
        ax.set_ylabel('Reynolds Number')
        ax.set_zlabel('Coefficient of Drag')
        ax.set_title("cL vs. cD")
        plt.show()

def launch_gui():
    root = tk.Tk()
    root.title("XFLR5 Data Stripper")

    # Folder selection
    folder_label = tk.Label(root, text="Select Airfoil Folder:")
    folder_label.pack()

    folder_entry = tk.Entry(root, width=50)
    folder_entry.pack()

    def browse_folder():
        folder = filedialog.askdirectory()
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, folder)

    browse_button = tk.Button(root, text="Browse", command=browse_folder)
    browse_button.pack()

    # Graph switch
    graph_var = tk.BooleanVar(value=True)
    graph_check = tk.Checkbutton(root, text="Enable Graphing", variable=graph_var)
    graph_check.pack()

    # Output box
    output_box = tk.Text(root, height=15, width=70)
    output_box.pack()

    # Run button
    def run_script():
        folder_path = folder_entry.get()
        if not Path(folder_path).exists():
            messagebox.showerror("Error", "Invalid folder path.")
            return
        output_box.delete(1.0, tk.END)
        process_files(folder_path, graph_var.get(), output_box)

    run_button = tk.Button(root, text="Run", command=run_script)
    run_button.pack()

    root.mainloop()

launch_gui()