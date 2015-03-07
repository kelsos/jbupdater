#!/usr/bin/python
import utilities
from gi.repository import Gtk
from datastore import DataStore


class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="JB IDE Updater")
        self.set_default_size(640, 480)

        grid = Gtk.Grid()
        grid.set_row_spacing(10)
        grid.set_column_spacing(15)
        self.add(grid)

        ide_label = Gtk.Label("IDE")
        installed_label = Gtk.Label("Install")
        eap_label = Gtk.Label("EAP")
        community_label = Gtk.Label("Community")
        installed_version_label = Gtk.Label("Installed")
        available_version_label = Gtk.Label("Available")

        grid.attach(ide_label, 1, 1, 1, 1)
        grid.attach(installed_label, 2, 1, 1, 1)
        grid.attach(eap_label, 3, 1, 1, 1)
        grid.attach(community_label, 4, 1, 1, 1)
        grid.attach(installed_version_label, 5, 1, 1, 1)
        grid.attach(available_version_label, 6, 1, 1, 1)

        idea_label = Gtk.Label("IntelliJ IDEA")
        php_label = Gtk.Label("PhpStorm")
        py_label = Gtk.Label("PyCharm")
        rb_label = Gtk.Label("RubyMine")
        web_label = Gtk.Label("WebStorm")
        c_label = Gtk.Label("CLion")
        db_label = Gtk.Label("0xDBE")

        grid.attach(idea_label, 1, 2, 1, 1)
        grid.attach(php_label, 1, 3, 1, 1)
        grid.attach(py_label, 1, 4, 1, 1)
        grid.attach(rb_label, 1, 5, 1, 1)
        grid.attach(web_label, 1, 6, 1, 1)
        grid.attach(c_label, 1, 7, 1, 1)
        grid.attach(db_label, 1, 8, 1, 1)

        idea_installed_check = Gtk.CheckButton()
        php_installed_check = Gtk.CheckButton()
        py_installed_check = Gtk.CheckButton()
        rb_installed_check = Gtk.CheckButton()
        web_installed_check = Gtk.CheckButton()
        c_installed_check = Gtk.CheckButton()
        db_installed_check = Gtk.CheckButton()

        grid.attach(idea_installed_check, 2, 2, 1, 1)
        grid.attach(php_installed_check, 2, 3, 1, 1)
        grid.attach(py_installed_check, 2, 4, 1, 1)
        grid.attach(rb_installed_check, 2, 5, 1, 1)
        grid.attach(web_installed_check, 2, 6, 1, 1)
        grid.attach(c_installed_check, 2, 7, 1, 1)
        grid.attach(db_installed_check, 2, 8, 1, 1)

        idea_eap = Gtk.CheckButton()
        php_eap = Gtk.CheckButton()
        py_eap = Gtk.CheckButton()
        rb_eap = Gtk.CheckButton()
        web_eap = Gtk.CheckButton()
        c_eap = Gtk.CheckButton()
        db_eap = Gtk.CheckButton()

        grid.attach(idea_eap, 3, 2, 1, 1)
        grid.attach(php_eap, 3, 3, 1, 1)
        grid.attach(py_eap, 3, 4, 1, 1)
        grid.attach(rb_eap, 3, 5, 1, 1)
        grid.attach(web_eap, 3, 6, 1, 1)
        grid.attach(c_eap, 3, 7, 1, 1)
        grid.attach(db_eap, 3, 8, 1, 1)

        idea_community = Gtk.CheckButton()
        php_community = Gtk.Label("Not available")
        py_community = Gtk.CheckButton()
        rb_community = Gtk.Label("Not available")
        web_community = Gtk.Label("Not available")
        c_community = Gtk.Label("Not available")
        db_community = Gtk.Label("Not available")

        grid.attach(idea_community, 4, 2, 1, 1)
        grid.attach(php_community, 4, 3, 1, 1)
        grid.attach(py_community, 4, 4, 1, 1)
        grid.attach(rb_community, 4, 5, 1, 1)
        grid.attach(web_community, 4, 6, 1, 1)
        grid.attach(c_community, 4, 7, 1, 1)
        grid.attach(db_community, 4, 8, 1, 1)

        idea_installed_version = Gtk.Label("0.0")
        php_installed_version = Gtk.Label("0.0")
        py_installed_version = Gtk.Label("0.0")
        rb_installed_version = Gtk.Label("0.0")
        web_installed_version = Gtk.Label("0.0")
        c_installed_version = Gtk.Label("0.0")
        db_installed_version = Gtk.Label("0.0")

        grid.attach(idea_installed_version, 5, 2, 1, 1)
        grid.attach(php_installed_version, 5, 3, 1, 1)
        grid.attach(py_installed_version, 5, 4, 1, 1)
        grid.attach(rb_installed_version, 5, 5, 1, 1)
        grid.attach(web_installed_version, 5, 6, 1, 1)
        grid.attach(c_installed_version, 5, 7, 1, 1)
        grid.attach(db_installed_version, 5, 8, 1, 1)

        idea_available_version = Gtk.Label("0.0")
        php_available_version = Gtk.Label("0.0")
        py_available_version = Gtk.Label("0.0")
        rb_available_version = Gtk.Label("0.0")
        web_available_version = Gtk.Label("0.0")
        c_available_version = Gtk.Label("0.0")
        db_available_version = Gtk.Label("0.0")

        grid.attach(idea_available_version, 6, 2, 1, 1)
        grid.attach(php_available_version, 6, 3, 1, 1)
        grid.attach(py_available_version, 6, 4, 1, 1)
        grid.attach(rb_available_version, 6, 5, 1, 1)
        grid.attach(web_available_version, 6, 6, 1, 1)
        grid.attach(c_available_version, 6, 7, 1, 1)
        grid.attach(db_available_version, 6, 8, 1, 1)

        update_button = Gtk.Button("Update")
        update_button.connect("clicked", self.on_button_clicked)
        grid.attach(update_button, 1, 9, 1, 1)

        datastore = DataStore()
        utilities.load_installed_versions(datastore)
        utilities.check_for_updates(datastore)

        idea_installed_version.set_text(datastore.idea.installed_version)
        php_installed_version.set_text(datastore.phpstorm.installed_version)
        py_installed_version.set_text(datastore.pycharm.installed_version)
        rb_installed_version.set_text(datastore.rubymine.installed_version)
        web_installed_version.set_text(datastore.webstorm.installed_version)
        c_installed_version.set_text(datastore.clion.installed_version)
        db_installed_version.set_text(datastore.dbe.installed_version)

        idea_available_version.set_text(datastore.idea.available_version)
        php_available_version.set_text(datastore.phpstorm.available_version)
        py_available_version.set_text(datastore.pycharm.available_version)
        rb_available_version.set_text(datastore.rubymine.available_version)
        web_available_version.set_text(datastore.webstorm.available_version)
        c_available_version.set_text(datastore.clion.available_version)
        db_available_version.set_text(datastore.dbe.available_version)


        print ("complete")

    def on_button_clicked(self, widget):
        print("Hello World")


win = MyWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()