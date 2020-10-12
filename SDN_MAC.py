import matplotlib.pyplot as plt
from pylab import *
import numpy as np
import numpy as np1 
import random
from Car import Car

DS =10 
TOLERANCE_TIME=0 
ARR_DEP_RATE = 0.833 
TRAFFIC_DENSITY_MIN = 0 
                        
TRAFFIC_DENSITY_MAX = 500 
LANE_SEPARATION =3 
COM_RANGE = 0   
COM_TIME_SAME_NEIGHBORS =100 
NUM_ITERATIONS = 0


lane1_car_positions = [] 
lane2_car_positions =[] 
lane3_car_positions = [] 
lane4_car_positions = [] 
lane1_cars= [] 
lane2_cars = []  
lane3_cars =[] 
lane4_cars =[] 
car_positions_in_each_lane = [lane1_car_positions, lane2_car_positions, lane3_car_positions, lane4_car_positions]   
cars_in_all_lanes = [lane1_cars, lane2_cars, lane3_cars, lane4_cars]        
target_car_position = [] 
id =0





def start_model():
    global target_car_position
    global id
    global car_positions_in_each_lane
    global cars_in_all_lanes


    
    for i in range(len(car_positions_in_each_lane)):
        lane = 2 +(i*3)
        for j in range(TRAFFIC_DENSITY_MIN):
            
            while True:
                y_axis =round(np.random.uniform(0,5000))

                
                if  not  y_axis in car_positions_in_each_lane[i]:
                    break
            car_positions_in_each_lane[i].append(y_axis)
            car = Car(lane,y_axis,id)
            id+=1
            cars_in_all_lanes[i].append(car)

    
    while True:
        lane = random.choice([0,1,2,3])
        y_axis = round(np.random.uniform(0,5000))
        lane_axis = 2 +(lane*3)
        target_car_position =[lane_axis,y_axis]


        
        if not y_axis in car_positions_in_each_lane[lane]:
            cars_in_all_lanes[lane].append(Car(lane_axis,y_axis,id,True))
            id+=1
            car_positions_in_each_lane[lane].append(y_axis)
            break





def entry_exit_vehicle(iteration):
    global id
    global target_car_position
    
    for i in range(len(car_positions_in_each_lane)):
        lane = 2 + (i*3)
        rand = np.mean(np.random.exponential(1,iteration+1))
        
        if len(car_positions_in_each_lane[i]) < TRAFFIC_DENSITY_MAX:
            if rand < ARR_DEP_RATE:
                
                ramp = random.choice([1500,2500,4000])
                if not ramp in car_positions_in_each_lane[i]:
                    cars_in_all_lanes[i].append(Car(lane,ramp,id))
                    id+=1
                    car_positions_in_each_lane[i].append(ramp)


        
        iterator = [1550,2550,4050]
        if len(car_positions_in_each_lane[i]) > TRAFFIC_DENSITY_MIN:
            for j in iterator:
                
                if j in car_positions_in_each_lane[i]:
                    
                    rand = np1.mean(np1.random.exponential(1,iteration+1))
                    if rand <  ARR_DEP_RATE:
                        
                        index = car_positions_in_each_lane[i].index(j)
                        
                        if cars_in_all_lanes[i][index].special == False :
                            car_positions_in_each_lane[i].remove(car_positions_in_each_lane[i][index])
                            car = cars_in_all_lanes[i][index]
                            cars_in_all_lanes[i].remove(cars_in_all_lanes[i][index])
                            del(car)



