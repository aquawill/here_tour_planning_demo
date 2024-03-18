# generate from response of Tour Planning API V2
# by https://app.quicktype.io/


# This code parses date/times, so please
#
#     pip install python-dateutil
#
# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = solution_from_dict(json.loads(json_string))

from typing import Optional, Any, List, TypeVar, Type, cast, Callable
from datetime import datetime
from enum import Enum
from uuid import UUID
import dateutil.parser


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


class Times:
    driving: Optional[int]
    serving: Optional[int]
    waiting: Optional[int]
    times_break: Optional[int]

    def __init__(self, driving: Optional[int], serving: Optional[int], waiting: Optional[int], times_break: Optional[int]) -> None:
        self.driving = driving
        self.serving = serving
        self.waiting = waiting
        self.times_break = times_break

    @staticmethod
    def from_dict(obj: Any) -> 'Times':
        assert isinstance(obj, dict)
        driving = from_union([from_int, from_none], obj.get("driving"))
        serving = from_union([from_int, from_none], obj.get("serving"))
        waiting = from_union([from_int, from_none], obj.get("waiting"))
        times_break = from_union([from_int, from_none], obj.get("break"))
        return Times(driving, serving, waiting, times_break)

    def to_dict(self) -> dict:
        result: dict = {}
        result["driving"] = from_union([from_int, from_none], self.driving)
        result["serving"] = from_union([from_int, from_none], self.serving)
        result["waiting"] = from_union([from_int, from_none], self.waiting)
        result["break"] = from_union([from_int, from_none], self.times_break)
        return result


class Statistic:
    cost: Optional[float]
    distance: Optional[int]
    duration: Optional[int]
    times: Optional[Times]

    def __init__(self, cost: Optional[float], distance: Optional[int], duration: Optional[int], times: Optional[Times]) -> None:
        self.cost = cost
        self.distance = distance
        self.duration = duration
        self.times = times

    @staticmethod
    def from_dict(obj: Any) -> 'Statistic':
        assert isinstance(obj, dict)
        cost = from_union([from_float, from_none], obj.get("cost"))
        distance = from_union([from_int, from_none], obj.get("distance"))
        duration = from_union([from_int, from_none], obj.get("duration"))
        times = from_union([Times.from_dict, from_none], obj.get("times"))
        return Statistic(cost, distance, duration, times)

    def to_dict(self) -> dict:
        result: dict = {}
        result["cost"] = from_union([to_float, from_none], self.cost)
        result["distance"] = from_union([from_int, from_none], self.distance)
        result["duration"] = from_union([from_int, from_none], self.duration)
        result["times"] = from_union([lambda x: to_class(Times, x), from_none], self.times)
        return result


class Location:
    lat: Optional[float]
    lng: Optional[float]

    def __init__(self, lat: Optional[float], lng: Optional[float]) -> None:
        self.lat = lat
        self.lng = lng

    @staticmethod
    def from_dict(obj: Any) -> 'Location':
        assert isinstance(obj, dict)
        lat = from_union([from_float, from_none], obj.get("lat"))
        lng = from_union([from_float, from_none], obj.get("lng"))
        return Location(lat, lng)

    def to_dict(self) -> dict:
        result: dict = {}
        result["lat"] = from_union([to_float, from_none], self.lat)
        result["lng"] = from_union([to_float, from_none], self.lng)
        return result


class ActivityTime:
    start: Optional[datetime]
    end: Optional[datetime]

    def __init__(self, start: Optional[datetime], end: Optional[datetime]) -> None:
        self.start = start
        self.end = end

    @staticmethod
    def from_dict(obj: Any) -> 'ActivityTime':
        assert isinstance(obj, dict)
        start = from_union([from_datetime, from_none], obj.get("start"))
        end = from_union([from_datetime, from_none], obj.get("end"))
        return ActivityTime(start, end)

    def to_dict(self) -> dict:
        result: dict = {}
        result["start"] = from_union([lambda x: x.isoformat(), from_none], self.start)
        result["end"] = from_union([lambda x: x.isoformat(), from_none], self.end)
        return result


class TypeEnum(Enum):
    ARRIVAL = "arrival"
    BREAK = "break"
    DELIVERY = "delivery"
    DEPARTURE = "departure"


