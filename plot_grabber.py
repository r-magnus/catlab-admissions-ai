# plot_grabber.py
# Takes user input to retrieve specific plots, for ease-of-use.
# @author Ryan Magnuson rmagnuson@westmont.edu

# Setup
import sys
import cv2

# Retrieval Mode
def retrieval(): # "grab"
  # User Input
  print("This is a tool intended for ease-of-use. Case sensitive.\n'Active Application' items omit 'Active Application:'")
  datapt1 = str(input("Enter the first data point > "))
  datapt2 = str(input("Enter the second data point > "))

  img = cv2.imread("scatters/%s_%s.jpg" % (datapt1, datapt2), cv2.IMREAD_ANYCOLOR)

  while True:
    cv2.imshow("%s_%s" % (datapt1, datapt2), img)
    cv2.waitKey(1)

    if cv2.getWindowProperty("%s_%s" % (datapt1, datapt2), cv2.WND_PROP_VISIBLE) < 1:
      break

  cv2.destroyAllWindows()

# Scroll Mode
def scroll(): # "all"
  print("This is a WIP. Run again.")
  pass
  #stub

# Main User Input
choice = input("Select a mode: grab, all > ")
while choice not in ['grab', 'all']:
  choice = input("Select a mode: grab, all > ")

if choice == "grab":
  retrieval()
else:
  scroll()
