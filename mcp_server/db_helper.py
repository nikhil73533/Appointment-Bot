import sqlite3

class DbHlper:
    def __init__(self,db_name:str = "devdatabase.db"):
        """Initializing the Sqllite database connection int constructor.

        Args:
            db_name (str, optional): database name. Defaults to "devdatabase.db".

        """
        # Defining the cursor and connecting to database.
        self.connection = sqlite3.connect(db_name,check_same_thread=False)
        self.cursor = self.connection.cursor()

    def run_sql(self, query: str,params:tuple):
        try:
            self.cursor.execute(query,params)
            print("Self cursor: ")
            rows = self.cursor.fetchall()
            self.connection.commit()
            print("SQL command executed successfully.")
            print("Rows: ",rows)
            return rows
        except Exception as e:
            print(f"While executing SQL command: {e}")
            raise Exception("Failed to execute the data")

    
    def create_schema(
        self,
        table_name: str,
        columns,
        primary_key  = None,
        foreign_keys  = None,
    ):
        """ Create a table with provided columns.

        Args:
            table_name (str):  Name of the table
            columns (_type_): Dict with column name as key and a dict as value containing:
            primary_key (_type_, optional):  Name of primary key column. Defaults to None.
            foreign_keys (_type_, optional): List of tuples:. Defaults to None.
        """
        try:
        
            column_defs = [] #Initializing the list. 

            # loop over the column dictonary.
            for col, props in columns.items():
                print(f"{col}: {props}")
                col_def = f"{col} {props.get('type', '')}"
                if props.get("nullable") == "NOT NULL":
                    col_def += " NOT NULL"
                column_defs.append(col_def)

            if primary_key:
                column_defs.append(f"PRIMARY KEY ({primary_key})")

            if foreign_keys:
                for col, ref_table, ref_col in foreign_keys:
                    column_defs.append(
                        f"FOREIGN KEY ({col}) REFERENCES {ref_table}({ref_col})"
                    )
            print("Create Table")
            create_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(column_defs)});"
            print("Create query: ",create_query)
            self.cursor.execute(create_query)
            self.connection.commit()
            print(f"Table '{table_name}' created successfully.")
            return f"Table created {table_name} successfully "
        except Exception as e:
            print(f"While Creating the schema: {e}")
            return None
        
    def edit(self, table_name: str, column: str, value, condition: str):
        """
        edit a column value where a condition is met.
        """
        try:
            query = f"UPDATE {table_name} SET {column} = ? WHERE {condition}"
            self.cursor.execute(query, (value,))
            self.connection.commit()
            result = self.cursor.fetchone()
            print(f"Updated {table_name} where {condition}")
            return result
        except Exception as e:
            print(f"Error updating table '{table_name}': {e}")
            return f"Failed to update the {table_name}"
        
    def delete(self, table_name: str, pk_column: str, pk_value):
        """
        Delete a row based on primary key value.
        """
        try:
            query = f"DELETE FROM {table_name} WHERE {pk_column} = ?"
            self.cursor.execute(query, (pk_value,))
            self.connection.commit()
            print(f"Deleted row from {table_name} where {pk_column} = {pk_value}")
        except Exception as e:
            print(f"Error deleting from table '{table_name}': {e}")
            return f"Failed to delete the appointment"

    def __del__(self):
        """Ensure the database connection is closed on object destruction."""
        self.connection.close()
        print("Database connection closed.")



if __name__=="__main__":
    db = DbHlper()
    sql_query = """SELECT * FROM Appointments WHERE user_email = ?"""
    user_email = "ng1200821@gmail.com"
    params = (' ng1200821@gmail.com',)
    print(db.run_sql(sql_query,params))