import math

def dimensions_shape():

    height = float(input("Enter height: "))
    width = float(input("Enter width: "))
    y_dist = float(input("Enter y_distance from bottom to bottom edge: "))


    centroid_from_bot = height/2 + y_dist

    return height,width,centroid_from_bot,y_dist



def find_shape_centroid(shapes_and_dim):
    sum_numerator = 0
    sum_denom = 0
    for key, value in shapes_and_dim.items():
        dims = shapes_and_dim[key]
        area = dims[0] * dims[1]
        d = dims[2]
        sum_numerator = sum_numerator + (area*d)
        sum_denom = sum_denom + area

    shape_centroid = sum_numerator/sum_denom
    return shape_centroid


{0: (2.5, 100.0, 83.75),
 1: (1.25, 10.0, 81.875),
 2: (80.0, 5.0, 41.25),
 3: (1.25, 10.0, 0.625),
 4: (1.25, 10.0, 81.875),
 5: (80.0, 5.0, 41.25),
 6: (1.25, 10.0, 0.625)}



def calculate_I(shapes_and_dim):
    shape_centroid = find_shape_centroid(shapes_and_dim)
    sum_I = 0
    for key, value in shapes_and_dim.items():
        dims = shapes_and_dim[key]
        I_0 = (dims[1] * (dims[0])**3) / 12
        A = dims[0] * dims[1]
        d = abs(dims[2] - shape_centroid)
        I_t = I_0 + A*d**2
        sum_I = sum_I + I_t
    return sum_I


def find_Q_max_centroid(shapes_and_dim):
    y=find_shape_centroid(shapes_and_dim)
    Q=0
    for k,v in shapes_and_dim.items():
        d=v
        if k in [2,3,5,6]:
            if v[0]>=y:
                new_height= y-d[3]
                A=new_height*d[1]
                d=((new_height/2) + d[3])
                Q+=A*d
            else:
                A=d[0]*d[1]
                d=y-d[2]
                Q+=A*d

    return Q

def find_Q_interfaces_top(shapes_and_dim):
    d=shapes_and_dim[0]
    y=find_shape_centroid(shapes_and_dim)
    A=d[0]*d[1]
    d=d[2]-y
    return A*d

def plate_buckling_1_top():
    E = 4000
    u = 0.2
    t = 2.5
    b = 60
    theta_c = ((4*((math.pi)**2)*E) / (12*(1 - u**2))) * (t/b)**2
    y_bar = find_shape_centroid(shapes_and_dim)
    I = calculate_I(shapes_and_dim)
    coeff_p = ((140) * (85 - y_bar)) / I
    P = theta_c / coeff_p
    return P

def plate_buckling_2_top():
    E = 4000
    u = 0.2
    t = 2.5
    b = 20
    theta_c = ((0.425*((math.pi)**2)*E) / (12*(1 - u**2))) * (t/b)**2
    y_bar = find_shape_centroid(shapes_and_dim)
    I = calculate_I(shapes_and_dim)
    coeff_p = ((140) * (85 - y_bar)) / I
    P = theta_c / coeff_p
    return P


def find_shear_force_in_terms_of_P(dist):
    if dist <= 280:
        return 0.5
    elif dist > 280 and dist < 670:
        return 0
    else:
        return -0.5

def find_bend_moment_in_terms_of_P(dist):
    if dist <= 280:
        moment = dist * 0.5
        return moment
    elif dist > 280 and dist < 670:
        return 140
    else:
        moment = 140 - 0.5*(670-dist)
        return moment


def max_bending_tension(shapes_and_dim):
    I = calculate_I(shapes_and_dim)
    shape_centroid = find_shape_centroid(shapes_and_dim)
    max_moment = find_bend_moment_in_terms_of_P(280)
    P = ((30 * I)/shape_centroid)/max_moment
    return P

def max_bending_compressive(shapes_and_dim):
    I = calculate_I(shapes_and_dim)
    shape_centroid = find_shape_centroid(shapes_and_dim)
    max_moment = find_bend_moment_in_terms_of_P(280)
    running_total_l = 0
    for key, value in shapes_and_dim.items():
        dim = value
        running_total_l = running_total_l + dim[0]
        if dim[3] == 0:
            break
    y = running_total_l - shape_centroid

    P = (((6 * I)/y)/max_moment)

    return P


if __name__ == "__main__":
    #Material Properties:
    Theta_c = -6 
    Theta_t = 16 
    tau_matboard = 4 
    tau_glue = 2 
    shapes_and_dim = {0: (2.5, 100.0, 83.75, 82.5),
    1: (1.25, 10.0, 81.875, 81.25),
    2: (80.0, 5.0, 41.25, 1.25),
    3: (1.25, 10.0, 0.625, 0.0),
    4: (1.25, 10.0, 81.875, 81.25),
    5: (80.0, 5.0, 41.25, 1.25),
    6: (1.25, 10.0, 0.625, 0.0)}
    # ------------------  |
    # ------------------  |   0
    #   ---        ---    | 1   4
    #   -            -    
    #   -            -    | 2   5
    #   -            -
    #   -            -
    #   ---        ---    | 4    6
    print(find_Q_max_centroid(shapes_and_dim))
    print(find_Q_interfaces_top(shapes_and_dim))
    print(plate_buckling_1_top())
    print(plate_buckling_2_top())
    '''
    We need the shear force diagrams
    For this beam: as follows:

    Shear Force Diagram
    |------|                           +
    |______|_______________________    
                           |      |    -
                           |------|
    <-280--><-----390-----><-280-->    
    Maximum positive shear: P/2
    Maximum negative Shear: -P/2

    Bending Moment diagram

                                    -
    ______________________________
    \                            /   +
     \                          /
      \________________________/

    Maximum positive moment: 140P
    '''