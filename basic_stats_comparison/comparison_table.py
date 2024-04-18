import pandas as pd


def fill_table(ticker_names, column_name_to_parse_func, ticker_name_to_info, ticker_name_to_data):
    df = pd.DataFrame(columns=list(column_name_to_parse_func.keys()), index=ticker_names)
    # end debug
    for ticker_name, row in df.iterrows():
        current_info = ticker_name_to_info[ticker_name]
        current_data = ticker_name_to_data[ticker_name]
        new_row = {column_name: column_name_to_parse_func[column_name](current_info,
                                                                       current_data) for column_name, v in row.items()}
        df.loc[ticker_name] = new_row
    df = df.dropna(how='all', axis=1)
    return df
