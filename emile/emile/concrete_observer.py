import math
import json
import time
from .survey_view import send_message, concrete_subject
from .obs_design_pattern import Subject, Observer

states = {
0: "init",
1: "init_response",
2: "ask_ideal_bedtime",
3: "as_current_bedtime",
4: "ask_time_zone",
5: "ask_time_zone_response",
6: "explain_rule",
7: "give_weekly_options",
8: "weekly_options_followup1",
9: "weekly_options_followup2",
10: "notify_bedtime"
}


def get_message_from_bank(msg_bank, curr_state):
    return msg_bank[states[curr_state]]

def to_minute(time): 
    time = time.replace(" ", "")
    hour = int(time[:-2].split(":")[0])
    minute = int(time[:-2].split(":")[1])
    if time[-2:] == 'pm':
        hour = hour + 12
    return hour*60+minute

def to_hour(time):
    hour = math.floor(time/60)
    minute = round(time%60)
    if minute == 0:
        minute = '00'
    if hour > 12:
        time = str(hour - 12) + ':' + str(minute) + 'pm'
    else:
        time = str(hour) + ':' + str(minute) + 'am'
    return time

def time_decrement(time, decrease_amt):
    return time - decrease_amt

# load message bank
msg_bank = None
with open("message_bank.json", "r") as msg:
    msg_bank = json.loads(msg.read())

class ConcreteObserver(Observer):
    _state: int = 0
    _number = ""
    _name = ""
    _ideal_bedtime = ""
    _current_bedtime = ""
    _time_zone = ""
    _notification_time = ""
    _bedtime_list = []
    _repetition = 0
    _sleep_states = [3,4,5,8]

    def __init__(self, number):
        super(ConcreteObserver, self).__init__()
        self._number = number

    def save(self,msg, state):
        if self._state == 3:
            self._ideal_bedtime = msg
        if self._state == 4:
            self._current_bedtime = msg
        if self._state == 5:
            self._time_zone = msg
        if self._state == 8:
            msg = msg.lower()
            if msg == 'a':
                self._notification_time = self._bedtime_list[0]
                self._repetition = self._bedtime_list[1]
            if msg == 'b':
                self._notification_time = self._bedtime_list[2]
                self._repetition = self._bedtime_list[3]
    
    def calculate_weekly_goal(self, ideal_time, current_time):
        #convert to minute format (output format: 8:00 am -> 480)
        current_time = to_minute(current_time)
        #calcualte weekly goal
        goal1 = time_decrement(current_time, 30)
        goal2 = time_decrement(current_time, 45)
        #convert to hour format (output format: 480 -> 8:00 am)
        goal1 = to_hour(goal1)
        goal2 = to_hour(goal2)
        self._bedtime_list = [goal1, str(3), goal2, str(2)]
        return goal1, goal2, str(3), str(2)

    def initiate_conversation(self):
        global msg_bank
        outgoing_msg = get_message_from_bank(msg_bank, self._state)
        print("Sending Message: {}\nCurrent state is: {}\n".format(outgoing_msg,self._state))
        send_message(outgoing_msg, self._number)
        self._state += 1

    def update(self, incoming_msg, state):
        global msg_bank
        # save user response
        self.save(incoming_msg, self._state)
        # generate emile response
        outgoing_msg = get_message_from_bank(msg_bank, self._state)
        
        print("Sending Message: {}\nCurrent state is: {}\n".format(outgoing_msg,self._state))
        send_message(outgoing_msg, self._number)
        time.sleep(1)
        self._state += 1

        while(self._state) not in self._sleep_states:
            outgoing_msg = get_message_from_bank(msg_bank, self._state)
            # special cases - fill in blanks
            if self._state == 7:
                print("times: {},  {}".format(self._ideal_bedtime, self._current_bedtime))
                time1, time2, rep1, rep2 = self.calculate_weekly_goal(self._ideal_bedtime, self._current_bedtime)
                outgoing_words = outgoing_msg.split(' ')
                for i in range(0,len(outgoing_words)):
                    if outgoing_words[i] == '<TIME1>':
                        outgoing_words[i] = time1
                    if outgoing_words[i] == '<REPETITION1>':
                        outgoing_words[i] = rep1
                    if outgoing_words[i] == '<TIME2>':
                        outgoing_words[i] = time2
                    if outgoing_words[i] == '<REPETITION2>':
                        outgoing_words[i] = rep2
                outgoing_msg = " ".join(outgoing_words)
            if self._state == 10:
                outgoing_words = outgoing_msg.split(' ')
                for i in range(0,len(outgoing_words)):
                    if outgoing_words[i] == '<TIME>':
                        outgoing_words[i] = self._notification_time
                outgoing_msg = " ".join(outgoing_words)
            print("Sending Message: {}\nCurrent state is: {}\n".format(outgoing_msg,self._state))
            send_message(outgoing_msg, self._number)
            time.sleep(1)
            self._state += 1
            if self._state == 11:
                exit()
