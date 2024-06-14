import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


class DataTransform:
    def __init__(self, data_frame):
        """
        The above function is an incomplete Python class constructor that initializes an instance
        variable with a DataFrame object.
        
        :param data_frame: The `__init__` method you provided is a constructor for a class that takes a
        `data_frame` parameter. The `data_frame` parameter is likely intended to be a DataFrame object,
        possibly from a library like Pandas in Python. This parameter is then assigned to an instance
        variable `self
        """
        self.data_frame = data_frame

    def convert_to_datetime(self, column):
        """
        The function `convert_to_datetime` converts a column in a DataFrame to datetime format using the
        pandas library in Python.
        
        :param column: The `column` parameter in the `convert_to_datetime` method is the name of the
        column in the DataFrame that you want to convert to datetime format. When you call this method,
        you pass the name of the column as an argument, and the method will convert the values in that
        column to datetime
        :return: The function `convert_to_datetime` returns the updated DataFrame after converting the
        specified column to datetime format using `pd.to_datetime`.
        """
        self.data_frame[column] = pd.to_datetime(self.data_frame[column])
        return self.data_frame

    def convert_to_numeric(self, column):
        """
        The function `convert_to_numeric` converts a specified column in a DataFrame to numeric values,
        handling errors by coercing them.
        
        :param column: The `column` parameter in the `convert_to_numeric` method refers to the column in
        the DataFrame that you want to convert to numeric data type. This method takes the column
        specified and converts its values to numeric type using the `pd.to_numeric` function from the
        pandas library. The `errors='
        :return: The `data_frame` with the specified column converted to numeric values is being
        returned.
        """
        self.data_frame[column] = pd.to_numeric(self.data_frame[column], errors='coerce')
        return self.data_frame

    def convert_to_categorical(self, column):
        """
        The function `convert_to_categorical` converts a specified column in a DataFrame to a
        categorical data type in Python.
        
        :param column: The `column` parameter in the `convert_to_categorical` method is the name of the
        column in the DataFrame that you want to convert to a categorical data type
        :return: The `data_frame` with the specified column converted to a categorical data type is
        being returned.
        """
        self.data_frame[column] = self.data_frame[column].astype('category')
        return self.data_frame

    def remove_symbols(self, column, symbols):
        """
        The function `remove_symbols` takes a DataFrame column and a list of symbols, and removes each
        symbol from the column's values.
        
        :param column: The `column` parameter in the `remove_symbols` method refers to the specific
        column in the DataFrame from which you want to remove symbols. This method is designed to remove
        specified symbols from the values in the specified column of the DataFrame
        :param symbols: The `symbols` parameter in the `remove_symbols` method is expected to be a list
        of symbols or characters that you want to remove from the specified column in the DataFrame.
        These symbols will be iterated over, and each symbol will be removed from the column's values
        using the `str.replace()`
        :return: The `data_frame` with the specified symbols removed from the specified column is being
        returned.
        """
        for symbol in symbols:
            self.data_frame[column] = self.data_frame[column].str.replace(symbol, '')
        return self.data_frame
    
    def identify_skewed_columns(self, skew_threshold=0.75):
        """
        The function `identify_skewed_columns` calculates the skewness of columns in a DataFrame and
        returns a list of columns that are skewed beyond a specified threshold.
        
        :param skew_threshold: The `skew_threshold` parameter is a value that is used to determine the
        threshold for identifying skewed columns in a dataset. Columns with skewness values greater than
        this threshold are considered to be skewed. The default value for `skew_threshold` is set to
        0.75 in the provided code
        :return: The function `identify_skewed_columns` returns a list of column names from the data
        frame that have skewness values greater than the specified threshold (default threshold is
        0.75).
        """
        numeric_columns = self.data_frame.select_dtypes(include=['number']).columns
        skewness = self.data_frame[numeric_columns].skew()
        skewed_columns = skewness[abs(skewness) > skew_threshold].index.tolist()
        return skewed_columns
    
    def transform_skewed_columns(self, columns=None):
        # This block of code is from the `transform_skewed_columns` method within the `DataTransform`
        # class. Let's break down what it does:
        if columns is None:
            columns = self.identify_skewed_columns()
        
        for col in columns:
            if col in self.data_frame.select_dtypes(include=['number']).columns:
                self.data_frame[col] = np.log1p(self.data_frame[col])
    
    def testing_import(self, message):
        return f"Message received: {message}"

  
class DataFrameInfo:
    def __init__(self, data_frame):
        self.data_frame = data_frame

    def describe_columns(self):
        """
        Describe all columns in the DataFrame to check their data types and summary statistics.
        """
        return self.data_frame.describe(include='all')

    def get_statistics(self):
        """
        Extract statistical values: median, standard deviation, and mean from the numeric columns.
        """
        stats = {
            'mean': self.data_frame.mean(),
            'median': self.data_frame.median(),
            'std_dev': self.data_frame.std()
        }
        return stats

    def count_distinct_values(self):
        """
        Count distinct values in categorical columns.
        """
        categorical_columns = self.data_frame.select_dtypes(include=['category', 'object']).columns
        distinct_counts = {col: self.data_frame[col].nunique() for col in categorical_columns}
        return distinct_counts

    def get_shape(self):
        """
        Print out the shape of the DataFrame.
        """
        return self.data_frame.shape

    def count_null_values(self):
        """
        Generate a count and percentage count of NULL values in each column.
        """
        null_counts = self.data_frame.isnull().sum()
        null_percentages = self.data_frame.isnull().mean() * 100
        return pd.DataFrame({'null_count': null_counts, 'null_percentage': null_percentages})

    def value_counts(self, column):
        """
        Get the value counts of a specific column.
        """
        return self.data_frame[column].value_counts()

    
