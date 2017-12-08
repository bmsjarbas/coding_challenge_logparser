
import unittest
import os
import datetime
from logparser.core import parse_row, group_logs_by_route_lenght, calculate_route_response_time_statistics, get_longest_route_length


class TestLogParser(unittest.TestCase):

    def setUp(self):
        short_row = "1464966058 \"GET http://fake_api_get_request HTTP/1.1\" 200 10 680 11"
        long_row = "1464966058 \"GET http://fake_api_get_request HTTP/1.1\" 200 20 681 100"
        verylong_row = "1464966058 \"GET http://fake_api_get_request HTTP/1.1\" 200 30 682 1000"
        other_row = "1464966058 \"GET http://fake_api_get_request HTTP/1.1\" 200 40 682 -"
        file_content = '\n'.join([short_row, long_row, verylong_row, other_row])
        file_name = 'test_logs.txt'
        with open(file_name, 'w') as file:
            file.write(file_content)
        self.__absolute_file_path = f'{os.getcwd()}/{file_name}' 

    def tearDown(self):
        os.remove(self.__absolute_file_path)

    def test_parse_row_return_dict(self):
        row = "1464966058 \"GET http://fake_api_get_request HTTP/1.1\" 200 7476 680 11"
        expectedTimeStamp = datetime.datetime.fromtimestamp(1464966058)

        output= parse_row(row)
        self.assertEqual(output['timestamp'], expectedTimeStamp)
        self.assertEqual(output['http_status'], 200)
        self.assertEqual(output['response_time'], 7476)
        self.assertEqual(output['response_size'], 680)
        self.assertEqual(output['route_length'], 11)
        self.assertEqual(output['route_category'], 'shortroute')

    def test_group_by_route_length(self):
        logs_output = group_logs_by_route_lenght(self.__absolute_file_path)
        self.assertEqual(logs_output["shortroute"], 1)
        self.assertEqual(logs_output["longroute"], 1)
        self.assertEqual(logs_output["verylongroute"], 1)
        self.assertEqual(logs_output["other"], 1)


    def test_calculate_statistics(self):
        routes = ["1464966058 \"GET http://fake_api_get_request HTTP/1.1\" 200 20 680 12",
         "1464966058 \"GET http://fake_api_get_request HTTP/1.1\" 200 10 680 13",
           "1464966058 \"GET http://fake_api_get_request HTTP/1.1\" 200 30 680 11"]

        with open(self.__absolute_file_path, 'a') as file:
            file.write("\n")
            file.write("\n".join(routes))
        statistics = calculate_route_response_time_statistics(self.__absolute_file_path, 'shortroute')
        self.assertEqual(statistics["response_time_average"], 0.0175)
        self.assertAlmostEqual(statistics["response_standard_deviation"], 0.00957427107753)
        self.assertEqual(statistics["response_time_percentile"], 0.03)

    def test_max_route_length(self):
        longest_route_length = get_longest_route_length(self.__absolute_file_path)
        self.assertEqual(longest_route_length, 1000)