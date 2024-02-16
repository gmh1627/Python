from plotly.graph_objs import Bar,Layout
from plotly import offline
from random import randint
class Die:
    def __init__(self,sides=6):
        self.sides=sides
    def roll(self):
            return randint(1,self.sides)
die1=Die()
die2=Die(10)
results=[]
for roll_num in range(10000):
    result=die1.roll()+die2.roll()
    results.append(result)
frequences=[]
max=die1.sides+die2.sides
for value in range(2,max+1):
    frequency=results.count(value)
    frequences.append(frequency)
x_values=list(range(2,max+1))
data=[Bar(x=x_values,y=frequences)]
x_axis_config={'title':'result','dtick':1}
y_axis_config={'title':'frequency'}
my_layout=Layout(title='The result of 10000 times of rolling a 6 sided die and a 10 sided die',
                 xaxis=x_axis_config,yaxis=y_axis_config)
offline.plot({'data':data,'layout':my_layout},filename='d6_d10.html')
