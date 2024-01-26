import requests
import json

endpoint_url = "https://hub.snapshot.org/graphql"

gqlVotes = """
query Votes {
  votes(first: 1000,
    skip: 0,
    where: {
      proposal_in: ["0xc2d7ebf5ef78084b26544905fd6febf0b8256293ce7f67a71fdcdefc5e6284a4"]
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

all_results = {"votes": [], "proposal": {}}
###################################################################
# get proposal
###################################################################






###################################################################
# get votes
###################################################################
created_value = 1


while True:
    # Format the GraphQL query with the current created value
    graphql_query = graphql_query_template % created_value

    # Send GraphQL query to the endpoint
    response = requests.post(endpoint_url, json={"query": graphql_query})

    if response.status_code == 200:
        result_data = response.json()

        if not result_data.get("data", {}).get("votes"):
            print("No more results. Exiting.")
            break

        last_created_value = result_data["data"]["votes"][-1]["created"]

        all_results["votes"].extend(result_data["data"]["votes"])

        print(f"GraphQL query successful. Result added.")

        created_value = last_created_value
    else:
        print(f"GraphQL query failed with status code: {response.status_code}")
        print(response.text)
        break

# Save the aggregated result in aggregated_data.json
with open("tmp.json", "w") as json_file:
    json.dump(all_results, json_file, indent=2)

print("Aggregated results saved in file")
