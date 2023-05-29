from urllib.request import urlopen
import requests
import json
import pandas as pd
from io import StringIO
import numpy as np
import math
import streamlit as st
from streamlit_lottie import st_lottie

# activate streamlitenv
# streamlit run app.py


API_KEY = "7818cd85b90c4c7966a9718f395c778e"

Income_Features = ["revenue",
        "costOfRevenue",
        "grossProfit",
        "grossProfitRatio",
        "researchAndDevelopmentExpenses",
        "generalAndAdministrativeExpenses",
        "sellingAndMarketingExpenses",
        "sellingGeneralAndAdministrativeExpenses",
        "otherExpenses",
        "operatingExpenses",
        "costAndExpenses",
        "interestIncome",
        "interestExpense",
        "depreciationAndAmortization",
        "ebitda",
        "ebitdaratio",
        "operatingIncome",
        "operatingIncomeRatio",
        "totalOtherIncomeExpensesNet",
        "incomeBeforeTax",
        "incomeBeforeTaxRatio",
        "incomeTaxExpense",
        "netIncome",
        "netIncomeRatio",
        "eps",
        "epsdiluted",
        "weightedAverageShsOut",
        "weightedAverageShsOutDil"]

Balance_Features = [
        "cashAndCashEquivalents",
        "shortTermInvestments",
        "cashAndShortTermInvestments",
        "netReceivables",
        "inventory",
        "otherCurrentAssets",
        "totalCurrentAssets",
        "propertyPlantEquipmentNet",
        "goodwill",
        "intangibleAssets",
        "goodwillAndIntangibleAssets",
        "longTermInvestments",
        "taxAssets",
        "otherNonCurrentAssets",
        "totalNonCurrentAssets",
        "otherAssets",
        "totalAssets",
        "accountPayables",
        "shortTermDebt",
        "taxPayables",
        "deferredRevenue",
        "otherCurrentLiabilities",
        "totalCurrentLiabilities",
        "longTermDebt",
        "deferredRevenueNonCurrent",
        "deferredTaxLiabilitiesNonCurrent",
        "otherNonCurrentLiabilities",
        "totalNonCurrentLiabilities",
        "otherLiabilities",
        "capitalLeaseObligations",
        "totalLiabilities",
        "preferredStock",
        "commonStock",
        "retainedEarnings",
        "accumulatedOtherComprehensiveIncomeLoss",
        "othertotalStockholdersEquity",
        "totalStockholdersEquity",
        "totalEquity",
        "totalLiabilitiesAndStockholdersEquity",
        "minorityInterest",
        "totalLiabilitiesAndTotalEquity",
        "totalInvestments",
        "totalDebt",
        "netDebt"]

CashFlow_Features = [
            "netIncome",
        "depreciationAndAmortization",
        "deferredIncomeTax",
        "stockBasedCompensation",
        "changeInWorkingCapital",
        "accountsReceivables",
        "inventory",
        "accountsPayables",
        "otherWorkingCapital",
        "otherNonCashItems",
        "netCashProvidedByOperatingActivities",
        "investmentsInPropertyPlantAndEquipment",
        "acquisitionsNet",
        "purchasesOfInvestments",
        "salesMaturitiesOfInvestments",
        "otherInvestingActivites",
        "netCashUsedForInvestingActivites",
        "debtRepayment",
        "commonStockIssued",
        "commonStockRepurchased",
        "dividendsPaid",
        "otherFinancingActivites",
        "netCashUsedProvidedByFinancingActivities",
        "effectOfForexChangesOnCash",
        "netChangeInCash",
        "cashAtEndOfPeriod",
        "cashAtBeginningOfPeriod",
        "operatingCashFlow",
        "capitalExpenditure",
        "freeCashFlow"]


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()



@st.cache_data
def get_jsonparsed_data(url):
    """
    Receive the content of ``url``, parse it as JSON and return the object.

    Parameters
    ----------
    url : str

    Returns
    -------
    dict
    """
    response = urlopen(url)
    data = response.read().decode("utf-8")
    return StringIO(data)

URL_SYMBOL = "https://financialmodelingprep.com/api/v3/stock/list?apikey="+API_KEY
symbol_df = pd.read_json(get_jsonparsed_data(URL_SYMBOL))
symbol_df = symbol_df[symbol_df['symbol'].isin(["AAPL", "TSLA","MSFT","NVDA","AMZN","META"])]
symbol_df["display"] = symbol_df.symbol + " - " + symbol_df.name

lottie_header = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_06a6pf9i.json")

