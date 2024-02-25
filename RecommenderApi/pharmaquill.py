# %%
import pandas as pd
import numpy as np

med_data = pd.read_csv("RecommenderApi\medicine_dataset.csv")


# %% [markdown]
# Read the data

# %%
med_data.head(2)

# %%
fil_med_data = med_data.loc[:,['name']]

fil_med_data.head()

# %%
fil_med_data['substitutes'] = med_data[['substitute0', 'substitute1', 'substitute2', 'substitute3', 'substitute4']].values.tolist()
fil_med_data.head()

# %%
fil_med_data['uses'] = med_data[['use0',	'use1',	'use2',	'use3',	'use4']].values.tolist()

# %%
# prompt: get all the sideEffect from 1 to 41 in a list in a column sideEffect

fil_med_data['sideEffect'] = med_data[['sideEffect0',	'sideEffect1',	'sideEffect2',	'sideEffect3',	'sideEffect4',	'sideEffect5',	'sideEffect6',	'sideEffect7',	'sideEffect8',	'sideEffect9',	'sideEffect10',	'sideEffect11',	'sideEffect12',	'sideEffect13',	'sideEffect14',	'sideEffect15',	'sideEffect16',	'sideEffect17',	'sideEffect18',	'sideEffect19',	'sideEffect20',	'sideEffect21',	'sideEffect22',	'sideEffect23',	'sideEffect24',	'sideEffect25',	'sideEffect26',	'sideEffect27',	'sideEffect28',	'sideEffect29',	'sideEffect30',	'sideEffect31',	'sideEffect32',	'sideEffect33',	'sideEffect34',	'sideEffect35',	'sideEffect36',	'sideEffect37',	'sideEffect38',	'sideEffect39',	'sideEffect40',	'sideEffect41']].values.tolist()


# %%
fil_med_data.head(1)

# %%
# cleanedList = [x for x in fil_med_data['uses'][0] if str(x) != 'nan']
# print(cleanedList)

def remove_nan_from_column(df, column_name):
    df[column_name] = df[column_name].apply(lambda x: [item for item in x if str(item) != 'nan'])
    return df


fil_med_data = remove_nan_from_column(fil_med_data, 'uses')
fil_med_data = remove_nan_from_column(fil_med_data,'substitutes')
fil_med_data = remove_nan_from_column(fil_med_data,'sideEffect')
fil_med_data.head(40)

# %%
fil_med_data['chemicals_class'] = med_data['Chemical Class']
fil_med_data.head(5)

# %%
def find_substitute(medicine_name, medicine_uses):
    for row in fil_med_data.iterrows():
        if row[1]['name'] == medicine_name:
            for use in row[1]['uses']:
                if use in medicine_uses:
                    return row[1]['substitutes']
    return None

def find_uses(medicine_name):
    for row in fil_med_data.iterrows():
        if row[1]['name'] == medicine_name:
            return row[1]['uses']
    return None


find_substitute("azithral 500 tablet",'Treatment of Bacterial infections')


# %%
## TOMORROW'S TASK IS TO ADD COMPOSITIONS AND GET THERE WITH IMPLEMENTATION AND
# USE CHEMICAL CLASS TO DIFFERNETIATE BETWEEN MEDS

# %%


def find_medicine_name(medicine_uses, limit=10):
    medicine_list = []
    for row in fil_med_data.iterrows():
        for use in row[1]['uses']:
            if use in medicine_uses:
                medicine_list.append(row[1]['name'])
    return medicine_list[:limit]


def find_chemical_class(medicine_name):
    for row in fil_med_data.iterrows():
        if row[1]['name'] == medicine_name:
            return row[1]['chemicals_class']
    return None


def find_substitute(medicine_name, medicine_uses):
    for row in fil_med_data.iterrows():
        if row[1]['name'] == medicine_name:
            for use in row[1]['uses']:
                if use in medicine_uses:
                    return row[1]['substitutes']
    return None

def find_all_details(medicine_uses, limit=10):
    medicine_list = find_medicine_name(medicine_uses, limit)
    details_list = []
    for medicine_name in medicine_list:
        chemical_class = find_chemical_class(medicine_name)
        substitute = find_substitute(medicine_name, medicine_uses)
        details_list.append({
            'medicine_name': medicine_name,
            'chemical_class': chemical_class,
            'substitute': substitute,
        })
    return details_list


# %%
find_all_details("Treatment of Bacterial infections")

# %%

def find_substitute(medicine_name, limit=10):
    for row in fil_med_data.iterrows():
        if row[1]['name'] == medicine_name:
            return row[1]['substitutes'][:limit]
    return None

def find_side_effect(medicine_name):
    for row in fil_med_data.iterrows():
        if row[1]['name'] == medicine_name:
            return row[1]['sideEffect']
    return None


find_side_effect("Fightox 625 Tablet")


# %%
find_substitute('Trulimax 500mg Tablet')
find_substitute("azithral 500 tablet")

# %%
def find_substitute_details(medicine_name, limit=10):
    for row in fil_med_data.iterrows():
        if row[1]['name'] == medicine_name:
            original_chemical_class = row[1]['chemicals_class']
            substitutes = row[1]['substitutes'][:limit]

            if not substitutes:
                return original_chemical_class, None, None

            substitute_details = []
            for substitute in substitutes:
                substitute_chemical_class = find_chemical_class(substitute)
                substitute_details.append({
                    'substitute_name': substitute,
                    'substitute_chemical_class': substitute_chemical_class
                })

            return original_chemical_class, substitutes, substitute_details

    return None, None, None

# # Example usage:
# medicine_name = "Trulimax 500mg Tablet"
# original_chemical_class, substitutes, substitute_details = find_substitute_details(medicine_name)

# print(f"Chemical Class for {medicine_name}: {original_chemical_class}")
# print(f"Substitutes for {medicine_name}: {substitutes}")
# if substitutes:
#     print("Substitute Details:")
#     for substitute_detail in substitute_details:
#         print(substitute_detail)
# else:
#     print("No substitutes available.")

# pass


# %%



