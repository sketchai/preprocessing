import math
import numpy as np

from sam.catalog_primitive import *
from sam.catalog_constraint import *

def compute_coords_of_entity(op):
    x_coords = []
    y_coords = []
    if isinstance(op, Point):
        x_coords.append(op.x)
        y_coords.append(op.y)
    
    elif isinstance(op, Line):

        x_coords.append(op.pnt1.x)
        y_coords.append(op.pnt1.y)

        x_coords.append(op.pnt2.x)  
        y_coords.append(op.pnt2.y)       
        
        
    elif isinstance(op,Arc):
        xCenter = op.center.x
        yCenter = op.center.y
        alpha = op.angle_start
        beta = op.angle_end
        radius = op.radius
        # append coords of the start and end angles
        x_coords.append(xCenter + radius*math.cos(alpha))
        x_coords.append(xCenter + radius*math.cos(beta))
        y_coords.append(yCenter + radius*math.sin(alpha))
        y_coords.append(yCenter + radius*math.sin(beta))

        # some part of the circle might still be outside the bounding box
        if beta < alpha:
            x_coords.append(xCenter + radius)
            beta += 2*np.pi
        if (alpha < 0.5*np.pi and beta > 0.5*np.pi) or (beta > 2.5*np.pi):
            y_coords.append(yCenter + radius)
        if (alpha < 1.0*np.pi and beta > 1.0*np.pi) or (beta > 3.0*np.pi):
            x_coords.append(xCenter - radius)
        if (alpha < 1.5*np.pi and beta > 1.5*np.pi) or (beta > 3.5*np.pi):
            y_coords.append(yCenter - radius)

        # add xcenter and ycenter 
        # This is not part of the bb but the radius might be greater than 1
        x_coords.append(xCenter)
        y_coords.append(yCenter)

    elif isinstance(op, Circle):
        xCenter = op.center.x
        yCenter = op.center.y
        radius = op.radius
        x_coords.append(xCenter + radius)
        y_coords.append(yCenter + radius)
        x_coords.append(xCenter - radius)
        y_coords.append(yCenter - radius)

    return x_coords, y_coords

