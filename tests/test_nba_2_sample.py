import unittest
import pandas as pd
from nba_2_sample.data_cleaning import clean_data, generate_vorp, generate_net, subsetplayer, subsetdates
from nba_2_sample.analysis import two_sample

class TestNBADataPipeline(unittest.TestCase):
    """
    Unit tests for the NBA data processing pipeline.
    """

    def setUp(self):
        """Set up sample data for testing."""
        self.raw_data = pd.DataFrame({
            'date_game': ['2024-10-01', '2024-10-02'],
            'mp': [1200, 900],
            'bpm': [3.0, -1.5],
            'ORtg': [110.0, 105.0],
            'DRtg': [108.0, 110.0],
        })

        self.cleaned_data = pd.DataFrame({
            'date_game': pd.to_datetime(['2024-10-01', '2024-10-02']),
            'mp': [20.0, 15.0],  # In minutes
            'bpm': [3.0, -1.5],
            'ORtg': [110.0, 105.0],
            'DRtg': [108.0, 110.0],
        })

        self.player_data = pd.DataFrame({
            'player': ['Player A', 'Player B'],
            'date': pd.to_datetime(['2024-10-01', '2024-10-02']),
            'mp': [30.0, 25.0],
            'bpm': [4.0, -2.0],
            'ORtg': [115.0, 100.0],
            'DRtg': [105.0, 110.0],
        })

    def test_clean_data(self):
        """Test the clean_data function."""
        cleaned_df = clean_data(self.raw_data)
        self.assertEqual(cleaned_df.shape[0], 2)
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(cleaned_df['date_game']))
        self.assertEqual(cleaned_df['mp'].iloc[0], 20.0)  # Converted seconds to minutes

    def test_generate_vorp(self):
        """Test the generate_vorp function."""
        vorp_df = generate_vorp(self.cleaned_data)
        self.assertIn('vorp', vorp_df.columns)
        self.assertAlmostEqual(vorp_df['vorp'].iloc[0], 0.0156, places=4)  # Calculated VORP

    def test_generate_net(self):
        """Test the generate_net function."""
        net_df = generate_net(self.cleaned_data)
        self.assertIn('net', net_df.columns)
        self.assertEqual(net_df['net'].iloc[0], 2.0)  # ORtg - DRtg

    def test_subsetplayer(self):
        """Test the subsetplayer function."""
        subset = subsetplayer(self.player_data, 'Player A')
        self.assertEqual(subset.shape[0], 1)
        self.assertEqual(subset['player'].iloc[0], 'Player A')

    def test_subsetdates(self):
        """Test the subsetdates function."""
        subset = subsetdates(self.player_data, '2024-10-01', '2024-10-01')
        self.assertEqual(subset.shape[0], 1)
        self.assertEqual(subset['date'].iloc[0], pd.Timestamp('2024-10-01'))

    def test_two_sample(self):
        """Test the two_sample function."""
        df1 = self.player_data[self.player_data['player'] == 'Player A']
        df2 = self.player_data[self.player_data['player'] == 'Player B']
        results = two_sample(df1, df2, 'bpm')

        self.assertIn('t-test', results)
        self.assertIn('ks-test', results)
        self.assertTrue(isinstance(results['t-test']['t-statistic'], float))
        self.assertTrue(isinstance(results['ks-test']['ks-statistic'], float))

if __name__ == '__main__':
    unittest.main()
