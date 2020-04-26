import rhinoscriptsyntax as rs

from . import util
ut = util.Util()
reload(util)


class Gcode():


    def gcode_start(self):
        return "( == gcode start == )\n%\nG90\nG54\n( == gcode start == )\n( = )\n"


    def gcode_end(self):
        return "( == gcode end == )\nS0\nM5\nG1 Z50.0\nM30\n%\n( == gcode end == )\n"


    def define_print_info(self):
        now = ut.get_current_time()
        return "( = Polyline to Gcode by Grasshopper = )\n( = For EB 3D Printer = )\n( = Export : {} = )\n( = )\n".format(now)


    def define_extrude_filament(self, parge_value):
        return "( == Extrude Filament == )\nM3 S{} P1\n".format(parge_value)


    def define_stop_filament(self, reverse_value):
        return "( == Stop Filament == )\nM4 S{} P1\n".format(reverse_value)


    def define_travel(self, current_z):
        ### buffer (mm)
        Z_BUFFER = float(25)
        new_z = str(float(current_z) + Z_BUFFER)
        return ("( == Travel == )\nG1 Z{}\n( = )\n".format(new_z))


    def points_to_gcode(self,points, m3_s, m4_s, f):

        txt = []

        ### Printing Start
        ### M3
        txt.append(self.define_extrude_filament(m3_s))


        ### Printing
        txt.append("( ==== Start Printing ==== )\n")

        for i in xrange(len(points)):
            _px, _py, _pz = points[i]
            px = str("{:f}".format(_px))
            py = str("{:f}".format(_py))
            pz = str("{:f}".format(_pz))

            txt.append("G1 X{} Y{} Z{} F{}\n".format(px, py, pz, f))

            ### get current z
            if i == (len(points) - 1):
                _cx, _cy, _cz = points[i]
                cz = "{:f}".format(_cz)

        txt.append("( ==== Stop Printing ==== )\n")


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
