'''Classes for manipulating users, bucket list and bucket list items. '''
class Users(object):
    ''' A class for manipulating user's passwords, names and emails '''
    all_users = [] #Empty list for holding users info
    def __init__(self, name=None, email=None, password=None):
        self.name = name
        self.email = email
        self.password = password

    def register_user(self, name, email, password):
        ''' register a user - sign up. Checks that all the users emails are unique'''
        if self.all_users:
            for user in self.all_users:
                if user.email != email:
                    user = Users(name, email, password)
                    self.all_users.append(user)
        user = Users(name, email, password)
        self.all_users.append(user)                
        
    def validate_login(self, email, password):
        '''Validate users login details - log in'''
        for user in self.all_users:
            if user.email == email and user.password == password:
                return 'login successful'
        return 'Invalid login details.'


class BucketListItems(object):
    '''A class to add, edit and remove bucket list items (CRUD)'''
    all_items = [] #holds items and bucketlists
    bucketlists = [] #Hold bucketlists

    def __init__(self, bucketlist_name=None, bucketlist_item=None):
        self.bucketlist_name = bucketlist_name
        self.bucketlist_item = bucketlist_item
            
    def add_bucketlist(self, bucketlist_name):
        '''Add a new bucketlist, taking care of whitespace characters and case '''
        bucketlist_name = bucketlist_name.strip() #removes leading and trailing whitespaces from the name
        if bucketlist_name and not bucketlist_name.isspace():
            lowercase_bucketlists = [item.lower() for item in self.bucketlists]
            if bucketlist_name.lower() not in lowercase_bucketlists:
                self.bucketlists.append(bucketlist_name)

    def delete_bucketlist(self, bucketlist_name):
        '''Removes bucket list and all its items '''
        bucketlist_name = bucketlist_name.strip()
        for item in self.all_items:
            if bucketlist_name and item.bucketlist_name == bucketlist_name:
                self.all_items.remove(item)  

        if bucketlist_name and not bucketlist_name.isspace():
            lowercase_bucketlists = [item.lower() for item in self.bucketlists]
            if bucketlist_name.lower() in lowercase_bucketlists:
                index = lowercase_bucketlists.index(bucketlist_name.lower())
                del self.bucketlists[index]

    def edit_bucketlist(self, bucketlist_name, new_name):
        '''Rename a bucket list '''
        bucketlist_name = bucketlist_name.strip()
        new_name = new_name.strip()
        for item in self.all_items:
            if bucketlist_name and item.bucketlist_name == bucketlist_name:
                item.bucketlist_name = new_name

        if bucketlist_name and not bucketlist_name.isspace():
            lowercase_bucketlists = [item.lower() for item in self.bucketlists]
            if bucketlist_name.lower() in lowercase_bucketlists:
                index = lowercase_bucketlists.index(bucketlist_name.lower())
                del self.bucketlists[index]
                self.bucketlists.insert(index, new_name)
                        
    def add_bucketlist_item(self, bucketlist_name, bucketlist_item=None):
        '''Creating a bucket list (when bucketlist_item has not been specified) and adding items into it '''
        bucketlist_item = bucketlist_item.strip()
        
        if bucketlist_item and not bucketlist_item.isspace():
            items = [bucket.bucketlist_item for bucket in self.all_items if bucket.bucketlist_name == bucketlist_name]
            if bucketlist_item.lower() not in [item.lower() for item in items]:
                item = BucketListItems(bucketlist_name, bucketlist_item)
                self.all_items.append(item)
        
    def remove_bucketlist_item(self, bucketlist_name, bucketlist_item):
        '''Removing Items from bucket list based on the item title 
        and bucket list in which it is in.'''
        bucketlist_item = bucketlist_item.strip()
        
        if bucketlist_item and not bucketlist_item.isspace():
            for item in self.all_items:
                if item.bucketlist_name.lower() == bucketlist_name.lower() and \
                item.bucketlist_item.lower() == bucketlist_item.lower():
                    self.all_items.remove(item)  

    def edit_bucketlist_item(self, bucketlist_name, bucketlist_item, new_name):
        '''Editing bucket list items '''
        bucketlist_item = bucketlist_item.strip()
        new_name = new_name.strip()
        
        if bucketlist_item and not bucketlist_item.isspace():
            for item in self.all_items:
                if item.bucketlist_name.lower() == bucketlist_name.lower() and \
                item.bucketlist_item.lower() == bucketlist_item.lower():
                    item.bucketlist_item = new_name
                
    def read_bucketlist(self, bucketlist_name):
        '''Prints the name of the bucket list and the items that are in the bucketlist'''
        for item in self.all_items:
            if item.bucketlist_name == bucketlist_name:
                print(item.bucketlist_name)
                print(item.bucketlist_item)
                            
    