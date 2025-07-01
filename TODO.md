# CJ Engine - OR-Tools VRP 구현 TODO

## 📋 현재 상황

### ✅ 완료된 작업
- [x] Request/Response 스키마 정의 완료
- [x] Field Validation 로직 구현 완료  
- [x] 5개의 다양한 복잡도 예시 파일 준비 완료
- [x] 프로젝트 구조 및 TDD 환경 구축 완료
- [x] Vehicle 및 ShipmentStep에 description 필드 추가

### 🎯 구현해야 할 핵심 로직

---

## 🚀 Phase 1: 기본 VRP 해결 (예시 01, 02 대응)

### 1.1 좌표 → 거리 매트릭스 변환
- [ ] **OSRM 클라이언트 구현**
  - [ ] `app/helpers/osrm_client.py` 생성
  - [ ] 단일 경로 계산 API 연동
  - [ ] 배치 거리 매트릭스 API 연동
  - [ ] 에러 처리 및 재시도 로직
  - [ ] 테스트 코드: `tests/helpers/test_osrm_client.py`

- [ ] **거리 매트릭스 생성 로직**
  - [ ] `app/modules/ortools/distance_matrix.py` 생성
  - [ ] 좌표 리스트 → 거리/시간 매트릭스 변환
  - [ ] 캐싱 전략 구현 (Redis 연동)
  - [ ] 중복 좌표 제거 및 최적화
  - [ ] 테스트 코드: `tests/modules/ortools/test_distance_matrix.py`

### 1.2 위치 인덱스 매핑 시스템
- [ ] **인덱스 매핑 매니저 구현**
  - [ ] `app/modules/ortools/index_manager.py` 생성
  - [ ] 위치 타입별 인덱스 할당 (depot, pickup, delivery, vehicle)
  - [ ] 인덱스 ↔ 실제 위치 매핑 관리
  - [ ] shipment ID ↔ pickup/delivery 인덱스 매핑
  - [ ] 테스트 코드: `tests/modules/ortools/test_index_manager.py`

### 1.3 기본 라우팅 모델 구축
- [ ] **OR-Tools 모델 초기화**
  - [ ] `app/modules/ortools/routing_model.py` 생성
  - [ ] RoutingIndexManager 생성 로직
  - [ ] RoutingModel 생성 및 기본 설정
  - [ ] 거리/시간 비용 함수 등록
  - [ ] 테스트 코드: `tests/modules/ortools/test_routing_model.py`

### 1.4 Pickup-Delivery 제약 구현
- [ ] **픽업-배송 연결 제약**
  - [ ] AddPickupAndDelivery() 구현
  - [ ] 동일 차량 배정 보장
  - [ ] 순서 제약 (pickup → delivery)
  - [ ] 테스트: 예시 01, 02 파일로 검증

### 1.5 기본 시간창 제약 구현
- [ ] **시간 변환 유틸리틱**
  - [ ] `app/helpers/time_converter.py` 개선
  - [ ] datetime string → 분 단위 정수 변환
  - [ ] 기준 시점 설정 로직
  - [ ] 테스트 코드: `tests/helpers/test_time_converter.py`

- [ ] **시간창 제약 추가**
  - [ ] 차량 운행 시간창 설정
  - [ ] 작업(pickup/delivery) 시간창 설정
  - [ ] 작업 소요 시간(worktime) 반영
  - [ ] 테스트: 시간창 위반 시 unassigned 확인

---

## 🔧 Phase 2: 제약 조건 확장 (예시 03, 04 대응)

### 2.1 담당 고정 권역 제약 (groups) 구현
- [ ] **권역 기반 차량 필터링**
  - [ ] `app/modules/ortools/constraints/groups.py` 생성
  - [ ] shipment.groups와 vehicle.groups 교집합 검사
  - [ ] allowed_vehicles 리스트 생성
  - [ ] OR-Tools VehicleVar.SetValues() 적용
  - [ ] 테스트: 예시 03, 05 파일로 권역 제약 검증

### 2.2 스킬 제약 (skills) 구현
- [ ] **스킬 기반 차량 필터링**
  - [ ] `app/modules/ortools/constraints/skills.py` 생성
  - [ ] shipment 필요 스킬 vs vehicle 보유 스킬 검사
  - [ ] 모든 필요 스킬 보유 차량만 허용
  - [ ] groups와 skills 동시 적용 로직
  - [ ] 테스트: 예시 03, 05 파일로 스킬 제약 검증

### 2.3 다차원 용량 제약 구현
- [ ] **다차원 용량 관리**
  - [ ] `app/modules/ortools/constraints/capacity.py` 생성
  - [ ] 각 차원별 별도 Dimension 생성
  - [ ] AddDimensionWithVehicleCapacity() 적용
  - [ ] 차량별 다른 용량 설정 지원
  - [ ] 테스트: 1차원(05), 2차원(02), 3차원(01) 검증

### 2.4 휴식 시간 제약 (breaktime) 구현
- [ ] **의무 휴식 시간 처리**
  - [ ] `app/modules/ortools/constraints/break_time.py` 생성
  - [ ] 차량별 휴식 시간창 설정
  - [ ] 휴식 시간 동안 서비스 불가 처리
  - [ ] Optional 휴식 시간 처리 (null 값)
  - [ ] 테스트: 예시 05 파일로 휴식 시간 검증

---

## ⚡ Phase 3: 성능 최적화 (예시 05 대응)

### 3.1 솔버 파라미터 튜닝
- [ ] **최적화 설정 관리**
  - [ ] `app/modules/ortools/solver_config.py` 생성
  - [ ] 시간 제한 설정 (기본 5분)
  - [ ] 초기 해 생성 전략 설정
  - [ ] Local Search 메타휴리스틱 설정
  - [ ] 문제 크기별 동적 파라미터 조정

