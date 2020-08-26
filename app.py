import webbrowser
import schedule
import time
import json
import sys

class Event():
    def __init__(self, name, days, time, zoom_link):
        """Initialise event object"""
        self.name = name
        self.days = days
        self.time = time
        self.zoom_link = zoom_link

    def open_zoom (self):
        """Open zoom link for the event on a web browser"""
        webbrowser.open(self.zoom_link)

    def set_schedule(self):
        """Set the scheduler to run for the given days and times"""
        for day in self.days:
            schedule.every().day.at(self.time).do(self.open_zoom)

def get_user_events():
    """Get user data regarding their recurring events"""
    addNewEvent = True
    event = None
    save_events = {}
    while addNewEvent:
        name = input("Please enter the name of the (recurring) event (or class) you'd like to add: ")
        week_num = 0
        while week_num < 1:
            week_num = int(input("Enter the number of times " + name + " occurs weekly: "))
        k = 0
        days = []
        while k < week_num:
            days.append(get_event_day())
            k += 1
        time = ""
        while time == "" or len(time) != 5 or time[2] != ":":
            time = input("Please enter the time of " + name + " separated by a colon (i.e. 14:15): ")
        zoom_link = input("Please enter the meeting link for " + name + " (i.e. https://make.sc/blah-blah): ")
        event = Event(name, days, time, zoom_link)
        save_events[event.name] = {
            'name': event.name,
            'days': event.days,
            'time': event.time,
            'zoom_link': event.zoom_link
        }
        print("\n  \n Event Saved! \n \n")
        addNewEvent = input("Would you like to add another event? (yes or no): ").lower() == "yes"
    save_to_json(save_events)
    return event

def get_event_day():
    """Retrieve the various days on which the recurring event occurs"""
    print("Monday | Tuesday | Wednesday | Thursday | Friday")
    while True:
        day = input(
                "Please enter the day on which this event occurs: "
            ).lower()
        if (
            day == "monday"
            or day == "tuesday"
            or day == "wednesday"
            or day == "thursday"
            or day == "friday"
        ):
            return day

def save_to_json(save_events):
    """Save event data in the saved_events.json file using json format"""
    with open('saved_events.json', 'w') as f:
        json.dump(save_events, f)
try:
    """Attempt to load saved data from the saved_events.json file"""
    print("\nLoading...\n")
    saved_events = open('saved_events.json')
    events = json.load(saved_events)
    sys.stdout.write("\033[F")
    print("Events loaded!")
    for event in events.values():
        new_event = Event(event['name'], event['days'], event['time'], event['zoom_link'])
        new_event.set_schedule()
    sys.stdout.write("\033[F")
    print("App is running :)")
except IOError:
    """Prompt user to enter data regarding their recurring events"""
    get_user_events()
    saved_events = open('saved_events.json')
    events = json.load(saved_events)
    for event in events.values():
        new_event = Event(event['name'], event['days'], event['time'], event['zoom_link'])
        new_event.set_schedule()
    print("App is running :)")
while True:
    """Run scheduled tasks"""
    schedule.run_pending()
    time.sleep(1)
