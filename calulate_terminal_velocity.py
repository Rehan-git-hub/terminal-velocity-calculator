import math
import csv

def get_terminal_velocity(radius,density_of_particle,density_of_fluid,viscosity):
    weight = (4*math.pi*(radius**3)*9.81*density_of_particle)/3
    buoyancy = (4*math.pi*(radius**3)*9.81*density_of_fluid)/3
    net_force = weight - buoyancy
    velocity1 = (2*(radius**2)*(density_of_particle-density_of_fluid)*9.81)/(9*viscosity)
    v_high =velocity1*2
    v_low = 0
    itteration = 0
    while True:
        v_mid = (v_high+v_low)/2
        reynolds = (density_of_fluid*2*radius*v_mid)/viscosity
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
            break

        if drag_force>net_force:
            itteration+=1
            v_high=v_mid
        elif drag_force<net_force:
            itteration+=1
            v_low=v_mid
