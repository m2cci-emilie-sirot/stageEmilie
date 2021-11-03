import numpy as np
import matplotlib.pyplot as plt
import datetime as dt

# Lecture des données
data = np.genfromtxt('emilie.csv', delimiter=';', skip_header = 1)

# Date de début
starting_date_str = str(data[0][0])
starting_year = int(starting_date_str[:4])
starting_month = int(starting_date_str[4:6])
starting_day = int(starting_date_str[6:8])
starting_date = dt.date(starting_year, starting_month, starting_day)

# Tableaux contenant les points (jour, valeur)
prod = []
ecor = []
bois = []
sub = []
land = []
medi = []

for i in range(0, len(data)):
    # Date courante
    current_date_str = str(data[i][0])
    current_year = int(current_date_str[:4])
    current_month = int(current_date_str[4:6])
    current_day = int(current_date_str[6:8])
    current_date = (dt.date(current_year, current_month, current_day) - starting_date).days

    if not np.isnan(data[i][6]):
        prod.append((current_date, float(data[i][6])))
    if not np.isnan(data[i][5]):
        ecor.append((current_date, float(data[i][5])))
    if not np.isnan(data[i][4]):
        bois.append((current_date, float(data[i][4])))
    if not np.isnan(data[i][3]):
        sub.append((current_date, float(data[i][3])))
    if not np.isnan(data[i][2]):
        land.append((current_date, float(data[i][2])))
    if not np.isnan(data[i][1]):
        medi.append((current_date, float(data[i][1])))
 
print("Exemple de tableau") 
print(prod)

points = np.array(prod)
# get x and y vectors
x_prod = points[:,0]
y_prod = points[:,1]

# calculate polynomial
z = np.polyfit(x_prod, y_prod, 5)
f_prod = np.poly1d(z)

# calculate new x's and y's
x_new_prod = np.linspace(x_prod[0], x_prod[-1], 100)
y_new_prod = f_prod(x_new_prod)

points = np.array(ecor)
# get x and y vectors
x_ecor = points[:,0]
y_ecor = points[:,1]

# calculate polynomial
z = np.polyfit(x_ecor, y_ecor, 5)
f_ecor = np.poly1d(z)

# calculate new x's and y's
x_new_ecor = np.linspace(x_ecor[0], x_ecor[-1], 100)
y_new_ecor = f_ecor(x_new_ecor)

points = np.array(bois)
# get x and y vectors
x_bois = points[:,0]
y_bois = points[:,1]

# calculate polynomial
z = np.polyfit(x_bois, y_bois, 5)
f_bois = np.poly1d(z)

# calculate new x's and y's
x_new_bois = np.linspace(x_bois[0], x_bois[-1], 100)
y_new_bois = f_bois(x_new_bois)

points = np.array(sub)
# get x and y vectors
x_sub = points[:,0]
y_sub = points[:,1]

# calculate polynomial
z = np.polyfit(x_sub, y_sub, 5)
f_sub = np.poly1d(z)

# calculate new x's and y's
x_new_sub = np.linspace(x_sub[0], x_sub[-1], 100)
y_new_sub = f_sub(x_new_sub)

points = np.array(land)
# get x and y vectors
x_land = points[:,0]
y_land = points[:,1]

# calculate polynomial
z = np.polyfit(x_land, y_land, 5)
f_land = np.poly1d(z)

# calculate new x's and y's
x_new_land = np.linspace(x_land[0], x_land[-1], 100)
y_new_land = f_land(x_new_land)

points = np.array(medi)
# get x and y vectors
x_medi = points[:,0]
y_medi = points[:,1]

# calculate polynomial
z = np.polyfit(x_medi, y_medi, 5)
f_medi = np.poly1d(z)

# calculate new x's and y's
x_new_medi = np.linspace(x_medi[0], x_medi[-1], 100)
y_new_medi = f_medi(x_new_medi)


plt.figure()
plt.subplots_adjust(hspace = 1.0)
plt.subplot(3,2,1)
plt.plot(x_prod, y_prod, x_new_prod, y_new_prod)
plt.xlim([x_prod[0]-1, x_prod[-1] + 1 ])
plt.title("prod")
plt.subplot(3,2,2)
plt.plot(x_ecor, y_ecor, x_new_ecor, y_new_ecor)
plt.xlim([x_ecor[0]-1, x_ecor[-1] + 1 ])
plt.title("ecor")
plt.subplot(3,2,3)
plt.plot(x_bois, y_bois, x_new_bois, y_new_bois)
plt.xlim([x_bois[0]-1, x_bois[-1] + 1 ])
plt.title("bois")
plt.subplot(3,2,4)
plt.plot(x_sub, y_sub, x_new_sub, y_new_sub)
plt.xlim([x_sub[0]-1, x_sub[-1] + 1 ])
plt.title("sub")
plt.subplot(3,2,5)
plt.plot(x_medi, y_medi, x_new_medi, y_new_medi)
plt.xlim([x_medi[0]-1, x_medi[-1] + 1 ])
plt.title("medi")
plt.subplot(3,2,6)
plt.plot(x_land, y_land, x_new_land, y_new_land)
plt.xlim([x_land[0]-1, x_land[-1] + 1 ])
plt.title("land")
plt.savefig("comparaison.png", dpi = 200)
plt.show()
plt.close()
