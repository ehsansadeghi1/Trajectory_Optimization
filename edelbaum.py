#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Edelbaum Low-Thrust Orbit Transfer, reformulated by Kéchichian.
----------
* Edelbaum, T. N. "Propulsion Requirements for Controllable
  Satellites", 1961.
* Kéchichian, J. A. "Reformulation of Edelbaum's Low-Thrust
  Transfer Problem Using Optimal Control Theory", 1997.
"""
from math import atan2, atan, tan, sin, cos, pi, sqrt, radians, degrees
import matplotlib.pyplot as plt
# =============================================================================
mu = 398600.4415  # earth gravitational constant (km^3/sec^2)
req = 6378.136    # earth equatorial radius (kilometers)
# =============================================================================
h_0 = 7000-req   # Km
h_f = 42166-req  # Km
inc_0 = 90     # Degrees
inc_f = 0        # Degrees
f = 3.5e-7       # km/sec^2
# =============================================================================
inc_0 = radians(inc_0)
inc_f = radians(inc_f)
r_0 = req + h_0
r_f = req + h_f
V_0 = sqrt(mu/r_0)
V_f = sqrt(mu/r_f)
d_inc = abs(inc_f-inc_0)
"initial yaw angle"
beta0 = atan2(sin(0.5*pi*d_inc), (V_0/V_f)-cos(0.5*pi*d_inc))
"Total delta_V"
dV_t = V_0*cos(beta0)-V_0*sin(beta0)/tan(0.5*pi*d_inc+beta0)
print("Total Delta-V = ", dV_t, "Km/sec")
"Flight Time"
f_time = dV_t/f
if f_time < 3600:
    # minutes
    tdflag = 1
    f_time = f_time/60
    print(f_time, "Minutes")
elif f_time < 86400:
    # Hours
    tdflag = 2
    f_time = f_time/3600
    print(f_time, "Hours")
else:
    # Days
    tdflag = 3
    f_time = f_time/86400
    print("Time of Flight = ", f_time, "Days")
# =============================================================================
dt = f_time/100
t_ = -dt
t = []
beta = []
V = []
a = []
i_ = []
for i in range(0, 101):
    t_ += dt
    if tdflag == 1:
        tsec = t_*60
    elif tdflag == 2:
        tsec = t_*3600
    else:
        tsec = t_*86400
    t.append(t_)
    beta_ = degrees(atan2(V_0*sin(beta0), (V_0*cos(beta0)-f*tsec)))
    V_ = sqrt(V_0**2-2*V_0*f*tsec*cos(beta0)+f**2*tsec**2)
    a_ = (mu/(V_*V_))/1000
    tmp1 = atan((f * tsec - V_0 * cos(beta0))/(V_0 * sin(beta0)))
    di = degrees((2/pi)*(tmp1 + 0.5 * pi - beta0))
    i = degrees(inc_0)-di
    beta.append(beta_)
    V.append(V_)
    a.append(a_)
    i_.append(i)
# =============================================================================
fig, ax1 = plt.subplots()
ax1.plot(t, i_, 'b')
ax1.set_xlabel('Time')
ax1.set_ylabel('Inclination (Degrees)', color='b')
ax1.tick_params('y', colors='b')
ax2 = ax1.twinx()
ax2.plot(t, V, 'r--')
ax2.set_ylabel('Velocity, Km/sec', color='r')
ax2.tick_params('y', colors='r')
plt.show()
plt.figure()
plt.plot(t, a)
plt.xlabel("Time")
plt.ylabel("Semi-Major Axis, Km")
plt.show()
