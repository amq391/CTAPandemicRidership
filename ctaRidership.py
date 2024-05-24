# main.py
# Project 1 - CTA Database Application
# 
# Name: Aaron Quino, University of Illinois at Chicago, Spring 2022
# UIN: 662037133
# Description: Takes in CTA database and outputs vital statistics. Then 
# repeatedly prompts user to enter commands.
# 

import sqlite3
import matplotlib.pyplot as figure

###########################################################  
#
# print_num_stations
#
# Executes an SQL query to retrieve and output total
# number of stations in database.
#
def print_num_stations(dbCursor):
    dbCursor.execute("Select count(*) From Stations;")
    row = dbCursor.fetchone()
    print("  # of stations:", f"{row[0]:,}")

###########################################################  
#
# print_num_stops
#
# Executes an SQL query to retrieve and output total
# number of train stops in database.
#
def print_num_stops(dbCursor):
    dbCursor.execute("Select count(*) From Stops;")
    row = dbCursor.fetchone()
    print("  # of stops:", f"{row[0]:,}")

###########################################################  
#
# print_num_entries
#
# Executes an SQL query to retrieve and output the total
# number of times a CTA station is taken by a rider.
#
def print_num_entries(dbCursor):
    dbCursor.execute("Select count(*) From Ridership;")
    row = dbCursor.fetchone()
    print("  # of ride entries:", f"{row[0]:,}")

###########################################################  
#
# print_date_range
#
# Executes an SQL query to retrieve and output the 
# range of dates spanned by the database.
#
def print_date_range(dbCursor):
    dbCursor.execute("""Select min(date(Ride_Date)) as rideDate 
                        From Ridership
                        Order by rideDate asc;""")
    minDate = dbCursor.fetchone()
    dbCursor.execute("""Select max(date(Ride_Date)) as rideDate 
                        From Ridership
                        Order by rideDate asc;""")
    maxDate = dbCursor.fetchone()
    print("  date range:", f"{minDate[0]:}" + " -", f"{maxDate[0]:}")

###########################################################  
#
# print_total_ridership
#
# Executes an SQL query to retrieve and output the 
# total number of rides taken throughout the span 
# of the database.
#
def print_total_ridership(dbCursor):
    dbCursor.execute("""Select sum(Num_Riders) From Ridership;""")
    row = dbCursor.fetchone()
    print("  Total ridership:", f"{row[0]:,}")

###########################################################  
#
# print_week_ridership
#
# Executes an SQL query to retrieve and output the 
# total number of rides taken throughout the span 
# of the database on a weekday (Monday - Friday).
#
def print_week_ridership(dbCursor):
    dbCursor.execute("""Select sum(Num_Riders) From Ridership 
                        Where Type_of_Day like 'W';""")
    weekRiders = dbCursor.fetchone()

    dbCursor.execute("""Select sum(Num_Riders) From Ridership;""")
    totalRiders = dbCursor.fetchone()

    percentage = 100 * (weekRiders[0] / totalRiders[0])
    print("  Weekday ridership:", f"{weekRiders[0]:,}" + " (" + ("%.2f" % percentage) + "%)")

###########################################################  
#
# print_sat_ridership
#
# Executes an SQL query to retrieve and output the 
# total number of rides taken throughout the span 
# of the database on a Saturday.
#
def print_sat_ridership(dbCursor):
    dbCursor.execute("""Select sum(Num_Riders) from Ridership 
                        where Type_of_Day like 'A';""")
    satRiders = dbCursor.fetchone()

    dbCursor.execute("""Select sum(Num_Riders) From Ridership;""")
    totalRiders = dbCursor.fetchone()

    percentage = 100 * (satRiders[0] / totalRiders[0])
    print("  Saturday ridership:", f"{satRiders[0]:,}" + " (" + ("%.2f" % percentage) + "%)")

###########################################################  
#
# print_sun_hol_ridership
#
# Executes an SQL query to retrieve and output the 
# total number of rides taken throughout the span 
# of the database on Sunday and holidays.
#
def print_sun_hol_ridership(dbCursor):
    dbCursor.execute("""Select sum(Num_Riders) from Ridership 
                        where Type_of_Day like 'U';""")
    sunRiders = dbCursor.fetchone()

    dbCursor.execute("""Select sum(Num_Riders) From Ridership;""")
    totalRiders = dbCursor.fetchone()

    percentage = 100 * (sunRiders[0] / totalRiders[0])
    print("  Sunday/holiday ridership:", f"{sunRiders[0]:,}" + " (" + ("%.2f" % percentage) + "%)")


