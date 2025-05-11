# TCG-Card-Scanner
This Scanner is intended to be used only on cards belonging to the One Piece Trading card game. 

In order to run this program a couple of libraries and tools are needed
  OpenCV - This library is what is used to access the images displayed through our phones camera.
  pytesseract - This library is necessary for processing any characters such as the numbers seen on the card
  numpy - This is used to help narrow down the color hues and values found on the color of the card.
  IP Webcam - This is an Android App used to send video data to OpenCV

It is necessary to modify the python file with the correct ip address to connect the phone video to the program.
The program is driven off of a while loop. The user is instructed to line up their One Piece Card with the borders displayed on the camera. 
The user can then press C for cost, P for Power, and T for Type or Color. To close the program down you can simply type q. 
