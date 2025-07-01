# cj-engine
CJ 프레시웨이 전용 엔진

## 개요

CJ-Engine은 대규모 차량 경로 문제(VRP, Vehicle Routing Problem)를 해결하기 위한 고성능 라우팅 엔진 API입니다. 
경유지 10,000개와 차량 1,000대 규모의 복잡한 물류 최적화 문제를 효율적으로 처리할 수 있도록 설계되었습니다.

## 핵심 기술

- **VRP 솔버**: Google OR-Tools - 대규모 제약 조건 최적화
- **라우팅 엔진**: OSRM - 고속 거리/시간 행렬 계산
- **API 프레임워크**: FastAPI - 고성능 비동기 웹 API
- **비동기 처리**: Celery + Redis - 백그라운드 작업 처리
- **지오코딩**: Geocoding Service - 주소-좌표 변환
- **테스트**: Pytest - TDD 중심 개발
- **컨테이너화**: Docker

## 시스템 아키텍처

```
Client Request → FastAPI API → Celery Task Queue → Background Worker
                                      ↓
                               Redis Result Backend
                                      ↑
Worker Process: Geocoding → OSRM Matrix → OR-Tools Solver → Result Storage
```

## 주요 특징

### 1. 대규모 처리 능력
- 경유지 10,000개 이상 처리 가능
- 차량 1,000대 이상 동시 최적화
- 비동기 처리로 응답성 보장

### 2. 실무 중심 설계
- Shipment 기반 픽업-배송 작업 처리
- 담당 고정 권역 기반 배차 시스템 (그룹 매칭)
- 다차원 용량 관리 (부피, 무게, 개수 등)
- 복잡한 시간 제약 조건 지원

### 3. 유연한 시간 관리
- `YYYY-MM-DD HH:mm:ss` 형식의 직관적 시간 표현
- 단일 시간창 지원
- 차량별 휴식 시간 설정

### 4. 정확한 위치 기반 처리
- WGS84 좌표계 기반 정밀한 위치 정보
- OSRM과의 직접 연동으로 빠른 거리/시간 계산
- 사용자 친화적인 주소 설명 제공

## API 스키마

### 요청 구조

```json
{
  "shipments": [
    {
      "pickup": {
        "location": {
          "longitude": 126.9778,
          "latitude": 37.5665
        },
        "description": "서울특별시 중구 세종대로 110 서울특별시청",
        "worktime": 300,
        "preworktime": 60,
        "timewindow": {"start": "2025-01-15 09:00:00", "end": "2025-01-15 12:00:00"}
      },
      "delivery": {
        "location": {
          "longitude": 127.0276,
          "latitude": 37.4979
        },
        "description": "서울특별시 강남구 테헤란로 152 강남파이낸스센터",
        "worktime": 180,
        "preworktime": 30,
        "timewindow": {"start": "2025-01-15 14:00:00", "end": "2025-01-15 18:00:00"}
      },
      "amount": [10, 0, 0],
      "groups": ["서울권역"],
      "skills": [1, 2]
    }
  ],
      "vehicles": [
      {
        "start_location": {
          "longitude": 126.9748,
          "latitude": 37.5665
        },
        "end_location": {
          "longitude": 127.0276,
          "latitude": 37.4979
        },
      "capacity": [500, 0, 0],
      "timewindow": {"start": "2025-01-15 08:00:00", "end": "2025-01-15 18:00:00"},
      "breaktime": {"start": "2025-01-15 12:00:00", "end": "2025-01-15 13:00:00"},
      "skills": [1, 2, 3],
      "groups": ["서울권역", "경기권역"]
    }
  ]
}
```

### 응답 구조

```json
{
  "routes": [
    {
      "vehicle_id": 1,
      "steps": [
        {
          "type": "start",
          "location": [126.9778, 37.5665],
          "arrival_time": "2025-01-15 08:00:00",
          "finish_time": "2025-01-15 08:00:00"
        },
        {
          "type": "pickup",
          "id": 1,
          "location": [126.9778, 37.5665],
          "arrival_time": "2025-01-15 09:00:00",
          "finish_time": "2025-01-15 09:05:00"
        },
        {
          "type": "delivery",
          "id": 1,
          "location": [127.0276, 37.4979],
          "arrival_time": "2025-01-15 14:00:00",
          "finish_time": "2025-01-15 14:03:00"
        },
        {
          "type": "end",
          "location": [127.0276, 37.4979],
          "arrival_time": "2025-01-15 18:00:00",
          "finish_time": "2025-01-15 18:00:00"
        }
      ],
      "total_distance_meters": 15000.0,
      "total_duration_seconds": 3600.0
    }
  ],
  "unassigned_shipments": []
}
```

### 데이터 모델

#### Address
- `longitude`: 경도 (WGS84, -180.0 ~ 180.0)
- `latitude`: 위도 (WGS84, -90.0 ~ 90.0)

#### TimeWindow
- `start`: 시작 시간 (YYYY-MM-DD HH:mm:ss)
- `end`: 종료 시간 (YYYY-MM-DD HH:mm:ss)

