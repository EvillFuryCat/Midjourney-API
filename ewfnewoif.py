headers = {"Authorization": f"{CLIENT_TOKEN}", "Content-Type": "application/json", "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
    data = {
   "type":2,
   "application_id":"936929561302675456",
   "guild_id":"285724843557781505",
   "channel_id":"285724843557781505",
   "session_id":"effacc7b-e32c-4002-8f61-d4b471fe22c7",
   "data":{
      "version":"1118961510123847772",
      "id":"938956540159881230",
      "name":"imagine",
      "type": 1,
      "options":[
         {
            "type":3,
            "name":"prompt",
            "description":"What is the question?",
            "required":True,
            "value": f"{prompt}"
         }
      ]
   }
}