class Activity:
    job_id: Optional[str]
    type: Optional[TypeEnum]
    job_tag: Optional[str]
    location: Optional[Location]
    time: Optional[ActivityTime]

    def __init__(self, job_id: Optional[str], type: Optional[TypeEnum], job_tag: Optional[str], location: Optional[Location], time: Optional[ActivityTime]) -> None:
        self.job_id = job_id
        self.type = type
        self.job_tag = job_tag
        self.location = location
        self.time = time

    @staticmethod
    def from_dict(obj: Any) -> 'Activity':
        assert isinstance(obj, dict)
        job_id = from_union([from_str, from_none], obj.get("jobId"))
        type = from_union([TypeEnum, from_none], obj.get("type"))
        job_tag = from_union([from_str, from_none], obj.get("jobTag"))
        location = from_union([Location.from_dict, from_none], obj.get("location"))
        time = from_union([ActivityTime.from_dict, from_none], obj.get("time"))
        return Activity(job_id, type, job_tag, location, time)

    def to_dict(self) -> dict:
        result: dict = {}
        result["jobId"] = from_union([from_str, from_none], self.job_id)
        result["type"] = from_union([lambda x: to_enum(TypeEnum, x), from_none], self.type)
        result["jobTag"] = from_union([from_str, from_none], self.job_tag)
        result["location"] = from_union([lambda x: to_class(Location, x), from_none], self.location)
        result["time"] = from_union([lambda x: to_class(ActivityTime, x), from_none], self.time)
        return result


class StopTime:
    arrival: Optional[datetime]
    departure: Optional[datetime]

    def __init__(self, arrival: Optional[datetime], departure: Optional[datetime]) -> None:
        self.arrival = arrival
        self.departure = departure

    @staticmethod
    def from_dict(obj: Any) -> 'StopTime':
        assert isinstance(obj, dict)
        arrival = from_union([from_datetime, from_none], obj.get("arrival"))
        departure = from_union([from_datetime, from_none], obj.get("departure"))
        return StopTime(arrival, departure)

    def to_dict(self) -> dict:
        result: dict = {}
        result["arrival"] = from_union([lambda x: x.isoformat(), from_none], self.arrival)
        result["departure"] = from_union([lambda x: x.isoformat(), from_none], self.departure)
        return result


class Stop:
    location: Optional[Location]
    time: Optional[StopTime]
    load: Optional[List[int]]
    activities: Optional[List[Activity]]

    def __init__(self, location: Optional[Location], time: Optional[StopTime], load: Optional[List[int]], activities: Optional[List[Activity]]) -> None:
        self.location = location
        self.time = time
        self.load = load
        self.activities = activities

    @staticmethod
    def from_dict(obj: Any) -> 'Stop':
        assert isinstance(obj, dict)
        location = from_union([Location.from_dict, from_none], obj.get("location"))
        time = from_union([StopTime.from_dict, from_none], obj.get("time"))
        load = from_union([lambda x: from_list(from_int, x), from_none], obj.get("load"))
        activities = from_union([lambda x: from_list(Activity.from_dict, x), from_none], obj.get("activities"))
        return Stop(location, time, load, activities)

    def to_dict(self) -> dict:
        result: dict = {}
        result["location"] = from_union([lambda x: to_class(Location, x), from_none], self.location)
        result["time"] = from_union([lambda x: to_class(StopTime, x), from_none], self.time)
        result["load"] = from_union([lambda x: from_list(from_int, x), from_none], self.load)
        result["activities"] = from_union([lambda x: from_list(lambda x: to_class(Activity, x), x), from_none], self.activities)
        return result


class TypeID(Enum):
    ISUZU = "isuzu"
    MITSUBISHI = "mitsubishi"


class Tour:
    vehicle_id: Optional[str]
    type_id: Optional[TypeID]
    stops: Optional[List[Stop]]
    statistic: Optional[Statistic]

    def __init__(self, vehicle_id: Optional[str], type_id: Optional[TypeID], stops: Optional[List[Stop]], statistic: Optional[Statistic]) -> None:
        self.vehicle_id = vehicle_id
        self.type_id = type_id
        self.stops = stops
        self.statistic = statistic

    @staticmethod
    def from_dict(obj: Any) -> 'Tour':
        assert isinstance(obj, dict)
        vehicle_id = from_union([from_str, from_none], obj.get("vehicleId"))
        type_id = from_union([TypeID, from_none], obj.get("typeId"))
        stops = from_union([lambda x: from_list(Stop.from_dict, x), from_none], obj.get("stops"))
        statistic = from_union([Statistic.from_dict, from_none], obj.get("statistic"))
        return Tour(vehicle_id, type_id, stops, statistic)

    def to_dict(self) -> dict:
        result: dict = {}
        result["vehicleId"] = from_union([from_str, from_none], self.vehicle_id)
        result["typeId"] = from_union([lambda x: to_enum(TypeID, x), from_none], self.type_id)
        result["stops"] = from_union([lambda x: from_list(lambda x: to_class(Stop, x), x), from_none], self.stops)
        result["statistic"] = from_union([lambda x: to_class(Statistic, x), from_none], self.statistic)
        return result


