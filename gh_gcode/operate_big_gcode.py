import rhinoscriptsyntax as rs

from . import util
ut = util.Util()
reload(util)


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
        ### M4
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
