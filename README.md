## cpgqls-client-python

`cpgqls-client-python` is a simple Python library for communicating with an instance of
a Code Property Graph server.

### Requirements

Python 3.7+

### Installation

```
pip install cpgqls-client
```

### Example usage

A prerequisite for the following example is access to a running instance of a
Code Property Graph server. An easy way to set one up is by using the open
source code analyzer [joern](https://joern.io):

```bash
$ ./joern --server
```

```python
from cpgqls_client import CPGQLSClient, import_code_query, workspace_query

server_endpoint = "localhost:8080"
basic_auth_credentials = ("username", "password")
client = CPGQLSClient(server_endpoint, auth_credentials=basic_auth_credentials)

# execute a simple CPGQuery
query = "val a = 1"
result = client.execute(query)
print(result)

# execute a `workspace` CPGQuery
query = workspace_query()
result = client.execute(query)
print(result['stdout'])

# execute an `importCode` CPGQuery
query = import_code_query("/home/user/code/x42/c", "my-c-project")
result = client.execute(query)
print(result['stdout'])

query = import_code_query("/home/user/code/x42/java/X42.jar", "my-java-project")
result = client.execute(query)
print(result['stdout'])

```

### Running the test suite

```bash
# set up the virtual environment
$ python -m venv .venv
$ . .venv/bin/activate

# install the dependencies
$ pip install -r requirements.txt
$ pip install -r requirements-tests.txt

# run the tests
$ python -m pytest
```

### References

* Code Property Graph specification and tools
  https://github.com/ShiftLeftSecurity/codepropertygraph/
* The open source code analyzer joern: https://joern.io

