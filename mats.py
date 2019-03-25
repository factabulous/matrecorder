# -*- coding: utf-8 -*-

import json

class Mats:
    def __init__(self, ref_file_name):
        """
        ref_file_name is the file location that contains all the reference
        information about materials and grades
        """
        self._GRADES_KEY = "grades"
        self._MAXIMUMS_KEY = "maximums"

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
    
