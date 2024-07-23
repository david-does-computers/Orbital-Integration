import rebound as rb
from rebound import hash as h
import matplotlib.pyplot as plt
import numpy as np

sa = rb.SimulationArchive("archive.bin")

print(f"Number of snapshots: {len(sa)}")
print("Time of first and last snapshot: {:.1f}, {:.1f}".format(sa.tmin, sa.tmax))

N_pl = 8
N_tp = 16

# sim = sa[0]
# rb.OrbitPlot(sim, unitlabel="[AU]", xlim=[-5,5], ylim=[-5,5], color=(N_pl-1)*["black"]+N_tp*["red"])
# plt.show()

# sim = sa[-1]
# rb.OrbitPlotSet(sim, unitlabel="[AU]", xlim=[-7,7], ylim=[-7,7], color=(N_pl-1)*["black"]+N_tp*["red"])
# plt.show()
# sim.status()

# orbits = sim.calculate_orbits()
# for orbit in orbits:
#     print(orbit)

pid = 108

# t = np.zeros(len(sa))
# a = np.zeros(len(sa))
# e = np.zeros(len(sa))

# for i, sim in enumerate(sa):
#     t[i] = sim.t/1e6
#     try:
#         a[i] = sim.particles[h(pid)].a
#         e[i] = sim.particles[h(pid)].e
#     except:
#         a = a[:i]
#         e = e[:i]
#         t = t[:i]
#         break

# print(t[:10])
# print(a[:10])
# print(e[:10])

# plt.plot(t,a,label="semi-major axis")
# plt.plot(t,a*(1-e),label="perihelion")
# plt.plot(t,a*(1+e),label="aphelion")
# plt.xlabel("Time [Myrs]")
# plt.ylabel("a [AU]")
# plt.title(f"Particle {pid}")
# plt.legend()
# plt.show()

count = 0
fig, ax = plt.subplots()

for i, sim in enumerate(sa):
    # if i % 75:
    #     continue
    try:
        op1 = rb.OrbitPlot(sim, fig=fig, ax=ax, orbit_style="solid", lw=1, particles=[1,2,3,4,5,6])
        op1.particles.set_sizes([0])
        op2 = rb.OrbitPlot(sim, fig=fig, ax=ax, orbit_style="solid", lw=1, particles=[h(pid)], color="red")
        op2.particles.set_sizes([0])

        ax.set_aspect("equal")
        ax.set_xlim(-8, 8)
        ax.set_ylim(-8, 8)
        ax.set_xlabel("x [AU]")
        ax.set_ylabel("y [AU]")

        ax.set_title(f"Particle {pid}")
        ax.text(-4, -7, "t={0} Myr".format(sim.t/1e6))
        fig.savefig("108_death_2/frame_{:04d}.png".format(count))

        ax.clear()
        count += 1
    except rb.ParticleNotFound:
        break

# i = 26180
# count = 0

# while count < 100:
#     sim = sa[i]
#     try:
#         op1 = rb.OrbitPlot(sim, fig=fig, ax=ax, orbit_style="solid", lw=1, particles=[1,2,3,4,5,6])
#         op1.particles.set_sizes([0])
#         op2 = rb.OrbitPlot(sim, fig=fig, ax=ax, orbit_style="solid", lw=1, particles=[h(pid)], color="red")
#         op2.particles.set_sizes([0])

#         ax.set_aspect("equal")
#         ax.set_xlim(-8, 8)
#         ax.set_ylim(-8, 8)
#         ax.set_xlabel("x [AU]")
#         ax.set_ylabel("y [AU]")

#         ax.set_title(f"Particle {pid}")
#         ax.text(-4, -7, "t={:4.1f} Myr".format(sim.t/1e6))
#         fig.savefig("108_death/frame_{:04d}.png".format(count))

#         ax.clear()
#         i -= 1
#         count += 1
        
#     except rb.ParticleNotFound:
#         i -= 1
#         print(i)
#         continue


# a_all = []
# e_all = []

# for i, sim in enumerate(sa):
#     for pid in range(100, 100+N_tp):
#         try:
#             a_all.append(sim.particles[h(pid)].a)
#             e_all.append(sim.particles[h(pid)].e)
#         except rb.ParticleNotFound:
#             continue

# amin, amax = 0, 5
# emin, emax = 0, 1
# h2d, xedge, yedge, im = plt.hist2d(a_all, e_all, bins=150, range=[[amin, amax], [emin, emax]])
# plt.xlabel("a [AU]")
# plt.ylabel("e")

# plt.colorbar()

# plt.plot(2.6090275933683564, 0.38967323455652847, '*', color="red")
# plt.show()

# sim = sa[26136]

# archive = "archive_new.bin"

# tstart = sim.t 
# tout = 200
# tend = 60000+tstart

# sim.automateSimulationArchive(archive, interval=tout)

# sim.collision_resolve = "halt"

# times = np.arange(tstart, tend, tout)
# Nsteps = len(times)

# for i in range(Nsteps):
#     sim.integrate(times[i], exact_finish_time=0)
#     print("Time {0:7.4f} Myr -- Fraction Done {1:5.4} -- # of clones {2}".format(sim.t/1e6, (sim.t-tstart)/(tend-tstart), sim.N-N_pl))