def update_model():

    global target_car_position
    global id

    cars_neighbors = [] 

    
    for i in range(5):
        for j in range(NUM_ITERATIONS):
            if j % 10 ==0:  
                entry_exit_vehicle((i*600)+j)
            cars_neighbors_100ms=[]
            
            for k in range(len(cars_in_all_lanes)):
                for m in range(len(cars_in_all_lanes[k])):
                    
                    try:
                        coordinates =cars_in_all_lanes[k][m].get_coordinates()
                        l = list(range(round(coordinates[1])+1,round(coordinates[1])+DS)) 
                    except IndexError:
                        break 

                    
                    cars_in_front =list(set(car_positions_in_each_lane[k]) & set (l))
                    if not cars_in_front :
                        cars_in_all_lanes[k][m].update_car_properties(False)
                        
                        car_positions_in_each_lane[k][m]=cars_in_all_lanes[k][m].y_axis
                    else:
                        same_lane = not lane_change(k,m,car_positions_in_each_lane[k][m])
                        if same_lane == False:
                            m -=1
                            if m <= 0:
                                m = 0
                            continue
                        cars_in_all_lanes[k][m].update_car_properties(True,min(cars_in_front)-coordinates[1])
                        car_positions_in_each_lane[k][m]=cars_in_all_lanes[k][m].y_axis

                    
                    if cars_in_all_lanes[k][m].special == True:
                        target_car_position= cars_in_all_lanes[k][m].get_coordinates()


                    
                    if cars_in_all_lanes[k][m].y_axis >5000:
                        target = cars_in_all_lanes[k][m].special

                    
                        car =cars_in_all_lanes[k][m]
                        cars_in_all_lanes[k].remove(cars_in_all_lanes[k][m])
                        car_positions_in_each_lane[k].remove(car_positions_in_each_lane[k][m])
                        del(car)
                        
                        m -=1
                        if m <0:
                            m = 0

                    
                        if len(cars_in_all_lanes[k]) ==TRAFFIC_DENSITY_MIN:
                            lane = k
                        else:
                            lane = random.choice([0,1,2,3])

                        
                        temp_list = set(range(0,5000))
                        pos =car_positions_in_each_lane[lane]
                        entry_position = random.choice(list(temp_list.difference(pos)))
                        cars_in_all_lanes[lane].append(Car(2+(lane*3),entry_position,id,target))
                        if target ==True:
                            target_car_position = [2+(lane*LANE_SEPARATION),entry_position]
                        id+=1
                        car_positions_in_each_lane[lane].append(entry_position)
                        continue

                    
                    if cars_in_all_lanes[k][m].special == False:
                        inside = math.pow((cars_in_all_lanes[k][m].x_axis -target_car_position[0]),2) + \
                                 math.pow((cars_in_all_lanes[k][m].y_axis -target_car_position[1]),2)
                        if inside <= math.pow(COM_RANGE,2):
                             cars_neighbors_100ms.append(cars_in_all_lanes[k][m].id)
            cars_neighbors.append(cars_neighbors_100ms)

    print("car_neighbors",cars_neighbors)
    return get_com_neighbor_info(cars_neighbors)






def lane_change(i,j,car_pos):
    is_car_within_safety_distance = False               
    lane_to_move_to = 0
    possible_lanes = []

    if i==0 or i==3:

        if i == 0:
            lane_to_move_to = 1
        elif i == 3:
            lane_to_move_to = 2


        
        if len(car_positions_in_each_lane[i]) <= TRAFFIC_DENSITY_MIN or len(car_positions_in_each_lane[lane_to_move_to]) >= TRAFFIC_DENSITY_MAX:
            
            return False

        points_within_safety_distance = list(range(car_pos-10,car_pos+11))

        for k in car_positions_in_each_lane[lane_to_move_to]:           
            
            
            if k in points_within_safety_distance:
                is_car_within_safety_distance = True    
                break
            else:
                is_car_within_safety_distance = False       

        if (is_car_within_safety_distance == False):
            
            move_car_to_next_lane(lane_to_move_to, car_pos, i, j)
            return True
        else:
            
            return False


    elif i == 1 or i == 2:
        possible_lanes = [i-1,i+1]                          
        lane_to_move_to = random.choice(possible_lanes)     

        if len(car_positions_in_each_lane[i]) <= TRAFFIC_DENSITY_MIN:
            
            return False

        n = 0
        points_within_safety_distance = list(range(car_pos-10,car_pos+11))  

        while n < 2:
            is_car_within_safety_distance = False                           

            for k in car_positions_in_each_lane[lane_to_move_to]:           
                
                if k in points_within_safety_distance:
                    is_car_within_safety_distance = True        
                    break
                else:
                    is_car_within_safety_distance = False

            if len(car_positions_in_each_lane[lane_to_move_to]) >= TRAFFIC_DENSITY_MAX:
                
                is_car_within_safety_distance = True

            if is_car_within_safety_distance == True:
                n = n+1
            else:
                n = 2

            if ( n < 2 and is_car_within_safety_distance == True):
                
                possible_lanes.remove(lane_to_move_to)              
                lane_to_move_to = possible_lanes[0]                 


        if (is_car_within_safety_distance == False):
            
            move_car_to_next_lane(lane_to_move_to, car_pos, i, j)
            return True
        else:
            return False


def move_car_to_next_lane(lane_to_move_to, car_pos, i, j):
    global car_positions_in_each_lane
    global car_in_all_lanes
    global id
    
    car_positions_in_each_lane[lane_to_move_to].append(car_pos)                                     
    cars_in_all_lanes[i][j].set_coordinates((2+(LANE_SEPARATION*lane_to_move_to)), car_pos)                       
    cars_in_all_lanes[lane_to_move_to].append(cars_in_all_lanes[i][j])                           
    cars_in_all_lanes[i].remove(cars_in_all_lanes[i][j])
    car_positions_in_each_lane[i].remove(car_pos)                                                   


