from . import util
ut = util.Util()
reload(util)


class ViewerMarlin():
    
    
    def open_file(self, path):
        with open(path) as f:
            l = f.readlines()
        # print(type(l))
        # print(len(l))
        # print(l)
        return l


    def get_value_move(self, str_):
        
        ### Split Elements
        ### Remove n
        str_.replace("\n", "")
        
        ### Remove Comments
        if ";" in str_:
            str_rm_comment = str_.split(";")
            new_str = str_rm_comment[0]
        else:
            new_str = str_

        ### Gcode (per Line)
        # print(new_str)

        ### Sprit Space
        elements = new_str.split()

        ### init
        xx = None
        yy = None
        zz = None
        ee = None
        
        for i in xrange(len(elements)):
            elm = elements[i]

            ### Get Value
            if ("X" in elm):
                tmp_x = elm.split("X")
                xx = float(tmp_x[1])
            
            elif ("Y" in elm):
                tmp_y = elm.split("Y")
                yy = float(tmp_y[1])
            
            elif ("Z" in elm):
                tmp_z = elm.split("Z")
                zz = float(tmp_z[1])

            elif ("E" in elm):
                tmp_e = elm.split("E")
                ee = float(tmp_e[1])

        return [xx, yy, zz, ee]


    def gcode_operate_move(self, gcode_line):

        none_list = [None, None, None, None]

        ### Move
        if ("G0" in gcode_line) or \
            ("G1" in gcode_line) or \
            ("G00" in gcode_line) or \
            ("G01" in gcode_line) or \
            ("G92 E0" in gcode_line):
            ### get position
            return self.get_value_move(gcode_line)

        ### Commment Out
        elif (";" in gcode_line[0]) or (gcode_line == "\n"):
            return none_list

        ### Setting G
        elif ("G4" in gcode_line) or \
            ("G04" in gcode_line) or \
            ("G21" in gcode_line) or \
            ("G28" in gcode_line) or \
            ("G90" in gcode_line) or \
            ("G91" in gcode_line) or \
            ("G92" in gcode_line):
            
            return none_list

        ### Setting M
        elif ("M82" in gcode_line) or \
            ("M84" in gcode_line) or \
            ("M104" in gcode_line) or \
            ("M106" in gcode_line) or \
            ("M107" in gcode_line) or \
            ("M109" in gcode_line) or \
            ("M140" in gcode_line) or \
            ("M190" in gcode_line) or \
            ("M204" in gcode_line) or \
            ("M205" in gcode_line):

            return none_list
        
        ### Setting T
        elif ("T0" in gcode_line) or \
            ("T1" in gcode_line):
            return none_list

        else:
            # return none_list
            return "bug!"


    def gcode_to_array(self, path):

        ### open gcode
        gcode = self.open_file(path)

        ### Get Vaules from gcode
        values = []
        for i in xrange(len(gcode)):
            gcode_line = gcode[i]

            ### XYZE
            elements = self.gcode_operate_move(gcode_line)

            ## DEBUG ALL
            # print(i, gcode_line)
            ### DEBUG bug
            if (elements == "bug!"):
                print(i, gcode_line)
            ## DEBUG

            values.append(elements)

        ### Padding Previous Value(None)
        values_zip = ut.zip_matrix(values)
        # print(len(values_zip))
        new_values = []
        for j in xrange(len(values_zip)):
            list_ = values_zip[j]
            list_pad = ut.padding_previous_value(list_)
            new_values.append(list_pad)
        gcode_values = ut.zip_matrix(new_values)

        # print(len(values))
        # print(len(gcode_values), len(gcode_values[0]))

        return gcode_values


    def segment_extrude(self, xyze):

        ### Segment Print / Travel
        ### https://docs.google.com/spreadsheets/d/1S4SQ-NT09Nh8sb3Lg6FSauKB1rZPMwLSDjvnrKerXFs/edit?usp=sharing
        array_seg = []
        list_seg = []

        for j in xrange(len(xyze)):

            xxx, yyy, zzz, eee = xyze[j]
            item = [xxx, yyy, zzz]
            
            # print(j)
            # print(j, xyze[j])

            ### Index[0]
            if (j == 0):
                
                x1, y1, z1, e1 = xyze[j]
                x2, y2, z2, e2 = xyze[j + 1]

                bool_b = e1 < e2

                if (bool_b == True):
                    list_seg = []
                    list_seg.append(item)
                
            ### Index[0] - Index[Last - 1]
            elif (j > 0) and (j < (len(xyze) - 1)):

                x0, y0, z0, e0 = xyze[j - 1]
                x1, y1, z1, e1 = xyze[j]
                x2, y2, z2, e2 = xyze[j + 1]

                bool_a = e0 < e1
                bool_b = e1 < e2

                if (bool_a == False) and (bool_b == True):
                    list_seg = []
                    list_seg.append(item)

                elif (bool_a == True) and (bool_b == True):
                    list_seg.append(item)

                elif (bool_a == True) and (bool_b == False):
                    list_seg.append(item)
                    array_seg.append(list_seg)

                elif (bool_a == False) and (bool_b == False):
                    pass

                else:
                    print("Error!!")
            
            ### Index[Last]
            elif (j == (len(xyze) - 1)):
                
                x0, y0, z0, e0 = xyze[j - 1]
                x1, y1, z1, e1 = xyze[j]

                bool_a = e0 < e1
                
                if (bool_a == True):
                    list_seg.append(item)
                    array_seg.append(list_seg)

        # print(array_out)

        return array_seg


    def remove_invalid_polylines(self, array_seg):

        ### Remove Invalid Polylines (Remove Same Element as the Previous One)
        layers = []

        for k in xrange(len(array_seg)):
            tmp_layer = array_seg[k]
            tmp_removed = ut.remove_previous_elements(tmp_layer)
            
            if len(tmp_removed) != 1:
                layers.append(tmp_removed)

        return layers


    def draw_path(self, values_4):

        ### Remove Same Element as the Previous One
        xyze = ut.remove_previous_elements(values_4)
        ### print(len(values_4), len(xyze))

        ### Segment Print / Travel
        array_seg = self.segment_extrude(xyze)

        ### Remove Invalid Polylines (Remove Same Element as the Previous One)
        layers = self.remove_invalid_polylines(array_seg)

        """
        ### Draw All Path
        pts = []
        for i in xrange(len(xyze)):
            x, y, z, e = values_4[i]
            pt = [x, y, z]
            pts.append(pt)
        """

        return layers

