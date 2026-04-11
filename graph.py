import pandas as pd 
import matplotlib.pyplot as plt 


df = pd.read_csv("results.csv")
plt.grid()

print(df.sample(10))

chosen_radius = 0.05
chosen_fluid = 1200
chosen_density = 7600

#/graph1
subset1 = df[(df["particle density(kg/m^3)"]==chosen_density) & (df["fluid density(kg/m^3)"]==chosen_fluid)]
plt.plot(subset1["Radius(m)"],subset1["Terminal velocity(m/s)"],marker='o')
plt.xlabel("radius")
plt.ylabel("Terminal velocity")
plt.title("RADIUS VS VELOCITY")
plt.show()

#/graph2
subset2 = df[(df["Radius(m)"]==chosen_radius) & (df["fluid density(kg/m^3)"]==chosen_fluid)]
plt.plot(subset2["particle density(kg/m^3)"],subset2["Terminal velocity(m/s)"],marker='o')
plt.xlabel("particle density")
plt.ylabel("Terminal velocity")
plt.title("DENSITY VS VELOCITY")
plt.show()

#/graph3
subset3 = df[(df["Radius(m)"]==chosen_radius) & (df["particle density(kg/m^3)"]==chosen_density)]
for fluid in subset3["fluid density(kg/m^3)"].unique():
    temp = subset3[subset3["fluid density(kg/m^3)"] == fluid]
    viscosity = temp["Viscosity(Pa.s)"].iloc[0]
    plt.scatter([fluid],temp["Terminal velocity(m/s)"],label = f"Fluid {fluid} Viscosity {viscosity}")
plt.xlabel("Fluid density")
plt.ylabel("Terminal velocity")
plt.legend()
plt.title("EFFECT OF FLUID")
plt.grid()
plt.show()
