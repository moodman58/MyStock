import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import matplotlib.pyplot as plt
from wsimple.api import Wsimple 
from wsimple.api import *
from requests.exceptions import RequestException
#First initalize lists of all my stocks, both general lists/dictionaries as well as category sorted ones. Sort by ETF's and just Other because those are the 2 types I have.
stockDict= {
            'AMD.NE': -1, 
            'NVDA.NE': -1, 
            'VFV.TO': -1, 
            'VOO': -1, 
            'XIC.TO': -1, 
            'XSP.TO': -1, 
            'ZCN.TO': -1
            }
stockDictBought = {
            'AMD.NE': 22.25, 
            'NVDA.NE': 40.74, 
            'VFV.TO': 105.65, 
            'VOO': 349.57, 
            'XIC.TO': 31.65, 
            'XSP.TO': 44.55, 
            'ZCN.TO': 26.67
            }
stockDictNumber = {
            'AMD.NE': 6, 
            'NVDA.NE': 2, 
            'VFV.TO': 5.4341, 
            'VOO': 0.3109, 
            'XIC.TO': 7.6634, 
            'XSP.TO': 3.367, 
            'ZCN.TO': 9.5077
                }
stockAvgValues = {
             'AMD.NE': -1, 
            'NVDA.NE': -1, 
            'VFV.TO': -1, 
            'VOO': -1, 
            'XIC.TO': -1, 
            'XSP.TO': -1, 
            'ZCN.TO': -1
            }

stockNNWC = {
            'AMD.NE': -1, 
            'NVDA.NE': -1, 
            'VFV.TO': -1, 
            'VOO': -1, 
            'XIC.TO': -1, 
            'XSP.TO': -1, 
            'ZCN.TO': -1
            }

myStocks = ['AMD.NE', 
            'NVDA.NE', 
            'VFV.TO', 
            'VOO', 
            'XIC.TO', 
            'XSP.TO', 
            'ZCN.TO']
stockETF = [
        'VFV.TO', 
        'VOO', 
        'XIC.TO', 
        'XSP.TO', 
        'ZCN.TO'
           ]
otherStocks = [
        'AMD.NE',
        'NVDA.NE',
            ]
def dailyPrice():
    #We put the date : stock price into a seperate file for each stock, and do this each day --> gonna have to upload to cloud and use a time library?. 
    for stock in myStocks:
        driver = webdriver.Chrome()
        driver.get('https://ca.finance.yahoo.com/quote/{}'.format(stock))
        try:
            
            stockValue = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//fin-streamer[@class='Fw(b) Fz(36px) Mb(-4px) D(ib)']")) )
            timeValue = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "(//div[@id='quote-market-notice'])")) )
            #NNWC per share = (Current Assets - Total Liabilities - Preferred stock) / Outstanding Shares, but yahoo finance doesnt have preferred stock info so just ignore preffered stock for now in calc 
            stockDict[stock] = stockValue.text
            with open(("stocks_{}.txt").format(stock), 'w') as file:
                file.write('%s,%s\n' % ((timeValue.text.split(':', 1))[1], stockDict[stock]))
                file.close()
        finally:
            driver.quit()
    return -1
#Find a couple of good parameters to look at when evalutating the quality of a stock

def NNWCPerShare(stock):
    try:
        driver = webdriver.Chrome()
        
        driver.get('https://ca.finance.yahoo.com/quote/{}/balance-sheet'.format(stock))
        currentAssets = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "(//div[@class = 'Ta(c) Py(6px) Bxz(bb) BdB Bdc($seperatorColor) Miw(120px) Miw(100px)--pnclg D(tbc)' ])[19]")))
        totalLiabilities = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "(//div[@class='Ta(c) Py(6px) Bxz(bb) BdB Bdc($seperatorColor) Miw(120px) Miw(100px)--pnclg D(tbc)'])[71]")))
        currentAssetsValue = int(currentAssets.text.replace(",", "")) * 1000
        totalLiabilitiesValue = int(totalLiabilities.text.replace(",", "")) * 1000
        
        
        driver.get('https://ca.finance.yahoo.com/quote/{}/key-statistics'.format(stock))
        outstandingShares = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "(//td[@class='Fw(500) Ta(end) Pstart(10px) Miw(60px)'])[19]")))
        outstandingSharesValue = float(outstandingShares.text.replace("B", "")) * 1000000000 
        
        
        NNWCPerShare = ((currentAssetsValue  - totalLiabilitiesValue) / outstandingSharesValue)
        # so our values from this are a bit weird right now so i put *100, and they are still weird. I need to double check this formula?
        return NNWCPerShare
    except:
        return None

