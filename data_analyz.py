import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv("coding_timer.csv")



# # Group the data by date and app and sum the timer duration
# time_summary_useage = df.groupby(["date", "app"])["timer"].sum().reset_index()

# # Sort the summary DataFrame by date and app
# time_summary_useage = time_summary_useage.sort_values(by=['date', "timer"])
# # Print the summary DataFrame

# time_summary_useage["minits"] = time_summary_useage['timer']//60

# print(time_summary_useage.to_string())



# print("----------------------------------------------------------")

# reason_summary_useage = df.groupby(["date", "app", "reason"])["timer"].sum().reset_index()

# # Sort the summary DataFrame by date and app
# reason_summary_useage = reason_summary_useage.sort_values(by=["reason", 'date'])
# # Print the summary DataFrame

# reason_summary_useage["minits"] = reason_summary_useage['timer']//60
# reason_summary_useage["hour"] = reason_summary_useage['timer']//60//60

# print(reason_summary_useage.to_string())


# print("----------------------------------------------------------")


# Group the data by date and app and sum the timer duration
app_summary_useage = df.groupby(["app", "reason"])["timer"].sum().reset_index()

# Sort the summary DataFrame by date and app
app_summary_useage = app_summary_useage.sort_values(by=["timer", "reason"])

# Print the summary DataFrame
app_summary_useage["minits"] = app_summary_useage['timer']//60
app_summary_useage["hour"] = app_summary_useage['minits']//60

print(app_summary_useage.to_string())


print("----------------------------------------------------------")

# Group the data by date and app and sum the timer duration
app_summary_useage_1 = df.groupby(["reason"])["timer"].sum().reset_index()

# Sort the summary DataFrame by date and app
app_summary_useage_1 = app_summary_useage_1.sort_values(by=["timer", "reason"])

# Print the summary DataFrame
app_summary_useage_1["minits"] = app_summary_useage_1['timer']//60
app_summary_useage_1["hour"] = app_summary_useage_1['minits']//60  # -24

print(app_summary_useage_1.to_string())

a = input("")