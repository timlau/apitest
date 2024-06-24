import threading
import time
import gi

gi.require_version('Gtk', '4.0')
from gi.repository import GLib, Gtk, GObject # type: ignore


class Application(Gtk.Application):

    def do_activate(self):
        window = Gtk.ApplicationWindow(application=self)
        window.props.default_height = 600
        window.props.default_width = 600
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6,
                      margin_start=12, margin_end=12, margin_top=30, margin_bottom=30)
        self.progress = Gtk.ProgressBar(show_text=True)
        box.append(self.progress)
        window.set_child(box)
        window.present()

        thread = threading.Thread(target=self.example_target)
        thread.daemon = True
        thread.start()

    def update_progress(self, i, text):
        print(text)
        self.progress.set_fraction(0.01*i)
        if text:
            self.progress.set_text(text)
        return False

    def example_target(self):
        for i in range(101):
            GLib.idle_add(self.update_progress, i, f"percent : {i}")
            time.sleep(0.2)


app = Application()
app.run()