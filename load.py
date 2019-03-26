# -*- coding: utf-8 -*-

import os
import Tkinter as tk
import ttk
import myNotebook as nb
from config import config
import sys
import plug
import version
import mat_info
from sys import platform
from util import GridHelper, debug, error
from ttkHyperlinkLabel import HyperlinkLabel

this = sys.modules[__name__]	# For holding module globals

this.target = None

#this.debug = True if platform == 'darwin' else False

window=tk.Tk()
window.withdraw()

def local_file(name):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), name)

def plugin_start():
    this._mats = mat_info.Mats(local_file("material_info.json"))
    return "matrecorder"

def plugin_stop():
    window.destroy()

def dashboard_entry(cmdr, is_beta, entry):
    pass

def plugin_app(parent):
    """
    Returns a frame containing the status fields we want to display to the 
    app in the main window
    """
    h = GridHelper()
    this.status_frame = tk.Frame(parent)

    #vcheck = version.Version("matrecorder", "https://raw.githubusercontent.com/factabulous/matrecorder/master/VERSION.md")
    #if vcheck.is_new_version():
        #HyperlinkLabel(this.status_frame, url="https://github.com/factabulous/kumay3305", text="New Kumay3305 version available! Click here").grid(row=h.row(), column=h.col(4), columnspan=4)
        #h.newrow()

    tk.Label(this.status_frame, text="Materials").grid(row=h.row(), column=h.col(), sticky=tk.W)
    h.newrow()

    this.report = tk.Message(this.status_frame, width=200)
    this.report.grid(row=h.row(),column=h.col(), sticky = tk.W)
    return this.status_frame

def summary():
    return " ".join("G{}:{}".format(x[0], x[1]) for x in this._mats.grade_counts())
        

def update_view():
    if this._mats.has_events():
        lines = [ "G{} {} ({}) {}/{} {:2.0f}%".format(l['grade'], l['local'], l['count'], l['now'], l['maximum'], l['percent']) for l in this._mats.recent() ]
        this.report['text'] = summary() + '\n' + '\n'.join(lines)
    else:
        this.report['text'] = 'Nothing collected'

def record_from_dict(info, take = False, name="Name", count="Count"):
    """
    Not all events have a localised name. If 'take' is set True
    the the counts are flipped as they are removing from available
    mats. You can override the fields used for when fdev use different names...
    """
    localised_key = name + '_Localised'
    if localised_key in info:
        local = info[localised_key]
    else:
        local = info[name]
    return _mats.record( info[name], local, info[count] * ( -1 if take else 1))


def journal_entry(cmdr, is_beta, system, station, entry, state):
    event = entry['event']
    if event == 'Materials':
        this._mats.snapshot(entry)
    if event == 'MaterialCollected':
        record_from_dict(entry)
        update_view()
    if event == 'EngineerCraft':
        for e in entry['Ingredients']:
            record_from_dict(e, take=True)
        update_view()
    if event == 'MaterialTrade':
        record_from_dict(entry['Received'], name="Material", count="Quantity")
        record_from_dict(entry['Paid'], take=True, name="Material", count="Quantity")
        update_view()
    if event == 'MissionCompleted':
        if 'MaterialsReward' in entry:
            for e in entry['MaterialsReward']:
                record_from_dict(e)
        update_view()
    if event == 'Synthesis':
        if 'Materials' in entry:
            for e in entry['Materials']:
                record_from_dict(e, take=True)
        update_view()
    if entry['event'] in [ 'Interdicted', 'SupercruiseExit', 'USSDrop']:
        this._mats.reset()
        update_view()
        

