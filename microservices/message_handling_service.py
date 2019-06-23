import requests
import sched
import time
import datetime
import atexit
from dateutil.parser import parse

from flask import Flask, request, jsonify
# from flask_apscheduler import APScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from conversation_state import WaterDrinkingReminderConversationState
from database_handler import mock_database_handler

app = Flask(__name__)
current_state = None
start_time = int(time.time())
scheduler = BackgroundScheduler()
io_service_url = 'http://127.0.0.1:5000'

# This service will include an api for processing user input


def handle_incorrect_response(example: str):
    print('Sorry. I did\'nt get that. Could you maybe try to say something like: %s'
                                % example)


def send_introduction(id: str = 'default'):
    global current_state
    current_state = WaterDrinkingReminderConversationState.START
    message = 'Hi! It\'s Timo. I help you drink enough water so you can get healthier. Type START to begin!'
    requests.post('%s/outgoing/%s' % (io_service_url, id), json={'message': message})
    


def send_reminder_after_wakeup():
    global start_time
    global current_state
    print('Morning! Time to drink some water! Reply yes after you finish!')
    # reminder_time = mock_database_handler.load_data('wakeup_reminder_time')
    # reminder_time += 24 * 3600 // 100
    # mock_database_handler.save_data('wakeup_reminder_time', reminder_time)
    # s.enter(start_time + reminder_time - time.time(), 1, send_reminder_after_wakeup)
    current_state = WaterDrinkingReminderConversationState.ASK_FINISH_DRINKING


def send_reminder_before_sleep():
    global start_time
    global current_state
    print('Time to have some water before you sleep! Reply yes after you finish!')
    # reminder_time = mock_database_handler.load_data('sleep_reminder_time')
    # reminder_time += 24 * 3600 // 100
    # mock_database_handler.save_data('sleep_reminder_time', reminder_time)
    # s.enter(start_time + reminder_time - time.time(), 1, send_reminder_before_sleep)
    current_state = WaterDrinkingReminderConversationState.ASK_FINISH_DRINKING


def handle_response(response: str):
    global current_state
    print('current_state: %s' % current_state)
    if current_state == WaterDrinkingReminderConversationState.SLEEP:
        return
    if current_state is None:
        send_introduction()
    elif current_state == WaterDrinkingReminderConversationState.START:
        handle_response_start(response)
    elif current_state == WaterDrinkingReminderConversationState.ASK_HYDRATION_HABIT:
        handle_response_hydration_habit(response)
    elif current_state == WaterDrinkingReminderConversationState.ASK_WAKEUP_TIME:
        handle_response_wakeup_time(response)
    elif current_state == WaterDrinkingReminderConversationState.ASK_BED_TIME:
        handle_response_bed_time(response)
    elif current_state == WaterDrinkingReminderConversationState.ASK_FINISH_DRINKING:
        handle_response_finish_drinking(response)


def handle_response_start(response: str):
    global current_state
    if response == 'START':
        print('Thanks for giving me a try! You can opt out anytime by typing OUT.')
        print(
            'How often do you drink water each day? You can type something like 4 times a day or I do not remember.')
        current_state = WaterDrinkingReminderConversationState.ASK_HYDRATION_HABIT
    else:
        exit(0)


def handle_response_hydration_habit(response: str):
    global current_state
    if 'a day' in response:
        if 'times a day' in response:
            # check if there is number
            try:
                freq = int(response[:response.find('times')])
            except ValueError:
                try:
                    freq = text2int(response[:response.find('times')].replace(' ', ''))
                except Exception:
                    handle_incorrect_response('4 times a day or I do not remember')
                    return
        else:
            if 'once' in response:
                freq = 1
            elif 'twice' in response:
                freq = 2
            else:
                handle_incorrect_response('4 times a day or I do not remember')
                return
    elif 'do not remember' in response:
        freq = -1
    else:
        handle_incorrect_response('4 times a day or I do not remember')
        return
    
    mock_database_handler.save_data('hydration_frequency', freq)
    
    if freq >= 0:
        print(
            'Got it! You are drinking water %d %s a day!' % (freq, 'time' if freq == 1 or freq == 0 else 'times'))
    else:
        print(
            'That is okay. I will help you keep track of how much water you drink and also how much you should drink!')
    
    print('Roughly when do you usually wake up every day?'
                                'Text something like 8:00 or 14:00 etc.')
    current_state = WaterDrinkingReminderConversationState.ASK_WAKEUP_TIME


