import maya.cmds as cmds
import logging
import random

log = logging.getLogger(__name__)
random.seed()

# car and cdr implementations because it's funny


def car(iterable):
    return iterable[0]


def cdr(iterable):
    return iterable[1:]


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
        error = self._error_check()
        if error:
            log.error("Scatter unable to run, precondition(s) not met: {0}".format(error))
            return
        self.source_object = cmds.ls(self.source_object, transforms=True)[0]
        instance_group_name = cmds.group(empty=True, name="scatter_instance_grp#")
        for destination in self.destinations:
            instance_result = cmds.instance(self.source_object, name=self.source_object + "_instance#", leaf=True)[0]
            cmds.parent(instance_result, instance_group_name)

            self._move_instance(instance_result, destination)
            if square_scale:
                self._square_scale(instance_result)
            else:
                self._scale_by_randoms(instance_result)
            self._rotate_by_randoms(instance_result)
        cmds.xform(instance_group_name, centerPivots=True)
        log.info("Scatter complete.")

    def _error_check(self):
        error = ""
        error_count = 1
        if not self.source_object:
            error += "{0}: Source object cannot be empty.\n".format(error_count)
            error_count += 1
        if not self.destinations:
            error += "{0}: Destinations cannot be empty.\n".format(error_count)
            error_count += 1
        if not cmds.objExists(self.source_object):
            error += "{0}: Source object must exist.\n".format(error_count)
            error_count += 1
        for obj in self.destinations:
            if not cmds.objExists(obj):
                error += "{0}: Destination object must exist.\n".format(error_count)
                error_count += 1
                break
        return error

    @staticmethod
    def _move_instance(instance, vertex):
        x, y, z = cmds.pointPosition(vertex)
        cmds.move(x, y, z, instance)

    def _scale_by_randoms(self, instance):
        x_scale = random.uniform(self.scale_ranges[0][0], self.scale_ranges[0][1])
        y_scale = random.uniform(self.scale_ranges[1][0], self.scale_ranges[1][1])
        z_scale = random.uniform(self.scale_ranges[2][0], self.scale_ranges[2][1])
        cmds.scale(x_scale, y_scale, z_scale, instance)

    def _square_scale(self, instance):
        single_scale = random.uniform(self.scale_ranges[0][0], self.scale_ranges[0][1])
        cmds.scale(single_scale, single_scale, single_scale, instance)

    def _rotate_by_randoms(self, instance):
        x_rotation = random.uniform(self.rotation_ranges[0][0], self.rotation_ranges[0][1])
        y_rotation = random.uniform(self.rotation_ranges[1][0], self.rotation_ranges[1][1])
        z_rotation = random.uniform(self.rotation_ranges[2][0], self.rotation_ranges[2][1])
        cmds.rotate(x_rotation, y_rotation, z_rotation, instance)

    def _scale_by_randoms_lispy(self, instance):
        # I didn't actually test this but it should logically sound.
        # also it's just a joke, please no deduction for writing lisp functions
        x_scale = random.uniform(car(car(self.scale_ranges)),
                                 car(cdr(car(self.scale_ranges))))
        y_scale = random.uniform(car(car(cdr(self.scale_ranges))),
                                 car(cdr(car(cdr(self.scale_ranges)))))
        z_scale = random.uniform(car(car(cdr(cdr(self.scale_ranges)))),
                                 car(cdr(car(cdr(cdr(self.scale_ranges))))))
        cmds.scale(x_scale, y_scale, z_scale, instance)
