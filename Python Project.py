#!/usr/bin/env python
# coding: utf-8

# In[7]:


import pandas as pd
import matplotlib.pyplot as plt   
import geopandas
from shapely.geometry import Point
import seaborn as sns
from datetime import datetime
get_ipython().run_line_magic('matplotlib', 'inline')


# In[15]:


#Reading in the raw data
uwpd = pd.read_excel(r"C:\Users\joshi\OneDrive\Desktop\Work Stuff\Extra Work & Certifications\Python Work\Joshi_Final_Project\UWPD Data.xls", header = 1,sheet_name='2019')
uwpd.head()


# In[16]:


#Changing the Time column to a datetime object by creating a new column and dropping the old one
uwpd['time'] = pd.to_datetime(uwpd['TIME'])
uwpd.drop('TIME', axis=1, inplace = True)
uwpd['time'] = pd.Series([val.time() for val in uwpd['time']])
uwpd


# In[17]:


#Finding all offense names present in data
#Using a set so I do not get repeat entries
all_offenses= uwpd['OFFENSE'].tolist()
all_offenses = set(all_offenses)
all_offenses


# In[18]:


uwpd.rename(columns = {'time':'TIME' }, inplace=True)


# In[19]:


fig, ax = plt.subplots(figsize=(20,5)) 
# Create a histogram of Offense frequency.

uwpd['OFFENSE'].value_counts().plot.bar()
ax.set_ylabel('FREQUENCY') 
ax.set_xlabel('OFFENSES')
ax.set_title('Frequency of each Offense in 2019')
ax.spines['right'].set_visible(False) # get ride of the line on the right
ax.spines['top'].set_visible(False)   # get rid of the line on top
plt.xticks(rotation=75) 
plt.show()


# In[20]:


#Renaming column names
uwpd = uwpd.rename(columns = {'OFFENSE': 'Offense', 'MONTH':'Month', 'LOCATION':'Location', 'OUTCOME':'Outcome', 'TIME':'Time'})

#Re-structuring the datetime objects and dropping/renaming columns
uwpd['Month1'] = uwpd['Month'].dt.strftime('%m/%Y')
uwpd = uwpd.drop(['Month'], axis = 1)
uwpd = uwpd.rename(columns = {'Month1': 'Month'})
uwpd


# In[21]:


uwpd = uwpd[['Month','Offense','Location','Time','Outcome']]
uwpd


# In[22]:


#I'm sure there is a more efficient way to do this
# Wanted to change all dates from MM/YYYY to Strings & find how many incidents where in each month at the same time
# Stored the result in the dictionary
result = {}
count1 = 0
count2 = 0
count3 = 0
count4 = 0
count5 = 0
count6 = 0
count7 = 0
count8 = 0
count9 = 0
count10 = 0
count11 = 0
count12  = 0
for i in range(len(uwpd)):
    if uwpd['Month'][i][0:2] == '01':
        count1+=1
        result['January'] = count1
        
    if uwpd['Month'][i][0:2] == '02':
        count2+=1
        result['February'] = count2
        
    if uwpd['Month'][i][0:2]== '03':
        count3+=1
        result['March'] = count3
        
    if uwpd['Month'][i][0:2] == '04':
        count4+=1
        result['April'] = count4
        
    if uwpd['Month'][i][0:2] == '05':
        count5+=1
        result['May'] = count5 
        
    if uwpd['Month'][i][0:2] == '06':
        count6+=1
        result['June'] = count6
        
    if uwpd['Month'][i][0:2] == '07':
        count7+=1
        result['July'] = count7
        
    if uwpd['Month'][i][0:2] == '08':
        count8+=1
        result['August'] = count8   
        
    if uwpd['Month'][i][0:2] == '09':
        count9+=1
        result['September'] = count9         
        
    if uwpd['Month'][i][0:2] == '10':
        count10+=1
        result['October'] = count10         
        
    if uwpd['Month'][i][0:2] == '11':
        count11+=1
        result['November'] = count11         
        
    if uwpd['Month'][i][0:2]== '12':
        count12+=1
        result['December'] = count12          
        
result


# In[23]:


