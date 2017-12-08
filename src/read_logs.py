import argparse
from logparser.core import parse_row, group_logs_by_route_lenght, calculate_route_response_time_statistics, get_longest_route_length


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', help='log file path', required=True)
    parser.add_argument('--action', choices=['routes_by_category', 'statistics', 'longest_route'])
    args = vars(parser.parse_args())
    file_path = args['file']
    action = args['action']
    if action == "routes_by_category":
        routes_by_group = group_logs_by_route_lenght(file_path)
        display_dict(routes_by_group)
    if action == 'statistics':
        statistics = calculate_route_response_time_statistics(file_path, 'shortroute')
        display_dict(statistics)
    if action == 'longest_route':
        longest_route = get_longest_route_length(file_path)
        print(f'longest route: {longest_route}' )

def display_dict(dictionary):
    for key in dictionary:
        print(f'{key}: {dictionary[key]}')
       

if __name__ == '__main__':
    main()
