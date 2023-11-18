import cv2
import pandas as pd
# pandas used to read the csv file

img_path = r'colorpic.jpg'
# giving the path to the picture to read it
img = cv2.imread(img_path)
# this returns the image as an array which is saved in img

# declaring global variables
clicked = False
# to find if user has clicked on the picture
r = g = b = x_pos = y_pos = 0
# x_pos and y_pos are positions of the mouse pointer which are all set to zero

# Reading csv file with pandas and giving names to each column
index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('colors.csv', names=index, header=None)
# used to read the csv file using pandas
# index has names of columns from the csv file


# function to calculate minimum distance from all colors and get the most matching color
def get_color_name(R, G, B):
    # getting names of colors from dataset
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        # getting the colors we have and the colors from the dataset
        if d <= minimum:
            minimum = d
            cname = csv.loc[i, "color_name"]
            # if d is less than the threshold value we gave then we choose that particular color
    return cname
# returning the name of the color


# function to get x,y coordinates of mouse double click
def draw_function(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        # this is set to left button double click
        global b, g, r, x_pos, y_pos, clicked
        clicked = True
        x_pos = x
        y_pos = y
        # to get the x and y values when the pointer is clicked
        b, g, r = img[y, x]
        # as this is how the channels are arranged in opencv
        b = int(b)
        g = int(g)
        r = int(r)
        # converts to pure integer values

cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_function)
# to get the r, g and b values of the mouse pointer where it is being clicked at
# image is the window that appears when the code is run

while True:

    cv2.imshow("image", img)
    if clicked:

        # cv2.rectangle(image, start point, endpoint, color, thickness)-1 fills entire rectangle
        # making a rectangle on our image to display the color name and the r, g, b values obtained
        cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)

        # Creating text string to display( Color name and RGB values )
        text = get_color_name(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)

        # cv2.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
        cv2.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

        # For very light colours we will display text in black colour
        if r + g + b >= 600:
            cv2.putText(img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

        clicked = False

    # Break the loop when user hits 'esc' key
    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()