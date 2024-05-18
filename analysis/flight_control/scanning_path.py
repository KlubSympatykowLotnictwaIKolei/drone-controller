from geopy.distance import geodesic
from geopy.distance import distance
from geopy.point import Point

DRONE_CAM = 10
GRID_RES = 2


def point_inside_polygon(x, y, poly):
    n = len(poly)
    inside = False

    p1x, p1y = poly[0]
    for i in range(n + 1):
        p2x, p2y = poly[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y

    return inside


def box_polygon_intersection_percentage(box, poly):
    x, y, width, height = box
    box_area = width * height

    intersection_area = 0

    for i in range(int(x), int(x + width)):
        for j in range(int(y), int(y + height)):
            if point_inside_polygon(i, j, poly):
                intersection_area += 1

    return intersection_area / box_area


def add_distance_to_coordinate(lat, lon, x, y):
    initial_point = Point(lat, lon)
    east_west_distance = distance(meters=y)
    north_south_distance = distance(meters=x)
    new_lat, new_lon = (
        east_west_distance.destination(initial_point, 0).latitude,
        north_south_distance.destination(initial_point, 90).longitude,
    )
    return (new_lat, new_lon)

# toilet corner: -35.36298462 149.16587905
# empty: -35.36265477 149.16586065
# box:	-35.36266542 149.16629863
# tarp:  -35.36302400 149.16631977 

polygon_lat_lon = [
    (51.10482345491133, 16.85848560864865),
    (51.103878221176984, 16.860484776731024),
    (51.10275905828721, 16.85990671412304),
    (51.103356386793386, 16.856089121744066),
    (51.105072953255316, 16.856269624494754),
]

# polygon_lat_lon = [
#     (-35.36298462 ,149.16587905),
#     (-35.36265477 ,149.16586065),
#     (-35.36266542 ,149.16629863),
#     (-35.36302400 ,149.16631977 ),
# ]



top_left = bottom_right = polygon_lat_lon[0]


for point in polygon_lat_lon[1:]:
    latitude, longitude = point
    top_left = (max(top_left[0], latitude), min(top_left[1], longitude))
    bottom_right = (min(bottom_right[0], latitude), max(bottom_right[1], longitude))

polygon_x_y = []

max_x = 0
max_y = 0

for point in polygon_lat_lon:
    x = geodesic((top_left[0], point[1]), point).meters
    y = geodesic((point[0], top_left[1]), point).meters
    if x > max_x:
        max_x = x
    if y > max_y:
        max_y = y
    polygon_x_y.append((x, y))


curr_y = 0
coord_grid = []
while curr_y < max_y:
    curr_x = 0
    curr_row = []
    while curr_x < max_x:
        curr_row.append((curr_x, curr_y))
        curr_x += GRID_RES
    coord_grid.append(curr_row)
    curr_y += DRONE_CAM

grid = [[0 for _ in row] for row in coord_grid]

boxes_to_draw = []

for i in range(len(coord_grid)):
    for j in range(len(coord_grid[i])):
        box_top_left_corner = coord_grid[i][j]
        box = (box_top_left_corner[0], box_top_left_corner[1], GRID_RES, DRONE_CAM)
        if box_polygon_intersection_percentage(box, polygon_x_y) > 0.01:
            grid[i][j] = 1
            boxes_to_draw.append(box)


flip = False
path = []
for i, row in enumerate(grid):
    first_one_index = row.index(1)
    last_one_index = len(row) - 1 - row[::-1].index(1)

    row_left_coord = coord_grid[i][first_one_index]
    row_left_coord = (row_left_coord[0], row_left_coord[1] + 0.5 * DRONE_CAM)

    row_right_coord = coord_grid[i][last_one_index]
    row_right_coord = (
        row_right_coord[0] + GRID_RES,
        row_right_coord[1] + 0.5 * DRONE_CAM,
    )

    if not flip:
        flip = True
        path.append(row_left_coord)
        path.append(row_right_coord)
    else:
        flip = False
        path.append(row_right_coord)
        path.append(row_left_coord)


path_gps = [add_distance_to_coordinate(*top_left, *point) for point in path]
print(path_gps)
