import pandas as pd
import numpy as np
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Lasso, LogisticRegression
from sklearn.feature_selection import SelectFromModel
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import Lasso



dataset=pd.read_csv(os.getcwd() +'UPLOADS/train.csv')




categorical_features=[feature for feature in dataset.columns if dataset[feature].dtypes=='O']
numerical_features = [feature for feature in dataset.columns if dataset[feature].dtypes != 'O']
year_feature = [feature for feature in numerical_features if 'Yr' in feature or 'Year' in feature]
discrete_feature=[feature for feature in numerical_features if len(dataset[feature].unique())<25 and feature not in year_feature+['Id']]
continuous_feature=[feature for feature in numerical_features if feature not in discrete_feature+year_feature+['Id']]
features_with_na=[features for features in dataset.columns if dataset[features].isnull().sum()>1]

##split the data into test data set and train data set
from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test=train_test_split(dataset,dataset['SalePrice'],test_size=0.1,random_state=0)
#splitted the data into 10% as test data and 90% as train data


## Replace missing value with a new label
def replace_cat_feature(dataset,features_nan):
    data=dataset.copy()
    data[features_nan]=data[features_nan].fillna('Missing')
    return data
features_nan=[feature for feature in dataset.columns if dataset[feature].isnull().sum()>1 and dataset[feature].dtypes=='O']
dataset=replace_cat_feature(dataset,features_nan)


#view all the categorical features having missing values
numerical_with_nan=[feature for feature in dataset.columns if dataset[feature].isnull().sum()>1 and dataset[feature].dtypes!='O']


## Replacing the numerical Missing Values
for feature in numerical_with_nan:
    ## We will replace by using median since there are outliers
    median_value=dataset[feature].median()
    
    ## create a new feature to capture nan values
    dataset[feature+'NaN']=np.where(dataset[feature].isnull(),1,0) 
    dataset[feature].fillna(median_value,inplace=True)

## Temporal Variables (Date Time Variables)
## It is more important to learn how many year since the House was sold, so we convert from year stamp to mention how many year 
## by simply subtracting these dated with YearSold

for feature in ['YearBuilt','YearRemodAdd','GarageYrBlt']:      
    dataset[feature]=dataset['YrSold']-dataset[feature]

num_features=['LotFrontage', 'LotArea', '1stFlrSF', 'GrLivArea', 'SalePrice']

for feature in num_features:
    dataset[feature]=np.log(dataset[feature])


##remove categorical variables that are present less than 1% of the observations
for feature in categorical_features:
    temp=dataset.groupby(feature)['SalePrice'].count()/len(dataset)
    temp_df=temp[temp>0.01].index
    dataset[feature]=np.where(dataset[feature].isin(temp_df),dataset[feature],'Rare_var')

for feature in categorical_features:
    labels_ordered=dataset.groupby([feature])['SalePrice'].mean().sort_values().index
    labels_ordered={k:i for i,k in enumerate(labels_ordered,0)}
    dataset[feature]=dataset[feature].map(labels_ordered)


##Feature Scaling

scaling_feature=[feature for feature in dataset.columns if feature not in ['Id','SalePerice'] ]
feature_scale=[feature for feature in dataset.columns if feature not in ['Id','SalePrice']]


scaler=MinMaxScaler()
scaler.fit(dataset[feature_scale])

scaler.transform(dataset[feature_scale])

# transform the train and test dataset into normalised form, and add on the Id and SalePrice variables
data = pd.concat([dataset[['Id', 'SalePrice']].reset_index(drop=True),
                    pd.DataFrame(scaler.transform(dataset[feature_scale]), columns=feature_scale)],
                    axis=1)

data.to_csv(os.getcwd() + 'UPLOADS/X_train.csv',index=False)

# to visualise al the columns in the dataframe
pd.pandas.set_option('display.max_columns', None)


transformed_dataset=data
transformed_dataset.head()

## Capture the dependent feature in y_train dataset
y_train=transformed_dataset[['SalePrice']]


## drop dependent feature from X_train dataset
X_train=transformed_dataset.drop(['SalePrice'],axis=1)


## for feature slection
# to visualise al the columns in the dataframe
pd.pandas.set_option('display.max_columns', None)
dataset=pd.read_csv('X_train.csv')


feature_sel_model = SelectFromModel(Lasso(alpha=0.005, random_state=0)) # remember the random state in this function  to be used in the other file
feature_sel_model.fit(X_train, y_train)

feature_sel_model.get_support()

# make a list of the selected features
selected_feat = X_train.columns[(feature_sel_model.get_support())]
X_train=X_train[selected_feat]
print('total number of selected features',X_train.shape)
X_train[selected_feat].to_csv(os.getcwd() +'/UPLOADS/selected.csv',index=False)


###Convert csv to json----------------------------------------------------------
import csv
import json
csvFilePath =os.getcwd() +'/UPLOADS/selected.csv'
jsonFilePath = os.getcwd() +'/UPLOADS/'
# Function to convert a CSV to JSON
# Takes the file paths as arguments
def make_json(csvFilePath, jsonFilePath):
	
	# create a dictionary
	data = {}
	
	# Open a csv reader called DictReader
	with open(csvFilePath, encoding='utf-8') as csvf:
		csvReader = csv.DictReader(csvf)
		
		# Convert each row into a dictionary
		# and add it to data
		for rows in csvReader:
			
			# Assuming a column named 'Id' to
			# be the primary key
			key = rows['Id']
			data[key] = rows

	# Open a json writer, and use the json.dumps()
	# function to dump data
	with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
		jsonf.write(json.dumps(data, indent=4))
		
# Driver Code

# Decide the two file paths according to your
# computer system
csvFilePath = os.getcwd() +'/UPLOADS/X_train.csv'
jsonFilePath = os.getcwd() +'/UPLOADS/JsonObject.json'

# Call the make_json function
make_json(csvFilePath, jsonFilePath)