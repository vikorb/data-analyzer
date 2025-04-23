import unittest
import pandas as pd
import numpy as np
import os
import sys
from datetime import datetime

# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.analyzer import DataAnalyzer

class TestDataAnalyzer(unittest.TestCase):
    """Test cases for the DataAnalyzer class."""
    
    def setUp(self):
        """Set up test data."""
        # Create sample data
        self.test_data = pd.DataFrame({
            'date': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', 
                           '2023-01-05', '2023-01-06']),
            'category': ['groceries', 'electronics', 'groceries', 'clothing',
                        'electronics', 'groceries'],
            'amount': [100.50, 250.75, 75.25, 125.00, 300.00, 50.00],
            'customer_id': ['C001', 'C002', 'C001', 'C003', 'C001', 'C002']
        })
        
        # Create a DataAnalyzer instance
        self.analyzer = DataAnalyzer(self.test_data)
    
    def test_get_summary_statistics(self):
        """Test getting summary statistics."""
        # Get summary statistics for the entire dataset
        stats = self.analyzer.get_summary_statistics()
        
        # Check that basic statistics were computed correctly
        self.assertAlmostEqual(stats['mean'], 150.25, places=2)
        self.assertEqual(stats['count'], 6)
        
        # Get summary statistics grouped by category
        grouped_stats = self.analyzer.get_summary_statistics(groupby='category')
        
        # Check that grouping worked correctly
        self.assertEqual(len(grouped_stats), 3)  # 3 unique categories
        self.assertAlmostEqual(grouped_stats.loc['groceries', 'mean'], 75.25, places=2)
        self.assertAlmostEqual(grouped_stats.loc['electronics', 'mean'], 275.375, places=2)
    
    def test_analyze_time_series(self):
        """Test analyzing time series data."""
        # Analyze time series by day
        time_series = self.analyzer.analyze_time_series(freq='D')
        
        # Check that resampling worked correctly
        self.assertEqual(len(time_series), 6)  # 6 days in the data
        
        # Analyze time series by category
        time_series_by_category = self.analyzer.analyze_time_series(freq='D', groupby='category')
        
        # Check that grouping worked correctly
        self.assertEqual(time_series_by_category.shape, (6, 3))  # 6 days, 3 categories
    
    def test_get_spending_distribution(self):
        """Test getting spending distribution."""
        # Get spending distribution by category
        distribution = self.analyzer.get_spending_distribution(by='category')
        
        # Check that distribution was computed correctly
        self.assertEqual(len(distribution), 3)  # 3 unique categories
        self.assertAlmostEqual(distribution['electronics'], 550.75, places=2)
        self.assertAlmostEqual(distribution['groceries'], 225.75, places=2)
        self.assertAlmostEqual(distribution['clothing'], 125.00, places=2)
    
    def test_get_top_spending_categories(self):
        """Test getting top spending categories."""
        # Get top 2 spending categories
        top_categories = self.analyzer.get_top_spending_categories(n=2)
        
        # Check that top categories were identified correctly
        self.assertEqual(len(top_categories), 2)
        self.assertEqual(top_categories.index[0], 'electronics')
        self.assertEqual(top_categories.index[1], 'groceries')
    
    def test_segment_customers(self):
        """Test customer segmentation."""
        # Segment customers
        segments = self.analyzer.segment_customers(n_segments=2)
        
        # Check that segmentation worked correctly
        self.assertEqual(len(segments), 3)  # 3 unique customers
        
        # Check that the segments were created correctly
        self.assertEqual(len(segments['segment'].unique()), 2)  # 2 segments
    
    def test_calculate_customer_metrics(self):
        """Test calculating customer metrics."""
        # Calculate customer metrics
        metrics = self.analyzer.calculate_customer_metrics()
        
        # Check that metrics were calculated correctly
        self.assertEqual(len(metrics), 3)  # 3 unique customers
        
        # Check that the required metrics are present
        for metric in ['amount_count', 'amount_sum', 'amount_mean', 'days_active']:
            self.assertIn(metric, metrics.columns)
        
        # Check specific metrics for a customer
        c001_metrics = metrics.loc['C001']
        self.assertEqual(c001_metrics['amount_count'], 3)
        self.assertAlmostEqual(c001_metrics['amount_sum'], 475.75, places=2)
    
    def test_get_category_correlation(self):
        """Test getting category correlation."""
        # Get category correlation
        correlation = self.analyzer.get_category_correlation()
        
        # Check that correlation matrix was computed correctly
        self.assertEqual(correlation.shape, (3, 3))  # 3x3 matrix for 3 categories
        
        # Check that diagonal elements are 1.0 (perfect correlation with self)
        for category in correlation.index:
            self.assertEqual(correlation.loc[category, category], 1.0)
    
    def test_no_data(self):
        """Test that analysis methods raise ValueError when no data is available."""
        # Create an analyzer with no data
        empty_analyzer = DataAnalyzer()
        
        # Check that methods raise ValueError
        with self.assertRaises(ValueError):
            empty_analyzer.get_summary_statistics()
        
        with self.assertRaises(ValueError):
            empty_analyzer.analyze_time_series()
        
        with self.assertRaises(ValueError):
            empty_analyzer.get_spending_distribution()

if __name__ == '__main__':
    unittest.main()