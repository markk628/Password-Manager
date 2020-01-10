from unittest import TestCase, main as unittest_main, mock
from flask import Flask
from app import app
from bson.objectid import ObjectId

sample_name_id = ObjectId('5d55cffc4a3d4031f42827a3')
sample_name = {
    'name': 'John Doe'
}
sample_form_data = {
    'name': sample_name['name']
}

class PMTests(TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    '''tests if home page renders'''
    def test_home(self):
        result = self.client.get('/')
        self.assertEqual(result.status, '200 OK')

    '''tests if generate password page renders'''
    def test_generate(self):
        result = self.client.get('/accounts/generate')
        self.assertEqual(result.status, '200 OK')

    '''tests if new person page renders'''
    def test_new(self):
        result = self.client.get('/new')
        self.assertEqual(result.status, '200 OK')
    
    '''uses mock data to see if individual person page renders'''
    @mock.patch('pymongo.collection.Collection.find_one')
    def test_person(self, mock_find):
        mock_find.return_value = sample_name
        result = self.client.get(f'/{sample_name_id}')
        self.assertEqual(result.status, '200 OK')

    '''uses mock data to see if edit person's name page renders'''
    @mock.patch('pymongo.collection.Collection.find_one')
    def test_edit_person(self, mock_find):
        mock_find.return_value = sample_name
        result = self.client.get(f'/{sample_name_id}/edit')
        self.assertEqual(result.status, '200 OK')
    
    '''uses mock data to see if new person has successfully been uploaded to database'''
    @mock.patch('pymongo.collection.Collection.insert_one')
    def test_submit_person(self, mock_insert):
        result = self.client.post('/', data=sample_form_data)
        self.assertEqual(result.status, '302 FOUND')
        mock_insert.assert_called_with(sample_name)

    '''uses mock data to see if a person has been deleted'''
    @mock.patch('pymongo.collection.Collection.delete_one')
    def test_delete_person(self, mock_delete):
        form_data = {'_method': 'DELETE'}
        result = self.client.post(f'/{sample_name_id}/delete', data=form_data)
        self.assertEqual(result.status, '302 FOUND')
        mock_delete.assert_called_with({'_id': sample_name_id})

if __name__ == '__main__':
    unittest_main()