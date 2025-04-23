import unittest
import pandas as pd
import numpy as np
import os
import sys
import matplotlib.pyplot as plt
import tempfile
from datetime import datetime

# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.visualizer import DataVisualizer

class TestDataVisualizer(unittest.TestCase):
    """Test cases for the DataVisualizer class."""
    
    def setUp(self):
        """Set up test data and visualizer."""
        # Create sample data
        self.test_series = pd.Series(
            [100, 200, 150, 300, 250],
            index=['A', 'B', 'C', 'D', 'E']
        )
        
        self.test_df = pd.DataFrame({
            'Category A': [100, 150, 200, 250, 300],
            'Category B': [150, 200, 250, 300, 350],
            'Category C': [200, 250, 300, 350, 400]
        }, index=pd.date_range('2023-01-01', periods=5, freq='D'))
        
        self.correlation_df = pd.DataFrame({
            'A': [1.0, 0.5, -0.3],
            'B': [0.5, 1.0, 0.2],
            'C': [-0.3, 0.2, 1.0]
        }, index=['A', 'B', 'C'])
        
        # Create a DataVisualizer instance
        self.visualizer = DataVisualizer()
        
        # Create a temporary directory for saving figures
        self.temp_dir = tempfile.TemporaryDirectory()
    
    def tearDown(self):
        """Clean up after tests."""
        # Close all figures to avoid memory leaks
        plt.close('all')
        
        # Clean up temporary directory
        self.temp_dir.cleanup()
    
    def test_bar_chart(self):
        """Test creating a bar chart."""
        # Create a bar chart
        fig, ax = self.visualizer.bar_chart(
            data=self.test_series,
            title='Test Bar Chart',
            xlabel='Categories',
            ylabel='Values'
        )
        
        # Check that the chart was created successfully
        self.assertIsNotNone(fig)
        self.assertIsNotNone(ax)
        self.assertEqual(ax.get_title(), 'Test Bar Chart')
        self.assertEqual(ax.get_xlabel(), 'Categories')
        self.assertEqual(ax.get_ylabel(), 'Values')
        
        # Check that the bars match the data
        self.assertEqual(len(ax.patches), len(self.test_series))
        
        # Test saving the figure
        save_path = os.path.join(self.temp_dir.name, 'bar_chart.png')
        fig, ax = self.visualizer.bar_chart(
            data=self.test_series,
            save_path=save_path
        )
        self.assertTrue(os.path.exists(save_path))
    
    def test_line_chart(self):
        """Test creating a line chart."""
        # Create a line chart
        fig, ax = self.visualizer.line_chart(
            data=self.test_df,
            title='Test Line Chart',
            xlabel='Date',
            ylabel='Values'
        )
        
        # Check that the chart was created successfully
        self.assertIsNotNone(fig)
        self.assertIsNotNone(ax)
        self.assertEqual(ax.get_title(), 'Test Line Chart')
        self.assertEqual(ax.get_xlabel(), 'Date')
        self.assertEqual(ax.get_ylabel(), 'Values')
        
        # Check that the lines match the data
        self.assertEqual(len(ax.lines), len(self.test_df.columns))
        
        # Test saving the figure
        save_path = os.path.join(self.temp_dir.name, 'line_chart.png')
        fig, ax = self.visualizer.line_chart(
            data=self.test_df,
            save_path=save_path
        )
        self.assertTrue(os.path.exists(save_path))
    
    def test_pie_chart(self):
        """Test creating a pie chart."""
        # Create a pie chart
        fig, ax = self.visualizer.pie_chart(
            data=self.test_series,
            title='Test Pie Chart'
        )
        
        # Check that the chart was created successfully
        self.assertIsNotNone(fig)
        self.assertIsNotNone(ax)
        self.assertEqual(ax.get_title(), 'Test Pie Chart')
        
        # Test saving the figure
        save_path = os.path.join(self.temp_dir.name, 'pie_chart.png')
        fig, ax = self.visualizer.pie_chart(
            data=self.test_series,
            save_path=save_path
        )
        self.assertTrue(os.path.exists(save_path))
    
    def test_heatmap(self):
        """Test creating a heatmap."""
        # Create a heatmap
        fig, ax = self.visualizer.heatmap(
            data=self.correlation_df,
            title='Test Heatmap'
        )
        
        # Check that the chart was created successfully
        self.assertIsNotNone(fig)
        self.assertIsNotNone(ax)
        self.assertEqual(ax.get_title(), 'Test Heatmap')
        
        # Test saving the figure
        save_path = os.path.join(self.temp_dir.name, 'heatmap.png')
        fig, ax = self.visualizer.heatmap(
            data=self.correlation_df,
            save_path=save_path
        )
        self.assertTrue(os.path.exists(save_path))
    
    def test_histogram(self):
        """Test creating a histogram."""
        # Create a histogram
        fig, ax = self.visualizer.histogram(
            data=self.test_df['Category A'],
            title='Test Histogram',
            xlabel='Values',
            ylabel='Frequency'
        )
        
        # Check that the chart was created successfully
        self.assertIsNotNone(fig)
        self.assertIsNotNone(ax)
        self.assertEqual(ax.get_title(), 'Test Histogram')
        self.assertEqual(ax.get_xlabel(), 'Values')
        self.assertEqual(ax.get_ylabel(), 'Frequency')
        
        # Test saving the figure
        save_path = os.path.join(self.temp_dir.name, 'histogram.png')
        fig, ax = self.visualizer.histogram(
            data=self.test_df['Category A'],
            save_path=save_path
        )
        self.assertTrue(os.path.exists(save_path))
    
    def test_box_plot(self):
        """Test creating a box plot."""
        # Create a box plot
        fig, ax = self.visualizer.box_plot(
            data=self.test_df,
            title='Test Box Plot',
            xlabel='Categories',
            ylabel='Values'
        )
        
        # Check that the chart was created successfully
        self.assertIsNotNone(fig)
        self.assertIsNotNone(ax)
        self.assertEqual(ax.get_title(), 'Test Box Plot')
        self.assertEqual(ax.get_xlabel(), 'Categories')
        self.assertEqual(ax.get_ylabel(), 'Values')
        
        # Test saving the figure
        save_path = os.path.join(self.temp_dir.name, 'box_plot.png')
        fig, ax = self.visualizer.box_plot(
            data=self.test_df,
            save_path=save_path
        )
        self.assertTrue(os.path.exists(save_path))
    
    def test_scatter_plot(self):
        """Test creating a scatter plot."""
        # Create a scatter plot
        fig, ax = self.visualizer.scatter_plot(
            x=self.test_df['Category A'],
            y=self.test_df['Category B'],
            title='Test Scatter Plot',
            xlabel='Category A',
            ylabel='Category B'
        )
        
        # Check that the chart was created successfully
        self.assertIsNotNone(fig)
        self.assertIsNotNone(ax)
        self.assertEqual(ax.get_title(), 'Test Scatter Plot')
        self.assertEqual(ax.get_xlabel(), 'Category A')
        self.assertEqual(ax.get_ylabel(), 'Category B')
        
        # Test saving the figure
        save_path = os.path.join(self.temp_dir.name, 'scatter_plot.png')
        fig, ax = self.visualizer.scatter_plot(
            x=self.test_df['Category A'],
            y=self.test_df['Category B'],
            save_path=save_path
        )
        self.assertTrue(os.path.exists(save_path))
    
    def test_create_output_dir(self):
        """Test creating output directory."""
        # Create output directory
        output_dir = os.path.join(self.temp_dir.name, 'output')
        created_dir = self.visualizer.create_output_dir(output_dir)
        
        # Check that the directory was created
        self.assertTrue(os.path.exists(created_dir))
        self.assertEqual(created_dir, output_dir)
        
        # Test creating an existing directory (should not raise an error)
        created_dir_again = self.visualizer.create_output_dir(output_dir)
        self.assertEqual(created_dir_again, output_dir)

if __name__ == '__main__':
    unittest.main()