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

ut = Util()


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
        
        return points


    def polylines_to_points(self, polylines):

        points_array = []

        for i in xrange(len(polylines)):

            points = self.polyline_to_points(polylines[i])
            points_array.append(points)

        return points_array


    def offset_z(self, points, z_offset_value):

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

gc = Curve()


class Gcode():


    def gcode_start(self):
        return "( == gcode start == )\n%\nG91\nG28 Z0.000\nG28 X0.000 Y0.000\nG49\nG80\nG90\nG5\n( == gcode start == )\n( --- )\n"


    def head_start(self):
        return "( === head1 start ===)\nM55\nM3 S0 P1\nM7\n( === head1 start ===)\n( - )\n"


    def gcode_end(self):
        return "( == gcode end == )\nS0\nM5\nG91\nG28 Z0\nG28 X0 Y0\nM30\n%\n( == gcode end == )\n"


    def define_print_msg(self):
        return "( Polyline to Gcode by Grasshopper )\n( For EB 3D Printer )\n( --- )\n"


    def define_print_parameter(self, f, m3, m4, z_offset, stop_time, z_buffer):
        now = ut.get_current_time()
        return "( Export : {} )\n( F Value : {} )\n( M3 S Value: {} )\n( M4 S Value : {} )\n( M4 Stop Time : {} )\n( Z Offset Value : {} )\n( --- )\n".format(now, f, m3, m4, stop_time, z_offset)


    def define_extrude_filament(self, parge_value):
        return "( ==== Start Printing ==== )\n( == Extrude Filament == )\nM3 S{} P1\n".format(parge_value)


    def define_stop_filament(self, reverse_value, stop_time):
        return "( == Stop Filament == )\nM4 S{} P1\nG4 X{}\nM3 S0\n".format(reverse_value, stop_time)


    def define_travel(self, current_z, z_buffer):
        ### buffer (mm)
        Z_BUFFER = float(z_buffer)
        new_z = str(float(current_z) + Z_BUFFER)
        return ("( == Travel == )\nG1 Z{}\n( - )\n".format(new_z))


    def points_to_gcode(self,points, m3_s, m4_s, f, stop_time, z_buffer):

        txt = []

        ### Printing
        for i in xrange(len(points)):
            _px, _py, _pz = points[i]
            px = str("{:f}".format(_px))
            py = str("{:f}".format(_py))
            pz = str("{:f}".format(_pz))

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
        ### M4
        txt.append(self.define_stop_filament(m4_s, stop_time))

        ### travel
        txt.append(self.define_travel(cz, z_buffer))

        txt_join = "".join(txt)

        return txt_join


    def points_list_to_gcode(self, points_list, m3_s, m4_s, f, z_offset, stop_time, z_buffer):
        
        export = []

        ### print msg, print parameter
        export.append(self.define_print_msg())
        export.append(self.define_print_parameter(f, m3_s, m4_s, z_offset, stop_time, z_buffer))

        ### gcode start
        export.append(self.gcode_start())

        ### head start
        export.append(self.head_start())

        ### gcode
        for i in xrange(len(points_list)):
            
            pts = points_list[i]

            export.append("( ========= Layer : {} ========= )\n".format(i + 1))
            export.append(self.points_to_gcode(pts, m3_s, m4_s, f, stop_time, z_buffer))
        
        ### gcode end
        export.append(self.gcode_end())

        export_join = "".join(export)

        return export_join

gg = Gcode()




##########



### Polylines to Points
pts = gc.polylines_to_points(POLYLINES)
POINTS = ut.flatten_runtime_list(pts)


### Z OFFSET
pts_off = gc.offset_z(pts, Z_OFFSET_VALUE)
DEV = ut.flatten_runtime_list(pts_off)


### Points to Gcode
gcode = gg.points_list_to_gcode(pts_off, M3_S_VALUE, M4_S_VALUE, F_VALUE, Z_OFFSET_VALUE, M4_STOP_TIME, Z_BUFFER)



if EXPORT == True:
    ut.export_gcode(EXPORT_DIR, gcode)
