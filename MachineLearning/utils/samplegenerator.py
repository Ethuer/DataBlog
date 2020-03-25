import pandas as pd
import numpy as np
import random
import string



class UserDataGenerator:
    
    def __init__(self,
                 colnames=['click_a','click_b','amount','purchased_stock','response_time','retrieved'],
                 column_types=['binom','binom','norm','categorical','chisquare','norm'], 
                 n_labels=6, 
                 nr_uninformative_columns=0.3,
                 preset_mean=200, 
                 preset_spread=20, 
                 n_categories = 5,
                 label_frequency=None):
        self.nr_uninformative_columns = nr_uninformative_columns
        self.colnames = colnames
        self.col_types = column_types
        self.n_labels = n_labels
        self.preset_mean = preset_mean
        self.preset_spread = preset_spread
        self.n_categories = n_categories
        self.label_list = list(string.ascii_lowercase)[:self.n_categories]    
        # create the labels
        
        self.label_dict,self.label_frequency = self._generate_label(n_labels, label_frequency)
        #print(label_frequency, self.label_frequency)
        
    def _params(self):
        return {'colnames':self.colnames, 
                'col_types':self.col_types,
                'preset_mean':self.preset_mean, 
                'preset_spread': self.preset_spread,
               'label_dict':self.label_dict,
               'label_freq':self.label_frequency,
               'number of labels':self.n_labels}
        
    def _generate_label(self,n_labels , label_freq=None):
        """
        Generate individual labels with sets of random variables
        
        Args:
        
        
        Rets:
        """

        label_list = self.label_list
        letters = list(string.ascii_lowercase)
    
        label_dict = {}
        
        for n in range(n_labels):
            
            is_uninformative = True
            
            label_dict[letters[n]] = []
            
            for counter , column in enumerate(self.col_types):
                
                if  counter >= self.nr_uninformative_columns:
                    is_uninformative = False
                
                if column == 'binom':
                    if is_uninformative:
                        col_mean = 0.5
                    else:
                        col_mean = random.random()
                        
                if column == 'norm':
                    if is_uninformative:
                        col_mean = 0.5
                    else:
                        col_mean = (self.preset_mean + 
                                (random.randint(0,self.preset_spread) - (self.preset_spread / 2)  ) )
                if column == 'categorical':
                # most common label
                    if is_uninformative:
                        col_mean = label_list[2]
                    else:
                        col_mean = random.choice(label_list)
                if column == 'chisquare':
                    if is_uninformative:
                        col_mean = 5
                    else:
                        col_mean = random.randint(0,self.preset_spread)

                label_dict[letters[n]].append(col_mean)
    
        if label_freq == None :
            label_frequency = [1/len(label_dict) for n in range(len(label_dict)) ]
        else:
            label_frequency = label_freq
        
        return label_dict, label_frequency
    
    def generate_user_df(self,n_users):
        users = pd.DataFrame()
        
        for n in range(n_users):
            user = self._generate_user(self.label_dict,self.label_frequency,self.col_types,self.colnames)
            
            users = users.append(pd.DataFrame.from_dict(user, orient='index').transpose() )
            
        return users
    
    def _generate_user(self,label_dict,label_frequency,columns, colnames):
        
        """
        Generate individual users from label distribution
        
        Args:
        
        
        Rets:
        """
    
        # choose label 
        label = np.random.choice(list(label_dict.keys()),1,p=label_frequency)[0]
    
        user_dict = {'label':label}
    
        for idx, column in enumerate(columns):
            if column == 'binom':
                value = np.random.binomial(n=1,p=label_dict[label][idx])
            if column == 'norm':
                value = np.random.normal(loc=label_dict[label][idx], scale=self.preset_spread)
            if column == 'categorical':
                # most common label , assign 0.1 to all other labels, residue is the called label
                residue = 0.5
                default_prob = ( 1-residue ) / (self.n_categories - 1)
            
                probabs = [default_prob for n in range(self.n_categories )]
                probabs[self.label_list.index(label_dict[label][idx])] = residue

                value = np.random.choice(self.label_list,1,p= probabs)[0]
            
            
            if column == 'chisquare':
                value = np.random.chisquare(label_dict[label][idx])
        
            user_dict[colnames[idx]] = value
        
        return user_dict
