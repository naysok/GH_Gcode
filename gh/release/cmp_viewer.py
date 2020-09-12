import rhinoscriptsyntax as rs
import Rhino.Geometry as rg

import datetime
import math
import time


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
        file_path = dir_path + now + ".gcode"

        ### Export
        with open(file_path, 'w') as f:
            f.write(txt)

        print("Export GCode : {}".format(file_path))


    def zip_matrix(self, mat):
        ### https://note.nkmk.me/python-list-transpose/
        return [list(x) for x in zip(*mat)]


    def padding_previous_value(self, list_):
        
        list_pad = []

        for i in xrange(len(list_)):
            
            item_ = list_[i]

            ### First 
            if i == 0:
                if (item_ == None):
                    list_pad.append(0)
                else:
                    list_pad.append(item_)
            
            ### Not Frist
            else:
                if (item_ == None):
                    tmp = list_pad[i-1]
                    list_pad.append(tmp)
                else:
                    list_pad.append(item_)
        
        return list_pad


    def remove_previous_elements(self, a_list):

        ### Remove Same Element as the Previous One
        new_list = []
        src_length = len(a_list)

        for i in range(src_length):
            tmp = a_list[i]

            ### 
            if i < src_length-1:
                if a_list[i] != a_list[i+1]:
                    new_list.append(tmp)
            ### Last
            else:
                new_list.append(tmp)
                
        return new_list

ut = Util()


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

        ### Remove Same Element as the Previous One
        xyzs = ut.remove_previous_elements(values_4)
        # print(len(values_4), len(xyzs))

        ### Draw All Path
        pts = []
        for i in xrange(len(xyzs)):
            x, y, z, s = xyzs[i]
            pt = [x, y, z]
            pts.append(pt)
        
        return pts

vb = ViewerBig()


###################################

###################################


ghenv.Component.Message = 'Viewer / 200821'


time_0 = time.time()


### gcode-file to Memory
xyzs = vb.gcode_to_array(PATH)


time_1 = time.time()


### Pick Values
points_ = vb.draw_path(xyzs)


time_2 = time.time()


### Draw Printing
MOVE = rs.AddPolyline(points_)


time_3 = time.time()




#time_01 = time_1 - time_0
#time_12 = time_2 - time_1
#time_23 = time_3 - time_2
#
#print ("Time 01 : {0}".format(time_01) + "[sec]")
#print ("Time 12 : {0}".format(time_12) + "[sec]")
#print ("Time 23 : {0}".format(time_23) + "[sec]")