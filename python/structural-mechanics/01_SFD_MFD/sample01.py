import numpy as np
import matplotlib.pyplot as plt

#inputs
w = 500 # uniform distributed load(udL, 一様荷重) [N]　
L = 10 # Length of the beam [m]  
R = w*L/2 # reaction (反力)
x = np.linspace(0,L,100) 

# create list and loop for each length of the beam
X = []
SF = []
M = []
for l in x:
    sf = R -(w*l)   # calculate shear force　(せん断力)
    m = (R*l) - (w*l**2/2) # calculate moment (モーメント)
    X.append(l)
    SF.append(sf)
    M.append(m)

# set graph size
plt.figure(figsize=(10,10))

# plot for shear force diagram
plt.subplot(2,1,1)
plt.plot(X,SF)
plt.fill_between(X,SF,color='green',hatch='||',alpha=0.47)
plt.title("Shear Force Diagram (SFD)")
plt.xlabel('Length of Beam [m]')
plt.ylabel('Shear Force [N]')
plt.grid()

# plot for bending moment diagram
plt.tight_layout(pad = 3.0)
plt.subplot(2,1,2)
plt.plot(X,M)
plt.fill_between(X,M,color='red',hatch='\\',alpha=0.5)
plt.title('Bending Moment Diagram (BMD)')
plt.xlabel('Length of Beam [m]')
plt.ylabel('Moment [Nm]')
plt.grid()

plt.show()