#Same thing but created a new column with default values to store the incident numbers I found above
uwpd['Count'] = 'default'
for i in range(len(uwpd)):
    if uwpd['Month'][i][0:2] == '01':
        uwpd['Month'][i] = 'January'
        uwpd['Count'][i] = 31
        
    if uwpd['Month'][i][0:2] == '02':
        uwpd['Month'][i] = 'February'
        uwpd['Count'][i] = 30

    if uwpd['Month'][i][0:2] == '03':
        uwpd['Month'][i] = 'March'
        uwpd['Count'][i] = 29

    if uwpd['Month'][i][0:2] == '04':
        uwpd['Month'][i] = 'April'
        uwpd['Count'][i] = 50

    if uwpd['Month'][i][0:2] == '05':
        uwpd['Month'][i] = 'May'
        uwpd['Count'][i] = 27

    if uwpd['Month'][i][0:2] == '06':
        uwpd['Month'][i] = 'June'
        uwpd['Count'][i] = 35

    if uwpd['Month'][i][0:2] == '07':
        uwpd['Month'][i] = 'July'
        uwpd['Count'][i] = 42

    if uwpd['Month'][i][0:2] == '08':
        uwpd['Month'][i] = 'August'
        uwpd['Count'][i] = 50

    if uwpd['Month'][i][0:2] == '09':
        uwpd['Month'][i] = 'September' 
        uwpd['Count'][i] = 49

    if uwpd['Month'][i][0:2] == '10':         
        uwpd['Month'][i] = 'October'
        uwpd['Count'][i] = 57

    if uwpd['Month'][i][0:2] == '11':
        uwpd['Month'][i] = 'November'
        uwpd['Count'][i] = 41

    if uwpd['Month'][i][0:2] == '12':
        uwpd['Month'][i] = 'December'
        uwpd['Count'][i] = 42
uwpd


# In[24]:


#Plotting the frequency of incidents per month
fig,  ax = plt.subplots(figsize=(15,5))

ax.plot(uwpd['Month'], uwpd['Count'])

ax.set_ylabel("Number of Incidents")
ax.set_xlabel("Month")
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.set_title("Incidents per Month in 2019")


# In[25]:


#Taking the top ten locations and finding their frequency of incidents
locations = set(uwpd['Location'])
result = {}
count1=0
count2=0
count3=0
count4=0
count5=0
count6=0
count7=0
count8=0
count9=0
count10=0
for i in range(len(uwpd)):
    if uwpd['Location'][i] == '600 HIGHLAND AV':
        count1+=1
        result['600 Highland Av'] = count1
        
    elif uwpd['Location'][i] == '800 LANGDON ST':
        count2+=1
        result['800 Langdon St'] = count2
        
    elif uwpd['Location'][i] == '610 HIGHLAND AV':
        count3+=1
        result['610 Highland Avenue'] = count3
        
    elif uwpd['Location'][i] == '455 N PARK ST':
        count4+=1
        result['455 N Park St'] = count4
        
    elif uwpd['Location'][i] == '1430 MONROE ST':
        count5+=1
        result['1430 Monroe St'] = count5
    elif uwpd['Location'][i] == '1308 W DAYTON ST':
        count6+=1
        result['1308 W Dayton St'] = count6
    elif uwpd['Location'][i] == '600 N PARK ST':
        count7+=1
        result['600 N Park St'] = count7
    elif uwpd['Location'][i] == '821 W JOHNSON ST':
        count8+=1
        result['821 W Johnson St'] = count8
    elif uwpd['Location'][i] == '615 W JOHNSON ST':
        count9+=1
        result['615 W Johnson St'] = count9  
    elif uwpd['Location'][i] == '770 W DAYTON ST':
        count10+=1
        result['770 W Dayton St'] = count10
    
result


# In[26]:


#Created a dataframe to plot the correlation between location and incident level
df = {
    'Location': ['600 Highland Av','800 Langdon St','610 Highland Avenue','1430 Monroe St','455 N Park St',
                 '1308 W Dayton St','600 N Park St','821 W Johnson St','615 W Johnson St','770 W Dayton St'],
    'Incidents': [48,30,27,19,19,16,15,11,9,9]
}

df = pd.DataFrame(df)
ax = df.plot.bar(figsize=(20,5),rot = 0, legend = None, x = "Location")
ax.set_ylabel('Incidents', fontsize = 15)
ax.set_xlabel('Location', fontsize = 15)
ax.set_title('Incidents per Most Common Locations (2019)', fontsize = 20)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)


# In[27]:


#Creating a dataframe that depicts location and respective longitude/latitude
location = pd.DataFrame({'Location': ['600 Highland Av', '800 Langdon St', '610 Highland Av', '455 N Park St', '1430 Monroe St', '1308 W Dayton St', '600 N Park St', '821 W Johnson St', '615 W Johnson St', '770 W Dayton St'],
                     'Longitude': [-89.42911,-89.39898,-89.42915,-89.40075, -89.41239, -89.407890, -89.401360,-89.39984,-89.39735,-89.39947],
                      'Latitude': [43.077255,43.075844,43.07742,43.062325,43.068066, 43.071850, 43.076660, 43.072075, 43.072014, 43.070934]})
