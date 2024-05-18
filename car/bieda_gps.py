import rasterio
import numpy as np
import cv2 as cv


class poorMansGps:

    def __init__(self, tif_path: str) -> None:
        self.og_img = cv.imread(tif_path)

        self.tif_map = rasterio.open(tif_path) 

        self.y_offset_start = 3300
        y_offset_len = 1300

        self.x_offset_start = 1100
        x_offset_len = 2400

        self.cropped_map = self.og_img[
            self.y_offset_start : self.y_offset_start + y_offset_len,
            self.x_offset_start : self.x_offset_start + x_offset_len,
        ].copy()
        self.cropped_map = cv.cvtColor(self.cropped_map, cv.COLOR_BGR2GRAY)

    def get_gps_from_photo(self, photo: np.ndarray) -> tuple[float, float]:

        result = self.match(photo)
        if result is None:
            print("no match found")
            return 0,0
        
        cropped_x, cropped_y = result
        cropped_x += self.x_offset_start
        cropped_y += self.y_offset_start

        return self.pixel_to_gps(cropped_x, cropped_y)


    def pixel_to_gps(self, x: int, y: int) -> tuple[float, float]:
        xs, ys = rasterio.transform.xy(self.tif_map.transform, [y], [x]) #tu ma być y x
        lons = np.array(xs)
        lats = np.array(ys)
        return lats[0], lons[0]

    def match(self, img_to_match: np.ndarray) -> tuple[int, int]:
        """
        prams:
            map - b&w\n
            img_to_match - b&w
        """

        sift = cv.SIFT_create()

        # Find keypoints and descriptors in both the template and the target image
        kp1, des1 = sift.detectAndCompute(img_to_match, None)
        kp2, des2 = sift.detectAndCompute(self.cropped_map, None)

        # Initialize Brute-Force Matcher
        bf = cv.BFMatcher()
        matches = bf.knnMatch(des1, des2, k=2)
        
        if len(matches) < 5:
            return None
        
        # Apply ratio test
        good_matches = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                good_matches.append(m)

        # Extract keypoints
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(
            -1, 1, 2
        )
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(
            -1, 1, 2
        )
        
        if len(src_pts) < 5 or len(dst_pts) < 5:
            return None # cannot find homography

        # Calculate transformation matrix
        M, _ = cv.findHomography(src_pts, dst_pts, cv.RANSAC, 5.0)

        # Get the corners of the template image
        h, w = img_to_match.shape
        pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(
            -1, 1, 2
        )


        print(pts)

        try:
            # Transform the corner points to get the bounding box in the target image
            dst = cv.perspectiveTransform(pts, M)
            middle_x = int((dst[0][0][0] + dst[2][0][0]) / 2)
            middle_y = int((dst[0][0][1] + dst[2][0][1]) / 2)
            middle_point = (middle_x, middle_y)
        except:
            return None
        
        img_bbox = cv.polylines(self.cropped_map, [np.int32(dst)], True, (0, 255, 0), 2, cv.LINE_AA)
        cv.drawMarker(img_bbox, middle_point, (255, 0, 0), markerType=cv.MARKER_CROSS, markerSize=10, thickness=2)
        cv.imshow('Bounding Box with Middle Point', img_bbox)
        cv.imwrite("aa.png", img_bbox)
        cv.waitKey(0)
        cv.destroyAllWindows()

        return middle_point
