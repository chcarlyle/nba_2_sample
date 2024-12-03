import unittest
import pandas as pd
from nba_2_sample.data_cleaning import clean_data
from nba_2_sample.analysis import calculate_margin

class TestNBADataScraper(unittest.TestCase):

    def test_clean_data(self):
        # Sample raw data for testing
        data = {
            'date_game': ['2024-10-01', '2024-10-02'],
            'vpts': ['100', '95'],
            'hpts': ['105', '90'],
        }
        df = pd.DataFrame(data)
        cleaned_df = clean_data(df)
        self.assertEqual(cleaned_df.shape[0], 2)

    def test_calculate_margin(self):
        data = {
            'hpts': [105, 90],
            'vpts': [100, 95],
        }
        df = pd.DataFrame(data)
        df_with_margin = calculate_margin(df)
        self.assertTrue('margin' in df_with_margin.columns)
        self.assertEqual(df_with_margin['margin'][0], 5)
        self.assertEqual(df_with_margin['margin'][1], -5)

if __name__ == '__main__':
    unittest.main()
