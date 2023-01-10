from splunk_soar import SplunkSOAR

local_soar = SplunkSOAR(base_url="https://192.168.5.128/rest", username="admin", password="password")

# r = local_soar.get_playbook(name="activedirectory_reset_password")

# r=local_soar.run_playbook(name="test parent for testing cf", container_id=25)

# r=local_soar.get_container(container_id=25)

# r=local_soar.get_container_artifacts(container_id=25)
# r=local_soar.get_container_attachments(container_id=25)
# r=local_soar.delete_artifacts(container_id=25, above_artifact=163)
# r=local_soar.delete_all_notes(container_id=25)
r=local_soar.delete_all_pins(container_id=25)

print(r)
