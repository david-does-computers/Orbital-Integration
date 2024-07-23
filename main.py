import rebound as rb
import matplotlib.pyplot as plt
import numpy as np
import os

discard_file_name = "discards2.txt"

try:
    os.remove(discard_file_name)
except:
    pass

def collision_discard_log(sim_pointer, collision, discard_file_name=discard_file_name):
    sim = sim_pointer.contents
    id_p1 = sim.particles[collision.p1].hash.value
    id_p2 = sim.particles[collision.p2].hash.value

    discard_file = open(discard_file_name, "a")

    if id_p1 > id_p2:
        print(f"Particle {id_p1} collided with {id_p2} at {sim.t} years")
        print(f"Particle {id_p1} collided with {id_p2} at {sim.t} years", file=discard_file)
        print(f"Removing particle {id_p1}")
        ToRemove = 1
    else:
        print(f"Particle {id_p2} collided with {id_p1} at {sim.t} years")
        print(f"Particle {id_p2} collided with {id_p1} at {sim.t} years", file=discard_file)
        print(f"Removing particle {id_p2}")
        ToRemove = 2
    
    discard_file.close()
    return ToRemove



sim = rb.Simulation()
sim.integrator = "mercurius"
h = rb.hash

sim.units = ("yr", "AU", "Msun")

date = "2024-06-25 4:23"

sim.add("Sun", date=date, hash=0)
sim.particles[h(0)].r = 0.00465047

sim.add("Venus", hash=1)
sim.add("Earth", hash=2)
sim.add("Mars", hash=3)
sim.add("Jupiter", hash=4)
sim.add("Saturn", hash=5)
sim.add("Uranus", hash=6)
sim.add("Neptune", hash=7)

sim.particles[h(1)].r = 4.0454e-5
sim.particles[h(2)].r = 4.2588e-5
sim.particles[h(3)].r = 2.2657e-5
sim.particles[h(4)].r = 4.6733e-4
sim.particles[h(5)].r = 3.8926e-4
sim.particles[h(6)].r = 1.6953e-4
sim.particles[h(7)].r = 1.6459e-4

N_pl = 8

sim.add(
    a=2.6090275933683564, e=0.38967323455652847, inc=0.2886307414612506, Omega=4.224496597238895, omega=1.6304233289390568, M=5.481939749791291,
    hash=100
)

sim.particles[h(100)].r = 5.7e-8

N_tp = 30
for i in range(1, N_tp):
    sim.add(
        a=np.random.normal(2.6090275933683564, 0.031),
        e=np.random.normal(0.38967323455652847, 0.0083),
        inc=np.random.normal(0.2886307414612506, 0.0019),
        Omega=np.random.normal(4.224496597238895, 0.00040),
        omega=np.random.normal(1.6304233289390568, 0.012),
        M=np.random.normal(5.481939749791291, 0.012),
        hash = 100+i
    )


sim.exit_max_distance = 1000
sim.collision = "direct"
sim.collision_resolve = collision_discard_log

sim.move_to_com()
tend = 50e6
tout = 1000

sim.dt = sim.particles[h(1)].P / 30

archive = "archive2.bin"
sim.automateSimulationArchive(archive, interval=tout)

times = np.arange(0, tend, tout)
Nsteps = len(times)

for i in range(Nsteps):
    try:
        sim.integrate(times[i], exact_finish_time=0)
    except:
        for j in range(8, sim.N):
            p = sim.particles[j]
            d2 = p.x*p.x + p.y*p.y + p.z*p.z

            if d2 > (sim.exit_max_distance * sim.exit_max_distance):
                index = j
        
        pid = sim.particles[index].hash.value
        print("Particle {0:2d} was too far from the Sun at {1:12.6e} yrs".format(pid, sim.t))
        
        discard_file = open(discard_file_name, "a")
        print("Particle {0:2d} was too far from the Sun at {1:12.6e} yrs".format(pid, sim.t), file=discard_file)
        discard_file.close()
        sim.remove(index=index)

    print("Time {0:6.3f} Myr-- Fraction Done {1:5.4f} -- # of Clones {2}".format(sim.t/1e6, sim.t/tend, sim.N-N_pl))

    if sim.N < N_pl:
        print("No more test particles, ending simulation")
        break

rb.OrbitPlotSet(sim, unitlabel="[AU]", xlim=[-5,5], ylim=[-5,5], color=(N_pl-1)*['blue'])
plt.show()