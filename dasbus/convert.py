# test dasbus methods to converting to/from dbus variants
import gi
from gi.repository import GLib 
from dasbus.typing import get_native, get_variant, Variant

names = {'names': ["text"]}
ver: Variant =get_variant(dict[str,list[str]],names)
print(type(ver),ver, type(get_native(ver)))


ver: Variant  = get_variant(str,"Text")
print(type(ver),ver,type(get_native(ver)))


str_var = GLib.Variant("s", "Test")
str_native = get_native(str_var)
print(str_var,type(str_var),str_native, type(str_native) )
