from matplotlib import markers
from Broker import Broker
from CloudProvider import CloudProvider
from HistoryData import HistoryData
from User import User
from random import randrange, uniform
from numpy import *
import matplotlib.pyplot as plt
import logging
import math

def main():
    FORMAT = '%(asctime)s %(levelname)s: %(message)s'
    logging.basicConfig(level=logging.DEBUG, filename='myLog.log', filemode='w', format=FORMAT)

    ''' Initial Data'''

    totalRound = 500
    m, n, k = 2, 4, 2 # Cloud, Broker, User
    arrivalRate = 80
    originalBusniessStrategyIndex = 1
    clouds, brokers, users = [], [], []
    for idx in range(m):
        clouds.append( CloudProvider(idx, n) )
    for idx in range(n):
        brokers.append( Broker(idx, m, n, k, originalBusniessStrategyIndex) )
    for idx in range(k):
        users.append( User(idx, n) )

    ''' for aggressive broker '''
    brokers[0].businessStrategyIndex = 2
    brokers[0].alpha = 1.2

    ##### B-round(n) starts #####
    ''' for plotting '''
    y, y2, y3 = [], [], []
    z, z2, z3 = [], [], []
    userDemand = []
    fairnessPlot = [[] for i in range(n)]
    
    for curRound in range(totalRound):
        print("------------------- round: ", curRound, "------------------")
        logging.info(f'-------------------round: {curRound}------------------')

        # User generage demand(step 1 -> done)
        for user in users:
            user.genDemand(m, curRound, arrivalRate)
        userDemand.append(users[0].demand)

        # Broker aggregate all users' demand(step 1 -> done)
        # logging.info(f'Broker aggregate all users demand')
        # for broker in brokers:
        #     broker.aggregateDemand(users)
        #     print("broker", broker.ID, "aggregate user demand sum:", broker.curUsersDemand)
        #     # y.append(broker.curUsersDemand)

        # # Broker decide D_bc (step 2 -> done)
        # for broker in brokers:
        #     for cloud in clouds:
        #         cloud.D_bc[broker.ID] = broker.cal_D_bc(cloud.ID)
                # cloud.D_bc_history[broker.ID].append(cloud.D_bc[broker.ID])

        # Cloud reply instance supply and price (step 3 -> done)
        # logging.info(f'Cloud reply instance supply and price')
        for cloud in clouds:
            cloud.type2Price = round(random.uniform(0.4, 0.6), 2)
            cloud.availableInstanceNum = cloud.genSupply()
            print('cloud',cloud.ID, 'available instance number:', cloud.availableInstanceNum)
        
        for user in users:

        # for broker in brokers:
        #     broker.getCloudSupply(clouds)
        #     broker.getCloudPrice(clouds)
        #     # update broker's history data: other brokers' instance
        #     broker.updateHistoryData_othersInstanceNum(clouds, broker)

        # Compare users' demand and cloud supply
        # for broker in brokers:
        #     if broker.curUsersDemand <= sum(broker.D_cb):
        #         print("profit-objective mode")
        #         logging.info('profit-objective mode')
                
        #         '''profit-objective mode'''
                
        #         listOfCloudPrice = broker.curCloudPrice
        #         dictOfCloudPrice = {i : listOfCloudPrice[i] for i in range(0, len(listOfCloudPrice))}
        #         sortedCloudPrice = {k: v for k, v in sorted(dictOfCloudPrice.items(), key = lambda item: item[1])} # dict
        #         dictOf_D_cb = {i : broker.D_cb[i] for i in range(0, len(broker.D_cb))}
        #         # print("sorted cloud price:", sortedCloudPrice)
        #         for user in users:
        #             # maxProfit, optimalPrice, actualPurchase = broker.calMaxProfit(broker.curUsersDemand, 
        #             #                                                                    user.priceSensitivity,
        #             #                                                                    min(broker.curCloudPrice)
        #             #                                                                 )
        #             keyListOfSortedCloudPrice = []
        #             for k in sortedCloudPrice:
        #                 keyListOfSortedCloudPrice.append(k)
        #             curIdx = 0
        #             if user.demand[broker.ID] > dictOf_D_cb[keyListOfSortedCloudPrice[curIdx]]:
        #                 curIdx = curIdx + 1
                    
        #             maxProfit, optimalPrice, actualPurchase = broker.calMaxProfit(     user.demand[broker.ID], 
        #                                                                                user.priceSensitivity,
        #                                                                                broker.curCloudPrice[keyListOfSortedCloudPrice[curIdx]]
        #                                                                          )
        #             dictOf_D_cb[keyListOfSortedCloudPrice[curIdx]] = dictOf_D_cb[keyListOfSortedCloudPrice[curIdx]] - actualPurchase
        #             logging.info(f'maximum profit: {maxProfit}, optimal price: {optimalPrice}, actualPurchase: {actualPurchase}')
        #             print("maxProfit:", maxProfit, "optimalPrice:", optimalPrice, "actualPurchase", actualPurchase, "from cloud", keyListOfSortedCloudPrice[curIdx])
        #             demandSatisfaction = user.calDemandSatisfaction(0.5, broker.ID, actualPurchase)
        #             priceSatisfaction = user.calPriceSatisfaction(broker.ID, actualPurchase, optimalPrice, curRound + 2)
        #             print("user", user.ID, "satis to broker", broker.ID, demandSatisfaction, priceSatisfaction)
        #             user.update_D(broker.ID)
        #             user.update_D_success(actualPurchase, broker.ID)

        #         fairness = broker.calJainsFairness(sum(broker.D_cb), users, n, broker.ID)
        #         print("fairness:", fairness)
        #         fairnessPlot[broker.ID].append(fairness)
        #         logging.info(f'broker {broker.ID} fairness: {fairness}')
        #     else:
        #         print("fairness-objective mode")
        #         logging.info('fairness-objective mode')

        #         ''' fairness-objective mode'''
        #         # brokers give a basic amount of instances to all users
        #         remainInstance = sum(broker.D_cb) - 10 * k
        #         userDemandList = []
        #         for user in users:
        #             user.demand[broker.ID] = user.demand[broker.ID] - 10
        #             userDemandList.append(user.demand[broker.ID])

        #         # Is there any available instances?
        #         while remainInstance: 
        #             lastRemainInstance = 0
        #             # pick the most painful user and give him the instance
        #             maxUserDemand = max(userDemandList)
        #             maxUserId = userDemandList.index(maxUserDemand)
        #             print("remaininstance:", remainInstance, "maxuserdemand", maxUserDemand)
        #             if maxUserDemand < 0:
        #                 break
        #             if remainInstance >= maxUserDemand:
        #                 user.D_success[broker.ID] = maxUserDemand
        #                 userDemandList[maxUserId] = userDemandList[maxUserId] - remainInstance
        #                 remainInstance = remainInstance - maxUserDemand
        #             else:
        #                 user.D_success[broker.ID] = remainInstance
        #                 userDemandList[maxUserId] = userDemandList[maxUserId] - remainInstance
        #                 remainInstance = 0

        #             if remainInstance == lastRemainInstance:
        #                 break
        #             lastRemainInstance = remainInstance
                
        #         fairness = broker.calJainsFairness(sum(broker.D_cb), users, n, broker.ID)
        #         print("fairness: ", fairness)
        #         fairnessPlot[broker.ID].append(fairness)
        #         logging.info(f'broker {broker.ID} fairness: {fairness}')

        # update brokers' credit scored by cloud
        for cloud in clouds:
            cloud.updateBrokersCreditData(brokers)
            cloud.calBrokersCredit()
            print(cloud.brokersCredit)
        
        # print(fairnessPlot[1])

        y.append(clouds[0].brokersCredit[0])
        z.append(clouds[0].brokersCredit[1])
        # y2.append(demandSatisfaction)
        # y3.append(priceSatisfaction)
    
    ''' plotting '''
    plt.figure()
    plt.xlim([100, 400])
    # plt.subplot(3, 1, 1)
    plt.plot(y)
    plt.plot(z)
    plt.title("brokers' credit over time")
    plt.xlabel("Time (hour)")
    plt.ylabel("brokers' credit")
    plt.legend(['aggressive', 'not aggressive'])

    # plt.subplot(3, 1, 2)
    # plt.plot(y2)
    #plt.title("user demand satisfaction")
    
    # plt.subplot(3, 1, 3)
    # plt.plot(y3)
    #plt.title("user price satisfaction")

    plt.figure()
    plt.ylim([0,200])
    plt.plot(userDemand)
    plt.title("user demand")

    plt.figure()
    # x = linspace(0, totalRound, n)
    plt.xlim([100, 400])
    plt.ylim([0,1])
    listPlot = fairnessPlot[0]
    for i, x in enumerate(fairnessPlot[0]):
        listPlot[i] = (x - min(fairnessPlot[0])) / (max(fairnessPlot[0]) - min(fairnessPlot[0]))
    plt.plot(listPlot)
    listPlot2 = fairnessPlot[1]
    for i, x in enumerate(fairnessPlot[1]):
        listPlot2[i] = (x - min(fairnessPlot[1])) / (max(fairnessPlot[1]) - min(fairnessPlot[1]))
    plt.plot(listPlot2)
    # print(fairnessPlot[0])
    # plt.plot(fairnessPlot[1])
    plt.title("Jain's fairness")
    plt.legend(['aggressive', 'not aggressive'])

    plt.show()
    
    logging.info('simulation done...')

if __name__ == '__main__':
    main()