def get_com_neighbor_info(neighbors_100ms):
    num_neighbors=[]
    same_3_neighbors = sorted(neighbors_100ms[0])
    same_3_neighbors_time =0
    same_3_neighbors_times=[]
    same_3_neighbors_count =0
    same_neighbors = sorted(neighbors_100ms[0])
    same_neighbors_time =0
    same_neighbors_lengths=[]
    same_neighbors_count =0

    
    for i in range(len(neighbors_100ms)):
        
        current =neighbors_100ms[i]
        current_length = len(current)
        num_neighbors.append(current_length)
        
        try:
            next =neighbors_100ms[i+1]
        except IndexError:
            if same_3_neighbors_time !=0:
                same_3_neighbors_times.append(same_3_neighbors_time)
            if same_neighbors_time> COM_TIME_SAME_NEIGHBORS:
                same_neighbors_lengths.append(len(same_neighbors))
            break

    
        if not current:
            same_3_neighbors=sorted(set(next))
            
            if same_3_neighbors_time !=0:
                same_3_neighbors_times.append(same_3_neighbors_time)
            same_3_neighbors_time=0
            same_neighbors= sorted(set(next))
            same_neighbors_time=0
            continue

        
        sorted(current)
        sorted(next)

        
        if len(set(same_3_neighbors) & set(next)) >=3:
            same_3_neighbors_time+=1
            same_3_neighbors= sorted(set(same_3_neighbors) & set(next))
        else:

            
            if same_3_neighbors_time !=0:
                same_3_neighbors_times.append(same_3_neighbors_time)
                same_3_neighbors_time=0

        
        if set(same_neighbors).issubset(set(next)) :
            
            
            same_neighbors_time+=1
            if same_neighbors_time> COM_TIME_SAME_NEIGHBORS:
                same_neighbors_lengths.append(len(same_neighbors))
                print("S_N_L:",same_neighbors_lengths)

                same_neighbors_time =0
        
        else:
            same_neighbors= next
            same_neighbors_time=0
    avg_num_neighbors = round(np.mean(num_neighbors))
    if same_3_neighbors_times:
       same_3_neighbors_count = round(np.mean(same_3_neighbors_times)*100) 
    if same_neighbors_lengths:
        same_neighbors_count = round(np.mean(same_neighbors_lengths))
    print('Get_com_neighbors')
    print([avg_num_neighbors,same_3_neighbors_count,same_neighbors_count])
    print('Same_3_neighbors',same_3_neighbors)
    return [avg_num_neighbors,same_3_neighbors_count,same_neighbors_count]


def reset_model():
    global target_car_position
    global id
    global car_positions_in_each_lane
    global cars_in_all_lanes
    global lane1_car_positions,lane2_car_positions, lane3_car_positions, lane4_car_positions
    global lane1_cars ,lane2_cars ,lane3_cars ,lane4_cars

    
    lane1_car_positions = []
    lane2_car_positions =[]
    lane3_car_positions = []
    lane4_car_positions = []
    lane1_cars= []
    lane2_cars = []
    lane3_cars =[]
    lane4_cars =[]
    car_positions_in_each_lane = [lane1_car_positions, lane2_car_positions, lane3_car_positions, lane4_car_positions]
    cars_in_all_lanes = [lane1_cars, lane2_cars, lane3_cars, lane4_cars]        
    target_car_position = [] 
    id =0





traffic_densities = list(range(100,550,50))

num_neighbors = [] 
time_3_neighbors =[] 
same_neighbors = [] 
fig1 = plt.figure(1)
fig2 = plt.figure(2)
fig3 = plt.figure(3)
ax1 = fig1.add_subplot(111)
ax2 = fig2.add_subplot(111)
ax3 = fig3.add_subplot(111)


ax1.grid(True)
ax1.set_xlim([0,550])
ax1.ticklabel_format(useOffset=False)
ax2.grid(True)
ax2.ticklabel_format(useOffset=False)
ax2.set_xlim([0,550])
ax3.grid(True)
ax3.set_xlim([0,550])
ax3.ticklabel_format(useOffset=False)


COM_RANGE = int(input('Enter the communication range: '))
NUM_ITERATIONS = int(input('Enter the number of 100ms iterations desired: '))


for i in traffic_densities:
    
    TRAFFIC_DENSITY_MIN = i
    
    
    reset_model()
    start_model()
    results=update_model()
    print("results",results)
    num_neighbors.append(results[0])
    time_3_neighbors.append(results[1])
    same_neighbors.append(results[2])


ax1.set_title('Average number of VANET neighbors')
ax1.set_xlabel('traffic density per lane')
ax1.set_ylabel('vehicles')
ax1.scatter(traffic_densities,num_neighbors)
ax1.plot(traffic_densities,num_neighbors ,label='number of neighbors')
legend = ax1.legend(loc='upper center', shadow=True)


ax2.set_title('Average time with at least 3 same neighbors')
ax2.set_xlabel('traffic density per lane')
ax2.set_ylabel('Time (ms)')
ax2.scatter(traffic_densities,time_3_neighbors)
ax2.plot(traffic_densities,time_3_neighbors,label='time with at least same three neighbors')
legend = ax2.legend(loc='upper center', shadow=True)

ax3.set_title('Same communication neighbors the target have for 10 seconds')
ax3.set_xlabel('traffic density per lane')
ax3.set_ylabel('vehicles')
ax3.scatter(traffic_densities,same_neighbors)
ax3.plot(traffic_densities,same_neighbors, label='number of same com neighbors for 10 seconds')
legend = ax3.legend(loc='upper center', shadow=True)


plt.show()





























