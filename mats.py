# -*- coding: utf-8 -*-

import json

class Mats:
    def __init__(self, ref_file_name):
        """
        ref_file_name is the file location that contains all the reference
        information about materials and grades
        """

        self._localised = {}
        self._events = []

        with open(ref_file_name, "rt") as ref_file:
            self._mats = json.load(ref_file)

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
        name and a count of how many
        """
        if self.grade(name):
            self._localised[name] = local_name
            self._events.append( { "name": name, "count": count } )

    def recent(self, count = 5):
        """
        Return recently collected materials - up to a maximum of 'count'
        """
        return self.decorate(self._events[-count:])

    def decorate(self, events):
        """
        Adds extra fields onto a set of events 
        """
        return events
        
    
