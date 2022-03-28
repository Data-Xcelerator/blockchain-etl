import csv
import random

from bcetl import transform
import unittest

class TestStringMethods(unittest.TestCase):

    def test_we_can_start(self):
        self.assertTrue(True)

    def test_data_is_loaded(self):
        file_path = 'tests/fixtures/transactions.csv'
        rslt = transform.calculate_address_balance(file_path)
        expected = _check_balance(file_path)
        random_address = random.choice(list(expected.keys()))
        random_token = random.choice(list(expected[random_address].keys()))
        res = int(rslt.loc[
            rslt['address'] == random_address
        ]['value'])
        self.assertEqual(expected[random_address][random_token], res)


class AutoDict(dict):
    '''Cleanest Way to create a nested dict on the fly'''
    def __missing__(self, k):
        self[k] = AutoDict()
        return self[k]

def _check_balance(file_path):
    address_dict = AutoDict()
    csvfile = open(file_path)
    reader = csv.DictReader(csvfile)
    for row in reader:
        if address_dict.get(row['from_address'], {}).get(row['token_address']) is None:
            address_dict[row['from_address']][row['token_address']] = int(row['value']) * -1
        else:
            address_dict[row['from_address']][row['token_address']] -= int(row['value'])
        if address_dict.get(row['to_address'], {}).get(row['token_address']) is None:
            address_dict[row['to_address']][row['token_address']] = int(row['value'])
        else:
            address_dict[row['to_address']][row['token_address']] += int(row['value'])
    return address_dict