location['Coordinates'] = list(zip(location.Longitude,location.Latitude)) 
location['Coordinates'] = location['Coordinates'].apply(Point)
location 


# In[28]:


#Locking in the coordinates for each location
glocation = geopandas.GeoDataFrame(location, geometry = 'Coordinates')
glocation


# In[36]:


#Downloaded essential information from cityofmadison.com
wisc_map = geopandas.read_file(r"C:\Users\joshi\OneDrive\Desktop\Work Stuff\Extra Work & Certifications\Python Work\Joshi_Final_Project\City_Limit-shp\0168939f-fec2-48f2-8c86-73dea806abf92020329-1-deilff.6mf5b.shp")
wisc_lakes = geopandas.read_file(r"C:\Users\joshi\OneDrive\Desktop\Work Stuff\Extra Work & Certifications\Python Work\Joshi_Final_Project\Lakes_and_Rivers-shp\f5b114cc-178c-4165-bb6a-4164d8b8f7cc2020329-1-1lpyrv8.yndd.shp")
police = geopandas.read_file(r"C:\Users\joshi\OneDrive\Desktop\Work Stuff\Extra Work & Certifications\Python Work\Joshi_Final_Project\Police_Stations-shp\fd8155aa-9bfd-4d5b-be4f-008c8f7880182020329-1-7fwwor.fdxwx.shp")
streets = geopandas.read_file(r"C:\Users\joshi\OneDrive\Desktop\Work Stuff\Extra Work & Certifications\Python Work\Joshi_Final_Project\Street_Centerlines_and_Pavement_Data-shp\f35fc2c9-abe7-419f-9d70-56bf958365ec2020329-1-z8lqni.p66r.shp")


# In[39]:


# Here I plotted all the information from the cell above. Re-formatted the colors of the points and streets 
# so everything would be clear and visible properly. I added the 'Capital' landmark to give the viewer
# a sense of direction because the streets are difficult to see. 
# Only added the most 'dangerous' locations because others would have overlapped. 
ax = wisc_map.plot(color='gray', alpha = 0.3, figsize = (20,15))
wisc_lakes.plot(ax=ax, color="lightblue")
streets.plot(ax=ax, color = "white", alpha = 0.4)
police.plot(ax=ax, color = 'blue', label = "Police Stations")
glocation.plot(ax=ax, color = "red", label = "Top 10 Incident Locations")
plt.legend(loc = 'upper right', frameon= False)
ax.text(-89.381,43.073,"Capital")
ax.text(-89.44,43.080,"600/610 Highland Av", fontsize = 10)
ax.text(-89.425,43.110, "LAKE MENDOTA")
ax.text(-89.36,43.075, "LAKE MONONA")
ax.text(-89.56, 43.175, "MADISON, WISCONSIN", fontsize = 20)
ax.set_axis_off()


# In[40]:


#Here I attempt to change the datatype of the 'Time' Column to strings 
#so I can then replace the time with values that correspond to that time

uwpd['Time'] = uwpd['Time'].astype(str)
for i in range(len(uwpd)):
    time = uwpd['Time'][i]
    if (uwpd['Time'][i] >= '12:00:00') & (uwpd['Time'][i] <= '17:00:00'):
        uwpd['Time'] = uwpd['Time'].replace(uwpd['Time'][i], "After-Noon (12pm - 5pm)")
    elif (uwpd['Time'][i] >= '18:00:00') & (uwpd['Time'][i] <= '23:00:00'):
        uwpd['Time'] = uwpd['Time'].replace(uwpd['Time'][i], "Evening (6pm - 11pm)")
    elif (uwpd['Time'][i] >= '00:00:00') & (uwpd['Time'][i] <= '4:00:00'):
        uwpd['Time'] = uwpd['Time'].replace(uwpd['Time'][i], "After-Midnight (12am - 4am)")
    elif (uwpd['Time'][i] >= '05:00:00') & (uwpd['Time'][i] <= '10:00:00'):
        uwpd['Time'] = uwpd['Time'].replace(uwpd['Time'][i], "Morning (5am - 10am)")


# In[41]:


# Plotting the bar-plot that relates frequency of incidents depending on time of day
# No incidents happen in the morning, that's why 5am-10am is missing
fig, ax = plt.subplots(figsize=(15,5))

uwpd['Time'].value_counts().plot.bar(rot = 0, width = 0.3)

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.set_ylabel('Frequency of Incident', fontsize = 15)
ax.set_xlabel('Time of Incident', fontsize = 15)
ax.set_title('Number of Incidents Based on Time of Day', fontsize = 20)

