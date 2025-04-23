import unittest
import pandas as pd
import os
import sys
from datetime import datetime
import tempfile

# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.data_loader import DataLoader

class TestDataLoader(unittest.TestCase):
    """Test cases for the DataLoader class."""
    
    def setUp(self):
        """Set up test data."""
        # Create a temporary CSV file for testing
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_csv_path = os.path.join(self.temp_dir.name, 'test_data.csv')
        
        # Sample data
        self.test_data = pd.DataFrame({
            'date': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04'],
            'category': ['groceries', 'electronics', 'groceries', 'clothing'],
            'amount': [100.50, 250.75, 75.25, 125.00],
            'customer_id': ['C001', 'C002', 'C001', 'C003']
        })
        
        # Write to CSV
        self.test_data.to_csv(self.test_csv_path, index=False)
        
        # Create a DataLoader instance
        self.loader = DataLoader()
    
    def tearDown(self):
        """Clean up after tests."""
        self.temp_dir.cleanup()
    
    def test_load_data(self):
        """Test loading data from a CSV file."""
        # Load the test data
        data = self.loader.load_data(self.test_csv_path)
        
        # Check that the data was loaded correctly
        self.assertEqual(len(data), 4)
        self.assertEqual(list(data.columns), ['date', 'category', 'amount', 'customer_id'])
        
        # Check that data was parsed correctly
        self.assertIsInstance(data['date'][0], pd.Timestamp)
        self.assertIsInstance(data['amount'][0], float)
    
    def test_missing_file(self):
        """Test that loading a non-existent file raises an error."""
        with self.assertRaises(FileNotFoundError):
            self.loader.load_data('non_existent_file.csv')
    
    def test_validate_data_missing_columns(self):
        """Test validation of required columns."""
        # Create a CSV with missing columns
        incomplete_data = pd.DataFrame({
            'date': ['2023-01-01', '2023-01-02'],
            'amount': [100.50, 250.75]
        })
        
        incomplete_csv_path = os.path.join(self.temp_dir.name, 'incomplete_data.csv')
        incomplete_data.to_csv(incomplete_csv_path, index=False)
        
        # Create a DataLoader with specific required columns
        loader = DataLoader(required_columns=['date', 'category', 'amount'])
        
        # Loading should raise ValueError due to missing 'category' column
        with self.assertRaises(ValueError):
            loader.load_data(incomplete_csv_path)
    
    def test_filter_by_date_range(self):
        """Test filtering data by date range."""
        # Load the test data
        self.loader.load_data(self.test_csv_path)
        
        # Filter by date range
        filtered_data = self.loader.filter_by_date_range(
            start_date='2023-01-02',
            end_date='2023-01-03'
        )
        
        # Check that only data within the date range was returned
        self.assertEqual(len(filtered_data), 2)
        self.assertTrue(all(
            filtered_data['date'] >= pd.Timestamp('2023-01-02')
        ))
        self.assertTrue(all(
            filtered_data['date'] <= pd.Timestamp('2023-01-03')
        ))
    
    def test_filter_by_category(self):
        """Test filtering data by category."""
        # Load the test data
        self.loader.load_data(self.test_csv_path)
        
        # Filter by single category
        filtered_data = self.loader.filter_by_category('groceries')
        self.assertEqual(len(filtered_data), 2)
        self.assertTrue(all(filtered_data['category'] == 'groceries'))
        
        # Filter by multiple categories
        filtered_data = self.loader.filter_by_category(['groceries', 'clothing'])
        self.assertEqual(len(filtered_data), 3)
        self.assertTrue(all(filtered_data['category'].isin(['groceries', 'clothing'])))
    
    def test_filter_by_customer(self):
        """Test filtering data by customer ID."""
        # Load the test data
        self.loader.load_data(self.test_csv_path)
        
        # Filter by single customer
        filtered_data = self.loader.filter_by_customer('C001')
        self.assertEqual(len(filtered_data), 2)
        self.assertTrue(all(filtered_data['customer_id'] == 'C001'))
        
        # Filter by multiple customers
        filtered_data = self.loader.filter_by_customer(['C001', 'C002'])
        self.assertEqual(len(filtered_data), 3)
        self.assertTrue(all(filtered_data['customer_id'].isin(['C001', 'C002'])))
    
    def test_get_unique_categories(self):
        """Test getting unique categories."""
        # Load the test data
        self.loader.load_data(self.test_csv_path)
        
        # Get unique categories
        categories = self.loader.get_unique_categories()
        self.assertEqual(set(categories), {'groceries', 'electronics', 'clothing'})
    
    def test_get_unique_customers(self):
        """Test getting unique customer IDs."""
        # Load the test data
        self.loader.load_data(self.test_csv_path)
        
        # Get unique customer IDs
        customers = self.loader.get_unique_customers()
        self.assertEqual(set(customers), {'C001', 'C002', 'C003'})
    
    def test_get_date_range(self):
        """Test getting the date range."""
        # Load the test data
        self.loader.load_data(self.test_csv_path)
        
        # Get date range
        min_date, max_date = self.loader.get_date_range()
        self.assertEqual(min_date, pd.Timestamp('2023-01-01'))
        self.assertEqual(max_date, pd.Timestamp('2023-01-04'))

if __name__ == '__main__':
    unittest.main()