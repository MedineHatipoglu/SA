#!/usr/bin/env python
# coding: utf-8

# In[1]:


#import needed libraries
import pandas as pd
pd.options.display.float_format = '{:,.2f}'.format
import numpy as np
import matplotlib.pyplot as plt


# In[2]:


#read the data user_day
df1=pd.read_csv('C:\\Users\\Snow\\Desktop\\sa_data_test\\user_day.csv', encoding='utf-8-sig', engine='python')
df1.head()


# In[3]:


#read the data user_cpi
df2=pd.read_csv('C:\\Users\\Snow\\Desktop\\sa_data_test\\user_cpi.csv', encoding='utf-8-sig', engine='python')
df2.head()


# In[4]:


#merge the dataframes 
frames = [df1, df2]
df3= pd.merge(df1, df2, how="left", on=["player_id", "game"])
df3.head()


# In[5]:


#select 'My Lovely Horse' game data
df4=df3.loc[df3['game'] == 'My Lovely Horse']
df4.sample(5)


# In[6]:


#check data type and size
df4.info()


# In[7]:


#check numerical fields
df4.describe()


# In[8]:


#check categorical fields
df4_categorical=df4.select_dtypes(include=['object']).copy()
print(df4_categorical.describe())


# In[9]:


#create cohorts based on install_date 
grouped = df4.groupby(['install_date','event_date'])
cohorts = grouped.agg({'player_id': pd.Series.nunique})
cohorts.rename(columns={'player_id': 'TotalUsers'}, inplace=True)
cohorts.head()


# In[10]:


#Create a `CohortPeriod` column, which is the Nth period based on the user's login date.
def cohort_period(df4):
    df4['CohortPeriod'] = np.arange(len(df4)) 
    return df4

cohorts = cohorts.groupby(level=0).apply(cohort_period)
cohorts.head()


# In[11]:


# reindex the DataFrame
cohorts.reset_index(inplace=True)
cohorts.set_index(['install_date', 'CohortPeriod'], inplace=True)

# create a Series holding the total size of each CohortGroup
cohort_group_size = cohorts['TotalUsers'].groupby(level=0).first()
cohort_group_size.head()


# In[12]:


cohorts['TotalUsers'].head()


# In[13]:


cohorts['TotalUsers'].unstack(1).head()


# In[14]:


#create user retention rates
user_retention = cohorts['TotalUsers'].unstack(1).divide(cohort_group_size, axis=0)
user_retention.head()


# In[15]:


user_retention.to_excel (r'C:\Users\Snow\Desktop\sa_data_test\MyLovelyHorse.xlsx', index = True, header=True)


# In[16]:


#show the retention rates
import seaborn as sns
colormap=sns.light_palette("#ff796c",as_cmap=True, reverse=False)

plt.figure(figsize=(72,48))
plt.title('Cohorts: User Retention')
sns.heatmap(user_retention.T, mask=user_retention.T.isnull(), annot=True, fmt='.0%',cmap=colormap);

