from application.infrastructure.repository.TSPProblemRepository import TSPProblemRepository
import time
import random

class VRPOPProblemRepository(TSPProblemRepository):
    def fitness(self, agent):
        routes = self.transfer(agent, self.DAYS_COUNT)
        # Mendapatkan total durasi perjalanan
        duration = self.get_multi_day_travel_duration(routes)
        return duration
    
    def get_unassigned_pois_by_route(self, route):
        assigned_pois = []
        for days_route in route:
            assigned_pois.extend(days_route)
        return list(
            set(self.selected_pois).difference(assigned_pois)
        )

    # orienteering problem

    def validate_route(self, route):
        if len(route) == 0:
            return
        checked_poi = []

        total_duration = 0
        for poi in route:
            checked_poi.append(poi)
            last_poi_id = checked_poi[len(checked_poi)-1]
            total_duration += self.get_single_day_duration(checked_poi)

            arrival_time_to_poi = total_duration - self.get_travel_time(last_poi_id, self.HOTEL_ID) - self.get_poi_duration(last_poi_id)
            departure_time_from_poi = arrival_time_to_poi + self.get_poi_duration(last_poi_id)
            arrival_time_to_hotel = departure_time_from_poi + self.get_travel_time(last_poi_id, self.HOTEL_ID)

            if arrival_time_to_hotel > self.ARRIVAL_TIME:
                raise Exception('Arrival time to hotel exceed user time windows')
            
            if departure_time_from_poi > self.get_poi_closing_hour(last_poi_id):
                raise Exception('Departure time from POI exceed POI closing hour')
            
            if arrival_time_to_poi < self.get_poi_opening_hour(last_poi_id):
                raise Exception('Arrival time to POI lower than POI opening hour')

    def try_insertion(self, route, unassigned_poi):
        if len(unassigned_poi) == 0:
            return route, unassigned_poi
        random_unassigned_id = unassigned_poi[random.randint(0,len(unassigned_poi)-1)]
        for i in range(len(route)):
            try:
                new_route = route.copy()
                new_route.insert(i, random_unassigned_id)
                self.validate_route()
                if self.total_score(new_route) > self.total_score(route):
                    unassigned_poi = list(set(unassigned_poi).difference(set(new_route)))
                    return new_route, unassigned_poi
            except:
                continue
        return route, unassigned_poi

    def try_swap(self, route, unassigned_poi):
        if len(unassigned_poi) == 0:
            return route, unassigned_poi
        random_unassigned_id = unassigned_poi[random.randint(0,len(unassigned_poi)-1)]
        for i in range(len(route)):
            try:
                new_route = route.copy()
                new_route[i] = random_unassigned_id
                self.validate_route()
                if self.total_score(new_route) > self.total_score(route):
                    unassigned_poi = list(set(unassigned_poi).difference(set(new_route)))
                    return new_route, unassigned_poi
            except:
                continue
        return route, unassigned_poi

    def apply_move(self, route, unassigned_poi, move_type):
        if move_type == "insertion":
            return self.try_insertion(route, unassigned_poi)
        elif move_type == "swap":
            return self.try_swap(route, unassigned_poi)
        elif move_type == "2opt":
            return self.try_2opt(route, unassigned_poi)
        else:
            return None
    
    def total_score(self, ids):
        return self.get_average_rating(ids)

    def orieenteering(self, route, unassigned_poi, max_duration):
        """
        Find optimal single route (max value POI)

        Args:
            route (list): Single route
            unassigned_poi (int): POI that not been assigned yet
            max_duration (int): Maximum duration in seconds

        Returns:
            route: Optimized route
            unassigned_poi: POI that not been assigned yet after the route is optimized
        """
        if len(unassigned_poi) == 0: # if no POI to be inserted
            return route, unassigned_poi

        start_time = time.time()
        neighborhood_list = ["insertion", "swap"]
        is_improved = False
        while time.time() - start_time < max_duration and not is_improved:
            for neighborhood in neighborhood_list:
                new_route, new_unassigned_poi = self.apply_move(route, unassigned_poi, neighborhood)
                if self.total_score(new_route) > self.total_score(route):
                    route = new_route
                    unassigned_poi = new_unassigned_poi
                    is_improved = True
                    break

        return route, unassigned_poi
