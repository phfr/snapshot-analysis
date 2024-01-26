import requests
import json
import sys

if len(sys.argv) != 2:
    print("Usage: python script.py <proposalId>")
    sys.exit(1)

proposalId = sys.argv[1]

endpoint_url = "https://hub.snapshot.org/graphql"

all_results = {"votes": [], "proposal": {}}


gqlVotes = """
query Votes {
  votes(first: 1000,
    skip: 0,
    where: {
      proposal_in: ["%s"]
      created_gt: %s
    }, orderBy: "created", orderDirection: asc) {
    voter
    created
    vp
    choice
  }
}
"""

gqlVotes = """
    query Votes {
      votes(first: 1000,
        skip: 0,
        where: {
          proposal_in: ["%s"]
          created_gt: %s
        }, orderBy: "created", orderDirection: asc) {
        voter
        created
        vp
        choice
      }
    }
"""

gqlProposal = """
    query Proposal {
      proposal(id:"%s") {
        id
        title
        created
        strategies {
          network
          params
        }
        plugins
        discussion
        type
        body
        choices
        start
        end
        quorum
        scores
        scores_state
        snapshot
        state
        author
        space {
          id
          name
        }
        votes
      }
    }
"""

def execute_query(query_template, key, *args):
    graphql_query = query_template % args
    response = requests.post(endpoint_url, json={"query": graphql_query})

    if response.status_code == 200:
        result_data = response.json()
        if not result_data.get("data", {}).get(key):
            print(f"No more {key} results. Exiting.")
            return None, None
        if (key == "votes"):
          return result_data["data"][key], result_data["data"][key][-1]["created"]
        else:
          return result_data["data"][key]
    else:
        print(f"GraphQL query failed with status code: {response.status_code}")
        print(response.text)
        return None

created_value = 1;


# Fetch votes data
while True:
    votes_data, last_created_value_votes = execute_query(gqlVotes, "votes", proposalId, created_value)
    if votes_data is None:
        break
    all_results["votes"].extend(votes_data)
    print(f"GraphQL query for votes successful. Results appended to all_results.")
    if last_created_value_votes is None:
      break;
    created_value = last_created_value_votes


proposal_data = execute_query(gqlProposal, "proposal", proposalId)

if proposal_data:
    all_results["proposal"] = proposal_data
    print("GraphQL query for proposal successful. Result added to all_results.")


data = json.dumps(all_results, indent=2)

output_filename = f"{proposalId}.json"
with open(output_filename, "w") as output_file:
    output_file.write(data)
    
print("saved to file ", output_filename)