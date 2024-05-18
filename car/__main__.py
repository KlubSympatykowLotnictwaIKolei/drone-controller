import cv2 as cv

from bieda_gps import poorMansGps
import time



# tracker = Tracker()
# tracker.run_tracker()

# test idea, go to the middle of the field, fly up check gps after  
# python car > somefile.txt

p = poorMansGps("./img/fotomapa_lubin.tif")



#for testing

photo = cv.imread("./img/rotated_fucked_4_times.png")
photo = cv.cvtColor(photo, cv.COLOR_BGR2GRAY)
a = p.get_gps_from_photo(photo)
# building's south west corner on tif map
print(f'{a[0]}, {a[1]}')


# a = p.pixel_to_gps(275012341, -13123954)


# for i in range(1000):
#     photo = c.take_a_photo()
#     photo = cv.cvtColor(photo, cv.COLOR_BGR2GRAY)
#     a = p.get_gps_from_photo(photo)
#     print(f'{a[0]}, {a[1]}')
#     time.sleep(5)