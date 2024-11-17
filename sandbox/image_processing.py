import cv2
import imutils
from imutils.perspective import four_point_transform
from skimage.filters import threshold_local


class ImageProcessing:
    def __init__(self) -> None:
        self.image_path = "sandbox/20241116_090948.jpg"
        self.ratio = 0

    def load_image(self):
        # Step 1: Load the image
        orig = cv2.imread(self.image_path)
        # need to copy the original because we will apply the transformation there
        copy = orig.copy()
        image = imutils.resize(copy, width=500)
        self.ratio = orig.shape[1] / float(image.shape[1])

        return image

    def edge_detection(self):
        # convert the image to grayscale, blur it slightly, and then apply
        # edge detection
        image = self.load_image()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(
            gray,
            (
                5,
                5,
            ),
            0,
        )
        edged = cv2.Canny(blurred, 75, 200)

        # Repeated Closing operation to remove text from the document and improve edge detection
        # kernel = np.ones((5, 5), np.uint8)
        # img_morphed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel, iterations=3)

        # save the image without the background and most of the content
        # cv2.imwrite("sandbox/receipt_edged.jpg", img_morphed)

        return edged

    def search_contour(self):
        # load the edged image
        edged = self.edge_detection()
        # find contours in the edge map and sort them by size in descending order
        cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

        # initialize a contour that corresponds to the receipt outline
        receiptCnt = None

        # loop over the contours
        for c in cnts:
            # approximate the contour
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            # if our approximated contour has four points, then we can
            # assume we have found the outline of the receipt
            if len(approx) == 4:
                receiptCnt = approx
                break
        # if the receipt contour is empty then our script could not find the
        # outline and we should be notified
        if receiptCnt is None:
            raise Exception(
                (
                    "Could not find receipt outline. "
                    "Try debugging your edge detection and contour steps."
                )
            )

        return receiptCnt

        # save the image without the background
        # cv2.imwrite("sandbox/receipt_edged.jpg", edged)

    def topdown_view(self):
        # load the original image
        orig = cv2.imread(self.image_path)
        receiptCnt = self.search_contour()
        # apply a four-point perspective transform to the *original* image to
        # obtain a top-down bird's-eye view of the receipt
        receipt = four_point_transform(orig, receiptCnt.reshape(4, 2) * self.ratio)

        ########################################
        #### TEST TO DRAW CONTOUR ####
        # print("COUNTOURS:", receiptCnt)
        orig = cv2.imread(self.image_path)
        reshape_contours = (receiptCnt.reshape(4, 2) * self.ratio).astype(int)  # Reshape and scale

        con = cv2.drawContours(orig, [reshape_contours], -1, (0, 255, 0), 20)
        cv2.imwrite("sandbox/test.jpg", con)  # DRAW ALL
        ########################################

        #######################
        # gray = cv2.cvtColor(receipt, cv2.COLOR_BGR2GRAY)
        # scan_like = cv2.adaptiveThreshold(
        #     gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 13, 21
        # )
        # convert the warped image to grayscale, then threshold it

        # to give it that 'black and white' paper effect
        warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
        T = threshold_local(warped, 11, offset=10, method="gaussian")
        warped = (warped > T).astype("uint8") * 255

        #######################

        # save transformed image
        cv2.imwrite("sandbox/receipt_topdown_view.jpg", imutils.resize(receipt, width=500))
        cv2.imwrite("sandbox/receipt_final_scan.jpg", scan_like)