###########################################################  
#
# print_stats
#
# Given a connection to the CTA database, executes various
# SQL queries to retrieve and output basic stats.
#
def print_stats(dbConn):
    dbCursor = dbConn.cursor()
    print("General stats:")
    print_num_stations(dbCursor)
    print_num_stops(dbCursor)
    print_num_entries(dbCursor)
    print_date_range(dbCursor)
    print_total_ridership(dbCursor)
    print_week_ridership(dbCursor)
    print_sat_ridership(dbCursor)
    print_sun_hol_ridership(dbCursor)

###########################################################  
#
# get_tot_ridership
#
# Helper function that returns the total amount of 
# riders from the database.
#
def get_tot_ridership(dbConn):
    dbCursor = dbConn.cursor()
    dbCursor.execute("Select sum(Num_Riders) From Ridership")
    row = dbCursor.fetchone()
    return row[0]

###########################################################  
#
# plot
#
# Plots data from a table called rows on a line graph
# with the appropriate title and labels
#
def plot(rows, xlabel, ylabel, title):
    x = []
    y = []

    for row in rows:
      if len(row[0]) > 2:
        x.append(row[0][2:])
      else:
        x.append(row[0])
      y.append(row[1])
    
    figure.xlabel(xlabel)
    figure.ylabel(ylabel)
    figure.title(title)

    figure.plot(x, y)
    figure.show()

###########################################################  
#
# get_table
#
# Main mechanism to execute sql queries. Returns the wanted
# data in a table which is a list of tuples.
#
def get_table(dbConn, query, sqlParameter):
    dbCursor = dbConn.cursor()
    if sqlParameter == []:
      dbCursor.execute(query)
    else:
      dbCursor.execute(query, sqlParameter)
    resultTable = dbCursor.fetchall();
    return resultTable

###########################################################  
#
# cmd_one
#
# Prompts user to enter partial station name and outputs
# all the stations with their IDs in the database that 
# have a similar name.
#
def cmd_one(dbConn, query):
    print()
    partialName = input("Enter partial station name (wildcards _ and %): ")
    rows = get_table(dbConn, query, [partialName])
    if rows != []:
      for row in rows:
        print(row[0], ":",row[1]) # might have to format this for autograder
    else:
      print("**No stations found...")
    

###########################################################  
#
# cmd_two
#
# Outputs the ridership of each station along with the percentage
# of each stations share in total ridership.
#
def cmd_two(dbConn, query):
    print("** ridership all stations **")
    rows = get_table(dbConn, query, [])
    total = get_tot_ridership(dbConn)
    for row in rows:
      percentage = 100 * (row[1] / total)
      print(row[0], ":", f"{row[1]:,}", f"({percentage:.2f}%)")

###########################################################  
#
# cmd_three
#
# Outputs top 10 busiest stations from the database in 
# descending order by ridership along with the percentage 
# of their share of the total ridership.
#
def cmd_three(dbConn, query):
    print("** top-10 stations **")
    rows = get_table(dbConn, query, [])
    total = get_tot_ridership(dbConn)
    for row in rows:
      percentage = 100 * (row[1] / total)
      print(row[0], ":", f"{row[1]:,}", f"({percentage:.2f}%)")

###########################################################  
#
# cmd_four
#
# Outputs 10 least busiest stations from the database in 
# ascending order by ridership along with the percentage 
# of their share of the total ridership.
#
def cmd_four(dbConn, query):
    print("** least-10 stations **")
    rows = get_table(dbConn, query, [])
    total = get_tot_ridership(dbConn)
    for row in rows:
      percentage = 100 * (row[1] / total)
      print(row[0], ":", f"{row[1]:,}", f"({percentage:.2f}%)")

###########################################################  
#
# cmd_five
#
# Prompts user for line color and outputs all the stops
# that are part of that line. If the line doesn't exist, an error
# message is output. Also output is the direction of the 
# stop and if the stop is handicap-accessible.
#
def cmd_five(dbConn, query):
    print()
    color = input("Enter a line color (e.g. Red or Yellow): ")
    rows = get_table(dbConn, query, [color])
    if rows != []:
      for row in rows:
        if row[2] == 1:
          adaVal = "yes"
        else:
          adaVal = "no"
        print(row[0], ":", "direction =", row[1], "(accessible?", adaVal + ")")
    else:
      print("**No such line...")

###########################################################  
#
# cmd_six
#
# Outputs the total ridership by month in ascending order. 
# User is then prompted to choose to plot data on line graph.
#
def cmd_six(dbConn, query):
    print("** ridership by month **")
    rows = get_table(dbConn, query, [])
    for row in rows:
      print(row[0], ":", f"{row[1]:,}")
    print()
    plotCmd = input("Plot? (y/n) ")
    if plotCmd == "y":
      plot(rows, "month", "number of riders (x * 10^8)", "monthly ridership")


