#to bring the print funtion from Python 3 into Python 2.6
from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

#   Methods for driving the Google Drive API with (six functions)
#   1. create_folder(service,name_folder)
#   2. list_files(service,number_items)
#   3. query_files(service,mimeType)
#   4. send_file(service,filename,filepath,mimeType)
#   5. file_in_folder(service,file_name,id_folder,path_file)
#   6. main()

SCOPES = 'https://www.googleapis.com/auth/drive'

def create_folder(service,name_folder):
    file_metadata = {'name':name_folder,
                     'mimeType':'application/vnd.google-apps.folder'}
    file = service.files().create(body=file_metadata,
                        fields='id').execute()
	text = '{0} folder was created in Google Drive with id {1}'
    print(text.format(name_folder,file.get('id')))
    return file.get('id')

def list_files(service,number_items):
    #call the Drive v3 API
    results = service.files().list(
          pageSize = number_items,
          fields='nextPageToken, files(id,name)').execute()
    items = results.get('files', [])
    if not items:
        print('Not files found.')
    else:
        print('List of files: ')
        for item in items:
            print(u'{0} ({1})'.format(item['name'],item['id']))

def query_files(service,mimeType):
    i = 0
    flag = False
    id_folder = []
    page_token = None
    while True:
        response = service.files().list(q = mimeType,
                                   #spaces = 'drive',
                                   fields = 'nextPageToken,files(id,name)',
                                   pageToken = page_token).execute()
        items = response.get('files',[])
        if not items:
            flag = False
            id_folder.append(None)
            print("Files didn't find")
        else:
            flag = True
            print('Files found:')
            for item,folder in enumerate(items):
                print(' %s (%s)'%(folder.get('name'),folder.get('id')))
                id_folder.append(folder.get('id'))
        i = len(id_folder)-1
        page_token = response.get('nextPageToken',None)
        if page_token is None:
            break
    return flag,id_folder[i]

def send_file(service,filename,filepath,mimeType):
    file_metadata = {'name':filename}
    media = MediaFileUpload(filename=filepath,
                             mimetype=mimeType)
    file = service.files().create(
                             body = file_metadata,
                             media_body = media,
			     fields = 'id').execute()
    print('File id: {0}'.format(file.get('id')))

def file_in_folder(service,filename,id_folder,path_file):
    file_name = filename.split(path_file) #'/home/pi/outsider/')
    name = file_name[1]
    file_metadata = {'name':name,
                      'parents': [id_folder]}
    media = MediaFileUpload(filename,
                       mimetype=None,
                       resumable=True)
    file = service.files().create(body = file_metadata,
                      media_body = media,
                      fields = 'id').execute()
    #print ("Files id {0}".format(file.get('id'))

def main():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle','rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
               'credentials_desktop.json',SCOPES)
            creds = flow.run_local_server(port=8080)
        with open('token.pickle','wb') as token:
            pickle.dump(creds,token)
    return  build('drive', 'v3', credentials=creds)

path_file = '/home/pi/'
filename = path_file+'yo.jpg'
name_folder = 'quickstart_folder'
mime = "mimeType='application/vnd.google-apps.folder' and name = '{0}'"
mimeType= mime.format(name_folder)

if __name__ == '__main__':
    service =  main()
    flag, id_folder = query_files(service,mimeType)
    if flag:
        print('Folder exists')
    else:
        id_folder = create_folder(service,name_folder)
    file_in_folder(service,filename,id_folder,path_file)
