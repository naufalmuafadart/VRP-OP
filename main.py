from dependency_injector import containers, providers

# infrastructure
from application.infrastructure.repository.PandasDataFrameRepository import PandasDataFrameRepository
from application.infrastructure.repository.KMeansClusteringRepository import KMeansClusteringRepository
from application.infrastructure.repository.TSPProblemRepository import TSPProblemRepository
from application.infrastructure.repository.VRPProblemRepository import VRPProblemRepository
from application.infrastructure.repository.OPProblemRepository import OPProblemRepository
from application.infrastructure.repository.SAAlgorithmRepository import SAAlgorithmRepository

# use case
from application.use_case.RunTSPUseCase import RunTSPUseCase
from application.use_case.RunVRPUseCase import RunVRPUseCase
from application.use_case.RunOPUseCase import RunOPUseCase

# Dependency container
class Container(containers.DeclarativeContainer):
    data_frame_repository = providers.Singleton(PandasDataFrameRepository)
    clustering_repository = providers.Singleton(KMeansClusteringRepository)
    tsp_repository = providers.Singleton(TSPProblemRepository)
    vrp_repository = providers.Singleton(VRPProblemRepository)
    op_repository = providers.Singleton(OPProblemRepository)
    bfoa_repository = providers.Singleton(SAAlgorithmRepository)

# Register the container
container = Container()

selected_pois = [62, 16, 59, 69, 46, 75, 82, 88, 85, 91, 39, 27, 68, 58, 13, 12, 84, 71, 98, 2, 10, 49, 20, 94, 50, 34, 83, 4, 40, 55, 63, 74, 26, 54, 6, 1, 3, 5, 7, 8]
n_days = 5

# Run TSP
use_case = RunTSPUseCase(
    container.data_frame_repository(),
    container.tsp_repository(),
    container.bfoa_repository()
)

use_case.execute(
    selected_pois,
    n_days,
    101 # hotel id
)

# Run VRP
use_case = RunVRPUseCase(
    container.data_frame_repository(),
    container.vrp_repository(),
    container.bfoa_repository()
)

use_case.execute(
    selected_pois,
    n_days,
    101 # hotel id
)

# Run OP
use_case = RunOPUseCase(
    container.data_frame_repository(),
    container.op_repository(),
    container.bfoa_repository()
)

use_case.execute(
    selected_pois,
    n_days,
    101 # hotel id
)
