from application.infrastructure.repository.TSPProblemRepository import TSPProblemRepository;

class OPProblemRepository(TSPProblemRepository):
    def fitness(self, agent):
        routes = self.transfer(agent, self.DAYS_COUNT)
        assigned_ids = []
        for day_route in routes:
            assigned_ids.extend(day_route)
        return self.get_average_rating(assigned_ids)
