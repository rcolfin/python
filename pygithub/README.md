Code to interact with the GitHub Rest API

See [GitHub REST API documentation](https://docs.github.com/en/rest/) for more details.

## CLI

```sh
python -m github create-jwt 1027349 ~/.ssh/interactionapp.2024-10-16.private-key.pem
```

```sh
python -m github get-access-token 1027349 ~/.ssh/interactionapp.2024-10-16.private-key.pem 56042046
```

```sh
python -m github get-app 1027349 ~/.ssh/interactionapp.2024-10-16.private-key.pem
```

```sh
python -m github get-app-installations 1027349 ~/.ssh/interactionapp.2024-10-16.private-key.pem
```

```sh
python -m github delete-workflow-runs $(whoami) python $(python -m github get-access-token 1027349 ~/.ssh/interactionapp.2024-10-16.private-key.pem 56042046)
```

```sh
python -m github list-workflow-runs $(whoami) python $(python -m github get-access-token 1027349 ~/.ssh/interactionapp.2024-10-16.private-key.pem 56042046)
```

## Python Example (deleting all job runs from the rcolfin/python repo)

```python
import json
from getpass import getuser
from pathlib import Path

import github

client_id = "1027349"
installation_id = "56042046"
signing_key = "~/.ssh/interactionapp.2024-10-16.private-key.pem"

owner = getuser()
provider = github.providers.Application(client_id, Path(signing_key).expanduser().read_bytes(), installation_id)
client = github.GitHub(provider)

workflows = client.workflows(owner, "mono")
for workflow in workflows:
    print(json.dumps(workflow, indent=True))  # noqa: T201
