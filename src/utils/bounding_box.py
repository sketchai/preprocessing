import math
import numpy as np
from sketchgraphs.data.sequence import EntityType

def compute_coords_of_op(op):
    x_coords = []
    y_coords = []
    if op.label == EntityType.Point:
        x_coords.append(op.parameters['x'])
        y_coords.append(op.parameters['y'])
    
    elif op.label == EntityType.Line:
        pntX = op.parameters['pntX']
        pntY = op.parameters['pntY']
        endParam = op.parameters['endParam']
        dirX = op.parameters['dirX']
        dirY = op.parameters['dirY']            
        x_coords.append(pntX)
        y_coords.append(pntY)
        x_coords.append(pntX + endParam*dirX)
        y_coords.append(pntY + endParam*dirY)
    
    elif op.label == EntityType.Arc:
        xCenter = op.parameters['xCenter']
        yCenter = op.parameters['yCenter']
        xDir = op.parameters['xDir']
        yDir = op.parameters['yDir']
        radius = op.parameters['radius']
        clockwise = op.parameters['clockwise']
        startParam = op.parameters['startParam']
        endParam = op.parameters['endParam']
        if clockwise:
            startParam, endParam = -endParam, -startParam
        theta = math.atan2(yDir,xDir)
        alpha = (theta + startParam) % (2*np.pi)
        beta = (theta + endParam) % (2*np.pi)
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


    elif op.label == EntityType.Circle:
        xCenter = op.parameters['xCenter']
        yCenter = op.parameters['yCenter']
        radius = op.parameters['radius']
        x_coords.append(xCenter + radius)
        y_coords.append(yCenter + radius)
        x_coords.append(xCenter - radius)
        y_coords.append(yCenter - radius)

    return x_coords, y_coords


