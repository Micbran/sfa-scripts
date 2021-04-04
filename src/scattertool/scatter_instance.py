import maya.cmds as cmds
import logging
import random
import constants

log = logging.getLogger(__name__)
random.seed()


class ScatterInstance(object):
    def __init__(self,
                 source_object,
                 destinations,
                 scale_ranges=(constants.MIN_SCALE, constants.MIN_SCALE, constants.MIN_SCALE),
                 rotation_ranges=(constants.MIN_ROTATION, constants.MIN_ROTATION, constants.MIN_ROTATION)):
        self.source_object = source_object
        self.destinations = destinations
        self.scale_ranges = scale_ranges
        self.rotation_ranges = rotation_ranges

    def scatter_on_source(self):
        pass

    def _scale_by_randoms(self, instance):
        pass
        # random.uniform()

    def _rotate_by_randoms(self, instance):
        pass
        # random.uniform()
