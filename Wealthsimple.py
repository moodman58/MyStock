import wealthsimple

def my_two_factor_function():
    MFACode = ""
    while not MFACode:
        # Obtain user input and ensure it is not empty
        MFACode = input("Enter 2FA code: ")
    return MFACode

ws = wealthsimple.WSTrade(
    "email",
    "password",
    two_factor_callback=my_two_factor_function,
)


def main():
    accounts = ws.get_accounts()
    AccountInfo = accounts[0] 
    for element in AccountInfo:
        print (element)
    CurrentBalance = AccountInfo['buying_power']['amount']
    NetDeposits = AccountInfo['net_deposits']['amount']
    AccountInfo['id']
    print('Current balance is: {}, total deposited is: {}'.format(CurrentBalance, NetDeposits))
    
    #deposits = ws.get_deposits()
    #history = ws.get_account_history("id")
    #print(ws.get_activities()[1])


main()