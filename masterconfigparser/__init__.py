"""Master/local configuration file parser.

A wrapper of ConfigParser.ConfigParser that supports a master/local configuration mix, supports the same
API semantics.
Access to configuration values will look in the local configuration first, followed by the master.
Any changes to the configuration dictionary is saved to the local instance only, not the master.
(This behaviour can be overridden by accessing the .master attribute of a MasterConfigParser instance)
Writing the configuration changes will only write the local, unless overridden as above.
"""

from ConfigParser import *
from ConfigParser import __all__

__all__ = list(__all__) + ['MasterConfigParser']


class MasterConfigParser(object):

    def __init__(self, defaults=None, dict_type=dict, _cls=ConfigParser):
        """Create master and local ConfigParser instances. The defaults argument is NOT
        passed to the local config, defaults only live on the master instance"""
        self.master = _cls(defaults=defaults, dict_type=dict_type)
        self.local = _cls(dict_type=dict_type)

    def read(self, filenames, master):
        if master:
            return self.master.read(filenames)
        else:
            return self.local.read(filenames)

    def readfp(self, fp, filename=None, master=None):
        if master is None:
            raise ValueError('master argument must be True or False')
        if master:
            return self.master.readfp(fp, filename)
        else:
            return self.local.readfp(fp, filename)

    def defaults(self):
        return self.master.defaults()

    def sections(self):
        """Return the combined list of sections available"""
        master_sections = self.master.sections()
        local_sections = self.local.sections()
        return list(set(master_sections + local_sections))

    def add_section(self, section):
        return self.local.add_section(section)

    def has_section(self, section):
        has_local = self.local.has_section(section)
        if has_local: return has_local
        return self.master.has_section(section)

    def options(self, section):
        local_opts = self.local.options(section)
        master_opts = self.local.options(section)
        return list(set(master_opts + local_opts))

    def get(self, section, option):
        try:
            return self.local.get(section, option)
        except (NoSectionError, NoOptionError):
            return self.master.get(section, option)

    def items(self, section):
        found_master = found_local = True
        try:
            d2 = self.master._sections[section]
        except KeyError:
            if section != DEFAULTSECT:
                found_master = False
            d2 = self.master._dict()
        d = self.master._defaults.copy()
        d.update(d2)
        try:
            d3 = self.local._sections[section]
        except KeyError:
            if section != DEFAULTSECT:
                found_local = False
            d3 = self.local._dict()
        d.update(d3)
        if not found_master and not found_local:
            raise NoSectionError(section)
        if '__name__' in d:
            del d['__name__']
        return d.items()

    @property
    def optionxform(self):
        """Masquerade over the ConfigParser optionxform definition"""
        return self.master.optionxform

    @optionxform.setter
    def optionxform(self, new_func):
        """Masquerade over the ConfigParser.optionxform attribute for setting on the master
        and local instances"""
        self.master.optionxform = new_func
        self.local.optionxform = new_func

    def has_option(self, section, option):
        local_option = self.local.has_option(section, option)
        if local_option: return local_option
        return self.master.has_section(section, option)

    def set(self, section, option, value):
        return self.local.set(section, option, value)

    def write(self, fp):
        return self.local.write(fp)

    def remove_option(self, section, option):
        return self.local.remove_option(section, option)

    def remove_section(self, section):
        return self.local.remove_section(section)

