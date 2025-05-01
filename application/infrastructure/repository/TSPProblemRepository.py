from application.domain.repository.ProblemRepository import ProblemRepository
import numpy as np
import copy

class TSPProblemRepository(ProblemRepository):
    def set_days_count(self, days_count):
        self.DAYS_COUNT = days_count
    
    def set_depart_time(self, depart_time):
        self.DEPART_TIME = depart_time

    def set_arrival_time(self, arrival_time):
        self.ARRIVAL_TIME = arrival_time
    
    def set_df_schedule(self, df_schedule):
        self.df_schedule = df_schedule

    def set_df_places(self, df_places):
        self.df_places = df_places

    def set_df_poi(self, df_poi):
        self.df_poi = df_poi

    def set_df_time_matrix(self, df_time_matrix):
        self.df_time_matrix = df_time_matrix
    
    def set_selected_pois(self, selected_pois):
        self.selected_pois = selected_pois
    
    def set_hotel_id(self, hotel_id):
        self.HOTEL_ID = hotel_id

    def transfer(self, agent, days_count):
        A = np.argsort(agent)
        R = [self.selected_pois[A[i]] for i in range(len(self.selected_pois))]
        R_assigned = []  # id yang sudah dimasukkan ke rute

        routes = [[] for _ in range(days_count)] # for storing route for each day
        is_any_poi_able_to_assign = self.check_any_poi_able_to_be_assigned(routes, R, R_assigned)
        while is_any_poi_able_to_assign: # if any POI able to be assigned
            days_included = []
            selected_day = self.get_day_with_fewest_poi(routes, days_included)
            poi_has_assigned = False
            while not poi_has_assigned:
                i = 0
                while i < len(R) and not poi_has_assigned:
                    if self.check_poi_able_to_be_assigned(routes[selected_day], R[i]) and R[i] not in R_assigned:
                        routes[selected_day].append(R[i])
                        R_assigned.append(R[i])
                        poi_has_assigned = True
                    i += 1
                if not poi_has_assigned: # jika tidak ada poi yang diassign, pilih hari lain
                    days_included.append(selected_day)
                    selected_day = self.get_day_with_fewest_poi(routes, days_included)
            is_any_poi_able_to_assign = self.check_any_poi_able_to_be_assigned(routes, R, R_assigned)

        return routes

    def fitness(self, agent):
        routes = self.transfer(agent, self.DAYS_COUNT)
        return self.get_multi_day_travel_duration(routes)
    
    def get_route_average_rating(self, routes):
        assigned_ids = []
        for day_route in routes:
            assigned_ids.extend(day_route)
        return self.get_average_rating(assigned_ids)

    def get_route_sum_rating(self, routes):
        assigned_ids = []
        for day_route in routes:
            assigned_ids.extend(day_route)
        return self.get_sum_rating(assigned_ids)

    def get_duration_percentage_utilization(self, routes):
        durations = 0
        for route in routes:
            durations += self.get_single_day_duration(route)
        return durations / ((self.ARRIVAL_TIME - self.DEPART_TIME) * self.DAYS_COUNT) * 100

    @staticmethod
    def get_number_of_assigned_pois(routes):
        assigned_ids = []
        for day_route in routes:
            assigned_ids.extend(day_route)
        return len(assigned_ids)
    
    def get_multi_day_travel_duration(self, routes):
        durations = 0
        for route in routes:
            durations += self.get_single_day_travel_duration(route)
        return durations

    def get_poi_rating(self, _id):
        return self.df_places[self.df_places['id'] == _id].iloc[0]['rating']

    def get_average_rating(self, _ids):
        return self.df_places[self.df_places['id'].isin(_ids)].mean(numeric_only=True)['rating']

    def get_sum_rating(self, _ids):
        return self.df_places[self.df_places['id'].isin(_ids)].sum(numeric_only=True)['rating']

    def get_single_day_travel_duration(self, single_day_route):
        if len(single_day_route) == 0:
            return 0

        if len(single_day_route) == 1:
            duration = self.get_travel_time(self.HOTEL_ID, single_day_route[0])
            duration += self.get_travel_time(single_day_route[0], self.HOTEL_ID)
            return duration

        duration = 0
        for i in range(len(single_day_route)):
            if i == 0: # first poi
                duration += self.get_travel_time(self.HOTEL_ID, single_day_route[i])
            elif i != len(single_day_route)-1:
                duration += self.get_travel_time(single_day_route[i], single_day_route[i+1])
            else: # last poi
                duration += self.get_travel_time(single_day_route[i], self.HOTEL_ID)

        return duration
    
    def get_poi_opening_hour(self, _id):
        return self.df_schedule[self.df_schedule['id_tempat'] == _id].iloc[0]['jam_buka']
    
    def get_poi_closing_hour(self, _id):
        return self.df_schedule[self.df_schedule['id_tempat'] == _id].iloc[0]['jam_tutup']
    
    def get_travel_time(self, _id1, _id2):
        df_filter = self.df_time_matrix[(self.df_time_matrix['id_a'] == _id1) & (self.df_time_matrix['id_b'] == _id2)]
        return df_filter.iloc[0]['durasi']

    def get_single_day_duration(self, single_day_route):
        if len(single_day_route) == 0:
            return 0

        if len(single_day_route) == 1:
            duration = self.get_travel_time(self.HOTEL_ID, single_day_route[0])
            duration += self.get_poi_duration(single_day_route[0])
            duration += self.get_travel_time(single_day_route[0], self.HOTEL_ID)
            return duration

        duration = 0
        for i in range(len(single_day_route)):
            if i == 0: # first poi
                duration += self.get_travel_time(self.HOTEL_ID, single_day_route[i])
                duration += self.get_poi_duration(single_day_route[i])
            elif i != len(single_day_route)-1:
                duration += self.get_travel_time(single_day_route[i], single_day_route[i+1])
                duration += self.get_poi_duration(single_day_route[i+1])
            else: # last poi
                duration += self.get_travel_time(single_day_route[i], self.HOTEL_ID)

        return duration
    
    def get_poi_duration(self, _id):
        return self.df_places[self.df_places['id'] == _id].iloc[0]['durasi']
    
    @staticmethod
    def get_day_with_fewest_poi(routes, index_ignored):
        selected_index = 0
        min_poi_assigned = 200
        for i in range(len(routes)):
            if i not in index_ignored:
                if len(routes[i]) < min_poi_assigned:
                    selected_index = i
                    min_poi_assigned = len(routes[i])
        return selected_index

    def check_poi_able_to_be_assigned(self, single_day_route, poi_id):
        if len(single_day_route) == 0:
            return True
        sdr = copy.deepcopy(single_day_route)
        sdr.append(poi_id)

        last_poi_id = single_day_route[len(single_day_route)-1]
        single_day_duration = self.get_single_day_duration(single_day_route)
        single_day_duration -= self.get_travel_time(last_poi_id, self.HOTEL_ID)
        single_day_duration += self.DEPART_TIME

        arrival_time_to_poi = single_day_duration + self.get_travel_time(last_poi_id, poi_id)
        departure_time_from_poi = arrival_time_to_poi + self.get_poi_duration(poi_id)
        arrival_time_to_hotel = departure_time_from_poi + self.get_travel_time(poi_id, self.HOTEL_ID)

        if arrival_time_to_hotel > self.ARRIVAL_TIME:
            return False

        if departure_time_from_poi > self.get_poi_closing_hour(poi_id):
            return False

        if arrival_time_to_poi < self.get_poi_opening_hour(poi_id):
            return False

        return True
    
    def check_any_poi_able_to_be_assigned(self, routes, R, R_assigned):
        for _id in R:  # perulangan untuk setiap _id POI
            if _id not in R_assigned:  # jika _id termasuk unassigned POI
                for route in routes:  # Perulangan untuk setiap day route
                    if self.check_poi_able_to_be_assigned(route, _id):  # cek apakah _id POI diassign ke hari tersebut
                        return True
        return False