### 3.2 대규모 문제 최적화
- [ ] **성능 최적화 전략**
  - [ ] 거리 매트릭스 캐싱 (Redis)
  - [ ] 배치 지오코딩 구현
  - [ ] 메모리 사용량 최적화
  - [ ] 점진적 해결 전략 (작은 문제부터)

### 3.3 해 품질 평가 구현
- [ ] **솔루션 평가 지표**
  - [ ] `app/modules/ortools/solution_evaluator.py` 생성
  - [ ] 총 이동 거리/시간 계산
  - [ ] 차량 활용률 계산
  - [ ] 시간창 준수율 계산
  - [ ] 배정되지 않은 작업 분석

---

## 🔍 데이터 전처리 및 검증

### 4.1 입력 데이터 정규화
- [ ] **데이터 전처리 파이프라인**
  - [ ] `app/services/data_preprocessor.py` 생성
  - [ ] 모든 위치 좌표 수집 및 중복 제거
  - [ ] 시간 데이터 정규화 (기준 시점 설정)
  - [ ] 용량 차원 수 검증 및 정렬
  - [ ] 제약 조건 호환성 검증

### 4.2 실행 가능성 사전 검증
- [ ] **문제 실행가능성 검사**
  - [ ] `app/services/feasibility_checker.py` 생성
  - [ ] 총 작업량 vs 총 차량 용량 검사
  - [ ] 시간창 충돌 검사 (pickup > delivery)
  - [ ] 권역/스킬 제약으로 인한 불가능 작업 검사
  - [ ] 검증 실패 시 상세 에러 메시지 제공

---

## 🎪 테스트 전략

### 5.1 단위 테스트 완성
- [ ] **개별 모듈 테스트**
  - [ ] 거리 매트릭스 생성 테스트
  - [ ] 시간 변환 로직 테스트
  - [ ] 각 제약 조건별 독립 테스트
  - [ ] 인덱스 매핑 정확성 테스트

### 5.2 통합 테스트 구현
- [ ] **예시 파일 기반 테스트**
  - [ ] `tests/integration/test_examples.py` 생성
  - [ ] 5개 예시 파일 각각 해결 가능성 테스트
  - [ ] 예상 결과와 실제 결과 비교
  - [ ] 성능 벤치마크 (해결 시간, 메모리 사용량)

### 5.3 에지 케이스 테스트
- [ ] **경계 조건 테스트**
  - [ ] 해결 불가능한 문제 처리
  - [ ] 빈 입력 데이터 처리
  - [ ] 극단적 시간창 설정
  - [ ] 용량 부족 상황 처리

---

## 🏗️ 서비스 레이어 구현

### 6.1 최적화 서비스 구현
- [ ] **비즈니스 로직 서비스**
  - [ ] `app/services/optimization_service.py` 완성
  - [ ] OptimizationRequest → OR-Tools 데이터 변환
  - [ ] OR-Tools 솔루션 → OptimizationSolution 변환
  - [ ] 에러 처리 및 로깅
  - [ ] 성능 모니터링

### 6.2 비동기 작업 구현
- [ ] **Celery 태스크 구현**
  - [ ] `app/tasks/optimization_tasks.py` 완성
  - [ ] 장시간 최적화 작업 비동기 처리
  - [ ] 진행 상황 모니터링
  - [ ] 결과 캐싱 및 조회

### 6.3 API 엔드포인트 완성
- [ ] **REST API 구현**
  - [ ] `app/api/endpoints/optimization.py` 완성
  - [ ] POST /optimize 엔드포인트 구현
  - [ ] 입력 검증 및 에러 응답
  - [ ] API 문서화 (Swagger)

---

## 📊 모니터링 및 로깅

### 7.1 로깅 시스템 구축
- [ ] **구조화된 로깅**
  - [ ] 요청/응답 로깅
  - [ ] 성능 메트릭 로깅
  - [ ] 에러 추적 및 알림
  - [ ] 디버깅용 상세 로그

### 7.2 성능 모니터링
- [ ] **메트릭 수집**
  - [ ] 해결 시간 분포
  - [ ] 메모리 사용량 추적
  - [ ] API 응답 시간
  - [ ] 성공/실패율

---

## 🎯 우선순위 및 마일스톤

### Milestone 1: 기본 VRP 해결 (2주)
- Phase 1 완료
- 예시 01, 02 파일 정상 처리
- 기본 테스트 통과

### Milestone 2: 제약 조건 확장 (2주)
- Phase 2 완료  
- 예시 03, 04 파일 정상 처리
- 모든 제약 조건 구현

### Milestone 3: 성능 최적화 (1주)
- Phase 3 완료
- 예시 05 파일 정상 처리
- 성능 목표 달성

### Milestone 4: 프로덕션 준비 (1주)
- 서비스 레이어 완성
- 모니터링 및 로깅 구축
- API 문서화 완료

---

## 📝 참고사항

### 기술적 고려사항
- **OSRM 서버**: 별도 구축 또는 외부 서비스 사용 결정 필요
- **Redis 연동**: 캐싱 및 세션 관리용
- **Docker 환경**: 개발/테스트/프로덕션 환경 일관성
- **성능 목표**: 1000개 작업, 100대 차량 기준 5분 이내 해결

### 메모리 기반 설계 원칙
- **담당 고정 권역**: `groups` 필드를 통한 Hard Constraint 구현
- **TDD 원칙**: 모든 기능은 테스트 우선 개발
- **MVVM 패턴**: 비즈니스 로직과 데이터 모델 분리
- **SOLID 원칙**: 각 모듈의 단일 책임 및 확장성 보장 