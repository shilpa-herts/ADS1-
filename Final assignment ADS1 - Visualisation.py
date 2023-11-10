# Assignment-1: ADS1 Visualisation
"""
The code represents the data anlysis about the customers preferences during 
shopping using line plot, pie chart and bar chart.
@Author - A.Shilpa
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Obtain the data file.
Trends_shopping = pd.read_csv("shopping_trends.csv")
Trends_shopping.head()
print(Trends_shopping)


# Function to create a multiple line chart
def plot_multiple_line_chart(dataframe, x_column, y_column, group_by_column, 
                             colors, title, xlabel, ylabel):
    """
        This function creates a multiple line chart with the provided data.

        Parameters:
        - dataframe: The pandas DataFrame containing the data.
        - x_column: The column to be used for the x-axis.
        - y_column: The column to be used for the y-axis.
        - group_by_column: The column by which to group and create separate 
          lines.
        - colors: A list of colors for the lines.
        - Headline: The chart's name.
        - Season: The x-axis's label.
        - purschase amount is the y-axis label
        """
# Group the data by the 'group_by_column' and the 'x_column' and calculate the 
#  mean of the 'y_column'
    grouped_data = dataframe.groupby([group_by_column, x_column])[y_column].mean().unstack(group_by_column)
    
 
    # Plotting each group with a different color
    fig, ax = plt.subplots(figsize = (12, 6))
    for (name, series), color in zip(grouped_data.items(), colors):
        ax.plot(series.index, series.values, label = name, color = color)

    # Setting the title and labels
    ax.set_title(Headline)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    # Adding a legend
    ax.legend()

    # Show the plot
    # Rotate x-axis labels for better readability if needed
    # Adjust the plot to ensure everything fits without overlapping
    plt.xticks(rotation = 45) 
    plt.tight_layout() 
    plt.show()

# Define the parameters for the multiple line chart
colors = ['red', 'green', 'blue', 'cyan', 'magenta', 'yellow', 'black']
Headline = 'Average Purchase Amount by Season and Category'
xlabel = 'Season'
ylabel = 'Average Purchase Amount (USD)'


# Call the function with the shopping data
plot_multiple_line_chart(
    dataframe = Trends_shopping,
    x_column ='Season',
    y_column ='Purchase Amount (USD)',
    group_by_column ='Category',
    colors = colors,
    title = Headline,
    xlabel = xlabel,
    ylabel = ylabel
)


# Function to Display a pie chart
def plot_pie_chart(dataframe, column, color_map, title):
    """
    This function creates a pie chart with the provided data.

    Parameters:
    - dataframe: The pandas DataFrame containing the data.
    - column: The column for which the pie chart is to be plotted.
    - color_map: A dictionary mapping unique values of the column to specific 
       colors.
    - title: The title of the chart.
    """

    # Count the unique values in the column
    value_counts = dataframe[column].value_counts()

    # Assign colors based on the unique values using the provided color_map
    pie_colors = [color_map.get(index, 'gray') for index in value_counts.index]

    # Creating the pie chart
    plt.figure(figsize = (8, 8))
    plt.pie(value_counts, labels = value_counts.index, colors = pie_colors, 
            autopct = '%1.1f%%', startangle = 140)

    # Setting the Headline
    plt.title(title)

    # Show the plot
    # Adjust the plot to ensure everything fits without overlapping
    plt.tight_layout() 
    plt.show()

# Define the parameters for the pie chart
# A color map for the payment methods
payment_methods = Trends_shopping['Payment Method'].unique()
color_map = {method: plt.cm.Paired(i/len(payment_methods)) for i, 
             method in enumerate(payment_methods)}  
title = 'Proportion of Purchases by Payment Method'

# Call the function with the shopping information
plot_pie_chart(
    dataframe = Trends_shopping,
    column = 'Payment Method',
    color_map = color_map,
    title = title
)


def plot_top_items(dataframe, item_column, amount_column, top_n = 10, 
                   colormap = 'viridis', title = '', xlabel = '', ylabel = '', 
                   show_mean_line = True):
    """
        This function creates a bar chart showing the top N items by total 
        purchase amount with various customizations.

        :parameter dataframe: Pandas DataFrame containing the data.
        :parameter item_column: String, the name of the column representing items.
        :parameter amount_column: String, the name of the column representing 
         purchase amounts.
        :parameter top_n: Integer, the number of top items to display  
         (default is 10).
        :parameter colormap: String, the name of the colormap for bar colors 
         (default is 'viridis').
        :parameter title: String, the Headline of the bar chart.
        :parameter xlabel: String, the label for the x-axis.
        :parameter ylabel: String, the label for the y-axis.
        :parameter show_mean_line: Boolean, whether to show a horizontal line at 
        the mean purchase amount (default is True).
        """
    # Calculate the total purchase amount for each item and get the top N items
    top_items = dataframe.groupby(item_column)[amount_column].sum().nlargest(top_n).reset_index()

    # Define colors for the bar chart
    top_items_colors = plt.cm.get_cmap(colormap)(np.linspace(0, 1, top_n))

    # Create a graph and axis objects for customization
    fig, ax = plt.subplots(figsize = (10, 6))

    # Displaying the bar chart for the top N items with variations
    bars = ax.bar(top_items[item_column], top_items[amount_column], 
                  color = top_items_colors, alpha = 0.7)

    # Adding data labels above the bars
    for bar, amount in zip(bars, top_items[amount_column]):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 50, 
                f'${amount:.2f}', ha = 'center', fontsize = 10, color = 'black')

    # Adding a horizontal line at the mean purchase amount for reference
    if show_mean_line:
        mean_purchase_amount = dataframe[amount_column].mean()
        ax.axhline(mean_purchase_amount, color = 'red', linestyle = '--', 
                   label = f'Mean Amount (${mean_purchase_amount:.2f})')

    # Setting the Headline and labels
    ax.set_title(title, fontsize = 14)
    ax.set_xlabel(xlabel, fontsize = 12)
    ax.set_ylabel(ylabel, fontsize = 12)

    # Rotate x-axis labels for better readability
    plt.xticks(rotation = 45, ha = 'right')

    # Adding a legend
    if show_mean_line:
        ax.legend()

    # Show the plot with tight layout
    plt.tight_layout()

    # Display the plot
    plt.show()
#  calling the function
plot_top_items(Trends_shopping, 'Item Purchased', 'Purchase Amount (USD)', 
               top_n = 5, colormap = 'viridis', 
               title = 'Top 10 Items by Total Purchase Amount', 
               xlabel = 'Item Purchased', 
               ylabel = 'Total Purchase Amount (USD)')
