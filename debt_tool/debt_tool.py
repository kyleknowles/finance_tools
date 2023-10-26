
def interest_sort(debt):
    return debt['interest']

debtNum = input("Number of debts: ")

debtList = []

for x in range(int(debtNum)):
    debtName = input("Debt " + str(x+1) + " Name: ")
    debtAmount = input("  Amount: $")
    debtInterest = input("  Interest Rate(%): ")
    debtMin = input("  Min Monthly Payment: $")
    debtInfo = {'name': debtName, 'amount': float(debtAmount), 'interest': float(debtInterest), 'min_mp': float(debtMin), 'month_pay': float(0)}
    debtList.append(debtInfo)

print()
TOTAL_DEBT = 0
debtList.sort(reverse = True, key=interest_sort)

for x in range(len(debtList)):
    debt = debtList[x]
    TOTAL_DEBT += debt["amount"]

print("Total Debt: $" + str(TOTAL_DEBT))
monthlyIncome = float(input("Monthly Income After Expenses: $"))
print()

month = 1
while (TOTAL_DEBT > 0):
    print()
    money_left = monthlyIncome
    print("Month " + str(month) + ":")
    print(" STARTING TOTAL DEBT:  $" + str(round(TOTAL_DEBT,2)))
    month += 1

    # update dict valuess (min mps and monthly totals )
    # pay min mps
    for x in range(len(debtList)):
        debt = debtList[x]
        debt['month_pay'] = 0
        if (debt['amount'] < debt['min_mp']):
            debt['min_mp'] = debt['amount']
    # pay min mps
        if (debt['min_mp'] <= money_left):
            debt['amount'] -= debt['min_mp']
            money_left -= debt['min_mp']
            debt['month_pay'] += debt['min_mp']
        else: # min monthly is more than money left
            debt['amount'] -= money_left
            debt['month_pay'] += money_left
            money_left = 0

    TOTAL_DEBT = 0
          # pay BEYOND min mps
    for z in range(len(debtList)):
        debt = debtList[z]
        if (debt['amount'] <= money_left):
            debt['month_pay'] += debt['amount']
            money_left -= debt['amount']
            debt['amount'] = 0
        else:
            debt['amount'] -= money_left
            debt['month_pay'] += money_left
            money_left = 0

        debt['amount'] = round((debt['amount'] * (1+(debt['interest']/100)/12)),2)
    
        TOTAL_DEBT += debt['amount']
        
        print("  " + debt['name'] + " Payment:  $" + str(round(debt['month_pay'],2)))
    

print()
print("Month " + str(month) + ":") 
print("DEBT FULLY PAID OFF BITCHES")

