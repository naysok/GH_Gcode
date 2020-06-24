import Rhino.Geometry as rg
import rhinoscriptsyntax as rs


from . import transform
tr = transform.Transform()
reload(transform)


class Curve():


    def polyline_to_points(self, polyline):

        ########## NEW CODE ##########

        ### Polyline to Points by RhinoCommon
        pl = rs.coercegeometry(polyline)
        new_pl = rg.PolylineCurve.ToPolyline(pl)
        points = new_pl.ToArray()

        ########## NEW CODE ##########


        """
        ########## OLD CODE 1 ##########

        points = []

        ### Start Point
        start_pt = rs.CurveStartPoint(polyline)
        points.append(start_pt)

        ### Segment Points
        ### Style : 3 = C2 - Continuous first and second derivative
        segments = rs.CurveDiscontinuity(polyline, 3)
        for j in range(len(segments)):
            points.append(segments[j])

        ### End Point
        end_pt =  rs.CurveEndPoint(polyline)
        points.append(end_pt)

        ########## OLD CODE 1 ##########

        ########## OLD CODE 2 ##########
        
        ### Polyline to Points by rhinoscriptsuntax
        ### https://developer.rhino3d.com/api/RhinoScriptSyntax/#collapse-PolylineVertices
        
        points = rs.PolylineVertices(polyline)
        
        ########## OLD CODE 2 ##########
        """
        
        return points


    def polylines_to_points(self, polylines):

        points_array = []

        for i in xrange(len(polylines)):

            points = self.polyline_to_points(polylines[i])
            points_array.append(points)

        return points_array


    def offset_z(self, points, z_offset_value):

        move_vec = [0, 0, z_offset_value]

        points_off = []

        for i in xrange(len(points)):
            sub = []
            tmp = points[i]
            for j in xrange(len(tmp)):
                pt = tmp[j]
                ### offset
                X, Y, Z = tr.move_pt_vec(pt, move_vec)
                pt_off = rg.Point3d(X, Y, Z)
                sub.append(pt_off)
            points_off.append(sub)
        
        return points_off
