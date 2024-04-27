import numpy as np
import matplotlib
import turtle as t 

turt = t.Turtle() 
turt.penup()
turt.speed(0)
t.bgcolor("grey")
turt.shape("square")
turt.shapesize(5)
bias = 0 

matrix = [1, 1, 
          -1, -1]
    
desired_matrix = [1, 1, 
                 -1, -1]

def show_checkerbox(): 
    turt.shapesize(5)
    turt.clear()
    turt.goto(0,0)
    
    for index, item in enumerate(matrix):
        if item ==1: 
            turt.color("white")
        else: 
            turt.color("black")
        
        turt.stamp()
        turt.fd(100)
        
        if index == 1: 
            turt.goto(0, -100)
    
    turt.goto(300,300)
    turt.shapesize(0.5)        
show_checkerbox()

class neuron():
    def __init__(self, *args:list[tuple], Bias=0, is_input_neuron=None, is_output_neuron=[], output_msg=""):
        #self.passedValue = 1 / (1+ np.e**(Win1*in1 + Win2*in2 + is_input_neuron - Bias))  
        self.connections = [item[0]*item[1] for item in args]
        self.passedValue = sum(self.connections) - Bias
        self.AValue = 0
        
        if is_input_neuron != None: 
            self.AValue = is_input_neuron
        elif self.passedValue > 0: 
            self.AValue = 1
        else: 
            self.AValue = 0    
        
        if is_output_neuron != [] and self.passedValue > 0:   
            print(is_output_neuron)  
            print(output_msg)
            print("sigmoid value:", self.passedValue)
    
    def activation(self) -> int: 
        return self.AValue
    
 
loost = []
for i in range(5):
    loost.append(neuro = neuron(is_input_neuron=1).activation())
print(loost[3])


#Layer One (Input)            
cell_one = neuron(is_input_neuron=matrix[0])
cell_two = neuron(is_input_neuron=matrix[1])
cell_three = neuron(is_input_neuron=matrix[2])
cell_four = neuron(is_input_neuron=matrix[3])

#Layer Two (Output Prep)
top_white_rect = neuron((cell_one.activation(), 1), (cell_two.activation(), 1), is_output_neuron=desired_matrix, output_msg="top white")
bottom_white_rect = neuron((cell_three.activation(), 1), (cell_four.activation(), 1), is_output_neuron = [-1, -1, 1, 1], output_msg="bottom white")




over = input("over?")