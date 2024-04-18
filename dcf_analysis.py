import pprint
import yfinance as yf

from companies.company import MyCompany


def main():
    company = MyCompany("COST")
    print(company.analyze_dcf(0))


if __name__ == "__main__":
    main()