# -*- coding: utf-8 -*-
"""
Created on Mon Aug 30 22:57:11 2021

@author: D99003734
"""
from datetime import datetime
from stock_class import Stock, DailyData
from account_class import  Traditional, Robo
import matplotlib.pyplot as plt
import json
import csv


def add_stock(stock_list):
    option = ""
    while option != "0":
        print("Add Stock ---")
        symbol = input("Enter Ticker symbol: ").upper()
        name = input("Enter company name: ")
        shares = float(input("Enter number of shares: "))
        new_stock = Stock(symbol, name, shares)
        stock_list.append(new_stock)
        option = input("Stock '{}' added, press Enter to add another stock or 0 to stop: ".format(symbol))


# Remove stock and all daily data
def delete_stock(stock_list):
    print("Delete Stock ----")
    print("Stock List: [", end="")
    for stock in stock_list:
        print(stock.symbol, end= " ")
    print("]")
    symbol = input("Which stock do you want to delte? (Enter Symbol): ".upper())
    found = False
    i = 0
    for stock in stock_list:
        if stock.symbol == symbol:
            found = True
            stock_list.pop(i)
        i += 1
    if found:
        print("Deleted {}".format(symbol))
    else:
        print("Could not find stock with symbol '{}'".format(symbol))
    _ = input("Press Enter to continue ***")
    
# List stocks being tracked
def list_stocks(stock_list):
    print("Stock List ----")
    print("SYMBOL", " "*5, "NAME", " "*13, "SHARES")
    print("="*38)
    for stock in stock_list:
        print(stock.symbol, " "*(11-len(stock.symbol)), stock.name, " "*(17-len(stock.name)), stock.shares)
    print("")
    _ = input("End of list, press Enter to continue. ***")
    
# Add Daily Stock Data
def add_stock_data(stock_list):
    print("Add Daily Stock Data ----")
    print("Stock List: [",end="")
    for stock in stock_list:
        print(stock.symbol," ",end="")
    print("]")
    symbol = input("Which stock do you want to use?: ").upper()
    found = False
    for stock in stock_list:
        if stock.symbol == symbol:
            found = True
            current_stock = stock
    if found == True:
        print("Ready to add data for: ",symbol)
        print("Enter Data Separated by Commas - Do Not use Spaces")
        print("Enter a Blank Line to Quit")
        print("Enter Date,Price,Volume")
        print("Example: 8/28/20,47.85,10550")
        data = input("Enter Date,Price,Volume: ")
        while data != "":
            date, price, volume = data.split(",")
            daily_data = DailyData(date,float(price),float(volume))
          
            current_stock.add_data(daily_data)
            data = input("Enter Date,Price,Volume: ")
        print("Date Entry Complete")
    else:
        print("Symbol Not Found ***")
    _ = input("Press Enter to Continue ***")

#Create Investment Account
def investment_type(stock_list):
    print("Investment Account ---")
    balance = float(input("What is your initial balance: "))
    number = input("What is your account number: ")
    acct= input("Do you want a Traditional (t) or Robo (r) account: ")
    if acct.lower() == "r":
        years = float(input("How many years until retirement: "))
        robo_acct = Robo(balance, number, years)
        print("Your investment return is ",robo_acct.investment_return())
        print("\n\n")
    elif acct.lower() == "t":
        trad_acct = Traditional(balance, number)
        temp_list=[]
        print("Choose stocks from the list below: ")
        while True:
            print("Stock List: [",end="")
            for stock in stock_list:
                print(stock.symbol," ",end="")
            print("]")
            symbol = input("Which stock do you want to purchase, 0 to quit: ").upper()
            if symbol =="0":
                break
            shares = float(input("How many shares do you want to buy?: "))
            found = False
            for stock in stock_list:
              if stock.symbol == symbol:
                  found = True
                  current_stock = stock
            if found == True:
                current_stock.shares += shares 
                temp_list.append(current_stock)
                print("Bought ",shares,"of",symbol)
            else:
                print("Symbol Not Found ***")
        trad_acct.add_stock(temp_list)

# Function to create stock chart
def display_stock_chart(stock_list,symbol):
    date = []
    price = []
    volume = []
    company =  ""
    for stock in stock_list:
        if stock.symbol == symbol:
            company = stock.name
            for dailyData in stock.DataList:
                date.append(dailyData.date)
                price.append(dailyData.close)
                volume.append(dailyData.volume)
    plt.plot(date, price)
    plt.xlabel(date)
    plt.ylabel(price)
    plt.title(company)
    plt.show()

# Display Chart
def display_chart(stock_list):
    print("Stock List: [", end= "")
    for stock in stock_list:
        print(stock.symbol," ",end="")
    print("]")
    symbol = input("Please choose which stock to query: ").upper()
    found = False
    for stock in stock_list:
        if stock.symbol == symbol:
            found = True
            current_stock = stock
    if found == True:
        display_stock_chart(stock_list, symbol)
    else:
        print("Invalid Stock Symbol!")
    _= input("Press enter to continue...")

def data_encoder(obj):
    data_dict = dict(date=obj.date, close = obj.close, volume = obj.volume)
    return data_dict

def obj_encoder(obj):
        dlist = []
        for o in obj.DataList:
            d = data_encoder(o)
            dlist.append(d)
        stock_dict = dict(symbol=obj.symbol, name = obj.name, shares = obj.shares, DataList = dlist)
        return stock_dict

