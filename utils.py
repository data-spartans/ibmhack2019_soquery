'''
Miscellaneous useful functions
'''
def color_interp(c1, c2, mix=0):
    '''
    Takes colors c1 and c2 as tuples of RGB values, and returns a tuple representing the mixture. The mix param is used to specify the position on gradient from 0 for c1 to 1 for c2.
    '''
    R = int((1 - mix) * c1[0] + mix * c2[0])
    G = int((1 - mix) * c1[1] + mix * c2[1])
    B = int((1 - mix) * c1[2] + mix * c2[2])
    return (R, G, B)

def color_to_hex(col):
    '''
    Returns hex representation of color (input as tuple of RGB values in range 0-255).

    For example, the tuple (255, 255, 255) is converted to '#ffffff'.
    '''
    val = col[0] * (16)**4 + col[1] * (16)**2 + col[2]
    ans = hex(val)[2:]
    # pad with 0s if there are less than 6 digits:
    ans = '0'*(6-len(ans)) + ans
    return '#' + ans

def color_for_confidence(conf, thresh=700, c1=(255, 0, 0), c2=(0, 255, 0)):
    '''
    Returns a color representation of confidence, assuming thresh as the highest confidence, with c1 representing low confidence, and c2 representing high confidence. 

    The returned value is a hex string representing the color
    '''
    mix = conf/thresh
    if mix > 1: mix = 1
    return color_to_hex(color_interp(c1, c2, mix))
