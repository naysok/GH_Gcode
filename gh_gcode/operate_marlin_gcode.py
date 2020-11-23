import rhinoscriptsyntax as rs

from . import util
ut = util.Util()
reload(util)


class MarlinGcode():


    def define_msg(self):
        return "; Polyline to Gcode by Grasshopper\n; For Mariln 3D Printer\n; ---\n"


    def define_print_parameter(self, component, e_amp, feed, temp_nozzle, temp_bed, fan, z_zuffer):
        
        ### Time Stamp
        now = ut.get_current_time()
        time = "; Export Time : {}\n".format(now)
        
        line_0 = "; ---\n"
        
        ### Print Parameter
        print_comp = "; Component Info : {}\n".format(component)
        print_e_amp = "; E_AMP : {}\n".format(str(e_amp))
        print_feed = "; FEED : {}\n".format(str(feed))
        print_temp_nozzle = "; TEMP_NOZZLE : {}\n".format(str(temp_nozzle))
        print_temp_bed = "; TEMP_BED : {}\n".format(str(temp_bed))
        print_fan = "; FAN : {}\n".format(str(fan))
        print_z_buffer = "; Z_BUFFER : {}\n".format(str(z_zuffer))
        
        line_1 = "; ---\n"
        
        print_prm = [time, line_0, print_comp, print_e_amp, print_feed, 
            print_temp_nozzle, print_temp_bed, print_fan, print_z_buffer, line_1]

        print_prm_join = "".join(print_prm)

        return print_prm_join


    def define_general_settings(self):

        ### G90 - Absolute Positioning
        set_g90 = "G90\n"

        ### M82 - E Absolute
        set_m82 = "M82\n"

        ### Set Tool
        set_t0 = "T0\n"

        settings = [set_g90, set_m82, set_t0]
        
        settings_join = "".join(settings)

        return settings_join


    def start_fan(self, fan):
        
        ### M106 - Set Fan Speed
        set_fan = "M106 S{} ; Set - Fan\n".format(str(fan))
        return set_fan


    def start_bed(self, temp_bed):
        
        ### M140 - Set Bed Temperature
        ### M190 - Wait for Bed Temperature

        set_temp_bed = "M140 S{} ; Set - Temp Bed\n".format(str(temp_bed))

        if float(temp_bed) < 40:
            return set_temp_bed

        else:
            wait_temp_bed = "M190 S{} ; Wait - Temp Bed\n".format(str(temp_bed))
            return set_temp_bed + wait_temp_bed


    def start_extruder(self, temp_nozzle):

        ### M104 - Set Hotend Temperature
        ### M109 - Wait for Hotend Temperature
        
        set_temp_extruder = "M104 S{} T0 ; Set - Temp Extruder\n".format(str(temp_nozzle))
        wait_temp_extruder = "M109 S{} T0 ; Wait - Temp Extruder\n".format(str(temp_nozzle))

        return set_temp_extruder + wait_temp_extruder


    def homing_all_axes(self):
        
        ### G28 - Auto Home
        homing = "G28 ; Homing\n"
        return homing 



    ###########



    def points_list_to_gcode(self, points, component, e_amp, feed, temp_nozzle, temp_bed, fan, z_zuffer):
        
        ### RUN ALL
        export = []

        ### Msg, Parameters
        export.append(self.define_msg())
        export.append(self.define_print_parameter(component, e_amp, feed, temp_nozzle, temp_bed, fan, z_zuffer))

        ### General Setting
        export.append(self.define_general_settings())

        ### Start Fan
        export.append(self.start_fan(fan))

        ### Start Bed
        export.append(self.start_bed(temp_bed))
        
        ### Start Extruder
        export.append(self.start_extruder(temp_nozzle))

        ### Homing
        export.append(self.homing_all_axes())


        ### JOIN
        export_join = "".join(export)

        return export_join