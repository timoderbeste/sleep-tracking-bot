import math
def to_minute(time): 
    time = time.replace(" ", "")
    hour = int(time[:-2].split(":")[0])
    minute = int(time[:-2].split(":")[1])
    if time[-2:] == 'am':
        hour = hour + 12
    print("time in hours: {}  hour: {}  minute: {}".format(time, hour, minute))
    return hour*60+minute

def to_hour(time):
    hour = math.floor(time/60)
    minute = round(time%60)
    print("time in minutes: {}  hour: {}  minute: {}".format(time, hour, minute))
    if hour > 12:
        time = str(hour - 12) + ':' + str(minute) + 'pm'
    else:
        time = str(hour) + ':' + str(minute) + 'am'
    return time

def time_decrement(time, decrease_amt):
    return time - decrease_amt

def calculate_weekly_goal(ideal_time, current_time):
    #convert to minute format (output format: 8:00 am -> 480)
    current_time = to_minute(current_time)
    print("convered to minutes: {}".format(current_time))
    #calcualte weekly goal
    goal1 = time_decrement(current_time, 30)
    goal2 = time_decrement(current_time, 45)
    print("goals in minutes: {}  {}".format(goal1, goal2))
    #convert to hour format (output format: 480 -> 8:00 am)
    goal1 = to_hour(goal1)
    goal2 = to_hour(goal2)
    print("goals in hours: {}  {}".format(goal1, goal2))
    #self._bedtime_list = [goal1, str(3), goal2, str(2)]
    return goal1, goal2, str(3), str(2)

calculate_weekly_goal('10:00pm', '1:20am')
