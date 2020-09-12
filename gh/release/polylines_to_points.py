import datetime
import math

import rhinoscriptsyntax as rs
import Rhino.Geometry as rg


class Util():


    def get_current_time(self):
        return str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))


    def remap_number(self, src, old_min, old_max, new_min, new_max):
        return ((src - old_min) / (old_max - old_min) * (new_max - new_min) + new_min)


    def flatten_runtime_list(self, list):
        all = []
        
        for i in xrange(len(list)):
            # print(i)
            sub = list[i]
            for j in xrange(len(sub)):
                # print(j)
                all.append(sub[j])

        return all


    def export_gcode(self, dir_path, txt):

        now = self.get_current_time()
        file_path = dir_path + now + ".gcode"

        ### Export
        with open(file_path, 'w') as f:
            f.write(txt)

        print("Export GCode : {}".format(file_path))


    def zip_matrix(self, mat):
        ### https://note.nkmk.me/python-list-transpose/
        return [list(x) for x in zip(*mat)]


    def padding_previous_value(self, list_):
        
        list_pad = []

        for i in xrange(len(list_)):
            
            item_ = list_[i]

            ### First 
            if i == 0:
                if (item_ == None):
                    list_pad.append(0)
                else:
                    list_pad.append(item_)
            
            ### Not Frist
            else:
                if (item_ == None):
                    tmp = list_pad[i-1]
                    list_pad.append(tmp)
                else:
                    list_pad.append(item_)
        
        return list_pad


    def remove_previous_elements(self, a_list):

        ### Remove Same Element as the Previous One
        new_list = []
        src_length = len(a_list)

        for i in range(src_length):
            tmp = a_list[i]

            ### 
            if i < src_length-1:
                if a_list[i] != a_list[i+1]:
                    new_list.append(tmp)
            ### Last
            else:
                new_list.append(tmp)
                
        return new_list


### Utilities fo EB
class Util_EB(Util):


    def calc_print_area(self, points_array):

        pts = self.flatten_runtime_list(points_array)
        bbox = rg.BoundingBox(pts)
        
        return bbox.Min, bbox.Max


    def check_print_area(self, points_array):

        machine_min = [0, 0, 0]
        machine_max = [1700, 1300, 1020]
        
        print_min, print_max = self.calc_print_area(points_array)

        bbox = None
        msg = []

        ### Draw Bouinding Box
        bbox = rg.BoundingBox(print_min, print_max)

        ### Check Print Area
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

        return msg, bbox


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


    def print_preview(self, points_array):

        pls = []
        lens_ = 0.0

        for i in xrange(len(points_array)):
            pl = rg.Polyline(points_array[i])
            pls.append(pl)
            
            len_ = pl.Length
            lens_ += float(len_)
        
        lens_int = int(lens_)

        return pls, lens_int

ut = Util_EB()


class Transform():


    def pt_pt_add(self, pt0, pt1):
        pt = [
            float(pt1[0]) + float(pt0[0]),
            float(pt1[1]) + float(pt0[1]),
            float(pt1[2]) + float(pt0[2])]
        return pt


    def pt_pt_subtract(self, pt0, pt1):
        pt = [
            float(pt0[0]) - float(pt1[0]),
            float(pt0[1]) - float(pt1[1]),
            float(pt0[2]) - float(pt1[2])]
        return pt


    def vector_multiplicate(self, vector, value):
        vec = [
            float(vector[0]) * value,
            float(vector[1]) * value,
            float(vector[2]) * value]
        return vec


    def vector_unitize(self, vector):
        length = math.sqrt(
            math.pow(float(vector[0]), 2) + 
            math.pow(float(vector[1]), 2) + 
            math.pow(float(vector[2]), 2))
        new_vector = self.vector_multiplicate(vector, (1.0 / length))
        return new_vector


    def move_pt_vec(self, pt, vec):
        p = [
            float(pt[0]) + float(vec[0]),
            float(pt[1]) + float(vec[1]),
            float(pt[2]) + float(vec[2])]
        return p

tr = Transform()


class Curve():


    def polyline_to_points(self, polyline):

        ########## NEW CODE ##########

        ### Polyline to Points by RhinoCommon
        pl = rs.coercegeometry(polyline)
        new_pl = rg.PolylineCurve.ToPolyline(pl)
        points = new_pl.ToArray()

        ########## NEW CODE ##########


        """
        ########## OLD CODE 1 ##########

        points = []

        ### Start Point
        start_pt = rs.CurveStartPoint(polyline)
        points.append(start_pt)

        ### Segment Points
        ### Style : 3 = C2 - Continuous first and second derivative
        segments = rs.CurveDiscontinuity(polyline, 3)
        for j in range(len(segments)):
            points.append(segments[j])

        ### End Point
        end_pt =  rs.CurveEndPoint(polyline)
        points.append(end_pt)

        ########## OLD CODE 1 ##########

        ########## OLD CODE 2 ##########
        
        ### Polyline to Points by rhinoscriptsuntax
        ### https://developer.rhino3d.com/api/RhinoScriptSyntax/#collapse-PolylineVertices
        
        points = rs.PolylineVertices(polyline)
        
        ########## OLD CODE 2 ##########
        """
        
        return points


    def polylines_to_points(self, polylines):

        points_array = []

        for i in xrange(len(polylines)):

            points = self.polyline_to_points(polylines[i])
            points_array.append(points)

        return points_array


    def offset_z_points(self, points, z_offset_value):

        move_vec = [0, 0, z_offset_value]

        points_off = []

        for i in xrange(len(points)):
            sub = []
            tmp = points[i]
            for j in xrange(len(tmp)):
                pt = tmp[j]
                ### offset
                X, Y, Z = tr.move_pt_vec(pt, move_vec)
                pt_off = rg.Point3d(X, Y, Z)
                sub.append(pt_off)
            points_off.append(sub)
        
        return points_off


    def offset_z_curves(self, curves, z_offset_value):

        move_vec = rs.CreateVector(0, 0, z_offset_value)
        geos_off = rs.MoveObjects(curves, move_vec)
        
        return geos_off

op_c = Curve()



##########

##########


ghenv.Component.Message = '(1) Polylines to Points / 200912'


### Z OFFSET
offset_curves = op_c.offset_z_curves(POLYLINES, Z_OFFSET_VALUE)
#DEV = offset_curves
INFO = Z_OFFSET_VALUE


### Polylines to Points
pts = op_c.polylines_to_points(offset_curves)
POINTS = pts


### Machine Info
mach = ut.draw_machine()
MACHINE = mach

### Print Area Check
msg, bbox = ut.check_print_area(pts)
MESSAGE = msg

### Print Preview
if __PRINT_PREVIEW == True:
    print_crvs, print_len = ut.print_preview(pts)
    __PRINT_BBOX = bbox
    __PRINT_CURVES = print_crvs
    __PRINT_LENGTH = print_len
