import requests
import json
import argparse

url = "https://api.angelstudios.com/graphql"

parser = argparse.ArgumentParser(description="Execute a GraphQL query from a file.")
parser.add_argument("file", help="Path to the .gql file containing the GraphQL query")
args = parser.parse_args()

with open(args.file) as f:
    query = f.read()
variables = {"slug": "tuttle-twins",
             "contentStates": ["EARLY_ACCESS"]}
response = requests.post(url, json={"query": query, "variables": variables})
print(json.dumps(response.json(), indent=2))



