import logging
import simpy
import random
import numpy as np

NUM_CLOUDS = 2
AVG_SUPPORT_TIME = 60
SIM_TIME = 1440
USER_INTERVAL = 10

users_handled = 0

FORMAT = '%(asctime)s %(levelname)s: %(message)s'
logging.basicConfig(level=logging.DEBUG, filename='myLog.log', filemode='w', format=FORMAT)

class Market(object):

    def __init__(self, env, num_clouds, support_time):
        self.env = env
        self.cloud = simpy.Resource(env, num_clouds)
        self.support_time = support_time

    def support(self, user):
        random_time = max(1, np.random.normal(self.support_time, 4))
        yield self.env.timeout(random_time)
        logging.info(f'Support finished for {user} at {self.env.now: .2f}')

def user(env, ID, market):
    global users_handled
    logging.info(f'User {ID} enters waiting queue at {env.now: 2f}!')
    with market.cloud.request() as request:
        yield request
        logging.info(f'User {ID} enters market at {env.now:.2f}')
        yield env.process(market.support(ID))
        users_handled += 1

def setup(env, num_clouds, support_time, user_interval):
    market = Market(env, num_clouds, support_time)

    for i in range(0, 5):
        env.process(user(env, i, market))

    while True:
        yield env.timeout(random.randint(user_interval - 1, user_interval + 1))
        i += 1
        i %= 6
        env.process(user(env, i, market))

logging.info(f'Starting Market Simulation')
# env = simpy.Environment()
# env.process(setup(env, NUM_CLOUDS, AVG_SUPPORT_TIME, USER_INTERVAL))
# env.run(until = SIM_TIME)

logging.info(f'Users handled: {users_handled}')

logging.info(f'Finished Simulation')

    