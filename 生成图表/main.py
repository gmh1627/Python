import matplotlib.pyplot as plt
plt.style.use('seaborn')

# input_values=[1,2,3,4,5]
# squares = [1, 4, 9, 16, 25]
x_values=range(1,100)
y_values= [x**2 for x in x_values]
fig, ax = plt.subplots()
ax.scatter(x_values,y_values,c=x_values,cmap=plt.cm.Reds,s=10)
#ax.plot(input_values,squares, linewidth=3)
ax.set_title("squared number",fontsize=24)
ax.set_xlabel("value",fontsize=14)
ax.set_ylabel("square",fontsize=14)
ax.tick_params(axis='both',labelsize=14)
ax.axis([0,100,0,1100000])
plt.show()

