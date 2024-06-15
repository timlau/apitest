import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk,GObject # type: ignore 

view = Gtk.ColumnView()
column = Gtk.ColumnViewColumn()
sorter = Gtk.Sorter()

for property in column.list_properties():
    print(property)
print(column.props.header_menu)
print(GObject.signal_list_names(view))