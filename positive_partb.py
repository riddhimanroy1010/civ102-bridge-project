import math
def calculate_local_centroid(shapes_and_dim):
    new={}
    for k,v in shapes_and_dim.items():
        new_value=(shapes_and_dim[k][0],shapes_and_dim[k][1], (shapes_and_dim[k][0]/2)+shapes_and_dim[k][3], shapes_and_dim[k][3])
        new[k]=new_value

    return new
def calculate_right_heights1(shapes_and_dim):
    new={}
    new[6]=(shapes_and_dim[6][0],shapes_and_dim[6][1], shapes_and_dim[6][2],0)
    new[3]=(shapes_and_dim[3][0],shapes_and_dim[3][1], shapes_and_dim[3][2],0)

    new[2]=(shapes_and_dim[2][0],shapes_and_dim[2][1], shapes_and_dim[2][2], new[3][0])
    new[5]=(shapes_and_dim[5][0],shapes_and_dim[5][1], shapes_and_dim[5][2], new[3][0])

    new[1]=(shapes_and_dim[1][0],shapes_and_dim[1][1], shapes_and_dim[1][2],new[2][3]+new[2][0])
    new[4]=(shapes_and_dim[4][0],shapes_and_dim[4][1], shapes_and_dim[4][2],new[2][3]+new[5][0])

    new[0]=(shapes_and_dim[0][0],shapes_and_dim[0][1], shapes_and_dim[0][2],new[1][3]+new[1][0])
    return new


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

def plate_buckling_1_top(shapes_and_dim,b):
    global max_mom,E,u
    t = shapes_and_dim[0][0]
    top=shapes_and_dim[0][3]+shapes_and_dim[0][0]
    theta_c = ((4*((math.pi)**2)*E) / (12*(1 - u**2))) * (t/b)**2
    y_bar = find_shape_centroid(shapes_and_dim)
    I = calculate_I(shapes_and_dim)
    coeff_p = ((max_mom) * (top - y_bar)) / I
    P = theta_c / coeff_p
    return P

def plate_buckling_2_top(shapes_and_dim,b):
    '''enter same b as plate buckling1'''
    global max_mom,E,u
    t = shapes_and_dim[0][0]
    b = (shapes_and_dim[0][1]-b)/2
    print("b:",b)
    top=shapes_and_dim[0][3]+shapes_and_dim[0][0]
    theta_c = ((0.425*((math.pi)**2)*E) / (12*(1 - u**2))) * (t/b)**2
    y_bar = find_shape_centroid(shapes_and_dim)
    I = calculate_I(shapes_and_dim)
    coeff_p = ((max_mom) * (top - y_bar)) / I
    P = theta_c / coeff_p
    return P

def web_buckling(shapes_and_dim):
    global max_mom
    E = 4000
    u = 0.2
    t = shapes_and_dim[2][1]
    y_bar = find_shape_centroid(shapes_and_dim)
    top=shapes_and_dim[0][3]+shapes_and_dim[0][0]
    b = top - y_bar
    
    theta_c = ((6*((math.pi)**2)*E) / (12*(1 - u**2))) * (t/b)**2
    I = calculate_I(shapes_and_dim)
    coeff_p = ((max_mom) * (top - y_bar)) / I
    P = theta_c / coeff_p
    return P

def total_area(shapes_and_dim):
    global lenght
    A=0
    for k,v in shapes_and_dim.items():
        A+= v[0] * v[1]

    return A*(lenght/1.27)

def max_bending_tension(shapes_and_dim):
    global max_mom,theta_t
    I = calculate_I(shapes_and_dim)
    shape_centroid = find_shape_centroid(shapes_and_dim)
    P = ((theta_t* I)/(shape_centroid*max_mom))
    return P

def max_bending_compressive(shapes_and_dim):
    global max_mom,theta_c
    I = calculate_I(shapes_and_dim)
    shape_centroid = find_shape_centroid(shapes_and_dim)
    print("max mom",max_mom)
    y_top= shapes_and_dim[0][0] + shapes_and_dim[0][3] - shape_centroid
    print("y:",y_top)
    P = ((theta_c * I)/(y_top*max_mom))
    return P

