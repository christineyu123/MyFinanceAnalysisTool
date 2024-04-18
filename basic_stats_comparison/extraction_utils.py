from basic_stats_comparison.helpers import skip_exception_decorator

@skip_exception_decorator
def get_beta(info, data):
    result = info.get('beta', None)
    if not result:
        result = info.get('beta3Year', None)
    return result

@skip_exception_decorator
def get_pe_ratio(info, data):
    result = info['trailingPE']
    return result

@skip_exception_decorator
def get_pb_ratio(info, data):
    result = info['priceToBook']
    return result

@skip_exception_decorator
def get_ps_ratio(info, data):
    result = info['priceToSalesTrailing12Months']
    return result

@skip_exception_decorator
def get_current_ratio(info, data):
    result = info['currentRatio']
    return result

@skip_exception_decorator
def get_roe(info, data):
    result = info['returnOnEquity']
    return result

@skip_exception_decorator
def get_market_cap(info, data):
    result = info.get('marketCap', None)
    if not result:
        result = info.get('totalAssets', None)
    return result

@skip_exception_decorator
def get_dividend_yield(info, data):
    result = info.get('dividendYield',None)
    if not result:
        result = info.get('yield', None)
    return result

@skip_exception_decorator
def get_profit_margin(info, data):
    result = info['profitMargins']
    return result

@skip_exception_decorator
def get_ytd_return(info, data):
    result = data['defaultKeyStatistics']['ytdReturn']
    return result

@skip_exception_decorator
def get_3_year_return(info, data):
    result = data['defaultKeyStatistics']['threeYearAverageReturn']
    return result

@skip_exception_decorator
def get_5_year_return(info, data):
    result = data['defaultKeyStatistics']['fiveYearAverageReturn']
    return result

@skip_exception_decorator
def get_expense_ratio(info, data):
    result = data['fundProfile']['feesExpensesInvestment']['annualReportExpenseRatio']
    return result

@skip_exception_decorator
def get_net_assets(info, data):
    result = info.get['totalAssets']
    return result


column_name_to_parse_func = {
    'p/e ratio': get_pe_ratio,
    'p/s ratio': get_ps_ratio,
    'p/b ratio': get_pb_ratio,
    'current ratio': get_current_ratio,
    'roe': get_roe,
    'market cap': get_market_cap,
    'dividend yield': get_dividend_yield,
    'profit margin': get_profit_margin,
    'ytd return': get_ytd_return,
    '3 year average return': get_3_year_return,
    '5 year average return': get_5_year_return,
    'expense ratio': get_expense_ratio,
    'beta': get_beta,
}