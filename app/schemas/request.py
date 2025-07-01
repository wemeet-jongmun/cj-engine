from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, field_validator, model_validator
import re


class Address(BaseModel):
    """주소 좌표 정보 모델"""

    longitude: float = Field(..., description="경도 (WGS84)")
    latitude: float = Field(..., description="위도 (WGS84)")

    @field_validator("longitude")
    @classmethod
    def validate_longitude(cls, v: float) -> float:
        """경도 범위 검증 (-180 ~ 180)"""
        if v < -180.0 or v > 180.0:
            raise ValueError("경도는 -180.0 ~ 180.0 범위여야 합니다")
        return v

    @field_validator("latitude")
    @classmethod
    def validate_latitude(cls, v: float) -> float:
        """위도 범위 검증 (-90 ~ 90)"""
        if v < -90.0 or v > 90.0:
            raise ValueError("위도는 -90.0 ~ 90.0 범위여야 합니다")
        return v


class TimeWindow(BaseModel):
    start: str
    end: str

    @field_validator("start", "end")
    @classmethod
    def validate_datetime_format(cls, v: str) -> str:
        """시간 형식 검증 (YYYY-MM-DD HH:mm:ss)"""
        if not v or not isinstance(v, str):
            raise ValueError("시간은 문자열이어야 합니다")

        # 문자열 날짜 형식 검증
        formats = [
            "%Y-%m-%d %H:%M:%S",  # 2025-01-15 09:00:00
            "%Y-%m-%d %H:%M",  # 2025-01-15 09:00
        ]

        for fmt in formats:
            try:
                datetime.strptime(v, fmt)
                return v
            except ValueError:
                continue

        raise ValueError(
            f"올바른 시간 형식이 아닙니다. 예: '2025-01-15 09:00:00'"
        )

    @model_validator(mode="after")
    def validate_time_order(self):
        """시작 시간이 종료 시간보다 빠른지 검증"""

        def parse_time_value(time_str: str) -> datetime:
            """시간 문자열을 datetime 객체로 변환"""
            try:
                return datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                return datetime.strptime(time_str, "%Y-%m-%d %H:%M")

        # 시간 순서 검증
        start_dt = parse_time_value(self.start)
        end_dt = parse_time_value(self.end)

        if start_dt >= end_dt:
            raise ValueError("시작 시간은 종료 시간보다 빨라야 합니다")

        return self


class ShipmentStep(BaseModel):
    location: Address
    description: str = Field(..., description="주소 설명/상세 정보")
    worktime: int = Field(0, description="작업 소요 시간(초)")
    preworktime: int = Field(0, description="사전 작업 소요 시간(초)")
    timewindow: TimeWindow

    @field_validator("description")
    @classmethod
    def validate_description(cls, v: str) -> str:
        """주소 설명 검증"""
        if not v or not isinstance(v, str):
            raise ValueError("주소 설명은 필수 입력사항입니다")

        v = v.strip()
        if len(v) < 5:
            raise ValueError("주소 설명은 최소 5자 이상이어야 합니다")

        if len(v) > 200:
            raise ValueError("주소 설명은 최대 200자까지 입력 가능합니다")

        return v

    @field_validator("worktime", "preworktime")
    @classmethod
    def validate_time_fields(cls, v: int) -> int:
        """작업 시간 검증"""
        if v < 0:
            raise ValueError("작업 시간은 0 이상이어야 합니다")

        if v > 86400:  # 24시간 = 86400초
            raise ValueError("작업 시간은 24시간(86400초)을 초과할 수 없습니다")

        return v


class Shipment(BaseModel):
    pickup: ShipmentStep
    delivery: ShipmentStep
    amount: List[int]
    groups: Optional[List[str]] = None
    skills: Optional[List[int]] = None

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, v: List[int]) -> List[int]:
        """화물 용량 검증"""
        if not v or len(v) == 0:
            raise ValueError("화물 용량 정보는 필수입니다")

        if len(v) > 10:
            raise ValueError("화물 용량 차원은 최대 10개까지 가능합니다")

        for i, amount in enumerate(v):
            if amount < 0:
                raise ValueError(f"화물 용량[{i}]은 0 이상이어야 합니다")

        return v

    @field_validator("groups")
    @classmethod
    def validate_groups(cls, v: Optional[List[str]]) -> Optional[List[str]]:
        """권역 그룹 검증"""
        if v is None:
            return v

        if len(v) == 0:
            return None

        for group in v:
            if not group or not isinstance(group, str):
                raise ValueError("권역 그룹명은 빈 문자열일 수 없습니다")

            if len(group) > 50:
                raise ValueError("권역 그룹명은 최대 50자까지 가능합니다")

        return v

    @field_validator("skills")
    @classmethod
    def validate_skills(cls, v: Optional[List[int]]) -> Optional[List[int]]:
        """스킬 검증"""
        if v is None:
            return v

        if len(v) == 0:
            return None

        for skill in v:
            if skill <= 0:
                raise ValueError("스킬 ID는 양수여야 합니다")

        return v


