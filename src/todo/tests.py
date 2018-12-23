from django.core.urlresolvers import reverse
from django.test import TestCase


# Create your tests here.
from rest_framework import status
from rest_framework.test import APITestCase

from todo.models import TodoItem


def createItem(client):
    url = reverse('todoitem-list')
    data = {'title': 'Walk the dog'}
    return client.post(url, data, format='json')

class TestCreateTodoItem(APITestCase):
    """
    Ensure we can create a new todo item
    """
    def setUp(self):
        response = createItem(self.client)
        self.assertEqual(TodoItem.objects.count(), 1)
        self.response = response

    def test_received_201_created_status_code(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_received_location_header_hyperlink(self):
        self.assertRegexpMatches(self.response['Location'], '^http://.+/todos/[\d]+$')

    def test_item_was_created(self):
        self.assertEqual(TodoItem.objects.count(), 1)

    def test_item_has_correct_title(self):
        self.assertEqual(TodoItem.objects.get().title, 'Walk the dog')

class TestUpdateTodoItem(APITestCase):
    """
    Ensure we can update an existing todo item using PUT
    """
    def setUp(self):
        response = createItem(self.client)
        self.assertEqual(TodoItem.objects.get().completed, False)
        url = response['Location']
        data = {'title': 'Walk the dog', 'completed': True}
        self.response = self.client.put(url, data, format='json')

    def test_received_200_status_code(self):
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_item_was_updated(self):
        self.assertEqual(TodoItem.objects.count(), 1)

    def test_item_was_updated(self):
        self.assertEqual(TodoItem.objects.get().completed, True)

class TestPatchTodoItem(APITestCase):
    """
    Ensure we can update an existing todo item using PUT
    """
    def setUp(self):
        response = createItem(self.client)
        self.assertEqual(TodoItem.objects.get().completed, False)
        url = response['Location']
        data = {'title': 'Walk the dog', 'completed': True}
        self.response = self.client.patch(url, data, format='json')

    def test_received_200_status_code(self):
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_item_was_updated(self):
        self.assertEqual(TodoItem.objects.count(), 1)

    def test_item_was_updated(self):
        self.assertEqual(TodoItem.objects.get().completed, True)

class TestDeleteTodoItem(APITestCase):
    """
    Ensure we can delete a single todo item
    """
    def setUp(self):
        response = createItem(self.client)
        self.assertEqual(TodoItem.objects.count(), 1)
        url = response['Location']
        self.response = self.client.delete(url)

    def test_received_204_no_content_status_code(self):
        self.assertEqual(self.response.status_code, status.HTTP_204_NO_CONTENT)

    def test_item_was_deleted(self):
        self.assertEqual(TodoItem.objects.count(), 0)


class TestDeleteAllTodoItems(APITestCase):
    """
    Ensure we can delete all todo items
    """
    def setUp(self):
        createItem(self.client)
        createItem(self.client)
        self.assertEqual(TodoItem.objects.count(), 2)
        self.response = self.client.delete(reverse('todoitem-list'))

    def test_received_204_no_content_status_code(self):
        self.assertEqual(self.response.status_code, status.HTTP_204_NO_CONTENT)

    def test_item_was_deleted(self):
        self.assertEqual(TodoItem.objects.count(), 0)