def obj_decoder(obj):
        symbol = obj["symbol"]
        name = obj["name"]
        shares = obj["shares"]
        DL = obj["DataList"]
        objStock = Stock(symbol, name, shares)
        for o in DL:
            d = o['date']
            c = o['close']
            v = o['volume']
            dd = DailyData(d,c,v)
            objStock.add_data(dd)
        return objStock

def file_processing(stock_list):
    json_dict = {}
    choice = ""
    while choice != "E":
        choice = input("Please enter S to save data, L to load data, D to import data, or E to exit: ").upper()
        if choice == "S":
            json_list = [obj_encoder(stock) for stock in stock_list]
            json_dict["Stock"] = json_list
            try:
                with open("stock_data.json", "w") as f:
                    json.dump(json_dict, f, indent=4)
                print("File saved successfuly.")
            except IOError:
                print("Error: unable to save file")
                break
        if choice == "L":
            try:
                with open("stock_data.json", "r") as f:
                    str_file = f.read()
                    str_file = str_file.replace("\'","\"")
                    stock_obj = json.loads(str_file)
                    for s in stock_obj["Stock"]:
                        temp = obj_decoder(s)
                        stock_list.append(temp)
                print("File loaded successfuly")
            except IOError:
                print("Error: Unable to load file.")
                break
        if choice == "D":
            print("Historical data will be imported...")
            symbol = input("Please enter stock symbol: ").upper()
            filename = input("Enter the csv filename: ")
            import_stock_csv(stock_list, symbol, filename) #to be implemented later
            display_report(stock_list, symbol) #to be implemented later

# Get price and volume history from Yahoo! Finance using CSV import.
def import_stock_csv(stock_list,symbol,filename):
        for stock in stock_list:
            if stock.symbol == symbol:
                with open(filename, newline='') as stockdata:
                    datareader = csv.reader(stockdata,delimiter=',')
                    next(datareader)
                    for row in datareader:
                        daily_data = DailyData(str(row[0]),float(row[4]),float(row[6]))
                        stock.add_data(daily_data)

    
    # Display Report for All Stocks
def display_report(stock_list, symbol):
    currentDate=datetime.now()
    print("Stock Report ---")
    for stock in stock_list:
        if stock.symbol == symbol:
            print("Report for: ",stock.symbol,stock.name)
            print("Shares: ", stock.shares)
            count = 0
            price_total = 0.00
            volume_total = 0
            lowPrice = 999999.99
            highPrice = 0.00
            lowVolume = 999999999999
            highVolume = 0
            startDate = datetime.strptime("12/31/2099","%m/%d/%Y")
            endDate = datetime.strptime("1/1/1900","%m/%d/%Y")
           
            for daily_data in stock.DataList: 
                currentDate= datetime.strptime(daily_data.date,"%Y-%m-%d")
                count = count + 1
                price_total = price_total + daily_data.close
                volume_total = volume_total + daily_data.volume
                if daily_data.close < lowPrice:
                    lowPrice = daily_data.close
                if daily_data.close > highPrice:
                    highPrice = daily_data.close
                if daily_data.volume < lowVolume:
                    lowVolume = daily_data.volume
                if daily_data.volume > highVolume:
                    highVolume = daily_data.volume
                if currentDate < startDate:
                    startDate = currentDate
                    startPrice = daily_data.close
                if currentDate > endDate:
                    endDate = currentDate
                    endPrice = daily_data.close
                priceChange = endPrice-startPrice
                print(daily_data.date,daily_data.close,daily_data.volume)
            if count > 0:
                print("Summary ---",startDate,"to",endDate)
                print("Low Price:", "${:,.2f}".format(lowPrice))
                print("High Price:", "${:,.2f}".format(highPrice))
                print("Average Price:", "${:,.2f}".format(price_total/count))
                print("Low Volume:", lowVolume)
                print("High Volume:", highVolume)
                print("Average Volume:", "${:,.2f}".format(volume_total/count))
                print("Starting Price:", "${:,.2f}".format(startPrice))
                print("Ending Price:", "${:,.2f}".format(endPrice))
                print("Change in Price:", "${:,.2f}".format(priceChange))
                print("Profit/Loss","${:,.2f}".format(priceChange * stock.shares))
            else:
                print("*** No daily history.")
            print("\n\n\n")
    print("--- Report Complete ---")
    _ = input("Press Enter to Continue")
    

    
def main_menu(stock_list):
    option = ""
    while True:
        print("Stock Analyzer ---")
        print("1 - Add Stock")
        print("2 - Delete Stock")
        print("3 - List stocks")
        print("4 - Add Daily Stock Data (Date, Price, Volume)")
        print("5 - Show Chart")
        print("6 - Investor Type")
        print("7 - Save/Load Data")
        print("0 - Exit Program")
        option = input("Enter Menu Option: ")
        if option =="0":
            print("Goodbye")
            break
        
        if option == "1":
            add_stock(stock_list)
        elif option == "2":
            delete_stock(stock_list)
        elif option == "3":
            list_stocks(stock_list)
        elif option == "4":
           add_stock_data(stock_list) 
        elif option == "5":
            display_chart(stock_list)
        elif option == "6":
            investment_type(stock_list)
        elif option == "7":
            file_processing(stock_list)
        else:
            
            print("Goodbye")

# Begin program
def main():
    stock_list = []
    main_menu(stock_list)

# Program Starts Here
if __name__ == "__main__":
    # execute only if run as a stand-alone script
    main()