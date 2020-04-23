import rhinoscriptsyntax as rs


class Curve():


    def polyline_to_points(self, polyline):

        points = []

        ### Start Point
        start_pt = rs.CurveStartPoint(polyline)
        points.append(start_pt)


        ### Segment Points / Style : 4 = G1
        segments = rs.CurveDiscontinuity(polyline, 4)
        for j in range(len(segments)):
            points.append(segments[j])

        ### End Point
        end_pt =  rs.CurveEndPoint(polyline)
        points.append(end_pt)
        
        return points
    


    def polylines_to_points(self, polylines):

        points_array = []

        for i in xrange(len(polylines)):

            points = self.polyline_to_points(polylines[i])
            points_array.append(points)

        return points_array
    