import datetime
import math
import rhinoscriptsyntax as rs


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
        file_path = dir_path + now + ".txt"

        ### Export
        with open(file_path, 'w') as f:
            f.write(txt)

        print("Export GCode : {}".format(file_path))

ut = Util()



class Curve():

    def polyline_to_points(self, polyline):

        points = []

        ### Start Point
        start_pt = rs.CurveStartPoint(polyline)
        points.append(start_pt)


        ### Segment Points / Style : 4 = G1
        segments = rs.CurveDiscontinuity(polyline, 4)
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

gc = Curve()


class Gcode():

    def gcode_start(self):
        return "( == gcode start == )\n%\nG90\nG54\n( == gcode start == )\n( = )\n"


    def gcode_end(self):
        return "( == gcode end == )\nS0\nM5\nG1 Z50.0\nM30\n%\n( == gcode end == )\n"

    def define_print_info(self):
        now = ut.get_current_time()
        return "( = Polyline to Gcode by Grasshopper = )\n( = For EB 3D Printer = )\n( = Export : {} = )\n( = )\n".format(now)

    def define_extrude_filament(self, parge_value):
        return "( ==== Start Printing ==== )\n( == Extrude Filament == )\nM3 S{} P1\n".format(parge_value)

    def define_stop_filament(self, reverse_value):
        return "( == Stop Filament == )\nM4 S{} P1\n".format(reverse_value)

    def define_travel(self, current_z):
        ### buffer (mm)
        Z_BUFFER = float(25)
        new_z = str(float(current_z) + Z_BUFFER)
        return ("( == Travel == )\nG1 Z{}\n( = )\n".format(new_z))

    def points_to_gcode(self,points, m3_s, m4_s, f):

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
        txt.append(self.define_stop_filament(m4_s))

        ### travel
        txt.append(self.define_travel(cz))

        txt_join = "".join(txt)

        return txt_join

    def points_list_to_gcode(self, points_list, m3_s, m4_s, f):
        
        export = []

        ### msg
        export.append(self.define_print_info())

        ### gcode start
        export.append(self.gcode_start())

        ### gcode
        for i in xrange(len(points_list)):
            
            pts = points_list[i]

            export.append("( ========= Layer : {} ========= )\n".format(i + 1))
            export.append(self.points_to_gcode(pts, m3_s, m4_s, f))
        
        ### gcode end
        export.append(self.gcode_end())

        export_join = "".join(export)

        return export_join

gg = Gcode()




####################




### Polylines to Points
pts = gc.polylines_to_points(POLYLINES)
POINTS = ut.flatten_runtime_list(pts)

### Points to Gcode
gcode = gg.points_list_to_gcode(pts, M3_S_VALUE, M4_S_VALUE, F_VALUE)



if EXPORT == True:
    ut.export_gcode(EXPORT_DIR, gcode)

