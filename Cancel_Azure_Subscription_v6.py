
# Az login - login first


import azure.mgmt.subscription
import time
from azure.identity import DefaultAzureCredential
import requests
from azure.cli.core import get_default_cli
import subprocess

# **************************************** Stage 1 Create Azure Exempt Policy ****************************************

# *********** Step 1a Create input request for subscription id ***********
subscription_id = input(
    "What is the subscription id you would like to cancel? ")

# *********** Step 1b confirm if this is the correct subscription id ***********

# create a new CLI instance
cli = get_default_cli()
print("\n")

# run the az account show command with name and sub id
result = cli.invoke(["account", "show", "--subscription", subscription_id,
                    "--output", "json", "--query", "[name,id]", "--output", "table"])
print("\n")
response = input("Is this the correct subscription name? y / n : ")

# If statement to verify the correct subscription
if response.lower() == "y":
    print("\n")
    print("\033[38;2;0;255;0mThank you!!\033[0m")  # Change color to Neon Green
    print("\n")
else:
    print("\033[31mTry again\033[0m")  # Change color to red
    exit()

# *********** Step 1c Create policy exemption ***********
cli = get_default_cli()
result = cli.invoke(
    ["policy", "exemption", "create", "--name", "Allow Owner for Azure Decom Test AZ CLI",
     "--display-name", "Allow Owner For Azure Decom Test AZ CLI",
     "--policy-assignment", "/providers/Microsoft.Management/managementGroups/a4454629-85ac-4c26-b6be-438709073c2a/providers/Microsoft.Authorization/policyAssignments/c34560e1adab441d96fe8cf7",
     "--exemption-category", "Waiver", "--scope", f"/subscriptions/{subscription_id}"]
)
print("\n")
print("\033[38;2;0;255;0mStage 1 creating exemptions policy is completed! \033[0m")


# **************************************** Stage 2 Grant Owner rights to user object id ****************************************

# *********** Step 2a Pull the user_object_id of current logged in user ***********
def get_current_logged_in_id():
    command = "az ad signed-in-user show --query id"
    output = subprocess.run(command, capture_output=True, shell=True).stdout
    # remove quotation mark from the output
    return output.decode("utf-8").replace('"', '')


user_object_id = get_current_logged_in_id()
#print(user_object_id)

# *********** Step 2b Grant current user object id an Owner Rights ***********
cli = get_default_cli()
result = cli.invoke(
    ["role", "assignment", "create", "--assignee-object-id", user_object_id,
     "--assignee-principal-type", "User", "--role", "owner", "--scope", f"/subscriptions/{subscription_id}"]
)
print("\n")
print(user_object_id)
print("\033[38;2;0;255;0mStage 2 granting owner rights is completed! \033[0m")
print("\n")
print("\n")


# **************************************** Stage 3 Cancel Subscription using REST API only****************************************

# *********** Step 3a Get current user credentials and access token ***********
def get_access_token():
    # Get the credentials
    credential = DefaultAzureCredential()

    # Get the access token
    access_token = credential.get_token('https://management.azure.com/')[0]
    return access_token


access_token = get_access_token()

# *********** Step 3b Set authorization header with access token ***********
headers = {"Authorization": f"Bearer {access_token}",
           "Content-Type": "application/json"}

# Build the URL for canceling subscription
url = f"https://management.azure.com/subscriptions/{subscription_id}/providers/Microsoft.Subscription/cancel?IgnoreResourceCheck=true&api-version=2019-03-01-preview"

# *********** Step 3c Send HTTP POST request to cancel subscription ***********
response = requests.post(url, headers=headers)

# Check the response status code
if response.status_code == 200:
    print("Subscription successfully canceled!")
    print("\033[38;2;0;255;0mStage 3 Canceling subscription is completed! \033[0m")
else:
    print(
        f"Failed to cancel subscription. Status code: {response.status_code}")
print("\n")


# **************************************** Stage 4 Verify Subscription Cancelation ****************************************

# *********** Stage 4a Get current user credentials ***********
credential = DefaultAzureCredential()
subscription_client = azure.mgmt.subscription.SubscriptionClient(
    credential=credential)

# *********** Stage 4b Check subcription.state status every 10 seconds ***********
# Insert a counter her to avoid infinie while loop
counter = 0
max_iterations = 30

while True:
    # Get subscription
    subscription = subscription_client.subscriptions.get(subscription_id)

    # Print display name and state of subscription
    # Change color to blue
    print("\n")
    print("\033[34mWaiting for confirmation... \033[0m Subscription has been canceled successfully!")
    print(f"Subscription display name: {subscription.display_name}")
    print(f"Subscription id: {subscription.id}")
    print("\n")

    # Check subscription state
    if subscription.state == "Warned":  # "W"arned should be capital
        # Change the text color to red
        print("\033[31mSubscription state: warned \033[0m")
        print('When Subscription state reads "warned", then it is canceled!')
        print("\033[38;2;0;255;0mStage 4 verification is completed! \033[0m")
        break
    else:
        print(f"Subscription state: {subscription.state}")
        # Necessary to refresh code here, so it catches quicker when subscription is canceled
        credential = DefaultAzureCredential()
        subscription_client = azure.mgmt.subscription.SubscriptionClient(
            credential=credential)

    print('When Subscription state reads "warned", then it is canceled!')
    print("\n")
    print("\n")
    counter += 1
    if counter >= max_iterations:
        print("\033[38;2;0;255;0mStage 4 verification timed out. Please cheack manually! \033[0m")
        print("\n")
        break


    start_time = time.time()  # Record the start time
    dot_spin = "*"
    for i in range(10):
        print(dot_spin, end=" ")
        time.sleep(1)  # Wait 1 second before printing the next star

print("\n")
print("\n")


# **************************************** Stage 5 Remove Owner Rights ****************************************


# *********** Step 5a Pull the user_object_id of the current logged in user ***********

def get_current_logged_in_id():
    command = "az ad signed-in-user show --query id"
    output = subprocess.run(command, capture_output=True, shell=True).stdout
    # remove quotation mark and trailing space from the output
    return output.decode("utf-8").replace('"', '').strip()


user_object_id = get_current_logged_in_id()
print(user_object_id)

# *********** Step 5b Remove owner rights from the user object id ***********
cli = get_default_cli()
result = cli.invoke(
    ["role", "assignment", "delete", "--assignee", user_object_id,
     "--role", "owner", "--scope", f"/subscriptions/{subscription_id}"]
)
print("\033[38;2;0;255;0mStage 5 removing owner rights is completed! \033[0m")
print("\n")
