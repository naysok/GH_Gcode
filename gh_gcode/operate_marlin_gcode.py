import rhinoscriptsyntax as rs

from . import util
ut = util.Util()
reload(util)


class MarlinGcode():


    def define_msg(self):
        return "; Polyline to Gcode by Grasshopper\n; For Mariln 3D Printer\n; ---\n"


    def define_print_parameter(self, component, e_amp, feed, temp_nozzle, temp_bed, z_zuffer):
        
        ### Time Stamp
        now = ut.get_current_time()
        time = "; Export Time : {}\n".format(now)
        
        line_0 = "; ---\n"
        
        ### Print Parameter
        print_comp = "; Component Info : {}\n".format(component)
        print_e_amp = "; E_AMP : {}\n".format(e_amp)
        print_feed = "; FEED : {}\n".format(feed)
        print_temp_nozzle = "; TEMP_NOZZLE : {}\n".format(temp_nozzle)
        print_temp_bed = "; TEMP_BED : {}\n".format(temp_bed)
        print_z_buffer = "; Z_BUFFER : {}\n".format(z_zuffer)
        
        line_1 = "; ---\n"
        
        print_prm = [time, line_0, print_comp, print_e_amp, print_feed, 
            print_temp_nozzle, print_temp_bed, print_z_buffer, line_1]

        print_prm_join = "".join(print_prm)

        return print_prm_join


    # def setting_g90(self):

    #     ### G90
    #     set_g90 = "G90\n"

    #     return set_g90


    # def wait_bed_temp(self, temp_bed):

    #     ### M190 ; Wait for Bed Temperature
    #     ### ex) M190 S60

    #     wait_bed = "M190 S{} ; Set Bed-Temp\n".format(temp_bed)

    #     return wait_bed


    # def set_extruder_Temp(self, temp_extruder):

    #     ### M104 ; Set Extruder Temperature
    #     ### ex) M104 S200 (PLA)

    #     set_extruder = "M104 S{} ; Set Extruder-Temp\n".format(temp_extruder)

    #     return set_extruder
    

    # def wait_extruder_temp(self, temp_extruder):

    #     ### M109 : Wait for Extruder Temperature
    #     ### ex) M109 S200

    #     wait_extruder = "M109 S{} ; Wait Extruder-Temp\n".format(temp_extruder)

    #     return wait_extruder
    

    # def set_extruder_mode(self):

    #     ### M83 : Set Extruder to Relative Mode
        
    #     extruder_mode = "M83 ; Relative Extrusion Mode\n"

    #     return extruder_mode



    def points_list_to_gcode(self, points, component, e_amp, feed, temp_nozzle, temp_bed, z_zuffer):
        
        ### RUN ALL
        export = []

        ### Msg
        export.append(self.define_msg())
        export.append(self.define_print_parameter(component, e_amp, feed, temp_nozzle, temp_bed, z_zuffer))


        
        export_join = "".join(export)

        return export_join