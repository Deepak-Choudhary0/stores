from datetime import datetime
from flask import Flask,jsonify, request
import pandas as pd
import psycopg2
import pytz

app = Flask(__name__)

@app.route('/trigger_report', methods=['POST'])
def trigger_report():
    conn = psycopg2.connect(host="localhost",
            database="reports",
            user="postgres",
            password="root")
    cur = conn.cursor()
    conn.close()
    return jsonify({'report_id': 'report_123'})

@app.route('/get_report', methods=['GET'])
def get_report():
    report_id = request.args.get('report_id')
    query = """
        SELECT bh.store_id, bh.day, bh.start_time_local, bh.end_time_local, st.timezone_str
        FROM business_hours bh
        INNER JOIN store_timezones st ON bh.store_id = st.store_id
        """
    conn = psycopg2.connect(host="localhost",
            database="reports",
            user="postgres",
            password="root")
    cur = conn.cursor()
    result = cur.fetchall()

    business_utc=[]

    for row in result:
        # print(row[0],get_day_name(row[1]),convert_time_to_utc(row[2],row[4]),convert_time_to_utc(row[3],row[4]),row[4])
        store_id = row[0]
        day_of_week = get_day_name(row[1])
        start_time_local = row[2]
        end_time_local = row[3]
        timezone_str = row[4]

        start_time_utc = convert_time_to_utc(start_time_local, timezone_str)
        end_time_utc = convert_time_to_utc(end_time_local, timezone_str)

        business_utc.append({
            'store_id': store_id,
            'day_of_week': day_of_week,
            'start_time_utc': start_time_utc,
            'end_time_utc': end_time_utc,
            'timezone_str': timezone_str
        })


    business_df = pd.DataFrame(business_utc)

    str_status=[]

    query = """
        SELECT store_id, status, timestamp_utc
        FROM store_status
    """

    cur.execute(query)

    result = cur.fetchall()

    for row in result:
        store_id = row[0]
        status = row[1]
        timestamp_utc = row[2]

        str_status.append({
            'store_id': store_id,
            'status': status,
            'timestamp_utc': timestamp_utc
        })

    store_df = pd.DataFrame(str_status)

    print(business_df,'\n',store_df)
    
    merged_df = pd.merge(business_df, store_df, on='store_id', how='inner')


    merged_df['timestamp_utc'] = pd.to_datetime(merged_df['timestamp_utc'])

    print(merged_df)
    output=get_uptime_downtime(merged_df)
    if(report_id == 'report_123'):
        return jsonify({'status': 'Complete', 'data': 'your_csv_data'})
    else:
        return jsonify({'status': 'Running'})

def convert_time_to_utc(local_time_str, timezone_str):
    local_tz = pytz.timezone(timezone_str)
    local_time = datetime.strptime(local_time_str, "%H:%M:%S").time()

    current_date = datetime.now(local_tz).date()

    local_dt = datetime.combine(current_date, local_time)

    utc_dt = local_tz.localize(local_dt, is_dst=None).astimezone(pytz.utc)

    utc_time_str = utc_dt.strftime("%H:%M:%S")
    return utc_time_str

def get_day_name(day_number):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    if 0 <= day_number <= 6:
        return days[day_number]

def connect():

    conn = None

    try:
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(host="localhost",
            database="reports",
            user="postgres",
            password="root")

        cur = conn.cursor()

        query = """
            SELECT bh.store_id, bh.day, bh.start_time_local, bh.end_time_local, st.timezone_str
            FROM business_hours bh
            INNER JOIN store_timezones st ON bh.store_id = st.store_id
        """

        cur.execute(query)

        result = cur.fetchall()

        business_utc=[]

        for row in result:
            # print(row[0],get_day_name(row[1]),convert_time_to_utc(row[2],row[4]),convert_time_to_utc(row[3],row[4]),row[4])
            store_id = row[0]
            day_of_week = get_day_name(row[1])
            start_time_local = row[2]
            end_time_local = row[3]
            timezone_str = row[4]

            start_time_utc = convert_time_to_utc(start_time_local, timezone_str)
            end_time_utc = convert_time_to_utc(end_time_local, timezone_str)

            business_utc.append({
                'store_id': store_id,
                'day_of_week': day_of_week,
                'start_time_utc': start_time_utc,
                'end_time_utc': end_time_utc,
                'timezone_str': timezone_str
            })


        business_df = pd.DataFrame(business_utc)

        str_status=[]

        query = """
            SELECT store_id, status, timestamp_utc
            FROM store_status
        """

        cur.execute(query)

        result = cur.fetchall()

        for row in result:
            store_id = row[0]
            status = row[1]
            timestamp_utc = row[2]

            str_status.append({
                'store_id': store_id,
                'status': status,
                'timestamp_utc': timestamp_utc
            })

        store_df = pd.DataFrame(str_status)

        print(business_df,'\n',store_df)
        
        merged_df = pd.merge(business_df, store_df, on='store_id', how='inner')


        merged_df['timestamp_utc'] = pd.to_datetime(merged_df['timestamp_utc'])

        print(merged_df)
        output=get_uptime_downtime(merged_df)
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


