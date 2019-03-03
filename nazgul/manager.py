import logging
import os

from nazgul.constants import LOGGER_NAME
from nazgul.utils import import_from

logger = logging.getLogger(LOGGER_NAME)


class Manager(object):
    class_to_import = ""
    path_to_search = ""
    module_to_search = ""

    def __init__(self, trigger_object, path=__file__):
        self.trigger_object = trigger_object
        self.path = os.path.dirname(path)

    def get_resources(self):
        return (self.import_resource(k) for k in sorted(os.listdir(os.path.join(self.path, self.path_to_search))) if
                k not in ['__pycache__', '__init__.py', ])

    def import_resource(self, resource_file):
        resource_module = resource_file.replace(".py", "")
        resource_object = import_from(self.module_to_search.format(module=resource_module),
                                      self.class_to_import)
        logger.info("Init {}: {}".format(self.class_to_import, resource_object))
        return resource_object()

    def get_by_trigger(self):
        for resource in self.get_resources():
            if resource.trigger(self.trigger_object):
                return resource
