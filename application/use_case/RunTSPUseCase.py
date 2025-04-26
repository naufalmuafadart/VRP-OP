class RunTSPUseCase:
    def __init__(
            self,
            data_frame_repository,
            tsp_repository,
            algorithm_repository
        ):
        self.data_frame_repository = data_frame_repository
        self.tsp_repository = tsp_repository
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

        # Menyiapkan data koordinat
        coordinate_data = []
        for i in range(self.data_frame_repository.get_length(df_poi)):
            coordinate_data.append([
                self.data_frame_repository.get_single_value(
                    df_poi,
                    i,
                    'latitude'
                ),
                self.data_frame_repository.get_single_value(
                    df_poi,
                    i,
                    'longitude'
                )
            ])

        route = []
        for i in range(n_days):
            # set data untuk TSP
            self.tsp_repository.set_days_count(1)
            self.tsp_repository.set_depart_time(8 * 3600)
            self.tsp_repository.set_arrival_time(21 * 3600)
            self.tsp_repository.set_df_schedule(df_schedule)
            self.tsp_repository.set_df_places(df_place)
            self.tsp_repository.set_df_poi(df_poi)
            self.tsp_repository.set_df_time_matrix(df_time_matrix)
            self.tsp_repository.set_selected_pois(list(df_poi['id']))
            self.tsp_repository.set_hotel_id(hotel_id)

            self.algorithm_repository.prepare(
                len(df_poi), # agent length
                self.tsp_repository.fitness, # fitness
                False
            )
            random_agent = self.algorithm_repository.run()
            [route_per_day] = self.tsp_repository.transfer(random_agent, 1)
            route.append(route_per_day)

            # df_poi = df_poi[~df_poi['id'].isin(route_per_day)]
            df_poi = self.data_frame_repository.filter_by_values_in_a_column(df_poi, 'id', route_per_day)
        print(route)
        print('Rata rata rating : ', self.tsp_repository.get_route_average_rating(route))
        print('Total durasi : ', self.tsp_repository.get_multi_day_travel_duration(route))
