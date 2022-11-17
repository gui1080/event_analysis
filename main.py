import os
import pandas as pd
from datetime import datetime

def main():
    
    # 1
    
    events_data = pd.read_csv(os.path.dirname(__file__) + r"/event_data.csv")

    # 2 and 3
    # -------------------------------------------------

    week_ids = []
    
    ids_33 = []
    count_weekid_33 = 0
    
    for index, row in events_data.iterrows():
        
        date = str(row["event_date"])
        id = str(row["user_id"])
        
        date_object = str(datetime.strptime(date, "%Y-%m-%d %H:%M:%S").isocalendar()[1])
        
        week_ids.append(date_object)
        
        if date_object == "33" and id not in ids_33:
            count_weekid_33 = count_weekid_33 + 1
            ids_33.append(id)
    
    events_data["week_ordinals"] = week_ids

    # 3
    # -------------------------------------------------
    
    print(count_weekid_33) # = 5102
    
    # 4
    # -------------------------------------------------
    # for each unique id
    # sort by ascend week_ordinals
    # newest is "week 0", next week is week 1...
    
    
    # Using groupby & sort_values to sort.
    events_data = events_data.sort_values(['user_id','event_date'],ascending=True).groupby('user_id').head(3)
    print(events_data)
    
    last_user = "0"
    retention_list = []
    
    for index, row in events_data.iterrows():
        
        current_user = str(row["user_id"])

        # new user!
        if current_user != last_user:
            retention = 0
            week = int(row["week_ordinals"])
            retention_list.append("Week " + str(retention))
        
        # same user
        else: 
            
            new_week = int(row["week_ordinals"])
            
            week_diff = new_week - week
            retention = retention + week_diff
            
            week = new_week
            retention_list.append("Week " + str(retention))

        last_user = current_user
    
    events_data["user_retention"] = retention_list
    print(events_data)
    
    # 5
    # -------------------------------------------------
    
    retention_data = events_data["user_retention"].value_counts(ascending=True)
    print(retention_data)
    
    # 6
    # -------------------------------------------------
    
    retention_list = events_data['user_retention'].unique()
    print(retention_list) # 3 different week retention did no happen once
    
    
    # 7
    # -------------------------------------------------
    
    # 8
    # -------------------------------------------------
    
    
if __name__ == '__main__':
    main()
