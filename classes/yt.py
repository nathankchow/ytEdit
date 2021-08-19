import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

class Yt:
    def __init__(self):
        scopes = ["https://www.googleapis.com/auth/youtube"]
        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "credentials.json"
        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_console()
        self.youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)


    def playlist_id_to_list(self, id='UUnQroFHMEwjpFrz3z7Kettw', write=False): #playlist for uploads
        '''
        #example
            
        request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id="UC_x5XG1OV2P6uZZ5FSM9Ttw"
        response = request.execute()
        print(response)
    )   '''
    
        request = self.youtube.playlistItems().list(
            part= 'snippet,id,contentDetails',
            maxResults=50,
            playlistId = id
        )
        response = request.execute()
        items = []
        items += response.get('items')
        while response.get('nextPageToken') != None: #get every item in playlist 
            request = self.youtube.playlistItems().list(
                part= 'snippet,id,contentDetails',
                maxResults=50,
                playlistId = id,
                pageToken = response.get('nextPageToken')
            )
            response = request.execute()
            items += response.get('items')
        
        results = [
            f"{video.get('snippet').get('title')},{video.get('snippet').get('resourceId').get('videoId')}" for video in items
            ]
        results_string = '\n'.join(results)
        print(results_string)
        if write:
            with open('data/video_catalog.csv',mode='a',encoding='utf-8') as f:
                f.write('\n' + results_string)
                f.close()
        return results
 
    #"UUnQroFHMEwjpFrz3z7Kettw" unknown playlist id.
        #titles = [video.get('snippet').get('title') for song in results.get('items')]
        #ids  = [video.get('snippet').get('resourceId').get('videoId') for song in results.get('items')] 

    def updateVideo(self,title, video_id, predefined=True):
        description = 'Copyrighted material of Bandai Namco Entertainment Inc., reproduced for educational purposes only.\nCustom MV player: https://nathankchow.github.io'
        request = self.youtube.videos().update(
            part="snippet,status", 
            body={
                "id": video_id,
                "snippet": {
                    "title": title,
                    "categoryId": 20,
                    "description": description
                },
                "status":{
                    "selfDeclaredMadeForKids": False,
                    "privacyStatus": "public",
                    "embeddable": "true"
                }
            }
        )
        response = request.execute()
        return response 