class DataFrameTransform:
    def __init__(self, data_frame):
        self.data_frame = data_frame
        
    def check_null_values(self):
        """
        Check for NULL values in each column of the DataFrame.
        
        :return: Dictionary containing count of NULL values for each column.
        """
        return self.data_frame.isnull().sum().to_dict()
    
    def drop_columns(self, columns_to_drop):
        """
        Drop specified columns from the DataFrame.
        
        :param columns_to_drop: List of column names to be dropped.
        """
        self.data_frame.drop(columns_to_drop, axis=1, inplace=True)
        
    def impute_missing_values(self, strategy='median'):
        """
        Impute missing values in numeric columns using median or mean.
        
        :param strategy: Imputation strategy ('median' or 'mean').
        """
        numeric_columns = self.data_frame.select_dtypes(include=['number']).columns
        
        if strategy == 'median':
            impute_values = self.data_frame[numeric_columns].median()
        elif strategy == 'mean':
            impute_values = self.data_frame[numeric_columns].mean()
        else:
            raise ValueError("Unsupported imputation strategy. Use 'median' or 'mean'.")
        
        self.data_frame.fillna(impute_values, inplace=True)
    
    def check_null_values_after(self):
        """
        Check for NULL values in each column of the DataFrame after imputation.
        
        :return: Dictionary containing count of NULL values for each column after imputation.
        """
        return self.data_frame.isnull().sum().to_dict()
    
class Plotter:
    def __init__(self, data_frame):
        self.data_frame = data_frame
        
    def plot_null_values(self):
      
        # `null_counts_before = self.data_frame.isnull().sum()` is a line of code within the
        # `plot_null_values` method of the `Plotter` class. This line is calculating the count of NULL
        # values in each column of the DataFrame before any removal or processing is done.
        null_counts_before = self.data_frame.isnull().sum()
    
        
       # The line `null_counts_after = self.data_frame.isnull().sum()` is calculating the count of
       # NULL values in each column of the DataFrame after any removal or processing has been done.
       # This line is used within the `plot_null_values` method of the `Plotter` class to compare the
       # count of NULL values before and after any data manipulation.
        null_counts_after = self.data_frame.isnull().sum()
        
       
        # The line `fig, ax = plt.subplots(figsize=(10, 6))` is creating a new figure and a set of
        # subplots within that figure for plotting. Here's a breakdown of what each part does:
        fig, ax = plt.subplots(figsize=(10, 6))
      

       # The line `bar_width = 0.35` in the `Plotter` class is setting the width of the bars in a bar
       # plot that will be created later in the `plot_null_values` method.
        bar_width = 0.35
        
       
       # In the provided code snippet, the line `indices = range(len(null_counts_before))` is creating
       # a range of indices based on the length of the `null_counts_before` Series object.
        indices = range(len(null_counts_before))
        
       
        # The code snippet `rects1 = ax.bar(indices, null_counts_before, bar_width, label='Before
        # Removal')` and `rects2 = ax.bar([i + bar_width for i in indices], null_counts_after,
        # bar_width, label='After Removal')` in the `Plotter` class is creating two sets of bar plots
        # on the same figure to visually compare the count of NULL values before and after any removal
        # or processing has been done on the DataFrame.
        rects1 = ax.bar(indices, null_counts_before, bar_width, label='Before Removal')
        rects2 = ax.bar([i + bar_width for i in indices], null_counts_after, bar_width, label='After Removal')
        
       
        # In the provided code snippet, the lines `ax.set_xticks([i + bar_width / 2 for i in
        # indices])` and `ax.set_xticklabels(null_counts_before.index, rotation=45)` are setting the
        # positions and labels for the x-axis ticks on the plot created within the `Plotter` class.
        ax.set_xticks([i + bar_width / 2 for i in indices])
        ax.set_xticklabels(null_counts_before.index, rotation=45)
        
      
        # The above code is setting the x-axis label to "Columns", the y-axis label to "Count of NULL
        # Values", and the title of the plot to "Count of NULL Values Before and After Removal". This
        # code is likely part of a data visualization task where the goal is to display the count of
        # NULL values before and after removal in a plot.
        ax.set_xlabel('Columns')
        ax.set_ylabel('Count of NULL Values')
        ax.set_title('Count of NULL Values Before and After Removal')
        
       
        # The code is calling the `legend()` method on the `ax` object to display a legend on the
        # plot, and then it is enabling the grid on the plot by setting `grid` property to `True`
        # using the `grid()` method on the `ax` object.
        ax.legend()
        ax.grid(True)
        
        # The code is attempting to adjust the layout of the plot using `plt.tight_layout()` and then
        # display the plot using `plt.show()`. However, the code is not properly formatted as the
        # indentation is incorrect. The correct code should be:
        plt.tight_layout()
        plt.show()