def max_shear_stress(shapes_and_dim):
    global max_shear,tau_matboard
    I = calculate_I(shapes_and_dim)
    Q=find_Q_max_centroid(shapes_and_dim)
    b=0

    for i,s in shapes_and_dim.items():
        if i in [2,5]:
            b+=s[1]
    P=(tau_matboard*I*b)/(Q*max_shear)
    return P

def shear_interface(shapes_and_dim):
    global max_shear, tau_glue
    I = calculate_I(shapes_and_dim)
    Q=find_Q_interfaces_top(shapes_and_dim)
    b=0
    for i,s in shapes_and_dim.items():
        if i in [1,4]:
            b+=s[1]
    P=(tau_glue*I*b)/(Q*max_shear)
    return P

def shear_bukling(shapes_and_dim,diaphramgs):
    '''check the value of t crit, might be too large'''
    global E,u,max_shear
    h=shapes_and_dim[0][3] + shapes_and_dim[0][0]
    t=shapes_and_dim[2][1]
    b= 2 * t  #at centroid
    print("h:",h,"t:",t)
    I=calculate_I(shapes_and_dim)
    Q=find_Q_max_centroid(shapes_and_dim)
    t_crit1= (5 * (math.pi**2) * E) / (12 * (1 - (u**2)))
    t_crit2= ((t/h)**2) + ((t/diaphramgs)**2)
    t_crit= t_crit1 * t_crit2
    P = (t_crit * I * b) / (Q*max_shear)
    return P


if __name__ == "__main__":
    area = []
    #Material Properties:
    theta_c = 6
    theta_t = 30
    tau_matboard = 4
    tau_glue = 2
    E = 4000
    u = 0.2
    lenght=280*2
    #enter the distance between webs
    b=60
    max_mom = 30.3
    max_shear=0.392
    print("Positive Zone")
    #                     height, length, centroid, dist from bot to bot edge
    shapes_and_dim= {6: (1.27, 3.81, 0.635, 0),
    3: (1.27, 3.81, 0.635, 0),
    2: (80, 1.27, 41.27, 1.27), 
    5: (80, 1.27, 41.27, 1.27), 
    1: (1.27, 3.81, 81.905, 81.27), 
    4: (1.27, 3.81, 81.905, 81.27), 
    0: (1.27, 100.0, 83.80999999999999, 82.53999999999999)}
    # ------------------  |
    # ------------------  |   0
    #   ---        ---    | 1   4
    #   -            -
    #   -            -    | 2   5
    #   -            -
    #   -            -
    #   ---        ---    | 3    6
    shapes_and_dim=calculate_right_heights1(shapes_and_dim)
    print(shapes_and_dim)
    shapes_and_dim = calculate_local_centroid(shapes_and_dim)
    print(shapes_and_dim)
    print("I", calculate_I(shapes_and_dim))
    print("Max Q", find_Q_max_centroid(shapes_and_dim))
    print("Q Interface top", find_Q_interfaces_top(shapes_and_dim))
    print("Plate buckling 1", plate_buckling_1_top(shapes_and_dim,b))
    print("Plate buckling 2", plate_buckling_2_top(shapes_and_dim,b))
    print("Web buckling", web_buckling(shapes_and_dim))
    print("Max shear stress", max_shear_stress(shapes_and_dim))
    print("Sheer interface", shear_interface(shapes_and_dim))
    print("Max bending tension", max_bending_tension(shapes_and_dim))
    print("Max bending compression", max_bending_compressive(shapes_and_dim))
    print("max sheer stress", max_shear_stress(shapes_and_dim))
    print("sheer interface", shear_interface(shapes_and_dim))
    print("Sheer buckling", shear_bukling(shapes_and_dim, 300))
    area.append(total_area(shapes_and_dim))
    print("Total area", total_area(shapes_and_dim) + 98000)
    print("matboard area:",(813*1016))

    print("total area used =", sum(area) + 98000)
    remaining = (813*1016) - (sum(area)  + 98000)
    print("remaining", remaining)
    

    '''
    We need the shear force diagrams
    For this beam: as follows:

    Shear Force Diagram
    max shear : 
    Bending Moment diagram
    max moment: 30.3P
    '''
    Matboard_used = 106192.7