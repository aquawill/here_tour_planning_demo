from dataclasses import dataclass
from typing import Optional, Any, List, TypeVar, Type, cast, Callable
from datetime import datetime
from enum import Enum
import dateutil.parser


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
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


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


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


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


@dataclass
class Notice:
    code: Optional[str] = None
    title: Optional[str] = None
    action: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Notice':
        assert isinstance(obj, dict)
        code = from_union([from_str, from_none], obj.get("code"))
        title = from_union([from_str, from_none], obj.get("title"))
        action = from_union([from_str, from_none], obj.get("action"))
        return Notice(code, title, action)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.code is not None:
            result["code"] = from_union([from_str, from_none], self.code)
        if self.title is not None:
            result["title"] = from_union([from_str, from_none], self.title)
        if self.action is not None:
            result["action"] = from_union([from_str, from_none], self.action)
        return result


@dataclass
class Times:
    driving: Optional[int] = None
    serving: Optional[int] = None
    waiting: Optional[int] = None
    stopping: Optional[int] = None
    times_break: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Times':
        assert isinstance(obj, dict)
        driving = from_union([from_int, from_none], obj.get("driving"))
        serving = from_union([from_int, from_none], obj.get("serving"))
        waiting = from_union([from_int, from_none], obj.get("waiting"))
        stopping = from_union([from_int, from_none], obj.get("stopping"))
        times_break = from_union([from_int, from_none], obj.get("break"))
        return Times(driving, serving, waiting, stopping, times_break)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.driving is not None:
            result["driving"] = from_union([from_int, from_none], self.driving)
        if self.serving is not None:
            result["serving"] = from_union([from_int, from_none], self.serving)
        if self.waiting is not None:
            result["waiting"] = from_union([from_int, from_none], self.waiting)
        if self.stopping is not None:
            result["stopping"] = from_union([from_int, from_none], self.stopping)
        if self.times_break is not None:
            result["break"] = from_union([from_int, from_none], self.times_break)
        return result


@dataclass
class Statistic:
    cost: Optional[float] = None
    distance: Optional[int] = None
    duration: Optional[int] = None
    times: Optional[Times] = None

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
        if self.cost is not None:
            result["cost"] = from_union([to_float, from_none], self.cost)
        if self.distance is not None:
            result["distance"] = from_union([from_int, from_none], self.distance)
        if self.duration is not None:
            result["duration"] = from_union([from_int, from_none], self.duration)
        if self.times is not None:
            result["times"] = from_union([lambda x: to_class(Times, x), from_none], self.times)
        return result


@dataclass
class Location:
    lat: Optional[float] = None
    lng: Optional[float] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Location':
        assert isinstance(obj, dict)
        lat = from_union([from_float, from_none], obj.get("lat"))
        lng = from_union([from_float, from_none], obj.get("lng"))
        return Location(lat, lng)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.lat is not None:
            result["lat"] = from_union([to_float, from_none], self.lat)
        if self.lng is not None:
            result["lng"] = from_union([to_float, from_none], self.lng)
        return result


@dataclass
class ActivityTime:
    start: Optional[datetime] = None
    end: Optional[datetime] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ActivityTime':
        assert isinstance(obj, dict)
        start = from_union([from_datetime, from_none], obj.get("start"))
        end = from_union([from_datetime, from_none], obj.get("end"))
        return ActivityTime(start, end)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.start is not None:
            result["start"] = from_union([lambda x: x.isoformat(), from_none], self.start)
        if self.end is not None:
            result["end"] = from_union([lambda x: x.isoformat(), from_none], self.end)
        return result


class TypeEnum(Enum):
    ARRIVAL = "arrival"
    BREAK = "break"
    DELIVERY = "delivery"
    DEPARTURE = "departure"


@dataclass
class Activity:
    job_id: Optional[str] = None
    type: Optional[TypeEnum] = None
    location: Optional[Location] = None
    time: Optional[ActivityTime] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Activity':
        assert isinstance(obj, dict)
        job_id = from_union([from_str, from_none], obj.get("jobId"))
        type = from_union([TypeEnum, from_none], obj.get("type"))
        location = from_union([Location.from_dict, from_none], obj.get("location"))
        time = from_union([ActivityTime.from_dict, from_none], obj.get("time"))
        return Activity(job_id, type, location, time)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.job_id is not None:
            result["jobId"] = from_union([from_str, from_none], self.job_id)
        if self.type is not None:
            result["type"] = from_union([lambda x: to_enum(TypeEnum, x), from_none], self.type)
        if self.location is not None:
            result["location"] = from_union([lambda x: to_class(Location, x), from_none], self.location)
        if self.time is not None:
            result["time"] = from_union([lambda x: to_class(ActivityTime, x), from_none], self.time)
        return result


@dataclass
class StopTime:
    arrival: Optional[datetime] = None
    departure: Optional[datetime] = None

    @staticmethod
    def from_dict(obj: Any) -> 'StopTime':
        assert isinstance(obj, dict)
        arrival = from_union([from_datetime, from_none], obj.get("arrival"))
        departure = from_union([from_datetime, from_none], obj.get("departure"))
        return StopTime(arrival, departure)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.arrival is not None:
            result["arrival"] = from_union([lambda x: x.isoformat(), from_none], self.arrival)
        if self.departure is not None:
            result["departure"] = from_union([lambda x: x.isoformat(), from_none], self.departure)
        return result


