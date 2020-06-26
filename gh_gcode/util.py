import datetime
import math

import rhinoscriptsyntax as rs
import Rhino.Geometry as rg

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
    

    def calc_print_area(self, points_array):

        pts = self.flatten_runtime_list(points_array)
        bbox = rg.BoundingBox(pts)
        
        return bbox.Min, bbox.Max


    def check_print_area(self, points_array):

        machine_min = [0, 0, 0]
        machine_max = [1700, 1300, 1020]
        
        print_min, print_max = self.calc_print_area(points_array)

        msg = []

        ### Left
        if machine_min[0] > print_min[0]:
            msg.append("Over X_Mini!!\n")

        ### Right
        if machine_max[0] < print_max[0]:
            msg.append("Over X_Max!!\n")

        ### Front
        if machine_min[1] > print_min[1]:
            msg.append("Over Y_Mini!!\n")

        ### Back
        if machine_max[1] < print_max[1]:
            msg.append("Over Y_Max!!\n")

        if msg == []:
            msg.append("OK!!")

        return msg


    def draw_machine(self):

        rects = []

        machine_origin = [-69, -100]
        machine_max = [1700, 1300]

        ### Panel
        panel_size = 500
        panel_count = 12
        vv = 3

        for i in xrange(panel_count):

            u, v = divmod(i, vv)
            tmp_origin = (machine_origin[0] + (500 * u) , machine_origin[1] + (500 *v), 0)
            pl = rs.MovePlane(rs.WorldXYPlane(), tmp_origin)
            rc = rs.AddRectangle(pl, panel_size, panel_size)
            rects.append(rc)

        ### Print Area
        print_origin = (0, 0, 0)
        pl = rs.MovePlane(rs.WorldXYPlane(), print_origin)
        rc = rs.AddRectangle(pl, machine_max[0], machine_max[1])
        rects.append(rc)

        return rects