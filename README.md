# nazgul
One bot to rule them all, one bot to find them, One bot to bring them all and in the darkness bind them.

![Example](https://raw.githubusercontent.com/avara1986/nazgul/master/docs/exmaple_chat.png)

# ENVS:

    export BOT_NAME=nazgul
    export GOOGLE_APPLICATION_CREDENTIALS=[Path_to_your_google_credentials]

# Gcloud commands
    
    gcloud functions deploy nazgul --env-vars-file .env.yaml --runtime python37 --trigger-http --entry-point nazgul_bot --region europe-west1


# Create Datastore indexes:

    gcloud datastore indexes create index.yaml

# Permissions on Gcloud:
- Cloud Functions
- Data Store
- Services Accounts