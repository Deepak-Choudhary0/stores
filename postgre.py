import pandas as pd
import psycopg2

def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(host="localhost",
            database="reports",
            user="postgres",
            password="root")
		
        # create a cursor
        cur = conn.cursor()
        
        # # Execute the SQL query to get the list of tables
        # cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")

        # # Fetch all rows of the result
        # tables = cur.fetchall()


        # table_names = [table[0] for table in tables]

        # for i in range(len(table_names)):
        #     # Execute the SQL query to get the schema details for the specified table
        #     cur.execute(f"SELECT column_name, data_type, is_nullable, column_default "
        #                 f"FROM information_schema.columns "
        #                 f"WHERE table_name = '{table_names[i]}' AND table_schema = 'public'")

        #     # Fetch all rows of the result
        #     schema_details = cur.fetchall()

        #     print( schema_details,'\n')
       

        # Read CSV files
        status_df = pd.read_csv("str_status.csv")
        business_hours_df = pd.read_csv("local_time.csv")
        timezones_df = pd.read_csv("timezones.csv")

        print(status_df,business_hours_df,timezones_df)

        print('Success')
        
        # Store data in PostgreSQL
        status_df.to_sql("store_status", conn, if_exists="replace", index=False)
        business_hours_df.to_sql("business_hours", conn, if_exists="replace", index=False)
        timezones_df.to_sql("store_timezones", conn, if_exists="replace", index=False)

	    # close the communication with the PostgreSQL
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':
    connect()
