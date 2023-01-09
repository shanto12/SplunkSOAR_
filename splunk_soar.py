import requests
import json


class SplunkSOAR:
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.username = username
        self.password = password

    def _make_request(self, endpoint, method, data=None):
        url = f"{self.base_url}/{endpoint}"
        auth = (self.username, self.password)
        headers = {'Content-Type': 'application/json'}
        if method == 'GET':
            response = requests.get(url, auth=auth, headers=headers)
        elif method == 'POST':
            response = requests.post(url, auth=auth, headers=headers, json=data)
        elif method == 'PUT':
            response = requests.put(url, auth=auth, headers=headers, json=data)
        elif method == 'DELETE':
            response = requests.delete(url, auth=auth, headers=headers)
        else:
            raise ValueError("Invalid HTTP method")
        return response.json()

    def create_playbook(self, name, playbook):
        endpoint = f"playbooks/{name}"
        data = {"playbook": playbook}
        return self._make_request(endpoint, 'POST', data)

    def get_playbook(self, name):
        endpoint = f"playbooks/{name}"
        return self._make_request(endpoint, 'GET')

    def update_playbook(self, name, playbook):
        endpoint = f"playbooks/{name}"
        data = {"playbook": playbook}
        return self._make_request(endpoint, 'PUT', data)

    def delete_playbook(self, name):
        endpoint = f"playbooks/{name}"
        return self._make_request(endpoint, 'DELETE')

    def create_action(self, name, action):
        endpoint = f"actions/{name}"
        data = {"action": action}
        return self._make_request(endpoint, 'POST', data)

    def get_action(self, name):
        endpoint = f"actions/{name}"
        return self._make_request(endpoint, 'GET')

    def update_action(self, name, action):
        endpoint = f"actions/{name}"
        data = {"action": action}
        return self._make_request(endpoint, 'PUT', data)

    def delete_action(self, name):
        endpoint = f"actions/{name}"
        return self._make_request(endpoint, 'DELETE')
