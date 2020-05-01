import rhinoscriptsyntax as rs

from . import util
ut = util.Util()
reload(util)


class ViewerBig():
    
    
    def open_file(self, path):
        with open(path) as f:
            l = f.readlines()
        # print(type(l))
        # print(len(l))
        # print(l)
        return l


    def get_value_g1(self, str_):
        
        ### Split Elements
        elements = str_.split()

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

        return [xx, yy, zz, None]


    def get_value_g28(self, str_):
        
        ### G28 = Machine Origin
        mo_x, mo_y, mo_z = [0, 0, 1300]

        ### Split Elements
        elements = str_.split()

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

        ### G28 = Macine Origin
        if xx != None:
            xxx = mo_x - xx
        else:
            xxx = None
        if yy != None:
            yyy = mo_y - yy
        else:
            yyy = None
        
        if zz != None:
            zzz = mo_z - zz
        else:
            zzz = None

        return [xxx, yyy, zzz, None]


    # def get_value_m3(self, str_):


    # def get_value_m4(self, str_):


    def gcode_oprate(self, gcode_line):

        none_list = [None, None, None, None]

        ### Move
        if ("G1" in gcode_line) or ("G01" in gcode_line):
            return self.get_value_g1(gcode_line)

        ### Commment Out
        elif ("(" in gcode_line) or ("%" in gcode_line):
            return none_list

        ### Print Start
        elif ("M3" in gcode_line) or ("M03" in gcode_line):
            # return "m3"
            return none_list

        ### Print Stop
        elif ("M4" in gcode_line) or ("M04" in gcode_line):
            # return "m4"
            return none_list

        ### Move G28
        elif ("G28" in gcode_line):
            # self.get_value_g28(gcode_line
            return none_list

        ### Setting G
        elif ("G4" in gcode_line) or ("G49" in gcode_line) or ("G54" in gcode_line) or ("G80" in gcode_line) or ("G90" in gcode_line) or ("G91" in gcode_line):
            return none_list

        ### Setting M
        elif ("M5" in gcode_line) or ("M7" in gcode_line) or ("M55" in gcode_line):
            return none_list
        
        ### Print S0
        elif ("S0" in gcode_line):
            return none_list

        else:
            return none_list
            # return "BUG"


    def gcode_to_array(self, path):

        ### open gcode
        gcode = self.open_file(path)

        ### Get Vaules from gcode
        values = []
        for i in xrange(len(gcode)):
            gcode_line = gcode[i]
            elements = self.gcode_oprate(gcode_line)

            ### DEBUG
            # if (elements == "BUG"):
            #     print(i, gcode_line)
            ### DEBUG

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
        # print(len(gcode_values))

        return gcode_values


    def draw_path(self, values_4):

        ### Draw All Path
        pts = []
        for i in xrange(len(values_4)):
            x, y, z, s = values_4[i]
            pt = [x, y, z]
            pts.append(pt)
        
        return pts