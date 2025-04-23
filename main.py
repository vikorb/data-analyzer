#!/usr/bin/env python
"""
Data Analyzer - Main Application

This script provides a command-line interface for analyzing and visualizing
data from CSV files using the components from the data_analyzer package.
"""

import os
import sys
import argparse
import pandas as pd
from datetime import datetime

# Import project modules
from src.data_loader import DataLoader
from src.analyzer import DataAnalyzer
from src.visualizer import DataVisualizer

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description='Data Analysis Tool')
    
    # Required arguments
    parser.add_argument('file', help='Path to the CSV file to analyze')
    
    # Analysis options
    analysis_group = parser.add_argument_group('Analysis Options')
    analysis_group.add_argument('--analysis', '-a', choices=[
        'summary', 'time-series', 'distribution', 'top-categories',
        'customer-segments', 'customer-metrics', 'correlation'
    ], default='summary', help='Type of analysis to perform (default: summary)')
    
    analysis_group.add_argument('--groupby', '-g', help='Column to group by for analysis')
    analysis_group.add_argument('--n-top', '-n', type=int, default=5,
                               help='Number of top items to show (default: 5)')
    analysis_group.add_argument('--frequency', '-f', default='M',
                               choices=['D', 'W', 'M', 'Q', 'Y'],
                               help='Frequency for time-series analysis (default: M)')
    analysis_group.add_argument('--start-date', help='Start date for filtering (YYYY-MM-DD)')
    analysis_group.add_argument('--end-date', help='End date for filtering (YYYY-MM-DD)')
    analysis_group.add_argument('--category', help='Filter by category')
    analysis_group.add_argument('--customer', help='Filter by customer ID')
    
    # Visualization options
    viz_group = parser.add_argument_group('Visualization Options')
    viz_group.add_argument('--plot', '-p', choices=[
        'bar', 'line', 'pie', 'heatmap', 'histogram', 'box', 'scatter'
    ], default='bar', help='Type of plot to create (default: bar)')
    
    viz_group.add_argument('--x-column', help='Column for X-axis in scatter plot')
    viz_group.add_argument('--y-column', help='Column for Y-axis in scatter plot')
    viz_group.add_argument('--title', help='Title for the plot')
    viz_group.add_argument('--xlabel', help='Label for X-axis')
    viz_group.add_argument('--ylabel', help='Label for Y-axis')
    viz_group.add_argument('--color', default='steelblue', help='Color for the plot')
    viz_group.add_argument('--horizontal', action='store_true', help='Create horizontal bar chart')
    viz_group.add_argument('--figsize', help='Figure size in inches (width,height)', default='10,6')
    
    # Output options
    output_group = parser.add_argument_group('Output Options')
    output_group.add_argument('--output', '-o', help='Directory to save output files')
    output_group.add_argument('--format', choices=['png', 'jpg', 'svg', 'pdf'],
                             default='png', help='Format for saving plots (default: png)')
    output_group.add_argument('--dpi', type=int, default=300, help='DPI for saving plots (default: 300)')
    output_group.add_argument('--no-display', action='store_true',
                             help='Do not display plots, only save them')
    
    return parser.parse_args()

