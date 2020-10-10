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


class BigGcode():


    def gcode_start(self):
        ### Original
        ### Go Through Machine Origin, Gcode Start
        return "%\nG91 ( == gcode start == )\nG28 Z0.000\nG28 X0.000 Y0.000\nG49\nG80\nG90\nG54\n"


    def gcode_start_no_origin(self):
        ### Not Go Through Machine Origin, Gcode Start
        return "%\nG91 ( == gcode start == )\nG49\nG80\nG90\nG54\n"


    def head1_start(self, m7_tf):
        ### Select M7 (Nozzle Fan) ON-OFF
        if str(m7_tf) == "0":
            return "M55 ( === head1 start ===)\nM3 S0 P1\nM7\n"
        else:
            return "M55 ( === head1 start ===)\nM3 S0 P1\n"


    def head2_start(self):
        return "( === head2 start ===)\nM57\nM13 S0 P2\nM7\n( === head2 start ===)\n( - )\n"


    def gcode_end(self):
        ### Original
        ### Go Through Machine Origin, Gcode End
        return "\nM3 S0 ( == gcode end == )\nM5\nG91\nG28 Z0\nG28 X0 Y0\nM30\n%\n( == gcode end == )\n"


    def gcode_end_no_origin(self):
        ### Not Go Through Machine Origin, Gcode End
        return "M3 S0 ( == gcode end == )\nM5\nG91\nG28 Z0\nM30\n%\n"


    def define_print_msg(self):
        return "( Polyline to Gcode by Grasshopper )\n( For EB 3D Printer )\n( --- )\n"


    def define_print_parameter(self, component, f, m3, m4, z_offset, stop_time, z_buffer):

        now = ut.get_current_time()
        time = "( Export : {} )\n".format(now)
        comp_info = "( Component Info : {} )\n".format(component)
        ### M4
        # values = "( F Value : {} )\n( M3 S Value: {} )\n( M4 S Value : {} )\n( M4 Stop Time : {} )\n( Z Offset Value : {} )\n".format(f, m3, m4, stop_time, z_offset)
        ### M4 Removed
        values = "( F Value : {} )\n( M3 S Value: {} )\n( Z Offset Value : {} )\n".format(f, m3, z_offset)
        line = "( --- )\n"

        return time + comp_info + values + line


    def define_extrude_filament(self, parge_value):
        return "M3 S{} P1 ( == Extrude Filament == )\n".format(parge_value)


    def define_stop_filament(self, reverse_value, stop_time):
        ### M4 (Reversed)
        # return "( == Stop Filament == )\nM4 S{} P1\nG4 X{}\nM3 S0\n".format(reverse_value, stop_time)
        ### M3
        return "M3 S0 ( == Stop Filament == )\n"


    def define_travel(self, current_z, z_buffer):
        ### buffer (mm)
        Z_BUFFER = float(z_buffer)
        new_z = str(float(current_z) + Z_BUFFER)
        return ("G1 Z{} ( == Travel == )\n".format(new_z))


    def points_to_gcode(self, layer_info, points, m3_s, m4_s, f, stop_time, z_buffer):

        txt = []

        ### Printing
        for i in xrange(len(points)):
            _px, _py, _pz = points[i]
            px = str("{:f}".format(_px))
            py = str("{:f}".format(_py))
            pz = str("{:f}".format(_pz))

            ### Add Layer Info on First Layer
            if i == 0:
                txt.append("G1 X{} Y{} Z{} F{} {}\n".format(px, py, pz, f, layer_info))
            else:
                txt.append("G1 X{} Y{} Z{} F{}\n".format(px, py, pz, f))

            ### Extrude Filament
            if i == 0:
                ### M3
                txt.append(self.define_extrude_filament(m3_s))

            ### get current z
            if i == (len(points) - 1):
                _cx, _cy, _cz = points[i]
                cz = "{:f}".format(_cz)

        ### Printting Stop
        ### M3 S0
        txt.append(self.define_stop_filament(m4_s, stop_time))

        ### Travel
        txt.append(self.define_travel(cz, z_buffer))

        txt_join = "".join(txt)

        return txt_join


    # def points_list_to_gcode(self, points_list, comp_info, m3_s, m3_s_1st, m4_s, f, f_1st,  z_offset, stop_time, z_buffer):
    #
    #    ### Go Through Machine Origin
    #
    #     export = []
    #
    #     ### print msg, print parameter
    #     export.append(self.define_print_msg())
    #     export.append(self.define_print_parameter(comp_info, f, m3_s, m4_s, z_offset, stop_time, z_buffer))
    #
    #     ### gcode start
    #     export.append(self.gcode_start())
    #
    #     ### head1 start
    #     export.append(self.head1_start())
    #
    #     ### gcode
    #     for i in xrange(len(points_list)):
    #
    #         pts = points_list[i]
    #         layer_info = "( ========= Layer : {} ========= )".format(i + 1)
    #
    #         ### Fisrt Layer
    #         if i == 0:
    #             export.append(self.points_to_gcode(layer_info, pts, m3_s_1st, m4_s, f_1st, stop_time, z_buffer))
    #
    #         ### Second - Last Layer
    #         else:
    #             export.append(self.points_to_gcode(layer_info, pts, m3_s, m4_s, f, stop_time, z_buffer))
    #
    #     ### gcode end
    #     export.append(self.gcode_end())
    #
    #     export_join = "".join(export)
    #
    #     return export_join


    def points_list_to_gcode_no_origin(self, points_list, comp_info, m7_tf, m3_s, m3_s_1st, m4_s, f, f_1st,  z_offset, stop_time, z_buffer):
        
        ### Not Go Through Machine Origin

        export = []

        ### print msg, print parameter
        export.append(self.define_print_msg())
        export.append(self.define_print_parameter(comp_info, f, m3_s, m4_s, z_offset, stop_time, z_buffer))

        ### gcode start
        export.append(self.gcode_start_no_origin())

        ### head1 start
        export.append(self.head1_start(m7_tf))

        ### gcode
        for i in xrange(len(points_list)):
            
            pts = points_list[i]
            layer_info = "( ========= Layer : {} ========= )".format(i + 1)
            
            ### Fisrt Layer
            if i == 0:
                export.append(self.points_to_gcode(layer_info, pts, m3_s_1st, m4_s, f_1st, stop_time, z_buffer))
            
            ### Second - Last Layer
            else:
                export.append(self.points_to_gcode(layer_info, pts, m3_s, m4_s, f, stop_time, z_buffer))
        
        ### gcode end
        export.append(self.gcode_end_no_origin())

        export_join = "".join(export)

        return export_join


