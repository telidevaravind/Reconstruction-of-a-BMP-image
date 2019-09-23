from PIL import Image
import binascii
import numpy as np

# TO SEE THE INPUT IMAGE TAKEN

image = Image.open('valley.bmp', 'r')
# print Image.shape
image.show(Image)


# READING THE INPUT IMAGE

print(type('valley.bmp'))
f = open('valley.bmp', 'r')
data = f.read()
f.close()

f = open('Image_details.txt', 'w')
data = binascii.b2a_hex(data)

# chunk_size = 1
# hex_list = [hex_str[i:i + 2]
#             for i in range(0, len(hex_str), 2)]
# hex_chunks = [hex_list[i:i + chunk_size]
#               for i in range(0, len(hex_list), chunk_size)]
# data = '\n'.join([' '.join(chunk) for chunk in hex_chunks])

f.write(data)
f.close()
# print data
split = [data[i:i + 2] for i in range(0, len(data), 2)]
integ = [int(x, 16) for x in split]
array = np.asarray(integ)
print (array[0:54])
# CHECKING IF THE IMAGE IS bmp OR NOT

if chr(array[0]) == "B" and chr(array[1]) == "M":
    print('it is a bmp file\n')
else:
    print('it is not a bmp file\n')

# IMAGE ATTRIBUTES

size_of_image = (sum(array[2:6]))  # SIZE OF THE IMAGE

Starting_address = (sum(array[10:14]))  # STARTING ADDRESS OF THE PIXEL DATA
print ("Starting_address: %d" % Starting_address)
size_of_DIB_header = (sum(array[14:18]))  # SIZE OF THE DIB HEADER
print ("size_of_DIB_header: %d" % size_of_DIB_header)
width = (sum(array[18:22]))  # WIDTH OF THE IMAGE
print ("width: %d" % width)
height = (sum(array[22:26]))  # HEIGHT OF THE IMAGE
print ("height: %d" % height)
number_of_bits_per_pixel = (sum(array[28:30]))  # NUMBER OF BYTES PER PIXEL
print ("number_of_bits_per_pixel: %d" % number_of_bits_per_pixel)
print ("Resolution of image: %d * %d" % (width, height))   # RESOLUTION OF THE IMAGE

#  TO REMOVE THE PADDING

s = width * height
size = 27
start = Starting_address
ending = size_of_image
# width_dec = hex2dec(width)
# height_dec = hex2dec(height)
array1 = array
if (width % 4) != 0:
    array[2] = 54 + s*3
    pad = 4 - (width * 3 % 4)
    print (pad)
    for a in range(start + (width * 3), ending, width * 3):
        for m in range(0, pad):
            array1 = np.delete(array1, a)

# IMAGE ATTRIBUTES AFTER REMOVAL OF PADDING

size_of_image_wo_pad = len(array1)
imag = array1[54:size_of_image_wo_pad]
print ('imag:\n',imag)
le = (len(imag))

# # imgr = fopen('imgr.txt', 'w')
# # fprintf(imgr, '%f \n', imag_dec)
# # fclose(imgr)
#
# SEPARATION OF R G B CHANNELS
red = np.zeros(le,int)
blue = np.zeros(le,int)
green = np.zeros(le,int)
for b in range(1, le + 1):
    if (b%3) == 2:
        green[b-1] = imag[b-1]
        # green[b - 2] = 0
for b in range(1, le + 1):
    if (b%3) == 0:
        red[b - 1] = imag[b-1]
        # red[b - 3] = 0
for b in range(1, le + 1):
    if (b%3) == 1:
        blue[b-1] = imag[b-1]
        # blue[b + 1] = 0
print ('blue:\n',blue)
print ('red:\n',red)
print ('green:\n',green)
# print(blue)
# WRITING THE R G B CHANNEL VALUES INTO FILE

r = open('red.txt', 'w')
g = open('green.txt', 'w')
b = open('blue.txt', 'w')
blue_hex = binascii.b2a_hex(blue)
red_hex = binascii.b2a_hex(red)
green_hex = binascii.b2a_hex(green)
r.write(red_hex)
g.write(green_hex)
b.write(blue_hex)
r.close()
g.close()
b.close()

#  RECONSTRUCTED IMAGE

reconstruct = red + green + blue
#reconstruct = cast(reconstruct, 'uint8')
# # % re = fopen('rec.txt', 'w')
# # % fprintf(re, '%f \n', reconstruct)
# # % fclose(re)

recon = np.zeros((height, width, 3,), int)
# print recon
# SIZE = size(recon)
u = 0

for row in range(height, 0, -1):
    for column in range(1, width+1, 1):
        recon[2][row-1][column-1] = reconstruct[u]
        recon[1][row-1][column-1] = reconstruct[u + 1]
        recon[0][row-1][column-1] = reconstruct[u + 2]
        u = u + 3

print ('recon:\n',recon)
# CHECKING THE RECONSTRUCTED IMAGE

op = Image.fromarray('valley_new.bmp', recon)
# print Image.shape
op.show('R', recon)
