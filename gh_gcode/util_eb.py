import datetime
import math

import rhinoscriptsyntax as rs
import Rhino.Geometry as rg


from . import util
reload(util)


### Utilities fo EB

class Util_EB(util.Util):


    def calc_print_area(self, points_array):

        pts = self.flatten_runtime_list(points_array)
        bbox = rg.BoundingBox(pts)
        
        return bbox.Min, bbox.Max


    def check_print_area(self, points_array):

        machine_min = [0, 0, 0]
        machine_max = [1700, 1300, 1020]
        
        print_min, print_max = self.calc_print_area(points_array)

        msg = []

        ### Left
        if machine_min[0] > print_min[0]:
            msg.append("Over X_Mini!!\n")

        ### Right
        if machine_max[0] < print_max[0]:
            msg.append("Over X_Max!!\n")

        ### Front
        if machine_min[1] > print_min[1]:
            msg.append("Over Y_Mini!!\n")

        ### Back
        if machine_max[1] < print_max[1]:
            msg.append("Over Y_Max!!\n")
        
        ### Bottom
        if machine_min[2] > print_min[2]:
            msg.append("Over Z_Mini!!\n")

        if msg == []:
            msg.append("OK!!")

        return msg


    def draw_machine(self):

        rects = []

        machine_origin = [-69, -100]
        machine_max = [1700, 1300]

        ### Panel
        panel_size = 500
        panel_count = 12
        vv = 3

        for i in xrange(panel_count):

            u, v = divmod(i, vv)
            tmp_origin = (machine_origin[0] + (500 * u) , machine_origin[1] + (500 *v), 0)
            pl = rs.MovePlane(rs.WorldXYPlane(), tmp_origin)
            rc = rs.AddRectangle(pl, panel_size, panel_size)
            rects.append(rc)

        ### Print Area
        print_origin = (0, 0, 0)
        pl = rs.MovePlane(rs.WorldXYPlane(), print_origin)
        rc = rs.AddRectangle(pl, machine_max[0], machine_max[1])
        rects.append(rc)

        return rects