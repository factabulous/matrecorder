# -*- coding: utf-8 -*-

import json

class Mats:
    def __init__(self, ref_file_name = "material_info.json"):
        """
        ref_file_name is the file location that contains all the reference
        information about materials and grades
        """

        self._localised = {} # name => local name
        self._events = [] # name / count
        self._storage = { } # name => count

        with open(ref_file_name, "rt") as ref_file:
            self._mats = json.load(ref_file)

    def has_events(self):
        """
        Returns True if there are events recorded
        """
        return len(self._events) > 0

    def grade_counts(self):
        """
        Returns an array of tuples containing grade counts and 
        number of mats found. Grades are ordered from low to high
        """
        res = []
        for grade_ in range(1, 6):
            c = 0
            for e in self._events:
                if self.grade(e['name']) == grade_:
                    c = c + e['count']
            if c:
                res.append( ( grade_, c) )
        return res

    def grade(self, material_name):
        """
        Returns the grade (1-5) for a material name - may be None if we
        don't recognise it
        """
        for m in self._mats['grades']:
            if m['name'] == material_name:
                return m['grade']
        return None

    def maximum(self, material_name):
        """
        Returns the maximu storage for a material_name, or None if the 
        name is not recognised
        """
        g = str(self.grade(material_name))
        if g and g in self._mats['maximums']:
            return self._mats['maximums'][g]
        return None

    def record(self, name, local_name, count = 3):
        """
        Records the finding of a material 'name'. Also gives the localised
        name and a count of how many. If the name already exists in the 
        events then the two will be merged and added at the end
        """
        if self.grade(name):
            self._localised[name] = local_name
            existing = 0
            for i in range(0, len(self._events)):
               if self._events[i]['name'] == name:
                   existing = self._events[i]['count']
                   del self._events[i]
                   break 
            self._events.append( { "name": name, "count": count + existing } )
            if name in self._storage:
                self._storage[name] = self._storage[name] + count
            else:
                self._storage[name] = count

    def recent(self, count = 5):
        """
        Return recently collected materials - up to a maximum of 'count'
        """
        return self.decorate(self._events[-count:])

    def decorate(self, events):
        """
        Adds extra fields onto a set of events 
        """
        return [ {
            'name': e['name'], 
            'count': e['count'], 
            'grade': self.grade(e['name']),
            'maximum': self.maximum(e['name']), 
            'now': self._storage[e['name']], 
            'percent': 100 * self._storage[e['name']] / self.maximum(e['name']),
            'local': self._localised[e['name']]} for e in events ]

    def snapshot(self, event):
        """
        Takes a snapshot of the current material levels from a journal
        event such as Materials
        """
        if 'event' in event and 'Materials' == event['event']:
            self._storage = {}
            for k in ['Raw', 'Encoded', 'Manufactured']:
                if k in event:
                    for e in event[k]:
                        self._storage[e['Name']] = e['Count']
        
    
