from abc import ABC, abstractmethod

class DataFrameRepository(ABC):
    @abstractmethod
    def get_data(self, file_name):
        pass

    @abstractmethod
    def get_head(self, df, n):
        pass

    @abstractmethod
    def get_length(self, df):
        pass

    @abstractmethod
    def get_single_value(self, df, index, column):
        pass

    @abstractmethod
    def add_column(self, df, data, column_name):
        pass

    @abstractmethod
    def filter_by_values_in_a_column(self, df, column_name, values):
        pass
