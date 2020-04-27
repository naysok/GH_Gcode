import rhinoscriptsyntax as rs


class Gcode_for_GH():
    
    def open_file(self, path):
        with open(path) as f:
            l = f.readlines()
        # print(type(l))
        # print(len(l))
        # print(l)
        return l
    
    def add_xyz_to_polyline(self, path):

        gcode = self.open_file(path)

        count = 0
        x = []
        y = []
        z = []

        ### init
        x.append(0)
        y.append(0)
        z.append(0)

        # loop = 20
        loop = len(gcode)

        for i in range(loop):

            count += 1
            str_ = gcode[i]
            
            if ("X" in str_):
                ### Split Elements
                elements = str_.split()
                for j in range(len(elements)):
                    e = elements[j]
                    
                    if ("X" in e):
                        tmp_x = e.split("X")
                        x.append(tmp_x[1])
            else:
                tmp_x = x[i]
                x.append(tmp_x)

        for ii in range(loop):

            str_ = gcode[ii]
            
            if ("Y" in str_):
                ### Split Elements
                elements = str_.split()
                for jj in range(len(elements)):
                    e = elements[jj]
                    
                    if ("Y" in e):
                        tmp_y = e.split("Y")
                        y.append(tmp_y[1])
            else:
                tmp_y = y[ii]
                y.append(tmp_y)

        for iii in range(loop):

            str_ = gcode[iii]
            
            if ("Z" in str_):
                ### Split Elements
                elements = str_.split()
                for jjj in range(len(elements)):
                    e = elements[jjj]
                    
                    if ("Z" in e):
                        tmp_z = e.split("Z")
                        z.append(tmp_z[1])
            else:
                tmp_z = z[iii]
                z.append(tmp_z)

        # print("x : {} / {}".format(len(x), x))
        # print("y : {} / {}".format(len(y), y))
        # print("z : {} / {}".format(len(z), z))

        print("Count : {}".format(count))
        
        return x, y, z
     
    def zip_matrix(self, mat):
        ### https://note.nkmk.me/python-list-transpose/
        return [list(x) for x in zip(*mat)]



###################################


gg = Gcode_for_GH()


v = gg.add_xyz_to_polyline(PATH)
v_f = gg.zip_matrix(v)

print(len(v_f))
#print(v_f)



MOVE = rs.AddPolyline(v_f)
