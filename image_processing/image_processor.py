import cv2

def measure_blur(image):
    return cv2.Laplacian(image, cv2.CV_64F).var()

def read_image(path):
    image = cv2.imread(path)
    return image

def gaussian_blur(image, kernel_size=(11, 11), sigma_x=0):
    blurred_image = cv2.GaussianBlur(image, kernel_size, sigma_x)
    return blurred_image

def gray_scale(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray_image

def threshold_image(image, threshold=115, max_value=255, type=cv2.THRESH_BINARY):
    _, threshold_image = cv2.threshold(image, threshold, max_value, type)
    return threshold_image

def show_image(image, title='Image'):
    cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
