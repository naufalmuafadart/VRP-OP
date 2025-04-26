from abc import ABC, abstractmethod

class ProblemRepository(ABC):
    @abstractmethod
    def set_days_count(self, days_count):
        pass

    @abstractmethod
    def set_depart_time(self, depart_time):
        pass

    @abstractmethod
    def set_arrival_time(self, arrival_time):
        pass

    @abstractmethod
    def set_df_schedule(self, df_schedule):
        pass

    @abstractmethod
    def set_df_places(self, df_places):
        pass

    @abstractmethod
    def set_df_poi(self, df_poi):
        pass

    @abstractmethod
    def set_df_time_matrix(self, df_time_matrix):
        pass

    @abstractmethod
    def set_selected_pois(self, selected_pois):
        pass

    @abstractmethod
    def set_hotel_id(self, hotel_id):
        pass

    @abstractmethod
    def transfer(self, agent, days_count):
        pass

    @abstractmethod
    def fitness(self, agent):
        pass

    @abstractmethod
    def get_route_average_rating(self, route):
        pass

    @abstractmethod
    def get_multi_day_travel_duration(self, routes):
        pass
