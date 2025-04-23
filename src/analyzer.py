import pandas as pd
import numpy as np
from datetime import datetime

class DataAnalyzer:
    """
    A class for analyzing data loaded from a CSV file.
    Provides methods for statistical analysis, time series analysis,
    and customer segmentation.
    """
    
    def __init__(self, data=None):
        """
        Initialize the DataAnalyzer with optional data.
        
        Args:
            data (pandas.DataFrame, optional): Data to analyze
        """
        self.data = data
    
    def set_data(self, data):
        """
        Set the data to analyze.
        
        Args:
            data (pandas.DataFrame): Data to analyze
        """
        self.data = data
    
    def _validate_data(self):
        """
        Validate that data is available for analysis.
        
        Raises:
            ValueError: If no data is available
        """
        if self.data is None or len(self.data) == 0:
            raise ValueError("No data available for analysis.")
    
    def get_summary_statistics(self, groupby=None):
        """
        Get summary statistics for the data.
        
        Args:
            groupby (str, optional): Column to group by (e.g., 'category')
            
        Returns:
            pandas.DataFrame: Summary statistics
        """
        self._validate_data()
        
        # If groupby is specified, group the data before computing statistics
        if groupby:
            if groupby not in self.data.columns:
                raise ValueError(f"Column '{groupby}' not found in data.")
                
            grouped = self.data.groupby(groupby)
            return grouped['amount'].agg(['count', 'mean', 'median', 'std', 'min', 'max', 'sum'])
        
        # Otherwise, compute statistics for the entire dataset
        return self.data['amount'].describe()
    
    def analyze_time_series(self, freq='M', groupby=None):
        """
        Analyze spending trends over time.
        
        Args:
            freq (str, optional): Frequency for resampling ('D', 'W', 'M', 'Q', 'Y')
            groupby (str, optional): Column to group by (e.g., 'category')
            
        Returns:
            pandas.DataFrame: Time series data resampled at the specified frequency
        """
        self._validate_data()
        
        # Convert to datetime if not already
        if not pd.api.types.is_datetime64_dtype(self.data['date']):
            self.data['date'] = pd.to_datetime(self.data['date'])
        
        # Set date as index for resampling
        data_with_date_index = self.data.set_index('date')
        
        # If groupby is specified, resample for each group
        if groupby:
            if groupby not in self.data.columns:
                raise ValueError(f"Column '{groupby}' not found in data.")
            
            # Group by the specified column and resample
            groups = []
            for name, group in data_with_date_index.groupby(groupby):
                # Resample and sum amounts
                resampled = group['amount'].resample(freq).sum()
                resampled.name = name
                groups.append(resampled)
            
            # Combine all groups into a single DataFrame
            if groups:
                return pd.concat(groups, axis=1)
            else:
                return pd.DataFrame()
        
        # Otherwise, resample the entire dataset
        return data_with_date_index['amount'].resample(freq).sum()
    
    def get_spending_distribution(self, by='category'):
        """
        Get spending distribution by the specified column.
        
        Args:
            by (str, optional): Column to group by (default: 'category')
            
        Returns:
            pandas.Series: Distribution of spending
        """
        self._validate_data()
        
        if by not in self.data.columns:
            raise ValueError(f"Column '{by}' not found in data.")
            
        return self.data.groupby(by)['amount'].sum().sort_values(ascending=False)
    
    def get_top_spending_categories(self, n=5):
        """
        Get the top N spending categories.
        
        Args:
            n (int, optional): Number of top categories to return
            
        Returns:
            pandas.Series: Top N spending categories
        """
        self._validate_data()
        
        return self.get_spending_distribution(by='category').head(n)
    
    def segment_customers(self, n_segments=3):
        """
        Segment customers based on spending patterns.
        
        Args:
            n_segments (int, optional): Number of segments to create
            
        Returns:
            pandas.DataFrame: Customer segmentation results
        """
        self._validate_data()
        
        # Get total spending by customer
        customer_spending = self.data.groupby('customer_id')['amount'].sum().reset_index()
        
        # Sort by spending and divide into segments
        customer_spending = customer_spending.sort_values('amount', ascending=False)
        
        # Create segment labels
        segment_size = len(customer_spending) // n_segments
        if segment_size == 0:  # Handle case with fewer customers than segments
            segment_size = 1
            n_segments = len(customer_spending)
        
        segments = []
        for i in range(n_segments):
            start_idx = i * segment_size
            end_idx = (i + 1) * segment_size if i < n_segments - 1 else len(customer_spending)
            segment_name = f"Segment {i + 1}"
            for idx in range(start_idx, end_idx):
                segments.append(segment_name)
        
        customer_spending['segment'] = segments
        
        return customer_spending
    
    def calculate_customer_metrics(self):
        """
        Calculate various metrics for each customer.
        
        Returns:
            pandas.DataFrame: Customer metrics
        """
        self._validate_data()
        
        # Group by customer_id
        customer_data = self.data.groupby('customer_id').agg({
            'amount': ['count', 'sum', 'mean', 'median', 'std'],
            'date': ['min', 'max']
        })
        
        # Flatten the column multi-index
        customer_data.columns = ['_'.join(col).strip() for col in customer_data.columns.values]
        
        # Calculate days between first and last purchase
        customer_data['days_active'] = (customer_data['date_max'] - customer_data['date_min']).dt.days
        
        # Calculate frequency (transactions per day active)
        # Avoid division by zero
        customer_data['frequency'] = np.where(
            customer_data['days_active'] > 0,
            customer_data['amount_count'] / customer_data['days_active'],
            customer_data['amount_count']
        )
        
        return customer_data
    
    def get_category_correlation(self):
        """
        Calculate correlation between spending in different categories.
        
        Returns:
            pandas.DataFrame: Correlation matrix
        """
        self._validate_data()
        
        # Pivot the data to get spending by category for each customer
        pivot_data = self.data.pivot_table(
            index='customer_id',
            columns='category',
            values='amount',
            aggfunc='sum',
            fill_value=0
        )
        
        # Calculate correlation
        return pivot_data.corr()