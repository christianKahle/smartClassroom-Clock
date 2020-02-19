import configparser
from datetime import *
class schedule():
    def __init__(self,schedule_file,schedule):
        self.file = schedule_file
        self.config = configparser.ConfigParser()
        self.schedule = schedule
        self.events = {}
        self.update()
    def update(self):
        self.config.read(self.file)
        self.name = self.config[self.schedule]['name']
        self.event_types = self.config[self.schedule]['event_types'].split(",")
        for e in self.event_types:
            self.events[e] = [self.config[self.schedule][e+str(i)] for i in range(1,int(self.config[self.schedule]["n_"+e])+1)]
    @staticmethod
    def sort_events(events):
        less = []
        equal = []
        greater = []

        if len(events) > 1:
            pivot = schedule.event_times(events[0])
            for e in events:
                ts = schedule.event_times(e)
                if ts[0] < pivot[0]:
                    less.append(e)
                elif ts[0] == pivot[0]:
                    if ts[1] < pivot[1]:
                        less.append(e)
                    elif ts[1] == pivot[1]:
                        equal.append(e)
                    elif ts[1] > pivot[1]:
                        greater.append(e)
                elif ts[0] > pivot[0]:
                    greater.append(e)
            return schedule.sort_events(less)+equal+schedule.sort_events(greater)
        else:
            return events

    def chronological_events(self):
        return schedule.sort_events(self.all_events())

    def all_events(self):
        all_events = []
        for et in self.event_types:
            all_events.extend(self.events[et])
        return all_events
    @staticmethod
    def event_times(event):
        es = event.split(",")
        ts = []
        for t in es[0:2]:
            ts.append(time.fromisoformat(t))
        return ts
    def current_events(self,time):
        cevents = []
        for e_type in self.event_types:
            for e in self.events[e_type]:
                ts = schedule.event_times(e)
                if (time > ts[0] and time < ts[1]):
                    cevents.append(e)
        return cevents
    def next_event(self, time):
        evc = self.chronological_events() 
        for e in evc:
            if time > schedule.event_times(e)[0]:
                continue
            if time < schedule.event_times(e)[0]:
                return e
        return '00:00,00:00,None'