class Code(Enum):
    MAX_DISTANCE_CONSTRAINT = "MAX_DISTANCE_CONSTRAINT"
    REACHABLE_CONSTRAINT = "REACHABLE_CONSTRAINT"
    SHIFT_TIME_CONSTRAINT = "SHIFT_TIME_CONSTRAINT"


class Description(Enum):
    CANNOT_BE_ASSIGNED_DUE_TO_MAX_DISTANCE_CONSTRAINT_OF_VEHICLE = "cannot be assigned due to max distance constraint of vehicle"
    CANNOT_BE_ASSIGNED_DUE_TO_SHIFT_TIME_CONSTRAINT_OF_VEHICLE = "cannot be assigned due to shift time constraint of vehicle"
    LOCATION_UNREACHABLE = "location unreachable"


class Reason:
    code: Optional[Code]
    description: Optional[Description]

    def __init__(self, code: Optional[Code], description: Optional[Description]) -> None:
        self.code = code
        self.description = description

    @staticmethod
    def from_dict(obj: Any) -> 'Reason':
        assert isinstance(obj, dict)
        code = from_union([Code, from_none], obj.get("code"))
        description = from_union([Description, from_none], obj.get("description"))
        return Reason(code, description)

    def to_dict(self) -> dict:
        result: dict = {}
        result["code"] = from_union([lambda x: to_enum(Code, x), from_none], self.code)
        result["description"] = from_union([lambda x: to_enum(Description, x), from_none], self.description)
        return result


class Unassigned:
    job_id: Optional[str]
    reasons: Optional[List[Reason]]

    def __init__(self, job_id: Optional[str], reasons: Optional[List[Reason]]) -> None:
        self.job_id = job_id
        self.reasons = reasons

    @staticmethod
    def from_dict(obj: Any) -> 'Unassigned':
        assert isinstance(obj, dict)
        job_id = from_union([from_str, from_none], obj.get("jobId"))
        reasons = from_union([lambda x: from_list(Reason.from_dict, x), from_none], obj.get("reasons"))
        return Unassigned(job_id, reasons)

    def to_dict(self) -> dict:
        result: dict = {}
        result["jobId"] = from_union([from_str, from_none], self.job_id)
        result["reasons"] = from_union([lambda x: from_list(lambda x: to_class(Reason, x), x), from_none], self.reasons)
        return result


class Solution:
    statistic: Optional[Statistic]
    problem_id: Optional[UUID]
    tours: Optional[List[Tour]]
    unassigned: Optional[List[Unassigned]]

    def __init__(self, statistic: Optional[Statistic], problem_id: Optional[UUID], tours: Optional[List[Tour]], unassigned: Optional[List[Unassigned]]) -> None:
        self.statistic = statistic
        self.problem_id = problem_id
        self.tours = tours
        self.unassigned = unassigned

    @staticmethod
    def from_dict(obj: Any) -> 'Solution':
        assert isinstance(obj, dict)
        statistic = from_union([Statistic.from_dict, from_none], obj.get("statistic"))
        problem_id = from_union([lambda x: UUID(x), from_none], obj.get("problemId"))
        tours = from_union([lambda x: from_list(Tour.from_dict, x), from_none], obj.get("tours"))
        unassigned = from_union([lambda x: from_list(Unassigned.from_dict, x), from_none], obj.get("unassigned"))
        return Solution(statistic, problem_id, tours, unassigned)

    def to_dict(self) -> dict:
        result: dict = {}
        result["statistic"] = from_union([lambda x: to_class(Statistic, x), from_none], self.statistic)
        result["problemId"] = from_union([lambda x: str(x), from_none], self.problem_id)
        result["tours"] = from_union([lambda x: from_list(lambda x: to_class(Tour, x), x), from_none], self.tours)
        result["unassigned"] = from_union([lambda x: from_list(lambda x: to_class(Unassigned, x), x), from_none], self.unassigned)
        return result


def solution_from_dict(s: Any) -> Solution:
    return Solution.from_dict(s)


def solution_to_dict(x: Solution) -> Any:
    return to_class(Solution, x)