def handle_response_wakeup_time(response: str):
    global start_time
    global current_state
    try:
        dt = parse(response)
        hour = dt.hour
        minute = dt.minute
        mock_database_handler.save_data('wakeup_time', (hour, minute))
        reminder_time = (hour * 3600 + minute * 60 + 5 * 60) / 100
        mock_database_handler.save_data('wakeup_reminder_time', reminder_time)
        
        print('Got it! You usually wake up around %s' %
                                    ('%d o\'clock' % hour if minute == 0 else
                                     '%d:0%d' % (hour, minute) if minute < 10 else
                                     '%d:%d' % (hour, minute)))
        print('I will remind you to have a glass of water after you wake up!')
        next_run_time = datetime.datetime.fromtimestamp(start_time + reminder_time)
        print('start_time: ', datetime.datetime.fromtimestamp(start_time))
        print('next_run_time: ', next_run_time)
        # s.enter(start_time + reminder_time - time.time(), 1, send_reminder_after_wakeup)
        scheduler.add_job(
            id='send_reminder_after_wakeup',
            func=send_reminder_after_wakeup, trigger='interval',
            next_run_time=next_run_time,
            seconds=3600 * 24 // 100)
    except ValueError:
        handle_incorrect_response('8:00 or 14:00 etc.')
    
    print('Now, please let me know when do you go to bed? Text something like 22:00 or 0:00 etc')
    current_state = WaterDrinkingReminderConversationState.ASK_BED_TIME


def handle_response_bed_time(response: str):
    global start_time
    global current_state
    try:
        dt = parse(response)
        hour = dt.hour
        minute = dt.minute
        mock_database_handler.save_data('wakeup_time', (hour, minute))
        reminder_time = (hour * 3600 + minute * 60 - 5 * 60) / 100
        mock_database_handler.save_data('sleep_reminder_time', reminder_time)
        
        print('Got it! You usually go to bed around %s' %
                                    ('%d o\'clock' % hour if minute == 0 else
                                     '%d:0%d' % (hour, minute) if minute < 10 else
                                     '%d:%d' % (hour, minute)))
        print('I will remind you to have a glass of water before you go to bed!')
        # s.enter(start_time + reminder_time - time.time(), 1, send_reminder_before_sleep)
        next_run_time = datetime.datetime.fromtimestamp(start_time + reminder_time)
        print('start_time: ', datetime.datetime.fromtimestamp(start_time))
        print('next_run_time: ', next_run_time)
        scheduler.add_job(
            id='send_reminder_before_sleep',
            func=send_reminder_before_sleep, trigger='interval',
            next_run_time=next_run_time,
            seconds=3600 * 24 // 100)
    except ValueError:
        handle_incorrect_response('8:00 or 14:00 etc.')
    
    current_state = WaterDrinkingReminderConversationState.SLEEP


def handle_response_finish_drinking(response: str):
    global current_state
    if response:
        if response == 'yes':
            print('Good job! Keep it up')
            
            num_finished = mock_database_handler.load_data('num_finished')
            if not num_finished:
                num_finished = 0
            mock_database_handler.save_data('num_finished', num_finished + 1)
        else:
            print('No worries. You can do it next time!')
            
            num_missed = mock_database_handler.load_data('num_missed')
            if not num_missed:
                num_missed = 0
            mock_database_handler.save_data('num_missed', num_missed + 1)
        current_state = WaterDrinkingReminderConversationState.SLEEP
    else:
        # TODO keep track of how many times there have been no responses for later use.
        pass

@app.route('/incoming/<id>', methods=['POST'])
def handle_incoming(id: str):
    incoming_message = request.json['message']
    print('Received input message for user %s: %s' % (id, incoming_message))
    handle_response(incoming_message)
    return jsonify()


def print_date_time():
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))


if __name__ == '__main__':
    send_introduction()
    scheduler.add_job(func=print_date_time, trigger="interval", seconds=3)
    scheduler.start()
    app.run(debug=True, port=5001)