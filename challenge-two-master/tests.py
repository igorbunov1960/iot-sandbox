''' Importing the unittest module for doing unit tests on flask app. '''
import unittest #imports the unittest module
from classes import BucketListItems #imports the BucketList class from the file bucket_list.py

#creating an instance of BucketListItems class for setting up unit tests.
bucket_items = BucketListItems() 

''' Class for the unit tests. Using two bucketlist called games and fruits '''
class BucketListTestCase(unittest.TestCase):
    '''Unit testing for testing the functionality for creating, reading, updating
    and deleting users' bucketlists and bucketlists' items'''
    def test_if_instance_of_class(self):
        '''Checks whether the bucket_items object is an instance of BucketListItems class.'''
        self.assertIsInstance(bucket_items, BucketListItems, msg='Bucket list should \
        be an instance of BucketList.')

    def tests_adding_bucketlist(self): 
        '''asserts that the number of bucketlists increases by one after addition of a bucketlist.'''
        a = len(bucket_items.all_items) #number of bucketlists before adding
        bucket_items.add_bucketlist_item("games", "football") #adds a games bucketlist with one item, football.
        b = len(bucket_items.all_items) #number of bucketlists after adding the games bucketlist.
        self.assertEqual(1, b-a , msg='New bucketlist, games, not added.')

    def tests_removing_bucketlist(self): 
        '''Checks whether the number of bucketlists reduces by one after deletion.'''
        a = len(bucket_items.all_items)
        bucket_items.remove_bucketlist_item("games", "football")
        b = len(bucket_items.all_items) #length after removing the games bucketlist
        self.assertEqual(1, a - b , msg='Bucketlist games not yet removed')
        
    def tests_editing_bucketlist(self): 
        '''Checks that the edited bucketlist changes its name. '''
        bucket_items.add_bucketlist_item('fruits', 'apple') 
        bucket_items.edit_bucketlist('fruits', 'food') #renames bucketlist from fruits to food.
        current_bucketlists = [obj.bucketlist_name for obj in bucket_items.all_items]
        self.assertNotIn("fruits", current_bucketlists, msg='Old bucket list name not removed')

    def tests_adding_bucketlist_item(self): 
        '''Asserts that an item added to a bucketlist gets added '''
        bucket_items.add_bucketlist_item('saturday', 'hiking') 
        bucket_items.add_bucketlist_item('saturday', 'boat racing') 
        current_items_in_bucketlist = [obj.bucketlist_item for obj in bucket_items.all_items if obj.bucketlist_name == "saturday"]
        self.assertIn("boat racing", current_items_in_bucketlist, msg='boat racing not added to saturday bucketlist')

    def tests_editing_bucketlist_item(self): 
        '''Asserts that an edited bucketlist item changes its name.'''
        bucket_items.edit_bucketlist_item('saturday', 'hiking', 'partying') #rename hiking to partying
        current_items_in_bucketlist = [obj.bucketlist_item for obj in bucket_items.all_items if obj.bucketlist_name == "saturday"]
        self.assertNotIn("hiking", current_items_in_bucketlist, msg='Item hiking not renamed')
        
    def test_removing_bucketlist_item(self):
        '''Asserts that the number of bucketlist items reduces by one when an item is removed'''
        bucket_items.add_bucketlist_item('classwork', 'calculus assignment') #adds calculus assignment 
        bucket_items.add_bucketlist_item('classwork', 'lab report') #adds lab report
        current_items_in_bucketlist = [obj.bucketlist_item for obj in bucket_items.all_items if obj.bucketlist_name == "classwork"]
        a = len(current_items_in_bucketlist)
        bucket_items.remove_bucketlist_item('classwork', 'lab report') #removes the lab report from classwork
        current_items_in_bucketlist = [obj.bucketlist_item for obj in bucket_items.all_items if obj.bucketlist_name == "classwork"]
        b = len(current_items_in_bucketlist)
        self.assertEqual(1, a - b, msg= "Number of bucketlist items has not reduced")

#Running these tests
if __name__ == '__main__':
    unittest.main()
