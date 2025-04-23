import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import datetime
import os

class DataVisualizer:
    """
    A class for visualizing data analysis results.
    Provides methods for creating various charts and visualizations.
    """
    
    def __init__(self, figsize=(10, 6), style='ggplot'):
        """
        Initialize the DataVisualizer with figure size and style.
        
        Args:
            figsize (tuple, optional): Figure size in inches (width, height)
            style (str, optional): Matplotlib style sheet name
        """
        self.figsize = figsize
        plt.style.use(style)
    
    def _setup_figure(self, figsize=None, title=None, xlabel=None, ylabel=None):
        """
        Set up a figure with common styling.
        
        Args:
            figsize (tuple, optional): Figure size in inches (width, height)
            title (str, optional): Figure title
            xlabel (str, optional): Label for x-axis
            ylabel (str, optional): Label for y-axis
            
        Returns:
            tuple: (fig, ax) - figure and axis objects
        """
        fig, ax = plt.subplots(figsize=figsize or self.figsize)
        
        if title:
            ax.set_title(title, fontsize=14, pad=20)
        
        if xlabel:
            ax.set_xlabel(xlabel, fontsize=12)
            
        if ylabel:
            ax.set_ylabel(ylabel, fontsize=12)
            
        return fig, ax
    
    def bar_chart(self, data, title=None, xlabel=None, ylabel='Amount', color='steelblue',
                  figsize=None, save_path=None, sort_values=True, horizontal=False):
        """
        Create a bar chart.
        
        Args:
            data (pandas.Series or pandas.DataFrame): Data to plot
            title (str, optional): Chart title
            xlabel (str, optional): Label for x-axis
            ylabel (str, optional): Label for y-axis
            color (str, optional): Bar color
            figsize (tuple, optional): Figure size in inches (width, height)
            save_path (str, optional): Path to save the figure
            sort_values (bool, optional): Whether to sort the data by values
            horizontal (bool, optional): Whether to create a horizontal bar chart
            
        Returns:
            tuple: (fig, ax) - figure and axis objects
        """
        # Sort the data if requested
        if sort_values and isinstance(data, pd.Series):
            data = data.sort_values(ascending=False)
        
        # Set up the figure
        fig, ax = self._setup_figure(figsize, title, xlabel, ylabel)
        
        # Create the bar chart
        if horizontal:
            if isinstance(data, pd.Series):
                data.plot.barh(ax=ax, color=color)
            else:
                data.plot.barh(ax=ax)
        else:
            if isinstance(data, pd.Series):
                data.plot.bar(ax=ax, color=color)
            else:
                data.plot.bar(ax=ax)
        
        # Add value labels
        if isinstance(data, pd.Series):
            for i, v in enumerate(data):
                text_color = 'black' if isinstance(color, str) and color.lower() in ['yellow', 'lightblue', 'lightgreen'] else 'white'
                if horizontal:
                    ax.text(v + (data.max() * 0.01), i, f'{v:.2f}', color=text_color, va='center')
                else:
                    ax.text(i, v + (data.max() * 0.01), f'{v:.2f}', ha='center', color=text_color)
        
        plt.tight_layout()
        
        # Save the figure if requested
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig, ax
    
    def line_chart(self, data, title=None, xlabel='Date', ylabel='Amount', color='steelblue',
                  figsize=None, save_path=None, marker='o', grid=True):
        """
        Create a line chart for time series data.
        
        Args:
            data (pandas.Series or pandas.DataFrame): Time series data to plot
            title (str, optional): Chart title
            xlabel (str, optional): Label for x-axis
            ylabel (str, optional): Label for y-axis
            color (str or list, optional): Line color(s)
            figsize (tuple, optional): Figure size in inches (width, height)
            save_path (str, optional): Path to save the figure
            marker (str, optional): Marker style
            grid (bool, optional): Whether to show grid lines
            
        Returns:
            tuple: (fig, ax) - figure and axis objects
        """
        # Set up the figure
        fig, ax = self._setup_figure(figsize, title, xlabel, ylabel)
        
        # Create the line chart
        if isinstance(data, pd.Series):
            data.plot(ax=ax, color=color, marker=marker)
        else:
            data.plot(ax=ax, marker=marker)
        
        # Add grid
        if grid:
            ax.grid(True, linestyle='--', alpha=0.7)
        
        # Add legend if multiple lines
        if isinstance(data, pd.DataFrame):
            ax.legend()
        
        plt.tight_layout()
        
        # Save the figure if requested
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig, ax
    
    def pie_chart(self, data, title=None, figsize=None, save_path=None, autopct='%1.1f%%',
                 startangle=90, shadow=False, explode=None):
        """
        Create a pie chart.
        
        Args:
            data (pandas.Series): Data to plot
            title (str, optional): Chart title
            figsize (tuple, optional): Figure size in inches (width, height)
            save_path (str, optional): Path to save the figure
            autopct (str, optional): Format for percentage labels
            startangle (int, optional): Starting angle for the pie chart
            shadow (bool, optional): Whether to add a shadow
            explode (list, optional): List of values to "explode" pie slices
            
        Returns:
            tuple: (fig, ax) - figure and axis objects
        """
        # Set up the figure
        fig, ax = self._setup_figure(figsize, title)
        
        # Create the pie chart
        wedges, texts, autotexts = ax.pie(
            data,
            labels=data.index,
            autopct=autopct,
            startangle=startangle,
            shadow=shadow,
            explode=explode
        )
        
        # Equal aspect ratio ensures the pie chart is circular
        ax.axis('equal')
        
        # Set font properties for percentage labels
        for autotext in autotexts:
            autotext.set_fontsize(10)
            autotext.set_color('white')
        
        plt.tight_layout()
        
        # Save the figure if requested
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig, ax
    
    def heatmap(self, data, title=None, figsize=None, save_path=None, cmap='coolwarm',
               annot=True, fmt='.2f', linewidths=0.5):
        """
        Create a heatmap.
        
        Args:
            data (pandas.DataFrame): Matrix data to plot
            title (str, optional): Chart title
            figsize (tuple, optional): Figure size in inches (width, height)
            save_path (str, optional): Path to save the figure
            cmap (str, optional): Colormap name
            annot (bool, optional): Whether to annotate cells
            fmt (str, optional): Format for annotations
            linewidths (float, optional): Width of lines between cells
            
        Returns:
            tuple: (fig, ax) - figure and axis objects
        """
        # Adjust figure size based on data dimensions
        adjusted_figsize = figsize or (max(8, len(data.columns) * 0.8), max(6, len(data.index) * 0.8))
        
        # Set up the figure
        fig, ax = self._setup_figure(adjusted_figsize, title)
        
        # Create the heatmap
        sns.heatmap(
            data,
            ax=ax,
            cmap=cmap,
            annot=annot,
            fmt=fmt,
            linewidths=linewidths
        )
        
        plt.tight_layout()
        
        # Save the figure if requested
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig, ax
    
    def histogram(self, data, bins=10, title=None, xlabel=None, ylabel='Frequency',
                 color='steelblue', figsize=None, save_path=None, kde=True):
        """
        Create a histogram.
        
        Args:
            data (pandas.Series): Data to plot
            bins (int, optional): Number of bins
            title (str, optional): Chart title
            xlabel (str, optional): Label for x-axis
            ylabel (str, optional): Label for y-axis
            color (str, optional): Histogram color
            figsize (tuple, optional): Figure size in inches (width, height)
            save_path (str, optional): Path to save the figure
            kde (bool, optional): Whether to show KDE
            
        Returns:
            tuple: (fig, ax) - figure and axis objects
        """
        # Set up the figure
        fig, ax = self._setup_figure(figsize, title, xlabel, ylabel)
        
        # Create the histogram
        sns.histplot(data, bins=bins, color=color, kde=kde, ax=ax)
        
        plt.tight_layout()
        
        # Save the figure if requested
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig, ax
    
    def box_plot(self, data, title=None, xlabel=None, ylabel=None, color='steelblue',
               figsize=None, save_path=None, vert=True):
        """
        Create a box plot.
        
        Args:
            data (pandas.Series or pandas.DataFrame): Data to plot
            title (str, optional): Chart title
            xlabel (str, optional): Label for x-axis
            ylabel (str, optional): Label for y-axis
            color (str, optional): Box color
            figsize (tuple, optional): Figure size in inches (width, height)
            save_path (str, optional): Path to save the figure
            vert (bool, optional): Whether to create a vertical box plot
            
        Returns:
            tuple: (fig, ax) - figure and axis objects
        """
        # Set up the figure
        fig, ax = self._setup_figure(figsize, title, xlabel, ylabel)
        
        # Create the box plot
        if isinstance(data, pd.Series):
            if vert:
                ax.boxplot(data, vert=vert, patch_artist=True,
                         boxprops=dict(facecolor=color, alpha=0.7))
            else:
                ax.boxplot(data, vert=vert, patch_artist=True,
                         boxprops=dict(facecolor=color, alpha=0.7))
        else:
            if vert:
                ax.boxplot([data[col].dropna() for col in data.columns], labels=data.columns,
                         vert=vert, patch_artist=True,
                         boxprops=dict(facecolor=color, alpha=0.7))
            else:
                ax.boxplot([data[col].dropna() for col in data.columns], labels=data.columns,
                         vert=vert, patch_artist=True,
                         boxprops=dict(facecolor=color, alpha=0.7))
        
        plt.tight_layout()
        
        # Save the figure if requested
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig, ax
    
    def scatter_plot(self, x, y, title=None, xlabel=None, ylabel=None, color='steelblue',
                   figsize=None, save_path=None, alpha=0.7, size=50):
        """
        Create a scatter plot.
        
        Args:
            x (pandas.Series): Data for x-axis
            y (pandas.Series): Data for y-axis
            title (str, optional): Chart title
            xlabel (str, optional): Label for x-axis
            ylabel (str, optional): Label for y-axis
            color (str, optional): Scatter color
            figsize (tuple, optional): Figure size in inches (width, height)
            save_path (str, optional): Path to save the figure
            alpha (float, optional): Opacity of points
            size (int, optional): Size of points
            
        Returns:
            tuple: (fig, ax) - figure and axis objects
        """
        # Set up the figure
        fig, ax = self._setup_figure(figsize, title, xlabel, ylabel)
        
        # Create the scatter plot
        ax.scatter(x, y, color=color, alpha=alpha, s=size)
        
        # Add grid
        ax.grid(True, linestyle='--', alpha=0.7)
        
        plt.tight_layout()
        
        # Save the figure if requested
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig, ax
    
    def create_output_dir(self, output_dir):
        """
        Create output directory if it doesn't exist.
        
        Args:
            output_dir (str): Path to output directory
            
        Returns:
            str: Path to output directory
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        return output_dir