masterconfigparser
===================
Master/local configuration file parser.                                                                                                                                                                 
                                                                                 
A wrapper of ConfigParser.ConfigParser that supports a master/local
configuration mix, supports a similar API as ConfigParser.

Access to configuration values will look in the local configuration first,
followed by the master.

Any changes to the configuration dictionary is saved to the local instance
only, not the master.

(This behaviour can be overridden by accessing the .master attribute of
a MasterConfigParser instance)

Writing the configuration changes will only write the local, unless
overridden as above.
