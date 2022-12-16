import os
import google_auth_oauthlib.flow #pip install google-auth-oauthlib
import googleapiclient.discovery #pip install google-api-python-client
import googleapiclient.errors
from time import sleep

#initialize permissions
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]


def main():
    #setup
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "views_secret.json"

    youtube = []
    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube.append(googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials))

    curr_api = 0
    
    while(True): 

        # Request (This is what asks Youtube API for the video data)
        try:
            request = youtube[curr_api].videos().list(
                part="snippet,statistics",
                id="TN-cHGmZzcA"
            )
            response = request.execute()

            data = response["items"][0]
            vid_snippet = data["snippet"]

            title = vid_snippet["title"]
            views = str(data["statistics"]["viewCount"])
            
            print("")
            print("Title of Video: " + title)
            print("Number of Views: " + views)

            change = (views not in title)

            if(change):
                title_upd = "This Video Has " + format(int(views), ",d") + " Views"
                vid_snippet["title"] = title_upd

                request = youtube[curr_api].videos().update(
                    part="snippet",
                    body={
                        "id": "TN-cHGmZzcA",
                        "snippet": vid_snippet
                    }
                )
                response = request.execute()
                
                print("Worked!")
                sleep(475)
            
        except Exception as e: 
            print(e)
            print("Error, trying again")
        sleep(44)
        
        
if __name__ == "__main__":
    main()