import math

def calculate_right_heights3(shapes_and_dim):
    new={}
    new[2]=(shapes_and_dim[2][0],shapes_and_dim[2][1], shapes_and_dim[2][2], 0)

    new[3]=(shapes_and_dim[3][0], shapes_and_dim[3][1], shapes_and_dim[3][2], new[2][0])
    new[1]=(shapes_and_dim[1][0], shapes_and_dim[1][1], shapes_and_dim[1][2], new[2][0])

    new[0]=(shapes_and_dim[0][0],shapes_and_dim[0][1], shapes_and_dim[0][2], new[1][0] + new[1][3])
    return new

def calculate_local_centroid(shapes_and_dim):
    new={}
    for k,v in shapes_and_dim.items():
        new_value=(shapes_and_dim[k][0],shapes_and_dim[k][1], (shapes_and_dim[k][0]/2)+shapes_and_dim[k][3], shapes_and_dim[k][3])
        new[k]=new_value

    return new

def find_shape_centroid(shapes_and_dim):
    sum_numerator = 0
    sum_denom = 0
    for key,value in shapes_and_dim.items():
        dims = shapes_and_dim[key]
        area = dims[0] * dims[1]
        d = dims[2]
        sum_numerator = sum_numerator + (area*d)
        sum_denom = sum_denom + area

    shape_centroid = sum_numerator/sum_denom
    return shape_centroid

def find_Q_max_centroid(shapes_and_dim):
    y=find_shape_centroid(shapes_and_dim)
    Q=0
    for k,v in shapes_and_dim.items():
        d=v
        if k in [2,3,5,6,7]:
            if v[0]>=y:
                print(k)
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

def find_Q_interfaces_top(shapes_and_dim):
    '''the same top and bottom because symmetric'''
    d=shapes_and_dim[0]
    y=find_shape_centroid(shapes_and_dim)
    A=d[0]*d[1]
    d=d[2]-y
    return A*d


def calculate_I(shapes_and_dim):
    shape_centroid = find_shape_centroid(shapes_and_dim)
    sum_I = 0
    for key, value in shapes_and_dim.items():
        dims = shapes_and_dim[key]
        I_0 = (dims[1] * (dims[0])**3) / 12
        A = dims[0] * dims[1]
        d = abs(dims[2] - shape_centroid)
        I_t = I_0 + A*(d**2)
        sum_I = sum_I + I_t
    return sum_I

def plate_buckling_1_top(shapes_and_dim,b):
    global max_mom,E,u
    t = shapes_and_dim[2][0]
    bot = 1.27
    theta_c = ((4*((math.pi)**2)*E) / ((12*(1 - u**2)))) * ((t/b)**2)
    y_bar = find_shape_centroid(shapes_and_dim)
    I = calculate_I(shapes_and_dim)
    coeff_p = ((max_mom) * (abs(bot - y_bar))) / I
    P = theta_c / coeff_p
    return P

def web_buckling(shapes_and_dim):
    global max_mom,E,u
    t = shapes_and_dim[1][1]
    y_bar = find_shape_centroid(shapes_and_dim)
    top=0
    b = top - y_bar
    theta_c = ((6*((math.pi)**2)*E) / (12*(1 - u**2))) * (t/b)**2
    I = calculate_I(shapes_and_dim)
    coeff_p = ((max_mom) * (abs(top - y_bar))) / I
    P = theta_c / coeff_p
    return P

def max_bending_compression(shapes_and_dim):
    global max_mom,theta_c
    I = calculate_I(shapes_and_dim)
    shape_centroid = find_shape_centroid(shapes_and_dim)
    P = ((theta_c * I)/(shape_centroid * max_mom))
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
    '''write a new funtion if it's not simmetric'''
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
    # ---------- 0
    # --------- 
    # |  |      1   3
    # |  |      
    # |  |      
    # |  |     
    # |  |     
    # |  |        
    # ---------
    # ---------  2
    area = []
    #Material Properties:
    theta_c = 6
    theta_t = 16
    tau_matboard = 4
    tau_glue = 2
    E = 4000
    u = 0.2
    lenght=280*2
    #enter the distance between webs
    b = 80
    max_mom = 45
    max_shear = 0.392
    #                 height, length, centroid, dist from bot to bot edge
    shapes_and_dim= {1: (600, 2.54, 81.905, 81.27), 
                     3: (600, 2.54, 81.905, 81.27), 
                     0: (1.27, 50.0, 83.80999999999999, 82.53999999999999),
                     2: (1.27, 50.0, 86.31, 0)}
    shapes_and_dim=calculate_right_heights3(shapes_and_dim)
    print(shapes_and_dim)
    shapes_and_dim = calculate_local_centroid(shapes_and_dim)
    print(shapes_and_dim)
    print("shape centroid", find_shape_centroid(shapes_and_dim))
    print("I", calculate_I(shapes_and_dim))
    print("Max Q", find_Q_max_centroid(shapes_and_dim))
    print("Q Interface top", find_Q_interfaces_top(shapes_and_dim))
    print("Plate buckling 1", plate_buckling_1_top(shapes_and_dim,b))
    print("Web buckling", web_buckling(shapes_and_dim))
    print("Sheer interface", shear_interface(shapes_and_dim))
    print("Max bending compression", max_bending_compression(shapes_and_dim))