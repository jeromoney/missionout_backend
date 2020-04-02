--- | Location                                              | Anonymous      | User        | Editor
---          | ---                                                   | ---          | ---                                  | ---
User    | /users/{user}                                         | no access |get,update own self | read,update own team 
Token        | /users/{user}/tokens/{token}                          | no access | create own token         | no access        
Team    | /teams/{team}    | no access                                     | get own team         | get,update own team                                  
Mission | /teams/{team}/missions/{mission}        | no access              | read own team         | read,write own team                               
Responses    | /teams/{team}/missions/{mission}/responses/{response}| no access | read own team, write own response         | read own team, write own response                                  
Pages        | /teams/{team}/missions/{mission}/pages/{page}         | no access         | create own team                                      | no access
