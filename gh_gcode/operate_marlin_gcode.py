import math

import rhinoscriptsyntax as rs

from . import util
ut = util.Util()
reload(util)


class MarlinGcode():


    def define_msg(self):
        return "; Polyline to Gcode by Grasshopper\n; For Mariln 3D Printer\n"


    def define_print_parameter(self, component, e_amp, feed, temp_nozzle, temp_bed, fan, z_zuffer):
        
        line = "; ----- Print Parameter -----\n"

        ### Time Stamp
        now = ut.get_current_time()
        time = "; Export Time : {}\n".format(now)
        
        ### Print Parameter
        print_comp = "; Component Info : {}\n".format(component)
        print_e_amp = "; E_AMP : {}\n".format(str(e_amp))
        print_feed = "; FEED : {}\n".format(str(feed))
        print_temp_nozzle = "; TEMP_NOZZLE : {}\n".format(str(temp_nozzle))
        print_temp_bed = "; TEMP_BED : {}\n".format(str(temp_bed))
        print_fan = "; FAN : {}\n".format(str(fan))
        print_z_buffer = "; Z_BUFFER : {}\n".format(str(z_zuffer))
        
        print_prm = [line, time, print_comp, print_e_amp, print_feed, 
            print_temp_nozzle, print_temp_bed, print_fan, print_z_buffer, line]

        print_prm_join = "".join(print_prm)

        return print_prm_join


    def define_general_settings(self):

        ### G90 - Absolute Positioning
        set_g90 = "G90 ; Absolute Positioning\n"

        ### M82 - E Absolute Mode
        set_m82 = "M82 ; E Absolute Mode\n"

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


    def homing_x(self):
        
        ### G28 - Auto Home
        homing = "G28 X0 ; Homing X\n"
        return homing 


    def reset_extrude_value(self):

        ### G92 - Set Position
        reset_e = "G92 E0 ; Reset Extruder Value\n"
        return reset_e


    def calc_distance_2pt(self, x0, y0, z0, x1, y1, z1):

        ### Calc Distance
        xx = x0 - x1
        yy = y0 - y1
        zz = z0 - z1
        dist = math.sqrt((xx * xx) + (yy * yy) + (zz * zz))

        return dist


    ##################################################################


    #################################
    ###                           ###
    ###     Print Start / End     ###
    ###                           ###
    #################################


    def print_start(self, fan, temp_bed, temp_nozzle):

        start = []

        start.append("; ----- Start Code -----\n")

        ### General Setting
        start.append(self.define_general_settings())
        
        ### Start Fan
        start.append(self.start_fan(fan))

        ### Start Bed
        start.append(self.start_bed(temp_bed))

        ### Start Extruder
        start.append(self.start_extruder(temp_nozzle))

        ### Homing
        start.append(self.homing_all_axes())

        ### Reset Extruder Value
        start.append(self.reset_extrude_value())

        start.append("; ----- Start Code -----\n")

        start_join = "".join(start)

        return start_join


    def print_end(self):

        end = []

        end.append("; ----- End Code -----\n")

        ### Homing X
        end.append(self.homing_x())

        ### End Part
        end.append("M106 S0 ; turn off cooling fan\n")
        end.append("M104 S0 ; turn off extruder\n")
        end.append("M140 S0 ; turn off bed\n")
        end.append("M84 ; disable motors\n")

        end.append("; ----- End Code -----\n")

        end_join = "".join(end)

        return end_join
    

    ##################################################################


    ########################
    ###                  ###
    ###     Printing     ###
    ###                  ###
    ########################


    def travel(self, z_current, z_zuffer):

        ### Travel
        gcode = []

        cmt = "; --- Travel ---\n"

        gz = str("{:.4f}".format(z_current + float(z_zuffer)))
        trv = "G1 Z{}\n".format(gz)

        gcode.append(cmt)
        gcode.append(trv)

        gcode_join = "".join(gcode)

        return gcode_join


    def point_to_gcode(self, count, pts, e_amp, feed, z_zuffer):
        
        layer = []

        ### CR-10 / TPU
        PRINTER_PARAMETER = 0.165

        for i in xrange(len(pts)):
            p = pts[i]
            xx, yy, zz = p

            ### Index[0]
            if i == 0:

                ### Initialize
                ee = 0

                ### Layer Info (Comment)
                start_comment = "; ----- Layer : {} / start -----\n".format(count)
                layer.append(start_comment)

                ### Reset Extruder Value
                layer.append(self.reset_extrude_value())

                gx = str("{:.4f}".format(xx))
                gy = str("{:.4f}".format(yy))
                gz = str("{:.4f}".format(zz))
                gf = str("{}".format(feed))

                gcode = "G1 X{} Y{} Z{} E0 F{}\n".format(gx, gy, gz, gf)
                layer.append(gcode)

            ### Index[1] - Index[Last]
            else:
                x0, y0, z0 = pts[i - 1]
                x1, y1, z1 = pts[i]
                
                distance = self.calc_distance_2pt(x0, y0, z0, x1, y1, z1)

                ### PRINTER_PARAMETER // 1.85 to 0.4
                ### e_amp // override
                ee += (distance * float(PRINTER_PARAMETER) * float(e_amp))

                gx = str("{:.4f}".format(xx))
                gy = str("{:.4f}".format(yy))
                gz = str("{:.4f}".format(zz))
                ge = str("{:.4f}".format(ee))
                
                gcode = "G1 X{} Y{} Z{} E{}\n".format(gx, gy, gz, ge)
                layer.append(gcode)
            
                ### Index[Last]
                if i == (len(pts) - 1):

                    ### Travel
                    travel = self.travel(zz, z_zuffer)
                    layer.append(travel)

                    ### Layer Info (Comment)
                    end_comment = "; ----- Layer : {} / end -----\n".format(count)
                    layer.append(end_comment)

        ### Join
        layer_join = "".join(layer)

        return layer_join


    ##################################################################


    ##############################
    ###                        ###
    ###     Generate Gcode     ###
    ###                        ###
    ##############################


    def points_list_to_gcode(self, points_list, component, e_amp, feed, temp_nozzle, temp_bed, fan, z_zuffer):
        
        ### RUN ALL
        export = []

        ### Msg, Parameters
        export.append(self.define_msg())
        export.append(self.define_print_parameter(component, e_amp, feed, temp_nozzle, temp_bed, fan, z_zuffer))

        ### Print Start
        export.append(self.print_start(fan, temp_bed, temp_nozzle))
        
        ### Printing
        for i in xrange(len(points_list)):

            pts = points_list[i]
            layer_count = str(i)
            export.append(self.point_to_gcode(layer_count, pts, e_amp, feed, z_zuffer))

        ### Print End
        export.append(self.print_end())


        ### JOIN
        export_join = "".join(export)

        return export_join


    ##################################################################


    #############################################
    ###                                       ###
    ###     Generate Gcode with Attribute     ###
    ###                                       ###
    #############################################
        
    def point_to_gcode_w_attribute(self, count, pts, ws, e_amp, feed, z_zuffer):
        
        layer = []

        ### CR-10 / TPU
        PRINTER_PARAMETER = 0.165

        for i in xrange(len(pts)):
            p = pts[i]
            xx, yy, zz = p

            ### Index[0]
            if i == 0:

                ### Initialize
                ee = 0

                ### Layer Info (Comment)
                start_comment = "; ----- Layer : {} / start -----\n".format(count)
                layer.append(start_comment)

                ### Reset Extruder Value
                layer.append(self.reset_extrude_value())

                gx = str("{:.4f}".format(xx))
                gy = str("{:.4f}".format(yy))
                gz = str("{:.4f}".format(zz))
                gf = str("{}".format(feed))

                gcode = "G1 X{} Y{} Z{} E0 F{}\n".format(gx, gy, gz, gf)
                layer.append(gcode)

            ### Index[1] - Index[Last]
            else:
                x0, y0, z0 = pts[i - 1]
                x1, y1, z1 = pts[i]
                w = ws[i]

                distance = self.calc_distance_2pt(x0, y0, z0, x1, y1, z1)

                ### PRINTER_PARAMETER // 1.85 to 0.4
                ### e_amp // override
                ee += (distance * float(PRINTER_PARAMETER) * float(e_amp) * float(w))
                
                ### Debug
                # ee = float(w)

                gx = str("{:.4f}".format(xx))
                gy = str("{:.4f}".format(yy))
                gz = str("{:.4f}".format(zz))
                ge = str("{:.4f}".format(ee))
                
                gcode = "G1 X{} Y{} Z{} E{}\n".format(gx, gy, gz, ge)
                layer.append(gcode)
            
                ### Index[Last]
                if i == (len(pts) - 1):

                    ### Travel
                    travel = self.travel(zz, z_zuffer)
                    layer.append(travel)

                    ### Layer Info (Comment)
                    end_comment = "; ----- Layer : {} / end -----\n".format(count)
                    layer.append(end_comment)

        ### Join
        layer_join = "".join(layer)

        return layer_join


    def points_list_to_gcode_w_attribute(self, points_list, weight_list, component, e_amp, feed, temp_nozzle, temp_bed, fan, z_zuffer):
        
        ### RUN ALL
        export = []

        ### Msg, Parameters
        export.append(self.define_msg())
        export.append(self.define_print_parameter(component, e_amp, feed, temp_nozzle, temp_bed, fan, z_zuffer))

        ### Print Start
        export.append(self.print_start(fan, temp_bed, temp_nozzle))
        
        ### Printing
        for i in xrange(len(points_list)):

            pts = points_list[i]
            ws = weight_list[i]
            layer_count = str(i)
            export.append(self.point_to_gcode_w_attribute(layer_count, pts, ws, e_amp, feed, z_zuffer))

        ### Print End
        export.append(self.print_end())


        ### JOIN
        export_join = "".join(export)

        return export_join