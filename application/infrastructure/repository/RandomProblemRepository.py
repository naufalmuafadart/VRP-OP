from application.infrastructure.repository.TSPProblemRepository import TSPProblemRepository
import random

class RandomProblemRepository(TSPProblemRepository):
    def run(self, selected_pois, n_days):
        routes = [[] for _ in range(n_days)]
        visited_pois = []
        is_any_poi_able_to_assign = self.check_any_poi_able_to_be_assigned(routes, selected_pois, visited_pois)
        while is_any_poi_able_to_assign: # if any POI able to be assigned
            days_included = []
            selected_day = self.get_day_with_fewest_poi(routes, days_included)
            poi_has_assigned = False
            while not poi_has_assigned:
                i = 0
                shuffled_pois = random.sample(selected_pois, len(selected_pois))  # Create a random permutation of selected_pois
                while i < len(shuffled_pois) and not poi_has_assigned:
                    selected_poi = shuffled_pois[i]
                    if self.check_poi_able_to_be_assigned(routes[selected_day], selected_poi) and selected_poi not in visited_pois:
                        routes[selected_day].append(selected_poi)
                        visited_pois.append(selected_poi)
                        poi_has_assigned = True
                    i += 1
                if not poi_has_assigned: # jika tidak ada poi yang diassign, pilih hari lain
                    days_included.append(selected_day)
                    selected_day = self.get_day_with_fewest_poi(routes, days_included)
            is_any_poi_able_to_assign = self.check_any_poi_able_to_be_assigned(routes, selected_pois, visited_pois)
        return routes