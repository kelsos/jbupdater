#!/usr/bin/python
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class Updater:

  def on_app_window_destroy(self, object, data=None):
    print("quit with cancel")
    Gtk.main_quit()

  def on_gtk_quit_activate(self, menuitem, data=None):
    print("quit from menu")
    Gtk.main_quit()

  def __init__(self):
    self.gladefile = 'main_ui.glade'
    self.builder = Gtk.Builder()
    self.builder.add_objects_from_file(self.gladefile, ('app_window', ''))
    self.builder.connect_signals(self)
    self.window = self.builder.get_object('app_window')
    self.window.show_all()

if __name__ == "__main__":
  main = Updater()
  Gtk.main()

