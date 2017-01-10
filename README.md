# Create-Centerline
Creates a centerline between two roughly parallel lines

This tool creates a line feature, in the middle of two roughly parallel lines.  It works by iterating over the vertices of one of the lines, and creating a point in the middle of that vertex and the nearest vertex on the other line.  There are thus two potential centerlines which can be created by this tool.  Currently it only creates one, and doesn't support selecting which line will be the base.  

The output will have the same number of vertices as the base line.
