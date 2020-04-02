--- | Location                                              | Users      | Editors        | Anonymous
---          | ---                                                   | ---          | ---                                  | ---
User    | /users/{user}                                         | get,update own self | read,update own team | no access                     
Token        | /users/{user}/tokens/{token}                          | create own token         | no access | no access        
Team    | /teams/{team}                                         | get own team         | get,update own team                                  | no access
Mission | /teams/{team}/missions/{mission}                      | read own team         | read,write own team                               | no access
Responses    | /teams/{team}/missions/{mission}/responses/{response} | read own team, write own response         | read own team, write own response                                  | no access
Pages        | /teams/{team}/missions/{mission}/pages/{page}         | no access         | create own team                                      | no access
