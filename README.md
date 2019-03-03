# nazgul
One bot to rule them all, one bot to find them, One bot to bring them all and in the darkness bind them.



# ENVS:

    export BOT_NAME=nazgul
    export GOOGLE_APPLICATION_CREDENTIALS=[Path_to_your_google_credentials]

# Gcloud commands
    
    gcloud functions deploy nazgul --env-vars-file .env_prod.yaml --runtime python37 --trigger-http --entry-point nazgul_bot --region europe-west1


# Create Datastore indexes:

    gcloud datastore indexes create index.yaml

# Permissions on Gcloud:
- Cloud Functions
- Data Store
- Services Accounts


# Google Chat

![Example](https://raw.githubusercontent.com/avara1986/nazgul/master/docs/exmaple_chat.png)

# Google Actions:

https://console.actions.google.com/u/0/

https://console.dialogflow.com/

https://console.actions.google.com/u/0/project/[YOUR_PROJECT_ID]/simulator/