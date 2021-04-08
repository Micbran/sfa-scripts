import maya.cmds as cmds
import logging
import random

log = logging.getLogger(__name__)
random.seed()


class ScatterInstance(object):
    def __init__(self,
                 source_object,
                 destinations,
                 scale_ranges=((1, 1), (1, 1), (1, 1)),
                 rotation_ranges=((0, 0), (0, 0), (0, 0))):
        # let's make Python look like Lisp
        self.source_object = source_object
        self.destinations = destinations
        self.scale_ranges = scale_ranges
        self.rotation_ranges = rotation_ranges

    def scatter_on_source(self, square_scale):
        pass

    def _scale_by_randoms(self, instance, square_scale):
        pass
        # random.uniform()

    def _rotate_by_randoms(self, instance):
        pass
        # random.uniform()