###########################################################  
#
# cmd_seven
#
# Outputs the total ridership by year in ascending order. 
# User is then prompted to choose to plot data on line graph.
#
def cmd_seven(dbConn, query):
    print("** ridership by year **")
    rows = get_table(dbConn, query, [])
    for row in rows:
      print(row[0], ":", f"{row[1]:,}")
    print()
    plotCmd = input("Plot? (y/n) ")
    if plotCmd == "y":
      plot(rows, "year", "number of riders (x * 10^8)", "yearly ridership")

###########################################################  
#
# doublePlot
#
# Plots two lines of ridership data from two different stations.
#
def doublePlot(station1, station2, xlabel, ylabel, title, name1, name2):
    x = []
    y = []
    day = 0

    for row in station1:
      day += 1
      x.append(day)
      y.append(row[1])

    v = []
    for row in station2:
      v.append(row[1])

    
    figure.xlabel(xlabel)
    figure.ylabel(ylabel)
    figure.title(title)

    figure.plot(x, y, label=name1)
    figure.plot(x, v, label=name2)
    figure.legend()
    figure.show()

###########################################################  
#
# cmd_eight
#
# Prompts user to enter two stations and a year and outputs the
# daily ridership of each station in the year specified.
# Output is shortened to show the first and last 5 days of the year.
# User is then prompted to plot the data on line graph.
#
def cmd_eight(dbConn, query):
    print()
    year = input("Year to compare against? ")

    print()
    station1 = input("Enter station 1 (wildcards _ and %): ")
    station1_info = get_table(dbConn, query["a"], [station1])
    if len(station1_info) == 0:
      print("**No station found...")
      return
    elif len(station1_info) > 1:
      print("**Multiple stations found...")
      return

    print()
    station2 = input("Enter station 2 (wildcards _ and %): ")
    station2_info = get_table(dbConn, query["a"], [station2])
    if len(station2_info) == 0:
      print("**No station found...")
      return
    elif len(station2_info) > 1:
      print("**Multiple stations found...")
      return

    station1_ridership = get_table(dbConn, query["b"], [station1, year])
    station2_ridership = get_table(dbConn, query["b"], [station2, year])
    station1_ridership_desc = get_table(dbConn, query["c"], [station1, year])
    station2_ridership_desc = get_table(dbConn, query["c"], [station2, year])

    print("Station 1:", station1_info[0][0], station1_info[0][1])
    for x in range(5):
      print(station1_ridership[x][0], station1_ridership[x][1])
    for x in range(4, -1, -1):
      print(station1_ridership_desc[x][0], station1_ridership_desc[x][1])
    
    print("Station 2:", station2_info[0][0], station2_info[0][1])
    for x in range(5):
      print(station2_ridership[x][0], station2_ridership[x][1])
    for x in range(4, -1, -1):
      print(station2_ridership_desc[x][0], station2_ridership_desc[x][1])
    print()
    plotCmd = input("Plot? (y/n) ")
    if plotCmd == "y":
      doublePlot(station1_ridership, station2_ridership, "day", "number of riders", "riders each day of " + year, station1_info[0][1], station2_info[0][1])

###########################################################  
#
# mapPlot
#
# Plots the latitude and longtitude of a number of 
# stations on a map of the CTA system.
#
def mapPlot(rows, color):
    x = []
    y = []

    for row in rows:
      x.append(row[2])

    for row in rows:
      y.append(row[1])

    image = figure.imread("chicago.png")
    xydims = [-87.9277, -87.5569, 41.7012, 42.0868]
    figure.imshow(image, extent=xydims)
    figure.title(color + " line")
    if (color.lower() == "purple-express"):
      color="Purple" # color="#800080"
    figure.plot(x, y, "o", c=color)
#
# annotate each (x, y) coordinate with its station name:
#
    for row in rows:
      figure.annotate(row[0], (row[2], row[1]))
    figure.xlim([-87.9277, -87.5569])
    figure.ylim([41.7012, 42.0868])
    figure.show()

###########################################################  
#
# cmd_nine
#
# Prompts user for line color then outputs all the station
# names that are part of that line. User is then propmted to 
# plot the data. The station names along that line are plotted
# on a map of the CTA system.
#
def cmd_nine(dbConn, query):
    print()
    color = input("Enter a line color (e.g. Red or Yellow): ")
    rows = get_table(dbConn, query, [color])
    if rows != []:
      for row in rows:
        print(row[0], ":", "(" + str(row[1]) + ", " + str(row[2]) + ")")
    else:
      print("**No such line...")
      return
    print()
    plotCmd = input("Plot? (y/n) ")
    if plotCmd == "y":
      mapPlot(rows, color)

