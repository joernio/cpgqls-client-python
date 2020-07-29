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

