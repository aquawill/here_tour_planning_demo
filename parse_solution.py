import folium
import flexpolyline
import requests
from folium.plugins import BeautifyIcon, AntPath
import solution_v3 as solution
import json
import random


def get_route(ori_lat, ori_lon, dest_lat, dest_lon, route_mode, departure_time):
    route_url = 'https://router.hereapi.com/v8/routes?'
    wp0 = ('{},{}'.format(ori_lat, ori_lon))
    wp1 = ('{},{}'.format(dest_lat, dest_lon))
    route_options = '&transportMode={}&departureTime={}&return=polyline'.format(route_mode, departure_time)
    url = route_url + 'apiKey=' + apikey + '&origin=' + wp0 + '&destination=' + wp1 + route_options
    json_result = json.loads(requests.get(url).text)
    routes = json_result['routes']
    route_shape = []
    decoded_polyline = flexpolyline.decode(routes[0]['sections'][0]['polyline'])
    return decoded_polyline


apikey = 'kVpNlN_Zq68gCvCKaZGJA8No9l-9nQfWKls02XySZus'  # your HERE location Services API Key

m = folium.Map(
    tiles='https://1.base.maps.ls.hereapi.com/maptile/2.1/maptile/newest/normal.day/{z}/{x}/{y}/256/png8?apiKey=' + apikey,
    location=[23, 121],
    max_zoom=20,
    attr='(c)2021 HERE'
)
folium.Marker([24.970504, 121.2516],
              icon=BeautifyIcon(icon='home', iconShape='marker', background_color='#000000', text_color='#FFFFFF'),
              popup='Home').add_to(m)

bounds = []

customer_dict = {}
unreachable_customer_names = []
solution = solution.solution_from_dict(j)
unassigned = solution.unassigned
unassigned_feature_group = folium.map.FeatureGroup(name='Unassigned', overlay=True, control=True, show=True)
icon_color = '#FF0000'
for destination_dict in destination_list:
    customer_dict[destination_dict['customer_id']] = destination_dict['name']
    if len(unassigned) > 0:
        for unassigned_destination in unassigned:
            job_id = unassigned_destination.job_id
            customer_name = ''
            if destination_dict['customer_id'] == job_id:
                customer_name = destination_dict['name']
                unreachable_customer_names.append(customer_name)
                folium.Marker([destination_dict['latitude'], destination_dict['longitude']],
                              icon=BeautifyIcon(icon='ban', iconShape='marker', background_color=icon_color,
                                                border_width=2), popup='{}/{}<br>{}'.format(job_id, customer_name,
                                                                                            unassigned_destination.reasons.__getitem__(
                                                                                                0).description)).add_to(
                    unassigned_feature_group)
unassigned_feature_group.add_to(m)
print("unreachable customers: ")
print(unreachable_customer_names)

tour_index = 0
tour_list = []
vehicle_list = []
while tour_index < len(solution.tours):
    icon_color = '#'
    i = 0
    while i < 6:
        icon_color += hex(random.randint(6, 16))[-1]
        i += 1
    tour = solution.tours.__getitem__(tour_index)
    vehicle_id = tour.vehicle_id
    vehicle_list.append(vehicle_id)
    statistic = tour.statistic
    print("\ncalculating routes for tour: {} / vehicle: {} / stops: {} / cost: {} / distance: {} / duration: {}".format(
        tour_index, vehicle_id, len(tour.stops), int(statistic.cost), statistic.distance, statistic.duration))
    feature_group = folium.map.FeatureGroup(name=vehicle_id, overlay=True, control=True, show=True)
    type_id = tour.type_id
    stops = tour.stops
    stop_index = 0
    stop_list = []
    trip_start_timestamp = 0
    trip_end_timestamp = 0
    movement_time = 0
    while stop_index < len(stops):
        stop = stops.__getitem__(stop_index)
        previous_stop = stops.__getitem__(stop_index - 1)
        stop_location = stop.location.to_dict()
        stop_time = stop.time
        stop_time_arrival = stop.time.arrival
        stop_time_departure = stop.time.departure
        stop_time_arrival_from_trip_start = 0
        stop_time_departure_from_trip_start = 0
        stop_activities = stop.activities

        if stop_index == 0:
            trip_start_timestamp = stop_time_departure
        else:
            stop_time_arrival_from_trip_start = stop_time_arrival - trip_start_timestamp
            stop_time_departure_from_trip_start = stop_time_departure - trip_start_timestamp
        print('\tstop_time_arrival_from_trip_start: {}'.format(stop_time_arrival_from_trip_start))
        print('\tstop_time_departure_from_trip_start: {}'.format(stop_time_departure_from_trip_start))
        if stop_index > 0:
            previous_stop = stops.__getitem__(stop_index - 1)
            movement_time = stop_time.arrival - previous_stop.time.departure
            movement_time.seconds
            print('\t~ movement time: {} ~'.format(movement_time))
        for stop_activity in stop_activities:
            job_id = stop_activity.job_id
            for destination_dict in destination_list:
                if destination_dict['customer_id'] == job_id:
                    stop_list.append({'stop_index': stop_index, 'job_id': job_id, 'destination': destination_dict})
                elif job_id == 'departure' or job_id == 'arrival' or job_id == 'break':
                    stop_list.append({'stop_index': stop_index, 'job_id': job_id,
                                      'destination': {'latitude': stop_location['lat'],
                                                      'longitude': stop_location['lng']}})
                    break
            customer_name = customer_dict.get(job_id)
            stop_load = stop.load
            if stop_index < len(stops) - 1:
                route_shape = get_route(stop_location['lat'], stop_location['lng'],
                                        stops.__getitem__(stop_index + 1).location.to_dict()['lat'],
                                        stops.__getitem__(stop_index + 1).location.to_dict()['lng'], 'truck',
                                        stop_time_departure.strftime('%Y-%m-%dT%H:%M:%SZ'))
                if stop_index > 0:
                    folium.Marker([stop_location['lat'], stop_location['lng']],
                                  icon=BeautifyIcon(icon='flag', iconShape='marker', background_color=icon_color,
                                                    border_width=2),
                                  popup='Vehicle ID: {}<br>Job ID: {}/{}<br>Arrival：{}<br>Departure：{}'.format(
                                      vehicle_id, job_id, customer_name, stop_time_arrival,
                                      stop_time_departure)).add_to(feature_group)
                shape_point_index = 0
                bounds.append([stop_location['lat'], stop_location['lng']])
                shape_point_list = []
                while shape_point_index < len(route_shape):
                    shape_point = route_shape[shape_point_index]
                    shape_point_list.append(shape_point)
                    shape_point_index += 1
                AntPath(shape_point_list, color=icon_color, weight=4, opacity=1).add_to(feature_group)
            print('{} --> {} / {} / {} / arr: {} dep: {} '.format(stop_index, job_id, customer_name,
                                                                  [stop_location['lat'], stop_location['lng']],
                                                                  stop_time.arrival, stop_time.departure))

        stop_index += 1
    statistic = tour.statistic
    tour_list.append({'vehicle_id': vehicle_id, 'stop_list': stop_list})
    feature_group.add_to(m)
    tour_index += 1