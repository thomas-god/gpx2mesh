1 - load track from gpx file to retrieve min and max lat and lon

2 - load elevation data from the matching file (elevation is a 2D-array at this
stage)

3 - map track to elevation coordinates and retrieve elevation for each point of
the track (track is of shape (T, 3) with T the track number of points and each
row is [elev_row, elev_col, elev_value])

4 - crop the elevation array to the track box, and update coordinates of the
track elevation ([elev_row - row_min, elev_col - col_min, elev_value])

5 - create the terrain mesh from the elevation array, and generate scaling
values

6 - create the mesh for the track using the same scaling values used for
generating the terrain mesh

7 - merge meshes and print !
