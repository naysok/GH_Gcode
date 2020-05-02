import rhinoscriptsyntax as rs

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

        elements = new_str.split()

        ### init
        xx = None
        yy = None
        zz = None
        
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

        return [xx, yy, zz]


    def gcode_oprate_move(self, gcode_line):

        none_list = [None, None, None]

        ### Move
        if ("G0" in gcode_line) or \
            ("G1" in gcode_line) or \
            ("G00" in gcode_line) or \
            ("G01" in gcode_line):
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
            elements = self.gcode_oprate_move(gcode_line)

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


    def draw_path(self, values_4):

        ### Draw All Path
        pts = []
        for i in xrange(len(values_4)):
            x, y, z = values_4[i]
            pt = [x, y, z]
            pts.append(pt)
        
        return pts