###########################################################  
#
# build_sql_queries
#
# Builds and returns a dictionary that holds all the sql queries needed
# for each command. Each key corresponds to a command.
#
def build_sql_queries():
    query_dict = {
      "1" : """Select Station_ID, Station_Name From Stations
               Where Station_Name like ?
               Order By Station_Name asc;""",
      "2" : """Select Station_Name, sum(Num_Riders)
               From Ridership Join Stations 
                  On Ridership.Station_ID = Stations.Station_ID
               Group By Stations.Station_ID
               Order By Station_Name asc;""",
      "3" : """Select Station_Name, sum(Num_Riders) as total
               From Ridership join Stations 
                  On Ridership.Station_ID = Stations.Station_ID
               Group By Stations.Station_ID
               Order By total desc
               Limit 10;""",
      "4" : """Select Station_Name, sum(Num_Riders) as total
               From Ridership join Stations 
                  On Ridership.Station_ID = Stations.Station_ID
               Group By Stations.Station_ID
               Order By total asc
               Limit 10;""",
      "5" : """Select Stop_Name, Direction, ADA
               From Stops Join StopDetails on Stops.Stop_ID = StopDetails.Stop_ID
                          Join Lines on StopDetails.Line_ID = Lines.Line_ID
               Where Color like ?
               Order By Stop_Name asc;""",
      "6" : """Select strftime('%m', Ride_Date) as month, sum(Num_Riders) 
               From Ridership 
               Group By month 
               Order By month asc;""",
      "7" : """Select strftime('%Y', Ride_Date) as year, sum(Num_Riders) 
               From Ridership 
               Group By year 
               Order By year asc;""",
      "8" : {"a" : """Select Station_ID, Station_Name From Stations
                      Where Station_Name like ?;""",
             "b" : """Select date(Ride_Date), Num_Riders
                      From Ridership Join Stations 
                      On Ridership.Station_ID = Stations.Station_ID
                      Where Station_Name like ?
                      and strftime('%Y', Ride_Date) == ?
                      Group By date(Ride_Date)
                      Order By date(Ride_Date) asc""",
             "c" : """Select date(Ride_Date), Num_Riders
                      From Ridership Join Stations 
                      On Ridership.Station_ID = Stations.Station_ID
                      Where Station_Name like ?
                      and strftime('%Y', Ride_Date) == ?
                      Group By date(Ride_Date)
                      Order By date(Ride_Date) desc
                      Limit 5;"""},
      "9" : """Select Distinct Station_Name, Latitude, Longitude
               From Stations Join Stops On Stations.Station_ID = Stops.Station_ID
                             Join StopDetails on Stops.Stop_ID = StopDetails.Stop_ID
                             Join Lines on StopDetails.Line_ID = Lines.Line_ID
               Where Color like ?
               Order By Station_Name asc;"""
    }
    return query_dict

###########################################################  
#
# process_cmd
#
# Takes user input and interprets which command to execute. If 
# command is not valid, an error message is output and user is 
# prompted to enter another command.
#
def process_cmd(cmd, dbConn, queries):
    if cmd == "1":
      cmd_one(dbConn, queries["1"])
    elif cmd == "2":
      cmd_two(dbConn, queries["2"])
    elif cmd == "3":
      cmd_three(dbConn, queries["3"])
    elif cmd == "4":
      cmd_four(dbConn, queries["4"])
    elif cmd == "5":
      cmd_five(dbConn, queries["5"])
    elif cmd == "6":
      cmd_six(dbConn, queries["6"])
    elif cmd == "7":
      cmd_seven(dbConn, queries["7"])
    elif cmd == "8":
      cmd_eight(dbConn, queries["8"])
    elif cmd == "9":
      cmd_nine(dbConn, queries["9"])
    else:
      print("**Error, unknown command, try again...")
    


###########################################################  
#
# command_loop
#
# Begins command loop after building sql query dictionary.
# Exits loop when user enters 'x'.
#
def command_loop(dbConn):
    queries = build_sql_queries()
    print()
    cmd = input("Please enter a command (1-9, x to exit): ")
    while cmd != "x":
      process_cmd(cmd, dbConn, queries)
      print()
      cmd = input("Please enter a command (1-9, x to exit): ")

###########################################################  
#
# main
#
print('** Welcome to CTA L analysis app **')
print()

dbConn = sqlite3.connect('CTA2_L_daily_ridership.db')

print_stats(dbConn)
command_loop(dbConn);

#
# done
#
