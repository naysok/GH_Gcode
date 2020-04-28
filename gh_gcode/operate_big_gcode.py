import rhinoscriptsyntax as rs

from . import util
ut = util.Util()
reload(util)


class Gcode():


    def gcode_start(self):
        return "( == gcode start == )\n%\nG90\nG54\n( == gcode start == )\n( --- )\n"


    def gcode_end(self):
        return "( == gcode end == )\nS0\nM5\nG1 Z50.0\nM30\n%\n( == gcode end == )\n"


    def define_print_msg(self):
        return "( Polyline to Gcode by Grasshopper )\n( For EB 3D Printer )\n( --- )\n"


    def define_print_parameter(self, f, m3, m4, z_offset, stop_time, z_buffer):
        now = ut.get_current_time()
        return "( Export : {} )\n( F Value : {} )\n( M3 S Value: {} )\n( M4 S Value : {} )\n( M4 Stop Time : {} )\n( Z Offset Value : {} )\n( --- )\n".format(now, f, m3, m4, stop_time, z_offset)


    def define_extrude_filament(self, parge_value):
        return "( ==== Start Printing ==== )\n( == Extrude Filament == )\nM3 S{} P1\n".format(parge_value)


    def define_stop_filament(self, reverse_value, stop_time):
        return "( == Stop Filament == )\nM4 S{} P1\nG4 X{}\nS0\n".format(reverse_value, stop_time)


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


        ### gcode
        for i in xrange(len(points_list)):
            
            pts = points_list[i]

            export.append("( ========= Layer : {} ========= )\n".format(i + 1))
            export.append(self.points_to_gcode(pts, m3_s, m4_s, f, stop_time, z_buffer))
        

        ### gcode end
        export.append(self.gcode_end())


        export_join = "".join(export)


        return export_join
