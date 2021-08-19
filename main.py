'''
specify youtube playlist id and modify all metadata of videos inside 
'''

from classes.yt import Yt


yt = Yt()
while True:
    answer = input('enter playlist id\n')
    results = yt.playlist_id_to_list(id=answer,write=True)
    print('\n') #line break
    bank = []
    for item in results:
        if not item in bank:
            bank.append(item)
        else:
            print(f'Duplicate detected: {item}')
    if len(bank) == len(results):
        print('No duplicates detected.\n')
    input('Press enter to edit videos...\n')
    for item in results:
        '''
        if results.index(item) == 1:
            break
        '''
        title = item.rsplit(',')[-2]
        id = item.rsplit(',')[-1]
        print(title, id)
        response = yt.updateVideo(title,id)
