import requests

url = 'http://127.0.0.1:5000/video'
myobj = {'mapID': '26171', 'video_url' : 'https://dmail-my.sharepoint.com/personal/dzografistou001_dundee_ac_uk/_layouts/15/stream.aspx?id=%2Fpersonal%2Fdzografistou001_dundee_ac_uk%2FDocuments%2FSerapis%2FU85%2FRedTeaming%20videos%2FRedTeamingMoonTrimmed.mp4'}

x = requests.post(url, params = myobj)

print(x.text)

#https://dmail-my.sharepoint.com/personal/dzografistou001_dundee_ac_uk/_layouts/15/stream.aspx?id=%2Fpersonal%2Fdzografistou001_dundee_ac_uk%2FDocuments%2FSerapis%2FU85%2FRedTeaming%20videos%2FRedTeamingMoonTrimmed.mp4