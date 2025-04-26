from application.domain.repository.DataFrameRepository import DataFrameRepository
import pandas as pd

class PandasDataFrameRepository(DataFrameRepository):
    def get_data(self, file_name):
        if (file_name == 'place_jadwal'):
            df_schedule = pd.read_csv('./dataset/place_jadwal.csv')
            df_schedule['jam_buka'] = df_schedule['jam_buka'].apply(lambda x: int(x[:2]) * 3600 + int(x[3:]) * 60)
            df_schedule['jam_tutup'] = df_schedule['jam_tutup'].apply(lambda x: int(x[:2]) * 3600 + int(x[3:]) * 60)
            return df_schedule
        return pd.read_csv(f'./dataset/{file_name}.csv')
    
    def get_head(self, df, n, is_copy=True):
        return df.head(n).copy(is_copy)
    
    def get_length(self, df):
        return len(df)
    
    def get_single_value(self, df, index, column):
        return df.iloc[index][column]
    
    def add_column(self, df, data, column_name):
        df[column_name] = data
        return df
    
    def filter_by_values_in_a_column(self, df, column_name, values):
        return df[df[column_name].isin(values)]
