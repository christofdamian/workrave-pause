#!/usr/bin/python
import os
import re
import sys
import pwd
import dbus
import dbus.decorators
import dbus.glib
import time
import gobject
import subprocess

class WorkraveDBus:

    def __init__(self):

        bus = dbus.SessionBus()
        obj = bus.get_object("org.workrave.Workrave", "/org/workrave/Workrave/Core")

        self.workrave = dbus.Interface(obj, "org.workrave.CoreInterface")
        self.config = dbus.Interface(obj, "org.workrave.ConfigInterface")

        
	for service in bus.list_names():
		if re.match('org.mpris.MediaPlayer2.', service):
			print "player: " + service
        		self.player_service = dbus.SessionBus().get_object(service, '/org/mpris/MediaPlayer2')
			break

	self.player = dbus.Interface(self.player_service, 'org.mpris.MediaPlayer2.Player')

        self.workrave.connect_to_signal("RestbreakChanged",
                                   self.on_restbreak_changed, sender_keyword='sender')
        self.workrave.connect_to_signal("DailylimitChanged",
                                   self.on_dailylimit_signal, sender_keyword='sender')

    def on_restbreak_changed(self, progress, sender=None):
        self.on_break_changed("restbreak", progress)

    def on_dailylimit_signal(self, progress, sender=None):
        self.on_break_changed("dailylimit", progress)

    def on_break_changed(self, breakid, progress, sender=None):

        if progress == "prelude":
            print "Break warning %s" % breakid
        elif progress == "break":
            print "Break %s started" % breakid
            self.player.Pause()
        elif progress == "none":
            print "Break %s idle" % breakid
        else:
            print "Unknown progress for %s: %s" % (breakid, progress)

if __name__ == '__main__':

    d = WorkraveDBus()

    loop = gobject.MainLoop()
    loop.run()
