import datetime
import os

from unittest import TestCase
from unittest.mock import patch, mock_open, call
from io import StringIO

from bs4 import BeautifulSoup

import forestclub


class ForestClubUnitTest(TestCase):
    def test_csv_file_to_list(self):
        """Tests if data is read from csv file and returned as a list of lists"""

        test_file = StringIO(
            'Date,Flats total,Flats free,Flats sold\n'
            '2020-01-01,74,14,60\n'
            '2020-01-02,74,13,61\n'
        )

        expected = [
            ['Date', 'Flats total', 'Flats free', 'Flats sold'],
            ['2020-01-01', '74', '14', '60'],
            ['2020-01-02', '74', '13', '61'],
        ]
        with patch('builtins.open', mock_open(read_data=test_file.read())) as mocked_file:
            data = forestclub.csv_file_to_list(mocked_file)

            self.assertListEqual(data, expected)

    def test_csv_to_apartments(self):
        """Tests if data is read from csv file and returned as a list of dicts (apartments)"""

        test_file = StringIO(
            'Apartment,Size,Rooms,Floor,Status,Link\n'
            'A.0.03,75.56,3,0,sold,https://www.forestclub.com.pl/wp-content/uploads/2019/04/A.0.03.pdf\n'
            'A.0.05,81.7,3,0,free,https://www.forestclub.com.pl/wp-content/uploads/2019/04/A.0.05.pdf\n'
        )

        expected = [
            {'Apartment': 'A.0.03', 'Size': '75.56', 'Rooms': '3', 'Floor': '0', 'Status': 'sold',
             'Link': 'https://www.forestclub.com.pl/wp-content/uploads/2019/04/A.0.03.pdf'},
            {'Apartment': 'A.0.05', 'Size': '81.7', 'Rooms': '3', 'Floor': '0', 'Status': 'free',
             'Link': 'https://www.forestclub.com.pl/wp-content/uploads/2019/04/A.0.05.pdf'},
        ]

        headers = ['Apartment', 'Size', 'Rooms', 'Floor', 'Status', 'Link']

        with patch('builtins.open', mock_open(read_data=test_file.read())) as mocked_file:
            apartments = forestclub.csv_to_apartments(mocked_file, headers)

            self.assertListEqual(apartments, expected)

    def test_stats_to_csv(self):
        """Tests if apartments stats are saved in the output file"""
        
        apartments = [
            {'Apartment': 'A.0.03', 'Size': '75.56', 'Rooms': '3', 'Floor': '0', 'Status': 'sold',
             'Link': 'https://www.forestclub.com.pl/wp-content/uploads/2019/04/A.0.03.pdf'},
            {'Apartment': 'A.0.05', 'Size': '81.7', 'Rooms': '3', 'Floor': '0', 'Status': 'free',
             'Link': 'https://www.forestclub.com.pl/wp-content/uploads/2019/04/A.0.05.pdf'},
        ]

        mock_op = mock_open()
        with patch('builtins.open', mock_op) as mocked_file:
            stat = os.stat_result(tuple(0 for _ in range(10)))
            with patch('os.stat', return_value=stat):
                forestclub.stats_to_csv(mocked_file, apartments)
                # print(mock_op.mock_calls)

                stats_date = datetime.date.today()
                expected_calls = [
                    call.write('Date,Flats total,Flats free,Flats sold\r\n'),
                    call.write(f'{stats_date},2,1,1\r\n'),
                ]

                mock_op().assert_has_calls(calls=expected_calls)

    def test_apartments_to_csv(self):
        """Tests if found apartments are saved in the output file"""

        apartments = [
            {'Apartment': 'A.0.03', 'Size': '75.56', 'Rooms': '3', 'Floor': '0', 'Status': 'sold',
             'Link': 'https://www.forestclub.com.pl/wp-content/uploads/2019/04/A.0.03.pdf'},
            {'Apartment': 'A.0.05', 'Size': '81.7', 'Rooms': '3', 'Floor': '0', 'Status': 'free',
             'Link': 'https://www.forestclub.com.pl/wp-content/uploads/2019/04/A.0.05.pdf'},
        ]
        headers = ['Apartment', 'Size', 'Rooms', 'Floor', 'Status', 'Link']

        mock_op = mock_open()
        with patch('builtins.open', mock_op) as mocked_file:
            forestclub.apartments_to_csv(mocked_file, apartments, headers)
            # print(mock_op.mock_calls)

            expected_calls = [
                call.write('Apartment,Size,Rooms,Floor,Status,Link\r\n'),
                call.write(
                    'A.0.03,75.56,3,0,sold,https://www.forestclub.com.pl/wp-content/uploads/2019/04/A.0.03.pdf\r\n'),
                call.write(
                    'A.0.05,81.7,3,0,free,https://www.forestclub.com.pl/wp-content/uploads/2019/04/A.0.05.pdf\r\n'),
            ]

            mock_op().assert_has_calls(calls=expected_calls)

    def test_compare_apartment_lists_1(self):
        """Tests if empty list is returned when old and new apartment lists are the same"""

        apart_old = [
            {'Apartment': 'A.0.03', 'Size': '75.56', 'Rooms': '3', 'Floor': '0', 'Status': 'sold',
             'Link': 'https://www.forestclub.com.pl/wp-content/uploads/2019/04/A.0.03.pdf'},
            {'Apartment': 'A.0.05', 'Size': '81.7', 'Rooms': '3', 'Floor': '0', 'Status': 'free',
             'Link': 'https://www.forestclub.com.pl/wp-content/uploads/2019/04/A.0.05.pdf'},
        ]

        apart_new = [
            {'Apartment': 'A.0.03', 'Size': '75.56', 'Rooms': '3', 'Floor': '0', 'Status': 'sold',
             'Link': 'https://www.forestclub.com.pl/wp-content/uploads/2019/04/A.0.03.pdf'},
            {'Apartment': 'A.0.05', 'Size': '81.7', 'Rooms': '3', 'Floor': '0', 'Status': 'free',
             'Link': 'https://www.forestclub.com.pl/wp-content/uploads/2019/04/A.0.05.pdf'},
        ]

        diff = forestclub.compare_apartment_lists(apart_old, apart_new)
        self.assertListEqual(diff, [])

    def test_compare_apartment_lists_2(self):
        """Tests if empty list is returned when there is no existing apartment list to compare with"""

        apart_old = []

        apart_new = [
            {'Apartment': 'A.0.03', 'Size': '75.56', 'Rooms': '3', 'Floor': '0', 'Status': 'sold',
             'Link': 'https://www.forestclub.com.pl/wp-content/uploads/2019/04/A.0.03.pdf'},
            {'Apartment': 'A.0.05', 'Size': '81.7', 'Rooms': '3', 'Floor': '0', 'Status': 'free',
             'Link': 'https://www.forestclub.com.pl/wp-content/uploads/2019/04/A.0.05.pdf'},
        ]

        diff = forestclub.compare_apartment_lists(apart_old, apart_new)
        self.assertListEqual(diff, [])

    def test_compare_apartment_lists_3(self):
        """Tests if list of differences is returned when old and new apartment lists are different and not empty"""

        apart_old = [
            {'Apartment': 'A.0.03', 'Size': '75.56', 'Rooms': '3', 'Floor': '0', 'Status': 'sold',
             'Link': 'https://www.forestclub.com.pl/wp-content/uploads/2019/04/A.0.03.pdf'},
            {'Apartment': 'A.0.05', 'Size': '81.7', 'Rooms': '3', 'Floor': '0', 'Status': 'free',
             'Link': 'https://www.forestclub.com.pl/wp-content/uploads/2019/04/A.0.05.pdf'},
        ]

        apart_new = [
            {'Apartment': 'A.0.03', 'Size': '75.56', 'Rooms': '3', 'Floor': '0', 'Status': 'sold',
             'Link': 'https://www.forestclub.com.pl/wp-content/uploads/2019/04/A.0.03.pdf'},
            {'Apartment': 'A.0.05', 'Size': '81.7', 'Rooms': '3', 'Floor': '0', 'Status': 'sold',
             'Link': 'https://www.forestclub.com.pl/wp-content/uploads/2019/04/A.0.05.pdf'},
        ]

        diff = forestclub.compare_apartment_lists(apart_old, apart_new)

        expected = [
            {'Apartment': 'A.0.05', 'Size': '81.7', 'Rooms': '3', 'Floor': '0', 'Status': 'sold',
             'Link': 'https://www.forestclub.com.pl/wp-content/uploads/2019/04/A.0.05.pdf'},
        ]

        self.assertListEqual(diff, expected)


    def test_find_apartments(self):
        """Tests if apartments are found on a given html page"""

        test_file = 'flats_test.html'
        cwd = os.getcwd()
        if cwd.endswith('tests'):
            test_file_path = cwd + '/unit/' + test_file
        elif cwd.endswith('unit'):
            test_file_path = cwd + '/' + test_file
        else:
            test_file_path = test_file

        with open(test_file_path) as html:
            soup = BeautifulSoup(html, 'html.parser')
        headers = ['Apartment', 'Size', 'Rooms', 'Floor', 'Status', 'Link']

        expected = [
            {'Apartment': 'A.0.03', 'Size': '75.56', 'Rooms': '3', 'Floor': '0', 'Status': 'sold',
             'Link': 'https://www.forestclub.com.pl/wp-content/uploads/2019/04/A.0.03.pdf'},
            {'Apartment': 'A.0.05', 'Size': '81.7', 'Rooms': '3', 'Floor': '0', 'Status': 'free',
             'Link': 'https://www.forestclub.com.pl/wp-content/uploads/2019/04/A.0.05.pdf'},
        ]

        apartments = forestclub.find_apartments(soup, headers)

        self.assertListEqual(apartments, expected)
