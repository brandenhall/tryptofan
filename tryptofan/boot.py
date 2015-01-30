import opc

client = opc.Client('localhost:7890')
pixels = [(255, 255, 255), (0, 0, 0), (0, 0, 0)] * 32
client.put_pixels(pixels)
client.put_pixels(pixels)