#### ShipmentStep
- `location`: 좌표 정보 (Address 객체)
- `description`: 주소 설명/상세 정보 (필수, 5-200자)
- `worktime`: 작업 소요 시간(초)
- `preworktime`: 사전 작업 시간(초)
- `timewindow`: 작업 가능 시간대

#### Shipment
- `pickup`: 픽업 단계 (필수)
- `delivery`: 배송 단계 (필수)
- `amount`: 화물 용량 (다차원 배열)
- `groups`: 작업이 속한 권역 그룹 ID (선택)
- `skills`: 필요 차량 스킬 (선택)

#### Vehicle
- `start_location`: 시작 좌표 (Address 객체)
- `end_location`: 종료 좌표 (Address 객체)
- `capacity`: 차량 용량 (다차원 배열)
- `timewindow`: 운행 시간대
- `skills`: 보유 스킬 (선택)
- `groups`: 차량이 담당하는 권역 그룹 (선택)
- `breaktime`: 휴식 시간 (선택)

#### SolvedRouteStep
- `type`: 단계 유형 ("start", "pickup", "delivery", "end")
- `id`: 작업 ID (선택)
- `location`: 좌표 [경도, 위도] (선택)
- `arrival_time`: 도착 시간 (선택)
- `finish_time`: 완료 시간 (선택)

#### SolvedRoute
- `vehicle_id`: 차량 ID
- `steps`: 경로 단계 목록
- `total_distance_meters`: 총 이동 거리(미터) (선택)
- `total_duration_seconds`: 총 소요 시간(초) (선택)

#### OptimizationSolution
- `routes`: 해결된 경로 목록
- `unassigned_shipments`: 배정되지 않은 작업 ID 목록

## 프로젝트 구조

TDD, MVVM 패턴, SOLID 원칙을 따라 각 모듈의 책임을 명확히 하고 신뢰성과 유지보수성을 극대화한 구조입니다.

```
cj-engine/
├── app/
│   ├── api/                  # (View) API 엔드포인트 및 라우터
│   │   └── endpoints/
│   │       └── optimization.py
│   ├── core/                 # 핵심 설정 및 초기화
│   │   ├── celery_app.py
│   │   └── config.py
│   ├── helpers/              # 재사용 가능한 헬퍼 함수
│   │   ├── time_converter.py
│   │   └── geocoding/
│   ├── schemas/              # (Model) Pydantic 데이터 모델 (스키마)
│   │   ├── request.py
│   │   └── response.py
│   ├── modules/              # 핵심 기능 모듈 (외부 서비스, 복잡한 로직)
│   │   └── ortools/
│   │       └── solver.py
│   ├── services/             # (ViewModel) 비즈니스 로직 서비스
│   │   └── optimization_service.py
│   └── tasks/                # Celery 비동기 작업 정의
│       └── optimization_tasks.py
├── tests/                    # 테스트 코드 디렉토리
│   ├── __init__.py
│   ├── api/
│   │   └── endpoints/
│   │       └── test_optimization.py
│   ├── services/
│   │   └── test_optimization_service.py
│   ├── helpers/
│   │   └── geocoding/
│   │       └── test_client.py
│   └── modules/
│       └── ortools/
│           └── test_solver.py
├── examples/                 # API 요청 예시 및 샘플 데이터
├── .vscode/                  # VS Code 디버깅 설정
│   └── launch.json
├── Dockerfile
├── pytest.ini               # Pytest 설정 파일
└── requirements.txt          # pytest, pytest-cov 등 테스트 의존성 포함
```

## API 엔드포인트

### POST /optimize
배차 최적화를 수행합니다.

**요청**: `OptimizationRequest`
**응답**: `OptimizationSolution`

차량 경로 문제(VRP)를 해결하여 최적의 배차 계획을 생성합니다.

## 개발 워크플로우 (TDD)

모든 기능 개발은 TDD(Test-Driven Development) 사이클을 따릅니다.

1. **RED**: 요구사항을 검증하는 실패하는 테스트 코드를 `tests/` 디렉토리에 먼저 작성합니다.
2. **GREEN**: 작성한 테스트를 통과시키는 최소한의 기능 코드를 `app/` 디렉토리에 작성합니다.
3. **REFACTOR**: 모든 테스트가 통과하는 것을 확인한 후, 기능 변경 없이 코드의 가독성과 구조를 개선합니다.

## 디버깅 환경

VS Code를 사용한 디버깅 환경이 구성되어 있습니다.

### 사용 가능한 디버그 설정
- **FastAPI Server**: API 서버를 디버그 모드로 실행
- **Run All Tests**: 전체 테스트 스위트 실행
- **Run Current Test File**: 현재 열린 테스트 파일만 실행
- **Debug OR-Tools Solver**: OR-Tools 솔버 관련 테스트 디버깅
- **Debug Optimization API**: 최적화 API 엔드포인트 테스트 디버깅

## 개발 환경 설정

### 요구사항
- Python 3.12+
- Docker
- Redis
- OSRM Backend
- Pytest (테스트 실행)

## 라이선스

CJ 프레시웨이 전용