def comparisonTestNNWC(NNWC, stock):

    with open("stocks_{}.txt".format(stock), 'r') as file:
        lines = file.read().splitlines()
        lastLine = lines[-1]
        stockPrice = (lastLine.split(',', 1))[1]
        if float(stockPrice) < NNWC:
            return True
        else:
            return False
def fiftyDayAverageComparison(stock):
    try:
        driver = webdriver.Chrome()
        driver.get('https://www.barchart.com/etfs-funds/quotes/{}/technical-analysis'.format(stock))
        fiftyDayAvg = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, "(//td[@class='up'])[3]")))
        AvgValue = float(fiftyDayAvg.text)
        with open("stocks_{}.txt".format(stock), 'r') as file:
            lines = file.read().splitlines()
            lastLine = lines[-1]
            stockPrice = (lastLine.split(',', 1))[1]
            if AvgValue > float(stockPrice):
                return '-' + str(round( ((float(stockPrice) - AvgValue) / AvgValue) * 100), 3) + '%'
            elif AvgValue < float(stockPrice):
                 return '+' + str(round(((float(stockPrice) - AvgValue) / AvgValue) * 100, 3)) + '%' 
    finally:
        driver.quit()
def graphStock(stock):
    days = []
    prices = []
    counter = 0
    with open('stocks_{}.txt'.format(stock), 'r') as file:
        for line in file:
            day = (line.split(',', 1))[0]
            price = float((line.split(',', 1))[1])
            days.append(day)
            prices.append(price) 
    for i in days:
        counter += 1
    dayCount = [i for i in range(counter)]
    plt.scatter(dayCount, prices, alpha=0.5)
    plt.show()
    return -1

def get_otp():
    return input("Enter otpnumber: \n>>>")
def login1():
    email = "#"
    password = "#" 

    # Create a Wsimple instance
    ws = Wsimple(email, password, otp_callback=get_otp)

    try:
        if ws.public_mode:
            print("Logged in successfully in Public Mode")
            # Perform actions specific to public mode if needed
        else:
            # Get basic account information
            me_info = ws.get_me()

            # Check if the 'user' attribute is present in the response
            if hasattr(me_info, 'user'):
                print("Logged in successfully")
                print("Account Information:")
                print(f"User ID: {me_info.user.id}")
                print(f"Email: {me_info.user.email}")
                print(f"Name: {me_info.user.name}")
            else:
                print("Logged in successfully")
                print("Account Information:")
                print("User information not available in the response.")

            # Get detailed account information
            account_info = ws.get_account()
            print("\nDetailed Account Information:")
            print(f"Account ID: {account_info.id}")
            print(f"Account Type: {account_info.account_type}")
            print(f"Account Status: {account_info.status}")

            # Get historical portfolio data
            historical_data = ws.get_historical_portfolio_data()
            print("\nHistorical Portfolio Data:")
            print(historical_data)

            # Get bank accounts
            bank_accounts = ws.get_bank_accounts()
            print("\nBank Accounts:")
            for account in bank_accounts.results:
                print(f"Bank Account ID: {account.id}")
                print(f"Bank Name: {account.institution}")
                print(f"Account Type: {account.type}")
                print()

    except Exception as e:
        print(f"An error occurred: {e}")
    
    #def summary_status(self):
    #ws.dashboard()
def login():
    email = "#"
    password = "#"

    # Create a Wsimple instance
    ws = Wsimple(email, password, otp_callback=get_otp)
    ws.dashboard()






#dailyPrice()
#graphStock('AMD.NE')
'''
NNWCVar = NNWCPerShare('AMD.NE')
if comparisonTestNNWC(NNWCVar,'AMD.NE'):
    print("NNWC test passed")
else:
    print("NNWC test failed")
'''
#print(fiftyDayAverageComparison('ZCN.TO'))
    
#After we updated our data file and stored data about the all the values we want in variables we dont need to scrape the website anymore.
#We can now use the data to make comparisons, first we can compare the avg value of the stock to today's value and provided a % difference between those values


#Find a couple of good parameters to look at when evalutating the quality of a stock
     
#time.sleep(10)

login()