# https://medium.com/analytics-vidhya/linear-regression-using-python-ce21aa90ade6
# https://towardsdatascience.com/simple-and-multiple-linear-regression-in-python-c928425168f9
# https://realpython.com/linear-regression-in-python/

from Tariff import Tariff
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression


class Broker():

    def __init__( self, idx ):

        ## ID number, cash balance, energy balance
        self.idx   = idx
        self.cash  = 0
        self.power = 0

        self.customer_usage = None
        self.other_data = None
        self.counter = 0

        ## Lists to contain:
        ##     asks: tuples of the form ( quantity, price )
        ##     tariffs: Tariff objects to submit to the market
        ##     customers: integers representing which customers are subscribed
        ##                to your tariffs.
        self.asks      = []
        self.tariffs   = []
        self.customers = []

    ## A function to accept the bootstrap data set.  The data set contains:
    ##     usage_data, a dict in which keys are integer customer ID numbers,
    ##                     and values are lists of customer's past usage profiles.
    ##     other_data, a dict in which 'Total Demand' is a list of past aggregate demand
    ##                 figures, 'Cleared Price' is a list of past wholesale prices,
    ##                 'Cleared Quantity' is a list of past wholesale quantities,
    ##                 and 'Difference' is a list of differences between cleared
    ##                 quantities and actual usage.
    def get_initial_data(self, usage_data, other_data ):
        self.customer_usage = usage_data
        self.other_data = other_data

    ## Returns a list of asks of the form ( price, quantity ).
    def post_asks(self, time):
        CustomerNums = pd.read_csv('C:/Users/khattakm/Desktop/CSC486/project/CustomerNums.csv', index_col=0, header=0)
        QuantitiesList1 = [] # column 1 to 24 - day 1
        QuantitiesList2 = []  # column 311 to 335 - last day
        for col in CustomerNums.columns[:24]:
            Quantities = (float(CustomerNums[col].mean()))
            QuantitiesList1.append(Quantities)

        for col in CustomerNums.columns[311:335]:
            Quantities = (float(CustomerNums[col].mean()))
            QuantitiesList2.append(Quantities)
        res_list = []
        for i in range(0, len(QuantitiesList1)):
            res_list.append(round(((QuantitiesList1[i] + QuantitiesList2[i])/2), 2))

        PriceNums = pd.read_csv('C:/Users/khattakm/Desktop/CSC486/project/OtherData.csv', index_col=0, header=0)
        PriceList1 = [] # column 1 to 24 - day 1
        PriceList2 = []  # column 311 to 335 - last day
        for col in PriceNums.columns[:24]:
            columnSeriesObj = PriceNums[col]
            PriceList1.append(round(columnSeriesObj.values[0], 2))

        for col in PriceNums.columns[311:335]:
            columnSeriesObj = PriceNums[col]
            PriceList2.append(round(columnSeriesObj.values[0], 2))

        res_list_price = []
        for i in range(0, len(PriceList1)):
            res_list_price.append(round((PriceList1[i] + PriceList2[i])/2, 2))
        list_of_tuples = []
        for quant, price in zip(res_list, res_list_price):
            list_of_tuples.append((price, quant))
        # a_tuple = []
        # for i in range(len(list_of_tuples)):
        #     if i == time:
        #         a_tuple = list_of_tuples[i]
        #     print(a_tuple)
        return list_of_tuples

    def post_tariffs(self, time):
        # print("here", self.counter)
        # self.counter += 1
        # am = []
        # return am
        ## Returns a list of Tariff objects.


        PricesModel = pd.read_csv('C:/Users/khattakm/Desktop/CSC486/project/OtherData.csv', index_col=0, header=0)
        QuantModel = pd.read_csv('C:/Users/khattakm/Desktop/CSC486/project/OtherData.csv')
        PricesForModeling = pd.DataFrame(PricesModel.iloc[0]) # select all the prices from the first row of OtherDataset.csv
        QuantityForModeling = pd.DataFrame(PricesModel.iloc[1])
        x = np.array(PricesForModeling).reshape((-1, 1))
        y = np.array(QuantityForModeling).reshape((-1, 1))

        model = LinearRegression().fit(y, x)
        r_sq = model.score(y, x)
        Myprediction = round((model.predict(y).mean()), 2)
        return [Tariff(self.idx, price=Myprediction, duration=3, exitfee=Myprediction*0.50)]

    ## Receives data for the last time period from the server.
    def receive_message( self, msg ):
        print(msg)
        
    ## Returns a negative number if the broker doesn't have enough energy to
    ## meet demand.  Returns a positive number otherwise.
    def get_energy_imbalance( self, data ):
        return self.power

    def gain_revenue( self, customers, data ):
        for c in self.customers:
            self.cash += data[c] * customers[c].tariff.price
            self.power -= data[c]

    ## Alter broker's cash balance based on supply/demand match.
    def adjust_cash( self, amt ):
        self.cash += amt