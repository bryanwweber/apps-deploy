# Deploy Apps on Talnet with Ansible

Generate secrets locally:

```bash
task generate-secrets
```

Deploy the app for updates:

```bash
uv run ansible-playbook playbook.yaml --tags hoarder
```
