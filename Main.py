from matplotlib import markers
from matplotlib.style import available
from Broker import Broker
from CloudProvider import CloudProvider
from HistoryData import HistoryData
from User import User
from Market import Market
from random import randrange, uniform
from numpy import *
import matplotlib.pyplot as plt
import logging
import math
import simpy


NUM_CLOUDS = 1
NUM_USERS = 6
AVG_SUPPORT_TIME = 60
# SIM_TIME = 1440 * 30 # a month
SIM_TIME = 1440
USER_INTERVAL = 10

users_handled = 0
y2, y3 = [], []

clouds, users = [], []
for idx in range(NUM_CLOUDS):
    clouds.append( CloudProvider(idx, NUM_CLOUDS) )
for idx in range(NUM_USERS):
    users.append( User(idx, NUM_CLOUDS))


def user(env, ID, market):
    global users_handled
    logging.info(f'User {ID} enters waiting queue at {env.now: 2f}!')
    users[ID].genDemand(NUM_CLOUDS, env.now, 80)
    # logging.info(f'User {ID} demand = {users[ID].demand}')
    print(users[ID].demand)
    
    with market.cloud.request() as request:
        yield request
        logging.info(f'User {ID} enters market at {env.now:.2f}')
        yield env.process(market.support(ID))
        users[ID].D_success[0] += 80 #users[ID].demand[0]
        users[ID].demand[0]  = 0
        
        users_handled += 1

def setup(env, num_clouds, support_time, user_interval):
    market = Market(env, num_clouds, support_time)

    for i in range(NUM_USERS):
        env.process(user(env, i, market))

    while True:
        yield env.timeout(random.randint(user_interval - 1, user_interval + 1))
        i += 1
        i %= NUM_USERS
        env.process(user(env, i, market))


def main():
    FORMAT = '%(asctime)s %(levelname)s: %(message)s'
    logging.basicConfig(level=logging.DEBUG, filename='myLog.log', filemode='w', format=FORMAT)

    ''' Set up the environment '''
    env = simpy.Environment()


    ''' simulation param '''
    END_TIME = 1440 # a day

    
    logging.info(f'Starting Market Simulation')

    env.process(setup(env, NUM_CLOUDS, AVG_SUPPORT_TIME, USER_INTERVAL))

    
    ''' Let's go! '''
    
    logging.info(f'Users handled: {users_handled}')
    env.run(until = END_TIME)

    logging.info('simulation done...')

    ''' calculate fairness '''
    wholeInstance = 0
    for user in users:
        wholeInstance += user.D_success[0] + user.demand
    x_i, fairness = [], []
    for user in users:
        x_i.append(user.D_success[0] / wholeInstance)
    fairness.append( (sum(x_i) ** 2) / (NUM_CLOUDS * sum(x_i)) )
    print("fairness: ", fairness)
    logging.info(f'fairness = {fairness}')

    ''' calculate satisfaction '''
    for round in range(400):
        for user in users:
            # demand satisfaction
            demandSatisfaction = user.calDemandSatisfaction(0.5, 0, random.randint(0, user.demand))
            print("round:",round)
            print("user", user.ID, "demand satisfaction: ", demandSatisfaction)
            user.update_D(0)
            user.update_D_success(user.demand, 0)
            y2.append(demandSatisfaction[0])
            
            # price satisfaction
            priceSatisfaction = user.calPriceSatisfaction(user.retailPrice, random.uniform(0.4, 0.6))
            print("user", user.ID, "price satisfaction: ", priceSatisfaction)
            y3.append(priceSatisfaction)
            user.retailPrice = random.uniform(0.4, 0.6)

    ''' ----- satisfaction ----- '''
    plt.figure()
    demandSatis = y2
    for i, x in enumerate(y2):
        demandSatis[i] = (x - min(y2)) / (max(y2) - min(y2)) - 0.3
    plt.subplot(3, 1, 1)
    plt.xlim([100, 400])
    plt.ylim([0,1])
    plt.plot(demandSatis, marker = '.')
    plt.title("user demand satisfaction")
    
    # priceSatis = y3
    # for i, x in enumerate(y3):
    #     priceSatis[i] = (x - min(y3)) / (max(y3) - min(y3))
    plt.subplot(3, 1, 2)
    plt.xlim([100, 400])
    # plt.ylim([0,1])
    plt.plot(y3, marker = '.')
    plt.title("user price satisfaction")

    satis = []
    for i in range(len(y3)):
        satis.append(demandSatis[i] * y3[i])
    plt.subplot(3, 1, 3)
    plt.xlim([100, 400])
    # plt.ylim([0,1])
    plt.plot(satis, marker = '.')
    plt.title("user satisfaction")

    plt.show()




if __name__ == '__main__':
    main()
