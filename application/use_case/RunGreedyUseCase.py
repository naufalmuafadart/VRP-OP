class RunGreedyUseCase:
    def __init__(
            self,
            data_frame_repository,
            greedy_repository
        ):
        self.data_frame_repository = data_frame_repository
        self.greedy_repository = greedy_repository

    def execute(self, selected_pois, n_days, hotel_id):
        # Mendapatkan dataset POI
        df_place = self.data_frame_repository.get_data('places')

        # Mendapatkan dataset timematrix
        df_time_matrix = self.data_frame_repository.get_data('place_timematrix')

        # Mendapatkan dataset schedule
        df_schedule = self.data_frame_repository.get_data('place_jadwal')

        # Mendapatkan subset data POI
        df_poi = self.data_frame_repository.get_head(df_place, 99)

        # Filter POI sesuai selected POIs
        df_poi = self.data_frame_repository.filter_by_values_in_a_column(df_poi, 'id', selected_pois)

        # set data untuk Greedy
        self.greedy_repository.set_days_count(n_days)
        self.greedy_repository.set_depart_time(8 * 3600)
        self.greedy_repository.set_arrival_time(21 * 3600)
        self.greedy_repository.set_df_schedule(df_schedule)
        self.greedy_repository.set_df_places(df_place)
        self.greedy_repository.set_df_poi(df_poi)
        self.greedy_repository.set_df_time_matrix(df_time_matrix)
        self.greedy_repository.set_selected_pois(list(df_poi['id']))
        self.greedy_repository.set_hotel_id(hotel_id)

        routes = self.greedy_repository.run(list(df_poi['id']), n_days)
        print(routes)
        total_quality = self.greedy_repository.get_route_sum_rating(routes)
        n_poi = self.greedy_repository.get_number_of_assigned_pois(routes)
        duration_utilization = self.greedy_repository.get_duration_percentage_utilization(routes)
        return routes, total_quality, n_poi, duration_utilization