class Vehicle(BaseModel):
    start_location: Address
    end_location: Address
    capacity: List[int]
    timewindow: TimeWindow
    breaktime: Optional[TimeWindow] = None
    skills: Optional[List[int]] = None
    groups: Optional[List[str]] = None

    @field_validator("capacity")
    @classmethod
    def validate_capacity(cls, v: List[int]) -> List[int]:
        """차량 용량 검증"""
        if not v or len(v) == 0:
            raise ValueError("차량 용량 정보는 필수입니다")

        if len(v) > 10:
            raise ValueError("차량 용량 차원은 최대 10개까지 가능합니다")

        for i, capacity in enumerate(v):
            if capacity <= 0:
                raise ValueError(f"차량 용량[{i}]은 양수여야 합니다")

        return v

    @field_validator("skills")
    @classmethod
    def validate_skills(cls, v: Optional[List[int]]) -> Optional[List[int]]:
        """스킬 검증 (Shipment와 동일)"""
        if v is None:
            return v

        if len(v) == 0:
            return None

        for skill in v:
            if skill <= 0:
                raise ValueError("스킬 ID는 양수여야 합니다")

        return v

    @field_validator("groups")
    @classmethod
    def validate_groups(cls, v: Optional[List[str]]) -> Optional[List[str]]:
        """권역 그룹 검증 (Shipment와 동일)"""
        if v is None:
            return v

        if len(v) == 0:
            return None

        for group in v:
            if not group or not isinstance(group, str):
                raise ValueError("권역 그룹명은 빈 문자열일 수 없습니다")

            if len(group) > 50:
                raise ValueError("권역 그룹명은 최대 50자까지 가능합니다")

        return v

    @model_validator(mode="after")
    def validate_breaktime(self):
        """휴식 시간이 운행 시간 내에 있는지 검증"""
        if self.breaktime is None:
            return self

        def parse_time_value(time_str: str) -> datetime:
            """시간 문자열을 datetime 객체로 변환"""
            try:
                return datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                return datetime.strptime(time_str, "%Y-%m-%d %H:%M")

        # 운행 시간 파싱
        work_start = parse_time_value(self.timewindow.start)
        work_end = parse_time_value(self.timewindow.end)

        # 휴식 시간 파싱
        break_start = parse_time_value(self.breaktime.start)
        break_end = parse_time_value(self.breaktime.end)

        # 휴식 시간이 운행 시간 내에 있는지 확인
        if break_start < work_start or break_end > work_end:
            raise ValueError("휴식 시간은 운행 시간 내에 있어야 합니다")

        return self


class OptimizationRequest(BaseModel):
    shipments: List[Shipment]
    vehicles: List[Vehicle]

    @field_validator("shipments")
    @classmethod
    def validate_shipments(cls, v: List[Shipment]) -> List[Shipment]:
        """작업 목록 검증"""
        if not v or len(v) == 0:
            raise ValueError("최소 1개 이상의 작업이 필요합니다")

        if len(v) > 10000:
            raise ValueError("작업은 최대 10,000개까지 처리 가능합니다")

        return v

    @field_validator("vehicles")
    @classmethod
    def validate_vehicles(cls, v: List[Vehicle]) -> List[Vehicle]:
        """차량 목록 검증"""
        if not v or len(v) == 0:
            raise ValueError("최소 1개 이상의 차량이 필요합니다")

        if len(v) > 1000:
            raise ValueError("차량은 최대 1,000대까지 처리 가능합니다")

        return v

    @model_validator(mode="after")
    def validate_capacity_dimensions(self):
        """모든 차량과 작업의 용량 차원이 일치하는지 검증"""
        if not self.shipments or not self.vehicles:
            return self

        # 첫 번째 차량의 용량 차원을 기준으로 설정
        capacity_dim = len(self.vehicles[0].capacity)

        # 모든 차량의 용량 차원 확인
        for i, vehicle in enumerate(self.vehicles):
            if len(vehicle.capacity) != capacity_dim:
                raise ValueError(f"차량[{i}]의 용량 차원이 일치하지 않습니다")

        # 모든 작업의 화물 용량 차원 확인
        for i, shipment in enumerate(self.shipments):
            if len(shipment.amount) != capacity_dim:
                raise ValueError(
                    f"작업[{i}]의 화물 용량 차원이 일치하지 않습니다"
                )

        return self
