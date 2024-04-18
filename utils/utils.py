import yfinance as yf

HISTORICAL_MARKET_RETURN = 0.0851

def compute_wacc(company_specific, this_year):

    # Cost of Debt Calculation
    interest_expense = company_specific.financials.loc["Interest Expense"][this_year]

    total_current_liabilities = company_specific.balance_sheet.loc["Total Current Liabilities"][this_year]
    account_payable = company_specific.balance_sheet.loc["Accounts Payable"][this_year]
    other_current_liabiltiies = company_specific.balance_sheet.loc["Other Current Liab"][this_year]
    
    debt_shortterm = total_current_liabilities - account_payable - other_current_liabiltiies
    debt_longterm = company_specific.balance_sheet.loc["Long Term Debt"][this_year]

    cost_of_debt = abs(interest_expense / (debt_shortterm + debt_longterm))

    income_tax_expense = company_specific.financials.loc["Income Tax Expense"][this_year]
    income_before_tax = company_specific.financials.loc["Income Before Tax"][this_year]
    effective_tax_rate = income_tax_expense/income_before_tax
    cost_of_debt_1minusT = cost_of_debt * (1 - effective_tax_rate)

    # Cost of Equity Calculation
    us_treasure_yield_10 = yf.Ticker("^TNX")
    risk_free_rate = us_treasure_yield_10.info["regularMarketPrice"] / 100
    beta = company_specific.info["beta"]
    market_return = HISTORICAL_MARKET_RETURN
    cost_of_equity = risk_free_rate + (beta * (market_return - risk_free_rate))

    # Weight of Debt and Equity Calculation
    total_debt = debt_shortterm + debt_longterm
    market_cap = company_specific.info["marketCap"]
    total = total_debt + market_cap
    total_debt_percent = total_debt / total
    market_cap_percent = market_cap / total

    wacc = (cost_of_debt_1minusT * total_debt_percent) + (cost_of_equity * market_cap_percent)

    return wacc, total_debt