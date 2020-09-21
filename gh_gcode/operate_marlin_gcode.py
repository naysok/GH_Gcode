import rhinoscriptsyntax as rs

from . import util
ut = util.Util()
reload(util)


class BigGcode():


    def gcode_start(self):
        pass


    def define_print_msg(self):
        return "( Polyline to Gcode by Grasshopper )\n( For Mariln 3D Printer )\n( --- )\n"


    def define_print_parameter(self, component):

        now = ut.get_current_time()
        time = "( Export : {} )\n".format(now)
        comp_info = "( Component Info : {} )\n".format(component)
        line = "( --- )\n"

        return time + comp_info + line