### Attribute Mode
class BigGcodeAttribute(BigGcode):


    def points_to_gcode_attribute(self, layer_info, points, weight, m3_s, m4_s, f, stop_time, z_buffer):

        txt = []

        ### Printing
        for i in xrange(len(points)):
            _px, _py, _pz = points[i]
            _w = float(weight[i])
            _m3 = float(m3_s)

            px = str("{:f}".format(_px))
            py = str("{:f}".format(_py))
            pz = str("{:f}".format(_pz))
            ss = str("{}".format(int(_m3 * _w)))

            ### Add Layer Info on First Layer
            if i == 0:
                txt.append("G1 X{} Y{} Z{} F{} {}\n".format(px, py, pz, f, layer_info))
            else:
                txt.append("G1 X{} Y{} Z{} F{} S{}\n".format(px, py, pz, f, ss))

            ### Extrude Filament
            if i == 0:
                ### M3
                txt.append(self.define_extrude_filament(m3_s))

            ### get current z
            if i == (len(points) - 1):
                _cx, _cy, _cz = points[i]
                cz = "{:f}".format(_cz)

        ### Printting Stop
        ### M3 S0
        txt.append(self.define_stop_filament(m4_s, stop_time))

        ### Travel
        txt.append(self.define_travel(cz, z_buffer))

        txt_join = "".join(txt)

        return txt_join


    def points_list_to_gcode_no_origin_attribute(self, points_list, weight_list, comp_info, m7_tf, m3_s, m3_s_1st, m4_s, f, f_1st,  z_offset, stop_time, z_buffer):
        
        ### Not Go Through Machine Origin

        export = []

        ### print msg, print parameter
        export.append(self.define_print_msg())
        export.append(self.define_print_parameter(comp_info, f, m3_s, m4_s, z_offset, stop_time, z_buffer))

        ### gcode start
        export.append(self.gcode_start_no_origin())

        ### head1 start
        export.append(self.head1_start(m7_tf))

        ### gcode with Attribute
        for i in xrange(len(points_list)):
            
            pts = points_list[i]
            weight = weight_list[i]

            layer_info = "( ========= Layer : {} ========= )".format(i + 1)
            
            ### Fisrt Layer
            if i == 0:
                export.append(self.points_to_gcode_attribute(layer_info, pts, weight, m3_s_1st, m4_s, f_1st, stop_time, z_buffer))
            
            ### Second - Last Layer
            else:
                export.append(self.points_to_gcode_attribute(layer_info, pts, weight, m3_s, m4_s, f, stop_time, z_buffer))
        
        ### gcode end
        export.append(self.gcode_end_no_origin())

        export_join = "".join(export)

        return export_join


op_bg = BigGcode()
op_bg_at = BigGcodeAttribute()



##########


ghenv.Component.Message = 'Points to gcode with Attribute / 201010'


comp_info = "Attribute_201010"
Z_OFFSET_VALUE = INFO
M4_S_VALUE = 0
M4_STOP_TIME = 0


### Points to Gcode (Not Go Through Machine Origin)
if RUN_AND_EXPORT:
    gcode = op_bg_at.points_list_to_gcode_no_origin_attribute(POINTS, WEIGHT, comp_info, M7_ON, M3_S_VALUE, M3_S_VALUE_1st, M4_S_VALUE, F_VALUE, F_VALUE_1st, Z_OFFSET_VALUE, M4_STOP_TIME, Z_BUFFER)
    ut.export_gcode(EXPORT_DIR, gcode)
