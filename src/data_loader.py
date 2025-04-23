import pandas as pd
from datetime import datetime

class DataLoader:
    """
    A class for loading, validating, and preprocessing CSV data for analysis.
    """
    
    def __init__(self, file_path=None, required_columns=None):
        """
        Initialize the DataLoader with optional file path and required columns.
        
        Args:
            file_path (str, optional): Path to the CSV file to load
            required_columns (list, optional): List of required column names
        """
        self.file_path = file_path
        self.data = None
        self.required_columns = required_columns or ['date', 'category', 'amount', 'customer_id']
        
        if file_path:
            self.load_data(file_path)
    
    def load_data(self, file_path):
        """
        Load data from a CSV file into a pandas DataFrame.
        
        Args:
            file_path (str): Path to the CSV file
            
        Returns:
            pandas.DataFrame: The loaded data
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If the data doesn't have the required columns
        """
        try:
            self.data = pd.read_csv(file_path)
            self.file_path = file_path
            self._validate_data()
            self._clean_data()
            return self.data
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")
    
    def _validate_data(self):
        """
        Validate that the data has the required columns.
        
        Raises:
            ValueError: If any required column is missing
        """
        missing_columns = [col for col in self.required_columns if col not in self.data.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        # Check for missing values in critical columns
        for col in self.required_columns:
            if self.data[col].isna().any():
                print(f"Warning: Missing values in column '{col}'. These will be handled during cleaning.")
    
    def _clean_data(self):
        """
        Perform basic data cleaning:
        - Parse dates
        - Convert amounts to numeric
        - Handle missing values
        """
        # Parse dates
        try:
            self.data['date'] = pd.to_datetime(self.data['date'])
        except Exception as e:
            print(f"Warning: Error parsing dates: {e}")
        
        # Convert amount to numeric, coercing errors to NaN
        self.data['amount'] = pd.to_numeric(self.data['amount'], errors='coerce')
        
        # Fill missing values
        # For numerical columns, fill with mean
        if 'amount' in self.data.columns:
            amount_mean = self.data['amount'].mean()
            self.data['amount'].fillna(amount_mean, inplace=True)
        
        # For categorical columns, fill with most frequent value
        if 'category' in self.data.columns:
            category_mode = self.data['category'].mode()[0]
            self.data['category'].fillna(category_mode, inplace=True)
        
        # For customer_id, fill with 'UNKNOWN'
        if 'customer_id' in self.data.columns:
            self.data['customer_id'].fillna('UNKNOWN', inplace=True)
    
    def filter_by_date_range(self, start_date=None, end_date=None):
        """
        Filter the data by a date range.
        
        Args:
            start_date (str or datetime, optional): Start date for filtering
            end_date (str or datetime, optional): End date for filtering
            
        Returns:
            pandas.DataFrame: Filtered data
        """
        if self.data is None:
            raise ValueError("No data loaded. Call load_data() first.")
        
        filtered_data = self.data.copy()
        
        if start_date:
            if isinstance(start_date, str):
                start_date = pd.to_datetime(start_date)
            filtered_data = filtered_data[filtered_data['date'] >= start_date]
            
        if end_date:
            if isinstance(end_date, str):
                end_date = pd.to_datetime(end_date)
            filtered_data = filtered_data[filtered_data['date'] <= end_date]
            
        return filtered_data
    
    def filter_by_category(self, categories):
        """
        Filter the data by categories.
        
        Args:
            categories (list or str): Category or list of categories to filter by
            
        Returns:
            pandas.DataFrame: Filtered data
        """
        if self.data is None:
            raise ValueError("No data loaded. Call load_data() first.")
        
        if isinstance(categories, str):
            categories = [categories]
            
        return self.data[self.data['category'].isin(categories)]
    
    def filter_by_customer(self, customer_ids):
        """
        Filter the data by customer IDs.
        
        Args:
            customer_ids (list or str): Customer ID or list of customer IDs to filter by
            
        Returns:
            pandas.DataFrame: Filtered data
        """
        if self.data is None:
            raise ValueError("No data loaded. Call load_data() first.")
        
        if isinstance(customer_ids, str):
            customer_ids = [customer_ids]
            
        return self.data[self.data['customer_id'].isin(customer_ids)]
    
    def get_unique_categories(self):
        """
        Get a list of unique categories in the data.
        
        Returns:
            list: Unique categories
        """
        if self.data is None:
            raise ValueError("No data loaded. Call load_data() first.")
            
        return self.data['category'].unique().tolist()
    
    def get_unique_customers(self):
        """
        Get a list of unique customer IDs in the data.
        
        Returns:
            list: Unique customer IDs
        """
        if self.data is None:
            raise ValueError("No data loaded. Call load_data() first.")
            
        return self.data['customer_id'].unique().tolist()
    
    def get_date_range(self):
        """
        Get the minimum and maximum dates in the data.
        
        Returns:
            tuple: (min_date, max_date)
        """
        if self.data is None:
            raise ValueError("No data loaded. Call load_data() first.")
            
        return (self.data['date'].min(), self.data['date'].max())