import simpy
import numpy as np
def factory_run(env, repairers,spares):
    global cost

    cost=0.0

    for i in range (50):
        env.process(operate_machine(env, repairers,spares))

        while True:
            cost += 3.75*8*repairers.capacity+30*spares.capacity
            yield env.timeout(8.0)


def operate_machine(env, repairers, spares):
    global cost

    while True:
        yield env.timeout(time_to_failure())
        t_broken= env.now
        print ("{:.2f} machine broke".format(t_broken))
        env.process(repair_machine())


        yield spares.get(1)
        t_replaced= env.now
        print ("{:.2f} machine replaced".format(t_replaced))
        cost+=20* (t_replaced-t_broken)


def repair_machine(env, repairers, spares):
    with repairers.request() as request:
        yield request
        yield env.timeout(generate_repair_time())
        yield spares.put(1)
    print("{:.2f} repair complete").format(env, now)


def time_to_failure():
    return np.random.uniform(132, 182)

def generate_repair_time():
    return np.random.uniform(4,10)

np.random.seed(0)

env= simpy.Environment()

repairers =simpy.Resource(env, capacity =3)

spares= simpy.Container(env, init=20, capacity=20)

env.process(factory_run(env, repairers, spares))

env.run(until=8*5)
