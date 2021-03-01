from unittest import TestCase
from unittest.mock import patch


import forestclub
import my_gmail


class ForestClubIntegrationTest(TestCase):
    def test_send_email_upon_change_new(self):
        """Tests if proper e-mail is sent when new apartments available"""

        stats = [
            ['Date', 'Flats total', 'Flats free', 'Flats sold'],
            ['2020-01-01', '74', '14', '60'],
            ['2020-01-02', '80', '20', '60'],
        ]
        with patch('forestclub.csv_file_to_list', return_value=stats):
            with patch('my_gmail.create_and_send_email') as mocked_email_send:
                sent = forestclub.send_email_upon_change('', '')  # arguments not important for this test
                # print(mocked_email_send.mock_calls)
                expected = '[ForestClub] New apartments available'

                assert expected in str(mocked_email_send.mock_calls)
                self.assertTrue(sent)

    def test_send_email_upon_change_sold(self):
        """Tests if proper e-mail is sent when apartment(s) sold"""

        stats = [
            ['Date', 'Flats total', 'Flats free', 'Flats sold'],
            ['2020-01-01', '74', '14', '60'],
            ['2020-01-02', '74', '13', '61'],
        ]
        with patch('forestclub.csv_file_to_list', return_value=stats):
            with patch('my_gmail.create_and_send_email') as mocked_email_send:
                sent = forestclub.send_email_upon_change('', '')  # arguments not important for this test
                # print(mocked_email_send.mock_calls)
                expected = '[ForestClub] Some apartment(s) sold'

                assert expected in str(mocked_email_send.mock_calls)
                self.assertTrue(sent)

    def test_send_email_upon_change_returned(self):
        """Tests if proper e-mail is sent when apartment(s) returned to the marked"""

        stats = [
            ['Date', 'Flats total', 'Flats free', 'Flats sold'],
            ['2020-01-01', '74', '14', '60'],
            ['2020-01-02', '74', '15', '59'],
        ]
        with patch('forestclub.csv_file_to_list', return_value=stats):
            with patch('my_gmail.create_and_send_email') as mocked_email_send:
                sent = forestclub.send_email_upon_change('', '')  # arguments not important for this test
                # print(mocked_email_send.mock_calls)
                expected = '[ForestClub] Some apartment(s) returned to the market'

                assert expected in str(mocked_email_send.mock_calls)
                self.assertTrue(sent)

    def test_send_email_upon_change_less(self):
        """Tests if proper e-mail is sent when total number of available apartments decreases"""

        stats = [
            ['Date', 'Flats total', 'Flats free', 'Flats sold'],
            ['2020-01-01', '74', '14', '60'],
            ['2020-01-02', '70', '10', '60'],
        ]
        with patch('forestclub.csv_file_to_list', return_value=stats):
            with patch('my_gmail.create_and_send_email') as mocked_email_send:
                sent = forestclub.send_email_upon_change('', '')  # arguments not important for this test
                # print(mocked_email_send.mock_calls)
                expected = '[ForestClub] Total number of apartments decreased'

                assert expected in str(mocked_email_send.mock_calls)
                self.assertTrue(sent)

    def test_send_email_upon_change_no_change(self):
        """Tests if no email is sent when no change in available apartments"""

        stats = [
            ['Date', 'Flats total', 'Flats free', 'Flats sold'],
            ['2020-01-01', '74', '14', '60'],
            ['2020-01-02', '74', '14', '60'],
        ]

        with patch('forestclub.csv_file_to_list', return_value=stats):
            sent = forestclub.send_email_upon_change('', '')  # arguments not important for this test

            self.assertFalse(sent)

    def test_send_email_upon_change_no_stats(self):
        """Tests if no email is sent when no previous stats available to compare with"""

        stats = [
            ['Date', 'Flats total', 'Flats free', 'Flats sold'],
            ['2020-01-01', '74', '14', '60'],
        ]

        with patch('forestclub.csv_file_to_list', return_value=stats):
            sent = forestclub.send_email_upon_change('', '')  # arguments not important for this test

            self.assertFalse(sent)
