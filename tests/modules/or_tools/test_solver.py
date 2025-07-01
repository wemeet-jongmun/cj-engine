import pytest
from app.modules.ortools.solver import OrToolsSolver
from app.schemas.request import OptimizationRequest

# conftest.py 또는 별도 파일에서 테스트용 데이터를 관리할 수 있습니다.
# 여기서는 간단한 예시 데이터를 직접 정의합니다.
SAMPLE_REQUEST_DATA = {
    "vehicles": [
        {
            "id": 1,
            "start_address": "A",
            "end_address": "A",
            "capacity": [10],
            "groups": ["group1"],
            "time_windows": [["2025-01-01 08:00:00", "2025-01-01 18:00:00"]],
        }
    ],
    "shipments": [
        {
            "pickup": {
                "id": 10,
                "location": {"lon": 127.0, "lat": 37.0},
                "timewindows": [["2025-01-01 09:00:00", "2025-01-01 17:00:00"]],
            },
            "delivery": {
                "id": 11,
                "location": {"lon": 127.1, "lat": 37.1},
                "timewindows": [["2025-01-01 09:00:00", "2025-01-01 17:00:00"]],
            },
            "amount": [1],
            "groups": ["group1"],
        }
    ],
}

SAMPLE_DISTANCE_MATRIX = [[0, 1000], [1000, 0]]  # A -> B, B -> A
SAMPLE_DURATION_MATRIX = [[0, 60], [60, 0]]  # A -> B, B -> A


def test_solver_initialization():
    """솔버가 정상적으로 초기화되는지 테스트합니다."""
    request = OptimizationRequest(**SAMPLE_REQUEST_DATA)
    solver = OrToolsSolver(
        request, SAMPLE_DISTANCE_MATRIX, SAMPLE_DURATION_MATRIX
    )
    assert solver is not None
    assert solver.request_data == request


@pytest.mark.skip(reason="Not implemented yet")
def test_solve_simple_case():
    """가장 간단한 케이스가 정상적으로 해결되는지 테스트합니다."""
    # TODO: 1. Mock Request, Matrices 생성
    # TODO: 2. Solver 실행
    # TODO: 3. 결과 검증 (e.g., 모든 shipment가 할당되었는지)
    assert False


@pytest.mark.skip(reason="Not implemented yet")
def test_fixed_zone_constraint():
    """담당 고정 권역 제약조건이 올바르게 동작하는지 테스트합니다."""
    # TODO: 1. Group이 맞지 않아 할당될 수 없는 케이스의 Request 생성
    # TODO: 2. Solver 실행
    # TODO: 3. 해당 shipment가 unassigned_shipments에 포함되는지 검증
    assert False
