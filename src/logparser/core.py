import datetime
import statistics
import math
import functools
import re

def parse_row(row):
    httpHeader = re.findall(r'"([^"]*)"', row)
    row = re.sub(r'".*"'," ",row)
    splitted_output = row.replace(' ', " ").split()  
    dict_row = {}
    dict_row["timestamp"] = datetime.datetime.fromtimestamp(int(splitted_output[0])) if splitted_output[0] != "-" else splitted_output[0]
    
    dict_row["http_status"] = int(splitted_output[1]) if is_not_empty(splitted_output[1]) else splitted_output[1]
    dict_row['response_time'] = int(splitted_output[2]) if is_not_empty(splitted_output[2]) else splitted_output[2]
    dict_row["response_size"] =  int(splitted_output[3]) if is_not_empty(splitted_output[3]) else splitted_output[3]
    dict_row["route_length"] =  int(splitted_output[4]) if is_not_empty(splitted_output[4]) else splitted_output[4]
    dict_row["route_category"] = get_route_category(dict_row["route_length"])
    return dict_row

def group_logs_by_route_lenght(file_path):
    route_lenght_groups = {"shortroute": 0, "longroute":0, "verylongroute":0, "other": 0 }
    with open(file_path, 'r') as file:
        for row in file:
            log_item = parse_row(row)
            route_length = log_item["route_length"]
            if not isinstance(route_length, int):
                route_lenght_groups["other"] += 1
            elif route_length < 100:
                route_lenght_groups["shortroute"] += 1
            elif route_length >= 100 and route_length < 1000:
                route_lenght_groups["longroute"] += 1
            elif route_length >= 1000:
                route_lenght_groups["verylongroute"] += 1

    return route_lenght_groups

def get_route_category(route_length):
    if not isinstance(route_length, int):
        return "other"
    elif route_length < 100:
        return "shortroute"
    elif route_length >= 100 and route_length < 1000:
        return "longroute"
    elif route_length >= 1000:
        return "verylongroute"

def calculate_route_response_time_statistics(file_path, route_category):
    data_output = {}
    response_time_list = []
    with open(file_path, 'r') as file:
        for row in file:
            log_item = parse_row(row)
            if log_item["route_category"] == route_category:
                response_time = log_item["response_time"]                
                response_time_list.append(response_time)

    data_output["response_time_average"] = statistics.mean(response_time_list) /1000
    data_output["response_standard_deviation"] = statistics.stdev(response_time_list) / 1000
    data_output["response_time_percentile"] = percentile(response_time_list, 0.98) / 1000
    return data_output

def percentile(input_list, percent):
    input_list.sort()
    index = math.ceil(len(input_list) * percent) - 1
    sorted_list = input_list.sort()
    return input_list[index]

def get_longest_route_length(file_path):
    longest_path = 0
    with open(file_path, 'r') as file:
        for row in file:
            log_item = parse_row(row)
            route_length = log_item["route_length"]
            if isinstance(route_length, int) and route_length > longest_path:
                longest_path = route_length
    return longest_path

def is_not_empty(value):
    return value != "-"
