import pandas as pd

from basic_stats_comparison.api_get_data_utils import create_ticker_name_to_info, create_ticker_name_to_data
from basic_stats_comparison.comparison_table import fill_table
from basic_stats_comparison.extraction_utils import *

if __name__ == "__main__":
    # ticker_names = ['SOXX', 'ZSP.TO', 'AMZN', 'SHOP.TO', 'RIO']
    # ticker_names = ['SOXX', 'ZSP.TO']
    ticker_names = ['AMZN', 'SHOP.TO', 'RIO']
    my_table_file_name = 'my_table.csv'

    ticker_name_to_info = create_ticker_name_to_info(ticker_names=ticker_names)

    ticker_name_to_data = create_ticker_name_to_data(ticker_names=ticker_names)

    my_table = fill_table(ticker_names=ticker_names,
                          column_name_to_parse_func=column_name_to_parse_func,
                          ticker_name_to_info=ticker_name_to_info,
                          ticker_name_to_data=ticker_name_to_data)
    pd.set_option('display.max_columns', 500)
    print(my_table)
    my_table.to_csv(my_table_file_name)
    print('Byebye!')
