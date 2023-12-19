const readline = require('readline-sync');
const plotly = require('plotly')('your_username', 'your_api_key');
const fs = require('fs');

function interestSort(debt) {
    return debt['interest'];
}

let debtList = [];
let TOTAL_DEBT = 0;

// Initialize Values
let debtNum = readline.question("Number of debts: ");

for (let x = 0; x < parseInt(debtNum); x++) {
    let debtName = readline.question(`Debt ${x + 1} Name: `);
    let debtAmount = parseFloat(readline.question("  Amount: $"));
    let debtInterest = parseFloat(readline.question("  Interest Rate(%): "));
    let debtMin = parseFloat(readline.question("  Min Monthly Payment: $"));
    let debtInfo = {
        'name': debtName,
        'amount': debtAmount,
        'interest': debtInterest,
        'min_mp': debtMin,
        'month_pay': 0
    };
    debtList.push(debtInfo);
    TOTAL_DEBT += debtAmount;
}
console.log();

debtList.sort((a, b) => interestSort(b) - interestSort(a));

console.log(`Total Debt: $${TOTAL_DEBT.toFixed(2)}`);
let takeHome = parseFloat(readline.question("Monthly Take-Home Income: $"));
let expenses = parseFloat(readline.question("Monthly Expenses (not including debt): $"));

let monthlyIncome = takeHome - expenses;
console.log(`Monthly Income After Expenses: $${monthlyIncome.toFixed(2)}`);
console.log();

// Initialize Values
let month = 1;
let Total_DoT = [TOTAL_DEBT];
let debtTime = [debtList.map(d => d['amount'])];

// Avalanche Loop
while (TOTAL_DEBT > 0) {
    console.log();
    let money_left = monthlyIncome;
    console.log(`Month ${month}:`);
    console.log(` STARTING TOTAL DEBT:  $${TOTAL_DEBT.toFixed(2)}`);
    month++;

    // update dict values (min mps and monthly totals )
    // pay min mps
    for (let x = 0; x < debtList.length; x++) {
        // update dictionary values
        let debt = debtList[x];
        debt['month_pay'] = 0;
        if (debt['amount'] < debt['min_mp']) {
            debt['min_mp'] = debt['amount'];
        }

        // pay min mps
        if (debt['min_mp'] <= money_left) {
            debt['amount'] -= debt['min_mp'];
            money_left -= debt['min_mp'];
            debt['month_pay'] += debt['min_mp'];
        } else {
            // min monthly is more than money left
            debt['amount'] -= money_left;
            debt['month_pay'] += money_left;
            money_left = 0;
        }
    }

    TOTAL_DEBT = 0;

    // pay BEYOND min mps
    for (let z = 0; z < debtList.length; z++) {
        let debt = debtList[z];
        if (debt['amount'] <= money_left) {
            debt['month_pay'] += debt['amount'];
            money_left -= debt['amount'];
            debt['amount'] = 0;
        } else {
            debt['amount'] -= money_left;
            debt['month_pay'] += money_left;
            money_left = 0;
        }

        debt['amount'] = parseFloat((debt['amount'] * (1 + (debt['interest'] / 100) / 12)).toFixed(2));

        TOTAL_DEBT += debt['amount'];

        console.log(`  ${debt['name']} Payment:  $${debt['month_pay'].toFixed(2)}`);
    }

    Total_DoT.push(TOTAL_DEBT);
    debtTime.push(debtList.map(d => d['amount']));
}

// Debt Fully Paid Off Message
console.log(`Month ${month}:`);
console.log(" DEBT FULLY PAID OFF BITCHES");

// Plotting (Using Plotly, you need to replace 'your_username' and 'your_api_key' with your actual Plotly username and API key)
const trace1 = {
    x: Array.from({ length: Total_DoT.length }, (_, i) => i + 1),
    y: Total_DoT,
    type: 'scatter',
    name: 'Total Debt'
};

const traces = [trace1];
for (let i = 0; i < debtList.length; i++) {
    const debtHistory = debtTime.map(debtMonth => debtMonth[i]);
    traces.push({
        x: Array.from({ length: debtTime.length }, (_, j) => j + 1),
        y: debtHistory,
        type: 'scatter',
        name: debtList[i]['name']
    });
}

const layout = {
    title: 'Debt',
    xaxis: {
        title: 'Month'
    },
    yaxis: {
        title: 'Total Debt'
    }
};

plotly.plot(traces, layout, { filename: 'debt-plot', fileopt: 'overwrite' }, function (err, msg) {
    if (err) return console.log(err);
    console.log(msg);
});
