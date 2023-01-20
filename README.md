# Cancel_Azure_Subscription

The code will cancel Azure subscription without deleting any of the resources. The code is written in vscode using Python Azure CLI, SDK, and REST API. Therefore, Azure CLI is a dependency. In our environment, we have a policy in place to prevent users having an owner rights. Therefore, we will need to create an exemption policy to grant admins owner rights on subscription. This allows admins to cancel it. 
The code has five stages. 
## 1-Creating Exemption policy
	Requires login to Azure
	Prompts for Subscription id
	Prompts for verification of subscription id
## 2-Granting the user owner rights to subscription
	Uses current logged in user object id
## 3-Canceling subscription
	Cancel subscription using REST API. Only method Microsoft provides
## 4-Confirming cancelation
	Checks status every 10 seconds for confirmation
## 5-Remove owner rights from user

The code will require login to Azure before execution. It will prompt for subscription id; it will grant owner rights to current logged in user object id. 

Code is created in Vscode, therefore, it requires multiple Azure extensions. Also, Azure CLI and multiple modules like, time, requests, subprocess, azure.identity and azure.mgmt.subscription are required.
Code was written on Windows Desktop. 
Make sure you login to Azure prior to running code. Have subscription id handy when prompted.
After each stages execute successfully, you will see a text in neon green " Stage 1, Stage 2, etc... is completed."
Done