@dataclass
class Stop:
    time: Optional[StopTime] = None
    load: Optional[List[int]] = None
    activities: Optional[List[Activity]] = None
    location: Optional[Location] = None
    distance: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Stop':
        assert isinstance(obj, dict)
        time = from_union([StopTime.from_dict, from_none], obj.get("time"))
        load = from_union([lambda x: from_list(from_int, x), from_none], obj.get("load"))
        activities = from_union([lambda x: from_list(Activity.from_dict, x), from_none], obj.get("activities"))
        location = from_union([Location.from_dict, from_none], obj.get("location"))
        distance = from_union([from_int, from_none], obj.get("distance"))
        return Stop(time, load, activities, location, distance)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.time is not None:
            result["time"] = from_union([lambda x: to_class(StopTime, x), from_none], self.time)
        if self.load is not None:
            result["load"] = from_union([lambda x: from_list(from_int, x), from_none], self.load)
        if self.activities is not None:
            result["activities"] = from_union([lambda x: from_list(lambda x: to_class(Activity, x), x), from_none], self.activities)
        if self.location is not None:
            result["location"] = from_union([lambda x: to_class(Location, x), from_none], self.location)
        if self.distance is not None:
            result["distance"] = from_union([from_int, from_none], self.distance)
        return result


class TypeID(Enum):
    ISUZU = "isuzu"
    MITSUBISHI = "mitsubishi"


@dataclass
class Tour:
    vehicle_id: Optional[str] = None
    type_id: Optional[TypeID] = None
    stops: Optional[List[Stop]] = None
    statistic: Optional[Statistic] = None
    shift_index: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Tour':
        assert isinstance(obj, dict)
        vehicle_id = from_union([from_str, from_none], obj.get("vehicleId"))
        type_id = from_union([TypeID, from_none], obj.get("typeId"))
        stops = from_union([lambda x: from_list(Stop.from_dict, x), from_none], obj.get("stops"))
        statistic = from_union([Statistic.from_dict, from_none], obj.get("statistic"))
        shift_index = from_union([from_int, from_none], obj.get("shiftIndex"))
        return Tour(vehicle_id, type_id, stops, statistic, shift_index)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.vehicle_id is not None:
            result["vehicleId"] = from_union([from_str, from_none], self.vehicle_id)
        if self.type_id is not None:
            result["typeId"] = from_union([lambda x: to_enum(TypeID, x), from_none], self.type_id)
        if self.stops is not None:
            result["stops"] = from_union([lambda x: from_list(lambda x: to_class(Stop, x), x), from_none], self.stops)
        if self.statistic is not None:
            result["statistic"] = from_union([lambda x: to_class(Statistic, x), from_none], self.statistic)
        if self.shift_index is not None:
            result["shiftIndex"] = from_union([from_int, from_none], self.shift_index)
        return result


class Code(Enum):
    REACHABLE_CONSTRAINT = "REACHABLE_CONSTRAINT"
    TIME_WINDOW_CONSTRAINT = "TIME_WINDOW_CONSTRAINT"


class Description(Enum):
    CANNOT_BE_ASSIGNED_DUE_TO_VIOLATION_OF_TIME_WINDOW = "cannot be assigned due to violation of time window"
    LOCATION_UNREACHABLE = "location unreachable"


@dataclass
class Reason:
    code: Optional[Code] = None
    description: Optional[Description] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Reason':
        assert isinstance(obj, dict)
        code = from_union([Code, from_none], obj.get("code"))
        description = from_union([Description, from_none], obj.get("description"))
        return Reason(code, description)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.code is not None:
            result["code"] = from_union([lambda x: to_enum(Code, x), from_none], self.code)
        if self.description is not None:
            result["description"] = from_union([lambda x: to_enum(Description, x), from_none], self.description)
        return result


@dataclass
class Unassigned:
    job_id: Optional[str] = None
    reasons: Optional[List[Reason]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Unassigned':
        assert isinstance(obj, dict)
        job_id = from_union([from_str, from_none], obj.get("jobId"))
        reasons = from_union([lambda x: from_list(Reason.from_dict, x), from_none], obj.get("reasons"))
        return Unassigned(job_id, reasons)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.job_id is not None:
            result["jobId"] = from_union([from_str, from_none], self.job_id)
        if self.reasons is not None:
            result["reasons"] = from_union([lambda x: from_list(lambda x: to_class(Reason, x), x), from_none], self.reasons)
        return result


@dataclass
class Solution:
    statistic: Optional[Statistic] = None
    tours: Optional[List[Tour]] = None
    unassigned: Optional[List[Unassigned]] = None
    notices: Optional[List[Notice]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Solution':
        assert isinstance(obj, dict)
        statistic = from_union([Statistic.from_dict, from_none], obj.get("statistic"))
        tours = from_union([lambda x: from_list(Tour.from_dict, x), from_none], obj.get("tours"))
        unassigned = from_union([lambda x: from_list(Unassigned.from_dict, x), from_none], obj.get("unassigned"))
        notices = from_union([lambda x: from_list(Notice.from_dict, x), from_none], obj.get("notices"))
        return Solution(statistic, tours, unassigned, notices)

    def to_dict(self) -> dict:
        result: dict = {}
        if self.statistic is not None:
            result["statistic"] = from_union([lambda x: to_class(Statistic, x), from_none], self.statistic)
        if self.tours is not None:
            result["tours"] = from_union([lambda x: from_list(lambda x: to_class(Tour, x), x), from_none], self.tours)
        if self.unassigned is not None:
            result["unassigned"] = from_union([lambda x: from_list(lambda x: to_class(Unassigned, x), x), from_none], self.unassigned)
        if self.notices is not None:
            result["notices"] = from_union([lambda x: from_list(lambda x: to_class(Notice, x), x), from_none], self.notices)
        return result


def solution_from_dict(s: Any) -> Solution:
    return Solution.from_dict(s)


def solution_to_dict(x: Solution) -> Any:
    return to_class(Solution, x)
