#!/usr/bin/python
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class Updater:

  def on_window1_destroy(self, object, data=None):
    print("quit with cancel")
    Gtk.main_quit()

  def on_gtk_quit_activate(self, menuitem, data=None):
    print("quit from menu")
    Gtk.main_quit()

  def __init__(self):
    self.gladefile = "main_ui.glade"
    self.builder = Gtk.Builder()
    self.builder.add_from_file(self.gladefile)
    self.builder.connect_signals(self)
    self.window = self.builder.get_object("app_window")
    self.window.show()

if __name__ == "__main__":
  main = Updater()
  Gtk.main()
        # datastore = DataStore()
        # utilities.load_installed_versions(datastore)
        # utilities.check_for_updates(datastore)
        #
        # idea_installed_version.set_text(datastore.idea.installed_version)
        # php_installed_version.set_text(datastore.phpstorm.installed_version)
        # py_installed_version.set_text(datastore.pycharm.installed_version)
        # rb_installed_version.set_text(datastore.rubymine.installed_version)
        # web_installed_version.set_text(datastore.webstorm.installed_version)
        # c_installed_version.set_text(datastore.clion.installed_version)
        # db_installed_version.set_text(datastore.dbe.installed_version)
        #
        # idea_available_version.set_text(datastore.idea.available_version)
        # php_available_version.set_text(datastore.phpstorm.available_version)
        # py_available_version.set_text(datastore.pycharm.available_version)
        # rb_available_version.set_text(datastore.rubymine.available_version)
        # web_available_version.set_text(datastore.webstorm.available_version)
        # c_available_version.set_text(datastore.clion.available_version)
        # db_available_version.set_text(datastore.dbe.available_version)
