class RunOPUseCase:
    def __init__(
            self,
            data_frame_repository,
            op_repository,
            algorithm_repository
        ):
        self.data_frame_repository = data_frame_repository
        self.op_repository = op_repository
        self.algorithm_repository = algorithm_repository

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

        # set data untuk VRP
        self.op_repository.set_days_count(n_days)
        self.op_repository.set_depart_time(8 * 3600)
        self.op_repository.set_arrival_time(21 * 3600)
        self.op_repository.set_df_schedule(df_schedule)
        self.op_repository.set_df_places(df_place)
        self.op_repository.set_df_poi(df_poi)
        self.op_repository.set_df_time_matrix(df_time_matrix)
        self.op_repository.set_selected_pois(list(df_poi['id']))
        self.op_repository.set_hotel_id(hotel_id)

        self.algorithm_repository.prepare(
            len(df_poi), # agent length
            self.op_repository.fitness, # fitness
            False
        )
        best_agent = self.algorithm_repository.run()
        route = self.op_repository.transfer(best_agent, n_days)
        print(route)
        print('Rata rata rating : ', self.op_repository.get_route_average_rating(route))
        print('Total durasi : ', self.op_repository.get_multi_day_travel_duration(route))
