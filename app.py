import streamlit as st
import math
import pandas as pd
import matplotlib.pyplot as plt
import csv

def get_terminal_velocity(radius,density_of_particle,density_of_fluid,viscosity):
    weight = (4*math.pi*(radius**3)*9.81*density_of_particle)/3
    buoyancy = (4*math.pi*(radius**3)*9.81*density_of_fluid)/3
    net_force = weight - buoyancy
    velocity1 = (2*(radius**2)*(density_of_particle-density_of_fluid)*9.81)/(9*viscosity)
    v_high =velocity1*2
    v_low = 0
    itteration = 0
    while itteration < 10000:
        v_mid = (v_high+v_low)/2
        reynolds = (density_of_fluid*2*radius*v_mid)/viscosity
        if reynolds<1:
            cd = 24/reynolds
        elif reynolds>1000:
            cd = 0.44
        else:
            cd = (24/reynolds)*(1+0.15*reynolds**0.687)
        drag_force = 0.5*cd*density_of_fluid*(math.pi)*(radius**2)*(v_mid**2)
        
        error = abs(drag_force-net_force)/net_force

        if error <= 0.00005:
            itteration+=1
            if reynolds<1:
                region = "Stokes region"
            elif reynolds>1000:
                region = "Newtons region"
            else:
                region = "Intermediate region"
            return v_mid,drag_force,cd,reynolds,region,itteration,error
            

        if drag_force>net_force:
            itteration+=1
            v_high=v_mid
        elif drag_force<net_force:
            itteration+=1
            v_low=v_mid
    raise ValueError(f"Did not converge for radius={radius}, dp={density_of_particle}")


st.title("Terminal Velocity Calculator")

radius_input = st.text_input("Radius values (m) comma separated", "0.001, 0.003, 0.005, 0.007, 0.01")
particle_input = st.text_input("Particle densities (kg/m³) comma separated", "7600, 2600")
fluid_input = st.text_input("Fluid densities (kg/m³) comma separated", "1000, 899")
viscosity_input = st.text_input("Viscosities (Pa.s) comma separated", "0.001, 0.8")

st.caption("Note: fluid densities and viscosities must be paired in order")

if st.button("Calculate"):
    radius_list = [float(x.strip()) for x in radius_input.split(",")]
    particle_list = [float(x.strip()) for x in particle_input.split(",")]
    fluid_list = [float(x.strip()) for x in fluid_input.split(",")]
    viscosity_list = [float(x.strip()) for x in viscosity_input.split(",")]

    if len(fluid_list) != len(viscosity_list):
        st.error("Fluid densities and viscosities must have same number of values")
    else:
        rows = []
        serial = 1
        for df_val, vis in zip(fluid_list, viscosity_list):
            for r in radius_list:
                for dp in particle_list:
                    vt, drag, cd, re, region, iterations, error = get_terminal_velocity(r, dp, df_val, vis)
                    rows.append([serial, r, dp, df_val, vis, vt, drag, cd, re, region, iterations, error])
                    serial += 1

        df = pd.DataFrame(rows, columns=["S.No", "Radius(m)", "particle density(kg/m^3)",
                                          "fluid density(kg/m^3)", "Viscosity(Pa.s)",
                                          "Terminal velocity(m/s)", "Drag(N)", "cd",
                                          "Reynolds", "Region", "iterations", "error"])

        df.to_csv("results.csv", index=False)
        st.success(f"Calculated {len(df)} combinations!")
        st.session_state.df = df

if "df" in st.session_state:
    df = st.session_state.df 
    
    st.subheader("Graphs")

    graph_type = st.selectbox("Select graph", [
        "Radius vs Velocity",
        "Particle Density vs Velocity", 
        "Effect of Fluid"
    ])
    chosen_radius = st.selectbox("Choose radius", sorted(df["Radius(m)"].unique()))
    chosen_fluid = st.selectbox("Choose fluid density", sorted(df["fluid density(kg/m^3)"].unique()))
    chosen_particle = st.selectbox("Choose particle density", sorted(df["particle density(kg/m^3)"].unique()))

    fig, ax = plt.subplots()

    if graph_type == "Radius vs Velocity":
        subset = df[(df["particle density(kg/m^3)"] == chosen_particle) & (df["fluid density(kg/m^3)"] == chosen_fluid)]
        ax.plot(subset["Radius(m)"], subset["Terminal velocity(m/s)"], marker='o')
        ax.set_xlabel("Radius (m)")
        ax.set_ylabel("Terminal Velocity (m/s)")

    elif graph_type == "Particle Density vs Velocity":
        subset = df[(df["Radius(m)"] == chosen_radius) & (df["fluid density(kg/m^3)"] == chosen_fluid)]
        ax.plot(subset["particle density(kg/m^3)"], subset["Terminal velocity(m/s)"], marker='o')
        ax.set_xlabel("Particle Density (kg/m³)")
        ax.set_ylabel("Terminal Velocity (m/s)")

    elif graph_type == "Effect of Fluid":
        subset = df[(df["Radius(m)"] == chosen_radius) & (df["particle density(kg/m^3)"] == chosen_particle)]
        for fluid in subset["fluid density(kg/m^3)"].unique():
            temp = subset[subset["fluid density(kg/m^3)"] == fluid]
            vis = temp["Viscosity(Pa.s)"].iloc[0]
            ax.scatter([fluid], temp["Terminal velocity(m/s)"], label=f"Fluid {fluid} Vis {vis}")
        ax.legend()
        ax.set_xlabel("Fluid Density (kg/m³)")
        ax.set_ylabel("Terminal Velocity (m/s)")

    ax.set_title(graph_type)
    ax.grid()
    st.pyplot(fig)
    st.subheader("Results Table")
    st.dataframe(df)
