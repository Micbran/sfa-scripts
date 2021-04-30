import maya.cmds as cmds
import logging
import random

from xyz_ranges import XYZMinMaxRange

log = logging.getLogger(__name__)
random.seed()


class ScatterInstance(object):
    def __init__(self,
                 source_object,
                 destinations,
                 scale_ranges=((1, 1), (1, 1), (1, 1)),
                 rotation_ranges=((0, 0), (0, 0), (0, 0)),
                 position_ranges=((0, 0), (0, 0), (0, 0)),
                 percentage_placement=1.0):
        self.source_object = source_object
        self.destinations = destinations
        # use value unpacking for easy construction from tuple
        self.scale_ranges = XYZMinMaxRange(*scale_ranges)
        self.rotation_ranges = XYZMinMaxRange(*rotation_ranges)
        self.position_ranges = XYZMinMaxRange(*position_ranges)

        self.percentage_placement = percentage_placement

    def scatter_on_source(self, option_set):
        error = self._error_check()
        if error:
            log.error("Scatter unable to run, precondition(s) not met: {0}".format(error))
            return
        self.source_object = cmds.ls(self.source_object, transforms=True)[0]
        self.do_scatter(option_set)
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

    def do_scatter(self, option_set):
        instance_group_name = cmds.group(empty=True, name="scatter_instance_grp#")
        percent_culled_destinations = self._apply_percentage_to_list(self.destinations)
        for destination in percent_culled_destinations:
            instance_result = cmds.instance(self.source_object, name=self.source_object + "_instance#", leaf=True)[0]
            cmds.parent(instance_result, instance_group_name)

            self._move_instance_to_vertex(instance_result, destination)
            if option_set.get('constrain_to_normals'):
                self._align_to_normals(destination, instance_result)
            if option_set.get('square_scale'):
                self._square_scale(instance_result)
            else:
                self._scale_by_randoms(instance_result)
            self._rotate_by_randoms(instance_result)
            self._move_by_randoms(instance_result)
        cmds.xform(instance_group_name, centerPivots=True)

    def _apply_percentage_to_list(self, input_list):
        list_length = len(input_list)
        sample_amount = int(round(list_length)*self.percentage_placement)
        sampled_list = random.sample(input_list, sample_amount)
        return sampled_list

    @staticmethod
    def _align_to_normals(destination, instance):
        cmds.normalConstraint([destination], instance, aimVector=[0, 1.0, 0])

    @staticmethod
    def _move_instance_to_vertex(instance, vertex):
        x, y, z = cmds.pointPosition(vertex)
        cmds.move(x, y, z, instance)

    def _scale_by_randoms(self, instance):
        x_scale, y_scale, z_scale = self.scale_ranges.random_values_within_ranges()
        cmds.scale(x_scale, y_scale, z_scale, instance)

    def _square_scale(self, instance):
        single_scale, _, _ = self.scale_ranges.random_values_within_ranges()
        cmds.scale(single_scale, single_scale, single_scale, instance)

    def _rotate_by_randoms(self, instance):
        x_rotation, y_rotation, z_rotation = self.rotation_ranges.random_values_within_ranges()
        cmds.rotate(x_rotation, y_rotation, z_rotation, instance, relative=True)

    def _move_by_randoms(self, instance):
        x_move, y_move, z_move = self.position_ranges.random_values_within_ranges()
        cmds.move(x_move, y_move, z_move, instance, relative=True)
