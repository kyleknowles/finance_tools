import numpy as np
import matplotlib.pyplot as plt

def interest_sort(debt):
    return debt['interest']



debtList = []
TOTAL_DEBT = 0

# Initialize Values
debtNum = input("Number of debts: ")

for x in range(int(debtNum)):
    debtName = input("Debt " + str(x+1) + " Name: ")
    debtAmount = input("  Amount: $")
    debtInterest = input("  Interest Rate(%): ")
    debtMin = input("  Min Monthly Payment: $")
    debtInfo = {'name': debtName, 'amount': float(debtAmount), 'interest': float(debtInterest),
                                                'min_mp': float(debtMin), 'month_pay': float(0)}
    debtList.append(debtInfo)
    TOTAL_DEBT += float(debtAmount)
print()

debtList.sort(reverse = True, key=interest_sort)

print("Total Debt: $" + str(format(TOTAL_DEBT,".2f")))
takeHome = float(input("Monthly Take-Home Income: $"))
expenses = float(input("Monthly Expenses (not including debt): $"))

monthlyIncome = takeHome - expenses
print("Monthly Income After Expenses: $" + str(format(monthlyIncome,".2f")))
print()

# Initialize Values
month = 1
Total_DoT = [TOTAL_DEBT]
debtTime = [[d['amount'] for d in debtList]]


# Avalanche Loop
while (TOTAL_DEBT > 0):
    print()
    money_left = monthlyIncome
    print("Month " + str(month) + ":")
    print(" STARTING TOTAL DEBT:  $" + str(format(TOTAL_DEBT,".2f")))
    month += 1

    # update dict values (min mps and monthly totals )
    # pay min mps
    for x in range(len(debtList)):
        # update dictionary values
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

        debt['amount'] = round(debt['amount'] * (1+(debt['interest']/100)/12),2)
    
        TOTAL_DEBT += debt['amount']
        
        print("  " + debt['name'] + " Payment:  $" + str(format(debt['month_pay'],".2f")))
    Total_DoT.append(TOTAL_DEBT)
    debtTime.append([d['amount'] for d in debtList])
   
# Debt Fully Paid Off Message
print("Month " + str(month) + ":")
print(" DEBT FULLY PAID OFF BITCHES")

# Plotting
months = np.linspace(1,len(Total_DoT),num=len(Total_DoT),endpoint=True)
fig, ax = plt.subplots()

ax.plot(months, Total_DoT) # Plot Total Debt Over Time

# Plot Individual Debts Over Time
for debt in range(len(debtList)):
    debtHistory = [debtMonth[debt] for debtMonth in debtTime]
    ax.plot(months, debtHistory)

plt.legend(['Total Debt'] + [d['name'] for d in debtList]) # Add Legend

# Titles, Labels, and Setting Figures
plt.title("Debt")
plt.xlabel('Month')
plt.ylabel('Total Debt')
plt.savefig("figure.jpg")