def get_uptime_downtime(df):

    # end_time = df["timestamp_utc"].max()
    end_time  = pd.to_datetime('2023-01-25 18:13:22.479220+00:00')

    print('Hourly Data','-'*100)
    # df = pd.DataFrame(hour_data)
    # df["timestamp_utc"] = pd.to_datetime(df["timestamp_utc"])

    start_time = end_time - pd.Timedelta(hours=1)

    filtered_data = df[(df["timestamp_utc"] >= start_time) & (df["timestamp_utc"] < end_time)]

    store_durations = {}

    for store_id, store_data in filtered_data.groupby("store_id"):
        active_duration = 0
        inactive_duration = 0
        status = None
        pointer_time = start_time
        for _, row in store_data.iterrows():
            if row["status"] == "active":
                status = "active"
                pointer_time = row["timestamp_utc"]
            elif status == "active":
                active_duration += (row["timestamp_utc"] - pointer_time).total_seconds() / 60
                status = None
            if row["status"] == "inactive":
                status = "inactive"
                pointer_time = row["timestamp_utc"]
            elif status == "inactive":
                inactive_duration += (row["timestamp_utc"] - pointer_time).total_seconds() / 60
                status = None
        if status == "active":
            active_duration += (end_time - pointer_time).total_seconds() / 60
        if status == "inactive":
            inactive_duration += (end_time - pointer_time).total_seconds() / 60

        store_durations[store_id] = {"active": round(active_duration, 2), "inactive": round(inactive_duration, 2)}

    # # Print the total active and inactive durations for each store
    # for store_id, durations in store_durations.items():
    #     print(f"Store {store_id}: Active Duration = {durations['active']} minutes, Inactive Duration = {durations['inactive']} minutes")
    
    df_hour_store_durations = pd.DataFrame.from_dict(store_durations, orient='index')

    df_hour_store_durations.rename(columns={'active': 'uptime_last_hour (in minutes)', 'inactive': 'downtime_last_hour (in minutes)'}, inplace=True)
    
    df_hour_store_durations = df_hour_store_durations.rename_axis('store_id').reset_index()

    print(df_hour_store_durations)

    # ----------------------------------------------------------------------------------------------------------------------------------
    print('Daily Data','-'*100)

    # # Create a DataFrame from the data
    # df = pd.DataFrame(day_data)
    # df["timestamp_utc"] = pd.to_datetime(df["timestamp_utc"])


    start_time = end_time - pd.Timedelta(days=1)

    filtered_data = df[(df["timestamp_utc"] >= start_time) & (df["timestamp_utc"] < end_time)]


    store_durations = {}

    for store_id, store_data in filtered_data.groupby("store_id"):
        active_duration = 0
        inactive_duration = 0
        status = None
        pointer_time = start_time
        for _, row in store_data.iterrows():
            if row["status"] == "active":
                status = "active"
                pointer_time = row["timestamp_utc"]
            elif status == "active":
                active_duration += (row["timestamp_utc"] - pointer_time).total_seconds() / 3600
                status = None
            if row["status"] == "inactive":
                status = "inactive"
                pointer_time = row["timestamp_utc"]
            elif status == "inactive":
                inactive_duration += (row["timestamp_utc"] - pointer_time).total_seconds() / 3600
                status = None
        if status == "active":
            active_duration += (end_time - pointer_time).total_seconds() / 3600
        if status == "inactive":
            inactive_duration += (end_time - pointer_time).total_seconds() / 3600

        store_durations[store_id] = {"active": round(active_duration, 2), "inactive": round(inactive_duration, 2)}

    df_day_store_durations = pd.DataFrame.from_dict(store_durations, orient='index')

    df_day_store_durations.rename(columns={'active': 'uptime_last_day (in hour)', 'inactive': 'downtime_last_day (in hour)'}, inplace=True)

    df_day_store_durations = df_day_store_durations.rename_axis('store_id').reset_index()


    print(df_day_store_durations)
    # ----------------------------------------------------------------------------------------------------------------------------------
    print('Weekly Data','-'*100)

    start_time = end_time - pd.Timedelta(weeks=1)

    filtered_data = df[(df["timestamp_utc"] >= start_time) & (df["timestamp_utc"] < end_time)]

    store_durations = {}

    for store_id, store_data in filtered_data.groupby("store_id"):
        active_duration = 0
        inactive_duration = 0
        status = None
        pointer_time = start_time
        for _, row in store_data.iterrows():
            if row["status"] == "active":
                status = "active"
                pointer_time = row["timestamp_utc"]
            elif status == "active":
                active_duration += (row["timestamp_utc"] - pointer_time).total_seconds() / 3600
                status = None
            if row["status"] == "inactive":
                status = "inactive"
                pointer_time = row["timestamp_utc"]
            elif status == "inactive":
                inactive_duration += (row["timestamp_utc"] - pointer_time).total_seconds() / 3600
                status = None
        if status == "active":
            active_duration += (end_time - pointer_time).total_seconds() / 3600
        if status == "inactive":
            inactive_duration += (end_time - pointer_time).total_seconds() / 3600

        store_durations[store_id] = {"active": round(active_duration, 2), "inactive": round(inactive_duration, 2)}

    # print(store_durations)
    
    df_week_store_durations = pd.DataFrame.from_dict(store_durations, orient='index')

    df_week_store_durations.rename(columns={'active': 'uptime_last_week (in hour)', 'inactive': 'downtime_last_week (in hour)'}, inplace=True)
    
    df_week_store_durations = df_week_store_durations.rename_axis('store_id').reset_index()

    print(df_week_store_durations)

    merged_df = pd.merge(df_hour_store_durations, df_day_store_durations, on='store_id')

    final_merged_df = pd.merge(merged_df, df_week_store_durations, on='store_id')

    return final_merged_df
if __name__ == '__main__':
    app.run()
    connect()