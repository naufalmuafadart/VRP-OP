class RunVRPUseCase:
    def __init__(
            self,
            data_frame_repository,
            vrp_repository,
            algorithm_repository
        ):
        self.data_frame_repository = data_frame_repository
        self.vrp_repository = vrp_repository
        self.algorithm_repository = algorithm_repository

    def execute(self, selected_pois, n_days, hotel_id, alfa, beta):
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

        # set data untuk VRP
        self.vrp_repository.set_days_count(n_days)
        self.vrp_repository.set_depart_time(8 * 3600)
        self.vrp_repository.set_arrival_time(21 * 3600)
        self.vrp_repository.set_df_schedule(df_schedule)
        self.vrp_repository.set_df_places(df_place)
        self.vrp_repository.set_df_poi(df_poi)
        self.vrp_repository.set_df_time_matrix(df_time_matrix)
        self.vrp_repository.set_selected_pois(list(df_poi['id']))
        self.vrp_repository.set_hotel_id(hotel_id)

        total_quality_poi = self.vrp_repository.get_route_sum_rating([selected_pois])

        self.algorithm_repository.prepare(
            len(df_poi), # agent length
            self.vrp_repository.fitness, # fitness
            False
        )
        best_agent = self.algorithm_repository.run()
        routes = self.vrp_repository.transfer(best_agent, n_days)

        total_quality = self.vrp_repository.get_route_sum_rating(routes)
        fitness = alfa * (total_quality / total_quality_poi) - beta * (
                self.vrp_repository.get_multi_day_travel_duration(routes) / 200_000)
        n_poi = self.vrp_repository.get_number_of_assigned_pois(routes)
        duration_utilization = self.vrp_repository.get_duration_percentage_utilization(routes)
        return routes, fitness, n_poi, duration_utilization
