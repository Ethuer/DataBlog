from datetime import datetime, timedelta
import random
import numpy as np
import pandas as pd

from datetime import datetime, timedelta
import random

from datetime import datetime, timedelta
import random

from datetime import datetime, timedelta
import random

class UserGenerator :
    """
    simulate user interactions
    
    
    
    initializes to set column names and prefix for user_ids 
    
    generate_purchase creates a pandas dataframe containing: 
    user_id :str, 
    whether purchased (0 or 1):int 
    and at what time purchase was completed ( in minutes)
    
    """
    def __init__(self, column_label='purchased', user_prefix='uid_',uid_offset=random.randint(0,10000)):
        """
        uid_offset + range(user_id) to generate more realistic user_ids
        
        """
        self.column_label = column_label
        self.user_prefix = user_prefix
        self.uid_offset = uid_offset
    
    def _generate_userlist(self,nr_of_users):
        """ return list of users """
        return [self.user_prefix + str(self.uid_offset +n) for n in range(nr_of_users)]
    
    def _generate_purchases(self, nr_of_users, positive_ratio):
        """ using numpys binomial distribution random sampling """
        return np.random.binomial(n=1, p=positive_ratio, size=nr_of_users)
    
    def _generate_timestamp(self, nr_of_users, nr_of_days):
        """
        generate timestamps for user purchases ranging certain days
        """
        return [self.create_timestamp(nr_of_days) for n in range(nr_of_users)]
        
    def generate_purchase_df(self, nr_of_users,  positive_ratio, nr_of_days):
        """
        Generate datetime events and 
        """
        users = self._generate_userlist(nr_of_users)
        purchase = self._generate_purchases(nr_of_users, positive_ratio)
        user_times = self._generate_timestamp( nr_of_users, nr_of_days)   
        
        df = pd.DataFrame()
        df['user_id'] = users
        df[self.column_label] = purchase
        df['datetime'] = user_times
        
        return df.set_index('user_id')
    
    def generate_ab_split_df(self, nr_of_users,  positive_ratio_A, positive_ratio_B, nr_of_days, AB_user_ratio=0.5):
        """
        additional label for group
        """
        users = self._generate_userlist(nr_of_users)
        user_times = self._generate_timestamp( nr_of_users, nr_of_days)   
        purchase_A = self._generate_purchases( int(nr_of_users * AB_user_ratio), positive_ratio_A)
        purchase_B = self._generate_purchases( len(users) - len(purchase_A), positive_ratio_B)
        
        df = pd.DataFrame()
        df['user_id'] = users
        
        
        df[self.column_label] = list(purchase_A) + list(purchase_B)
            
        df['datetime'] = user_times
        
        df['group'] = 'B'
        # change the amount of A group users to label A
        df.loc[df.index.to_series() < len(purchase_A) , 'group' ] = 'A'
        
        return df
    
    def generate_lift_data(self, nr_of_users, initial_rate, lift, nr_of_days , user_ratio=0.5 , distribution='binom' ):
        """
        create an increase lift after a certain amount of time
        """
        users = self._generate_userlist(nr_of_users)
        user_times = self._generate_timestamp( nr_of_users, nr_of_days)   
        
        if distribution=='binom':
            prelift = self._generate_purchases( int(nr_of_users * user_ratio), initial_rate)
            postlift = self._generate_purchases( len(users) - len(prelift), initial_rate + lift )
        
        else:
            # failure
            print("unsupported distribution,  choose binomial ")
        
        df = pd.DataFrame()
        df['user_id'] = users
        df['datetime'] = user_times
        
        df.sort_values('datetime', inplace=True)
        
        df[self.column_label] = list(prelift) + list(postlift)
        
        return df
        
        
    def create_timestamp(self, nr_of_days ):
        
        base = datetime.strptime('2020-01-01','%Y-%m-%d')
        #date_list = [base + datetime.timedelta(hours=x) for x in range(nr_of_days)]
        x = random.randint(0,(nr_of_days*24*60*60))
        return base + timedelta(seconds=x)
        
        
