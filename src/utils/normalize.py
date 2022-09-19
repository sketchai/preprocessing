from src.utils.logger import logger

def normalize_op(key, reference_list, coeff) -> bool:
    x_min = coeff.get('xmin')
    y_min = coeff.get('ymin')
    l_max = coeff.get('lmax')

    if key == 'x' :
        for reference in reference_list: 
            reference.update_parms({'x' : (reference.x - x_min)/l_max})


    elif key  == 'y' :
        for reference in reference_list:
            reference.update_parms({'y' : (reference.y - y_min)/l_max})


    elif key in ['radius', 'length'] :
        for reference in reference_list:
            reference.update_parms({key : reference.__dict__.get(key)/l_max })

    elif key in ['pnt1', 'pnt2', 'center'] :
        for reference in reference_list:
            reference.update_parms({key : [(reference.__dict__.get(key).x - x_min)/l_max, 
                                             (reference.__dict__.get(key).y - y_min)/l_max ]})
      
    return True