from application.infrastructure.repository.TSPProblemRepository import TSPProblemRepository;

class VRPProblemRepository(TSPProblemRepository):
    def fitness(self, agent):
        routes = self.transfer(agent, self.DAYS_COUNT)
        # Mendapatkan total durasi perjalanan
        duration = self.get_multi_day_travel_duration(routes)
        return duration
