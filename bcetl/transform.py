import pandas as pd

def calculate_address_balance(file_path):
    df = pd.read_csv(file_path)
    df_tos = df[['token_address', 'to_address', 'value']].rename(columns={'to_address': 'address'})
    df_tos['value'] = df_tos['value'].apply(lambda x: int(x))
    df_froms = df[['token_address', 'from_address', 'value']].rename(columns={'from_address': 'address'})
    df_froms['value'] = df_froms['value'].apply(lambda x: int(x) * -1)
    double_entry_book = pd.concat([df_tos, df_froms])
    double_entry_book = double_entry_book[double_entry_book['address'] != '0x0000000000000000000000000000000000000000']
    aggregated = double_entry_book.groupby(
        [
            'address',
            'token_address',
        ],
        as_index=False,
    )['value'].sum()
    return aggregated