def main():
    """Main function."""
    # Parse command-line arguments
    args = parse_args()
    
    # Create instances of the components
    loader = DataLoader()
    
    try:
        # Load the data
        print(f"Loading data from {args.file}...")
        data = loader.load_data(args.file)
        print(f"Loaded {len(data)} rows and {len(data.columns)} columns.")
        
        # Apply filters if specified
        if args.start_date or args.end_date:
            data = loader.filter_by_date_range(args.start_date, args.end_date)
            print(f"Filtered by date range: {len(data)} rows remaining.")
        
        if args.category:
            data = loader.filter_by_category(args.category)
            print(f"Filtered by category '{args.category}': {len(data)} rows remaining.")
        
        if args.customer:
            data = loader.filter_by_customer(args.customer)
            print(f"Filtered by customer '{args.customer}': {len(data)} rows remaining.")
        
        # Perform the analysis
        analyzer = DataAnalyzer(data)
        
        # Get the analysis results based on the specified type
        if args.analysis == 'summary':
            results = analyzer.get_summary_statistics(groupby=args.groupby)
            print("\nSummary Statistics:")
            print(results)
        
        elif args.analysis == 'time-series':
            results = analyzer.analyze_time_series(freq=args.frequency, groupby=args.groupby)
            print(f"\nTime Series Analysis (Frequency: {args.frequency}):")
            print(results)
        
        elif args.analysis == 'distribution':
            results = analyzer.get_spending_distribution(by=args.groupby or 'category')
            print(f"\nSpending Distribution by {args.groupby or 'category'}:")
            print(results)
        
        elif args.analysis == 'top-categories':
            results = analyzer.get_top_spending_categories(n=args.n_top)
            print(f"\nTop {args.n_top} Spending Categories:")
            print(results)
        
        elif args.analysis == 'customer-segments':
            results = analyzer.segment_customers()
            print("\nCustomer Segments:")
            print(results)
        
        elif args.analysis == 'customer-metrics':
            results = analyzer.calculate_customer_metrics()
            print("\nCustomer Metrics:")
            print(results)
        
        elif args.analysis == 'correlation':
            results = analyzer.get_category_correlation()
            print("\nCategory Correlation:")
            print(results)
        
        # Create visualization if analysis produced results
        if results is not None:
            # Parse figsize
            try:
                width, height = map(float, args.figsize.split(','))
                figsize = (width, height)
            except:
                figsize = (10, 6)
                print("Warning: Invalid figsize format. Using default (10,6).")
            
            # Create a visualizer
            visualizer = DataVisualizer(figsize=figsize)
            
            # Determine title if not specified
            title = args.title or f"{args.analysis.replace('-', ' ').title()} - {os.path.basename(args.file)}"
            
            # Set up save path if output is specified
            save_path = None
            if args.output:
                # Create output directory if it doesn't exist
                output_dir = visualizer.create_output_dir(args.output)
                
                # Generate a filename based on analysis type and current timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{args.analysis}_{timestamp}.{args.format}"
                save_path = os.path.join(output_dir, filename)
            
            # Create the visualization based on the specified plot type
            if args.plot == 'bar':
                # Determine x and y labels if not specified
                xlabel = args.xlabel or (args.groupby if args.groupby else 'Category')
                ylabel = args.ylabel or 'Amount'
                
                fig, ax = visualizer.bar_chart(
                    data=results,
                    title=title,
                    xlabel=xlabel,
                    ylabel=ylabel,
                    color=args.color,
                    save_path=save_path,
                    horizontal=args.horizontal
                )
                
                print(f"\nCreated bar chart{' and saved to ' + save_path if save_path else ''}.")
            
            elif args.plot == 'line':
                # Determine x and y labels if not specified
                xlabel = args.xlabel or 'Date'
                ylabel = args.ylabel or 'Amount'
                
                fig, ax = visualizer.line_chart(
                    data=results,
                    title=title,
                    xlabel=xlabel,
                    ylabel=ylabel,
                    color=args.color,
                    save_path=save_path
                )
                
                print(f"\nCreated line chart{' and saved to ' + save_path if save_path else ''}.")
            
            elif args.plot == 'pie':
                fig, ax = visualizer.pie_chart(
                    data=results,
                    title=title,
                    save_path=save_path
                )
                
                print(f"\nCreated pie chart{' and saved to ' + save_path if save_path else ''}.")
            
            elif args.plot == 'heatmap':
                fig, ax = visualizer.heatmap(
                    data=results,
                    title=title,
                    save_path=save_path
                )
                
                print(f"\nCreated heatmap{' and saved to ' + save_path if save_path else ''}.")
            
            elif args.plot == 'histogram':
                # Determine x and y labels if not specified
                xlabel = args.xlabel or 'Value'
                ylabel = args.ylabel or 'Frequency'
                
                # For histogram, we need a Series, not a DataFrame or Series with Index
                if isinstance(results, pd.DataFrame):
                    if args.x_column and args.x_column in results.columns:
                        data_to_plot = results[args.x_column]
                    else:
                        # Just use the first column
                        data_to_plot = results.iloc[:, 0]
                else:
                    data_to_plot = results
                
                fig, ax = visualizer.histogram(
                    data=data_to_plot,
                    title=title,
                    xlabel=xlabel,
                    ylabel=ylabel,
                    color=args.color,
                    save_path=save_path
                )
                
                print(f"\nCreated histogram{' and saved to ' + save_path if save_path else ''}.")
            
            elif args.plot == 'box':
                # Determine x and y labels if not specified
                xlabel = args.xlabel or 'Category'
                ylabel = args.ylabel or 'Value'
                
                fig, ax = visualizer.box_plot(
                    data=results,
                    title=title,
                    xlabel=xlabel,
                    ylabel=ylabel,
                    color=args.color,
                    save_path=save_path
                )
                
                print(f"\nCreated box plot{' and saved to ' + save_path if save_path else ''}.")
            
            elif args.plot == 'scatter':
                # For scatter plot, we need two Series for x and y
                if not args.x_column or not args.y_column:
                    if isinstance(results, pd.DataFrame) and len(results.columns) >= 2:
                        x_column = results.columns[0]
                        y_column = results.columns[1]
                    else:
                        print("Error: Scatter plot requires x_column and y_column arguments or a DataFrame with at least 2 columns.")
                        return
                else:
                    x_column = args.x_column
                    y_column = args.y_column
                
                # Make sure the columns exist
                if isinstance(results, pd.DataFrame):
                    if x_column not in results.columns or y_column not in results.columns:
                        print(f"Error: Columns '{x_column}' and/or '{y_column}' not found in results.")
                        return
                    
                    x_data = results[x_column]
                    y_data = results[y_column]
                else:
                    print("Error: Scatter plot requires a DataFrame.")
                    return
                
                # Determine x and y labels if not specified
                xlabel = args.xlabel or x_column
                ylabel = args.ylabel or y_column
                
                fig, ax = visualizer.scatter_plot(
                    x=x_data,
                    y=y_data,
                    title=title,
                    xlabel=xlabel,
                    ylabel=ylabel,
                    color=args.color,
                    save_path=save_path
                )
                
                print(f"\nCreated scatter plot{' and saved to ' + save_path if save_path else ''}.")
            
            # Display the plot if not suppressed
            if not args.no_display:
                import matplotlib.pyplot as plt
                plt.show()
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())