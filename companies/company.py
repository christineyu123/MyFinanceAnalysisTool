from typing import OrderedDict
from numpy import exp
from requests.sessions import dispatch_hook
from utils.utils import compute_wacc
import yfinance as yf
import pprint

CURRENT_YEAR = 2021
PERPETUAL_GROWTH_RATE = 0.025

class MyCompany:
    def __init__(self, ticker) -> None:
        # TODO: Check if the ticker is valid
        assert ticker is not None, "ticker is None"

        self.ticker = ticker
        company_specific = self.ask_yahoofinance()

        self.company_specific = company_specific
        self.analysis = company_specific.analysis
        self.balance_sheet_a = company_specific.balance_sheet
        self.cashflow_a = company_specific.cashflow
        self.earnings_a = company_specific.earnings

    def analyze_dcf(self, this_year):
        """
        REF: https://www.youtube.com/watch?v=bQB5T9cpqRQ
        """

        free_cashflow_growth_rate = self.get_free_cashflow_growth_rate()
        perpetual_growth_rate = self.get_perpetual_growth_rate()
        discount_rate, total_debt = self.compute_discount_rate(this_year)

        free_cashflow = self.compute_free_cashflow(this_year)

        next5year_cashflow = self.compute_next5year_cashflow(free_cashflow, free_cashflow_growth_rate)
        terminal_value = self.compute_terminal_value(next5year_cashflow, perpetual_growth_rate, discount_rate)
        next5year_cashflow[5] = next5year_cashflow[5] + terminal_value 

        # DCF Valuation
        enterprise_value = self.compute_enterprise_value(discount_rate, next5year_cashflow)
        cash_marketable_securities = self.get_cash_marketable_securities(this_year)

        equity = enterprise_value + cash_marketable_securities - total_debt
        intrinsic_value = equity / self.company_specific.info["sharesOutstanding"]

        current_price = self.company_specific.info["currentPrice"]
        upside = (intrinsic_value / current_price) - 1
        dcf_suggestion = "BUY" if upside >= 0 else "SELL"

        dcf_results = {}
        dcf_results["current_price"] = current_price
        dcf_results["intrinsic_value"] = intrinsic_value
        dcf_results["upside"] = upside
        dcf_results["dcf_suggestion"] = dcf_suggestion

        return dcf_results

        
    def ask_yahoofinance(self):
        company_specific = yf.Ticker(self.ticker)
        return company_specific

    def get_free_cashflow_growth_rate(self):
        """
        Compute the growth rate of free cash flow
        """
        free_cashflow_growth_rate = self.analysis.loc["+5Y"]["Growth"]
        return free_cashflow_growth_rate

    def get_perpetual_growth_rate(self):
        return PERPETUAL_GROWTH_RATE

    def compute_discount_rate(self, this_year, expected_rate=None):
        """
        Weight Averaged Cost of Captial
        """

        if expected_rate is None:
            discount_rate = self._compute_discount_rate(this_year)
        else:
            discount_rate = expected_rate
        
        return discount_rate

    def _compute_discount_rate(self, this_year, method="WACC"):
        if method == "WACC":
            discount_rate = compute_wacc(self.company_specific, this_year)

        return discount_rate


    def compute_free_cashflow(self, this_year):
        """
        Free cashflow = Total Cash From Operating Activities + Capital Expenditures
        """
        operating_cashflow = self.cashflow_a.loc["Total Cash From Operating Activities"][this_year]
        captial_expenditure = self.cashflow_a.loc["Capital Expenditures"][this_year] # this is a negative number

        free_cashflow = operating_cashflow + captial_expenditure
        return free_cashflow


    def compute_next5year_cashflow(self, free_cashflow, free_cashflow_growth_rate):
        projected_next5year_cashflow = OrderedDict()
        for i in range(1, 6, 1):
            projected_next5year_cashflow[i] = free_cashflow * (1+free_cashflow_growth_rate)**i
        
        return projected_next5year_cashflow

    def compute_terminal_value(self, projected_next5year_cashflow, perpetual_growth_rate, discount_rate):
        terminal_value = projected_next5year_cashflow[5] * (1 + perpetual_growth_rate) / (discount_rate - perpetual_growth_rate)
        return terminal_value

    def compute_enterprise_value(self, discount_rate, next5year_cashflow):
        """
        npv
        """
        npv = 0
        for k, v in next5year_cashflow.items():
            npv = v / ((1 + discount_rate) ** k) + npv
            
        return npv

    def get_cash_marketable_securities(self, this_year):
        cash_marketable_securities = self.balance_sheet_a.loc["Cash"][this_year] + self.balance_sheet_a.loc["Short Term Investments"][this_year]
        return cash_marketable_securities