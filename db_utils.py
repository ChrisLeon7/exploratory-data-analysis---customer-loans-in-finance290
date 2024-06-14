import yaml
import pandas as pd
from sqlalchemy import create_engine
import psycopg2 

"""
    The function `load_credentials` reads and loads credentials from a YAML file specified by the
    `yaml_file_path` parameter.
    
    :param yaml_file_path: The `yaml_file_path` parameter in the `load_credentials` function is the file
    path to the YAML file from which you want to load credentials. This function reads the YAML file and
    returns the credentials stored in it
    :return: The function `load_credentials` returns the credentials loaded from the YAML file located
    at the specified `yaml_file_path`.
    """
def load_credentials(yaml_file_path):
    with open(yaml_file_path, 'r') as file:
        credentials = yaml.safe_load(file)
    return {
        'username': credentials['RDS_USER'],
        'password': credentials['RDS_PASSWORD'],
        'host': credentials['RDS_HOST'],
        'port': credentials['RDS_PORT'],
        'database': credentials['RDS_DATABASE']
    }


class RDSDatabaseConnector:

    # The `RDSDatabaseConnector` class initializes a database connection object with credentials and
    # creates a database engine connection string in Python.


    def __init__(self, credentials):
        """
        The function initializes an object with credentials for a database connection.
        
        :param credentials: It looks like the `__init__` method of a class is being defined to initialize
        instance variables with values from a `credentials` dictionary. The `credentials` dictionary is
        expected to contain keys for 'username', 'password', 'host', 'port', and 'database'
        """
    
        self.username = credentials['username']
        self.password = credentials['password']
        self.host = credentials['host']
        self.port = credentials['port']
        self.database = credentials['database']

    def initialise_engine(self):
        """
        The `initialise_engine` function creates a connection string and initializes a database engine in
        Python.
        """
    
        connection_string = f'postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}'
        self.engine = create_engine(connection_string)

    def fetch_data(self, query):
        """
        The function fetches data from a SQL database using a specified query if the engine is
        initialized; otherwise, it raises a ValueError.
        
        :param query: The `query` parameter in the `fetch_data` method is a SQL query that will be
        executed to fetch data from a database using the `pd.read_sql_query` function. This query should
        be a valid SQL statement that retrieves the desired data from the database connected to the
        `self.engine` object
        :return: The function `fetch_data` is returning the result of executing the SQL query `query` on
        the database engine `self.engine` using the `pd.read_sql_query` function.
        """
      
        if self.engine is None:
            raise ValueError("Engine not initialized. Call 'initialize_engine' first.")
        return pd.read_sql_query(query, self.engine)

    def fetch_loan_payments(self):
        """
        This function fetches all loan payments from a database table named 'loan_payments'.
        :return: The `fetch_loan_payments` method is returning the result of fetching data from the
        `loan_payments` table in the database using the SQL query "SELECT * FROM loan_payments".
        """
       
        query = "SELECT * FROM loan_payments"
        return self.fetch_data(query)
    
    def save_data_to_csv(self, data_frame, file_path):
        """
        The function `save_data_to_csv` saves a pandas DataFrame to a CSV file without including the
        index.
        
        :param data_frame: The `data_frame` parameter is a pandas DataFrame that contains the data you
        want to save to a CSV file
        :param file_path: The `file_path` parameter in the `save_data_to_csv` function is the path where
        you want to save the CSV file. It should include the file name and extension (e.g., "data.csv")
        and the directory where you want to save the file
        """

        data_frame.to_csv(file_path, index=False)

    def load_data_from_csv(self, file_path):
        """
        Loads data from a CSV file into a Pandas DataFrame.

        :param file_path: Path to the CSV file to be loaded.
        :return: DataFrame containing the loaded data.
        """
        data_frame = pd.read_csv(file_path)
        print(data_frame.head())
        return data_frame
    
if __name__ == "__main__":
    yaml_file_path = 'credentials.yaml' 
    credentials = load_credentials(yaml_file_path)
    
    db_connector = RDSDatabaseConnector(credentials)
    db_connector.initialise_engine()
    loan_payments_df = db_connector.fetch_loan_payments()
    
    # Perform data transformations
    data_transformer = DataTransform(loan_payments_df)
    csv_file_path = 'loan_payments.csv'
    db_connector.save_data_to_csv(data_transformer.data_frame, csv_file_path)
    print(f"Data saved to {csv_file_path}")
    loaded_df = db_connector.load_data_from_csv(csv_file_path)
    print("Data loaded successfully")