with st.sidebar:
    st.header("Benford Law Analyser")

    st_lottie(lottie_header)

    STOCK_Sel = st.selectbox(
    'Pick your Stock',
    list(range(len(symbol_df))),
    format_func=  lambda x: symbol_df.iloc[x,6],
    help = "Limited Stocks" )
    st.caption("Data provided by https://site.financialmodelingprep.com/")
    st.caption("Proof of Concept Developed by Gabriel Fonteles gfonteles94@gmail.com")




STOCK = symbol_df.iloc[STOCK_Sel,0]

st.title(symbol_df.iloc[STOCK_Sel,6]+" Analysis")


def benford_calc (STOCK):

    n1=0
    n2=0
    n3=0
    n4=0
    n5=0
    n6=0
    n7=0
    n8=0
    n9=0

    INCOME_URL = "https://financialmodelingprep.com/api/v3/income-statement/"+STOCK+"?limit=120&apikey="+API_KEY

    data = pd.read_json(  get_jsonparsed_data(INCOME_URL)   )
    data = data[Income_Features]
    data = (data.abs()*10000).astype(str)

    for x in range(data.shape[0]):
        for y in range(data.shape[1]):
            n=data.iloc[x, y][:1]
            if n == '1':
                n1 += 1
            if n == '2':
                n2 += 1
            if n == '3':
                n3 += 1
            if n == '4':
                n4 += 1
            if n == '5':
                n5 += 1
            if n == '6':
                n6 += 1
            if n == '7':
                n7 += 1
            if n == '8':
                n8 += 1
            if n == '9':
                n9 += 1

    BALANCE_URL = "https://financialmodelingprep.com/api/v3/balance-sheet-statement/"+STOCK+"?limit=120&apikey="+API_KEY
    data = pd.read_json(  get_jsonparsed_data(BALANCE_URL)   )
    data = data[Balance_Features]
    data = (data.abs()*10000).astype(str)

    for x in range(data.shape[0]):
        for y in range(data.shape[1]):
            n=data.iloc[x, y][:1]
            if n == '1':
                n1 += 1
            if n == '2':
                n2 += 1
            if n == '3':
                n3 += 1
            if n == '4':
                n4 += 1
            if n == '5':
                n5 += 1
            if n == '6':
                n6 += 1
            if n == '7':
                n7 += 1
            if n == '8':
                n8 += 1
            if n == '9':
                n9 += 1


    CASHFLOW_URL = "https://financialmodelingprep.com/api/v3/cash-flow-statement/"+STOCK+"?limit=120&apikey="+API_KEY
    data = pd.read_json(  get_jsonparsed_data(CASHFLOW_URL)   )
    data = data[CashFlow_Features]
    data = (data.abs()*10000).astype(str)

    for x in range(data.shape[0]):
        for y in range(data.shape[1]):
            n=data.iloc[x, y][:1]
            if n == '1':
                n1 += 1
            if n == '2':
                n2 += 1
            if n == '3':
                n3 += 1
            if n == '4':
                n4 += 1
            if n == '5':
                n5 += 1
            if n == '6':
                n6 += 1
            if n == '7':
                n7 += 1
            if n == '8':
                n8 += 1
            if n == '9':
                n9 += 1

    
    benford = pd.DataFrame(data = {
        'Digit': ['1', '2', '3', '4', '5', '6', '7', '8', '9'],
        'Occurence': [n1,n2,n3,n4,n5,n6,n7,n8,n9]/np.sum([n1,n2,n3,n4,n5,n6,n7,n8,n9]),
        'Benford' : [math.log10(1+1/d) for d in [1, 2, 3, 4, 5, 6, 7, 8, 9]]})
    
    benford_res = benford
    total = np.sum([n1,n2,n3,n4,n5,n6,n7,n8,n9])
    benford_res['X2'] = (total*benford_res['Occurence']-total*benford_res['Benford'])**2/(total*benford_res['Benford'])
    chi_value = round(benford_res.X2.sum(),2)


    return benford, chi_value


data,chi=benford_calc(STOCK)

critical_value = 20.09
critical_value1 = 15.51
result = "passed" if chi<critical_value else "failed"

st.header("Benford Law Calculation")
st.caption("This test " + result + " the Benfors Law test with Chi of " + str(chi)+ " and critical value of "+str(critical_value)+" for a significance of 1%"  )

st.title("")
col1, col2, col3 = st.columns(3)
col1.metric("Chi Squared X2_8", str(chi))
col2.metric("1% Significance", str(critical_value), str(round(chi-critical_value,2) ))
col3.metric("5% Significance", str(critical_value1), str(round(chi-critical_value1,2) ))

st.title("")

col1, col2= st.columns([2,3])
with col1:
   st.table(data[["Occurence","Benford"]].set_index(data['Digit']))
with col2:
    st.line_chart(data = data, x = 'Digit', y = ['Occurence', 'Benford'] )