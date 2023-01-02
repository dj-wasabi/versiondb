import os
import sys
import api.server.config.settings

# create settings object corresponding to specified env
FLASK_ENV = os.environ.get('FLASK_ENV', 'ci')
_current = getattr(sys.modules['api.server.config.settings'], '{0}Config'.format(FLASK_ENV))()

# copy attributes to the module for convenience
for atr in [f for f in dir(_current) if not '__' in f]:
   # environment can override anything
   val = os.environ.get(atr, getattr(_current, atr))
   setattr(sys.modules[__name__], atr, val)


def as_dict():
   """Create a dict based on all of the configuration settings."""
   res = {}
   for atr in [f for f in dir(_current) if not '__' in f]:
       val = getattr(_current, atr)
       res[atr] = val
   return res


def getConfig(name="DEBUG"):
   """Get a specific configuration key, from the big 'as_dict' key."""
   config = as_dict()

   if name in config:
      return config[name]
   else:
      return None

