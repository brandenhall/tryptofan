import opc

client = opc.Client('localhost:7890')
pixels = [(0, 0, 0)] * (32 * 3)
client.put_pixels(pixels)
client.put_pixels(pixels)
