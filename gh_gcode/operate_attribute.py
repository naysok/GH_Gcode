import rhinoscriptsyntax as rs
import Rhino.Geometry as rg


from . import util
ut = util.Util()
reload(util)


class Attribute():


    def __init__(self):
        pass

    
    def points_in_brep(self, brep, points):

        bool_in = []

        for i in xrange(len(points)):
            pp = points[i]
            sub_bool = []
            
            for j in xrange(len(pp)):
                p = pp[j]
        
                ### Segment Point with Brep.IsPointInside
                ### https://developer.rhino3d.com/api/RhinoCommon/html/M_Rhino_Geometry_Brep_IsPointInside.htm
                sub_bool.append(rg.Brep.IsPointInside(brep, p, 0.01, True))
            
            bool_in.append(sub_bool)
        
        return bool_in


    def points_in_breps(self, breps, points):

        ### Segment Points with Brep.IsPointInside

        bool_array = []

        for i in xrange(len(breps)):
            brep = breps[i]
            brep_geo = rs.coercebrep(brep)

            bool_array.append(self.points_in_brep(brep_geo, points))

        ### Arrays
        # print(len(bool_array))
        bool_inside = ut.bitwise_or_arrays(bool_array)

        return bool_inside
    

    def define_attribute(self, bool_inside, weight_value):
        
        ### Define Attribute-Value (Weight)
        ### For Attribute Mode

        new_values = []

        for i in xrange(len(bool_inside)):
            bb = bool_inside[i]
            
            sub_ = []

            for j in xrange(len(bb)):
                b = bb[j]

                ### Inside
                if b:
                    sub_.append(float(weight_value))
                
                else:
                    sub_.append(1.0)
        
            new_values.append(sub_)
        
        return new_values
    

    def render_attribute(self, points, bool_inside):
        
        ### Render Attribute-Values

        render = []
        pts_weighting = []

        for i in xrange(len(points)):
            pp = points[i]
            bb = bool_inside[i]

            sub_render = []
            
            for j in xrange(len(pp)):
                p = pp[j]
                b = bb[j]

                if b:
                    sub_render.append(rs.AddCircle(p, 0.5))
                    pts_weighting.append(p)

                else:
                    sub_render.append(rs.AddCircle(p, 4))
            
            render.append(sub_render)
        
        return render, pts_weighting