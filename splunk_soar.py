import requests
import json


class SplunkSOAR:
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.username = username
        self.password = password

    def _make_request(self, endpoint, method, data=None, include_expensive=False, page_size=None, **params):
        url = f"{self.base_url}/{endpoint}"
        auth = (self.username, self.password)
        headers = {'Content-Type': 'application/json'}

        if include_expensive:
            url += f"?include_expensive"

        if page_size is 0 or page_size:
            params["page_size"] = page_size

        if method in ('GET', 'POST', 'PUT', 'DELETE'):
            r = requests.request(method, url, auth=auth, headers=headers, json=data, verify=False, params=params)

            return r.json()
        else:
            raise ValueError("Invalid HTTP method")

    def add_double_quotes(self, text):
        return f'"{text}"'

    def get_all_playbooks(self):
        endpoint = "playbook"
        return self._make_request(endpoint, 'GET', page_size=0)

    def get_playbook(self, name, params=dict()):
        endpoint = "playbook"
        params["_filter_name"] = self.add_double_quotes(name)
        return self._make_request(endpoint, 'GET', **params)

    def run_playbook(self, name, container_id, playbook_id=None, scope="all", data=dict()):
        if not playbook_id:
            playbook_id = self.get_playbook(name=name).get('data')[0].get('id')

        endpoint = "playbook_run"
        data["playbook_id"] = playbook_id
        data["container_id"] = container_id
        data["scope"] = scope
        data["run"] = True
        return self._make_request(endpoint, 'POST', data=data)

    def get_container(self, container_id, params=dict()):
        endpoint = f"container/{container_id}"
        return self._make_request(endpoint, 'GET', include_expensive=True, params=params)

    def get_container_artifacts(self, container_id, params=dict()):
        endpoint = f"artifact"
        params["_filter_container"] = container_id
        return self._make_request(endpoint, 'GET', **params)

    def get_container_attachments(self, container_id, params=dict()):
        endpoint = f"container_attachment"
        params["_filter_container_id"] = container_id
        return self._make_request(endpoint, 'GET', **params)

    def delete_artifact(self, artifact_id):
        endpoint = f"artifact/{artifact_id}"
        print(f"Removing artifact: {artifact_id}")
        return self._make_request(endpoint, 'DELETE')

    def delete_artifacts(self, container_id, except_artifact_ids=[], above_artifact=""):
        if except_artifact_ids or above_artifact:
            artifact_ids = [artifact.get('id') for artifact in
                            self.get_container_artifacts(container_id=container_id).get('data')]
            if except_artifact_ids:
                artifacts_to_remove = [a for a in artifact_ids if a not in except_artifact_ids]
            else:
                artifacts_to_remove = [a for a in artifact_ids if a > above_artifact]
            if not artifacts_to_remove:
                print(f"No artifacts to remove")
            else:
                for artifact_id in artifacts_to_remove:
                    self.delete_artifact(artifact_id)
        else:
            print(f"Must provide except_artifact_ids or above_artifact")

    def get_all_notes(self, container_id, params=dict()):
        endpoint = f"note"
        params["_filter_container_id"] = container_id
        return self._make_request(endpoint, 'GET', **params)

    def delete_note(self, note_id):
        endpoint = f"note/{note_id}"
        print(f"Removing note: {note_id}")
        return self._make_request(endpoint, 'DELETE')

    def delete_all_notes(self, container_id):

        note_ids = [note.get('id') for note in
                    self.get_all_notes(container_id=container_id).get('data')]

        if not note_ids:
            print(f"No notes to remove")
        else:
            for note_id in note_ids:
                self.delete_note(note_id)

    def get_all_pins(self, container_id, params=dict()):
        endpoint = f"container_pin"
        params["_filter_container_id"] = container_id
        return self._make_request(endpoint, 'GET', **params)

    def delete_pin(self, pin_id):
        endpoint = f"container_pin/{pin_id}"
        print(f"Removing pin: {pin_id}")
        return self._make_request(endpoint, 'DELETE')

    def delete_all_pins(self, container_id):

        pin_ids = [pin.get('id') for pin in
                   self.get_all_pins(container_id=container_id).get('data')]

        if not pin_ids:
            print(f"No pins to remove")
        else:
            for pin_id in pin_ids:
                self.delete_pin(pin_id)

    def clear_container(self, container_id, except_artifact_ids=None, above_artifact=None):
        self.delete_artifacts(except_artifact_ids=except_artifact_ids, above_artifact=above_artifact)
        self.delete_all_pins(container_id=container_id)
        self.delete_all_notes(container_id=container_id)
