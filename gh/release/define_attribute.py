import rhinoscriptsyntax as rs
import Rhino.Geometry as rg

import datetime
import math


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


    def bitwise_or_arrays(self, arrays):

        ### Merge Bool from Brep.isPointInside

        # print(len(arrays[0]))
        # print(len(arrays[0][0]))

        if len(arrays) == 1:
            return arrays[0]

        else:
            arrays_zip = self.zip_matrix(arrays)
            # print(len(arrays_zip))
            # print(len(arrays_zip[0]))
            # print(len(arrays_zip[0][0]))

            bool_inside = []

            for i in xrange(len(arrays_zip)):
                # print(i)

                sub_ = []

                item = arrays_zip[i]
                item_zip = self.zip_matrix(item)

                # print(len(item_zip))
                # print(len(item_zip[0]))

                for j in xrange(len(item_zip)):

                    values = item_zip[j]
                    
                    if True in values:
                        sub_.append(True)
                    else:
                        sub_.append(False)

                bool_inside.append(sub_)

            # print(len(bool_inside))
            # print(len(bool_inside[0]))

            return bool_inside



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


class Attribute():


    def __init__(self):
        pass

    
    def points_in_brep(self, brep, points):

        bool_in = []

        for i in xrange(len(points)):
            pp = points[i]
            sub_bool = []
            
            for j in xrange(len(pp)):
                p = pp[j]
        
                ### Segment Point with Brep.IsPointInside
                ### https://developer.rhino3d.com/api/RhinoCommon/html/M_Rhino_Geometry_Brep_IsPointInside.htm
                sub_bool.append(rg.Brep.IsPointInside(brep, p, 0.01, True))
            
            bool_in.append(sub_bool)
        
        return bool_in


    def points_in_breps(self, breps, points):

        ### Segment Points with Brep.IsPointInside

        bool_array = []

        for i in xrange(len(breps)):
            brep = breps[i]
            brep_geo = rs.coercebrep(brep)

            bool_array.append(self.points_in_brep(brep_geo, points))

        ### Arrays
        # print(len(bool_array))
        bool_inside = ut.bitwise_or_arrays(bool_array)

        return bool_inside
    

    def define_attribute(self, bool_inside, weight_value):
        
        ### Define Attribute-Value (Weight)
        ### For Attribute Mode

        new_values = []

        for i in xrange(len(bool_inside)):
            bb = bool_inside[i]
            
            sub_ = []

            for j in xrange(len(bb)):
                b = bb[j]

                ### Inside
                if b:
                    sub_.append(float(weight_value))
                
                else:
                    sub_.append(1.0)
        
            new_values.append(sub_)
        
        return new_values
    

    def render_attribute(self, points, bool_inside):
        
        ### Render Attribute-Values

        render = []
        pts_weighting = []

        for i in xrange(len(points)):
            pp = points[i]
            bb = bool_inside[i]

            sub_render = []
            
            for j in xrange(len(pp)):
                p = pp[j]
                b = bb[j]

                if b:
                    sub_render.append(rs.AddCircle(p, 0.5))
                    pts_weighting.append(p)

                else:
                    sub_render.append(rs.AddCircle(p, 4))
            
            render.append(sub_render)
        
        return render, pts_weighting


op_a = Attribute()


################################


ghenv.Component.Message = 'Define Attribute / 201010'


points = IN_POINTS
breps = IN_BREPS
weight = float(WEIGHT_FACTOR)


### Segment Inside / OutSide
bool_inside = op_a.points_in_breps(breps, points)


### Calc
weight_values = op_a.define_attribute(bool_inside, weight)

OUT_INFO = IN_INFO
OUT_POINTS = points
OUT_WEIGHT = weight_values


### Render
render_circle, render_pts = op_a.render_attribute(points, bool_inside)


if __DRAW:
    __DRAW_POINTS = ut.flatten_runtime_list(points)

if __RENDER:
    __RENDER_ATTRIBUTE = ut.flatten_runtime_list(render_circle)
    __RENDER_PTS = render_pts
