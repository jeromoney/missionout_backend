--- | Location                                              | Users      | Editors        | Different Team | Anonymous
---          | ---                                                   | ---          | ---          | ---                               | ---
User    | /users/{user}                                         | read,update only their document | read,update on their team | no access                      | no access
Token        | /users/{user}/tokens/{token}                          | null         | null         | no access                              | no access
Team    | /teams/{team}                                         | null         | null         | no access                              | no access
Mission | /teams/{team}/missions/{mission}                      | null         | null         | no access                              | no access
Responses    | /teams/{team}/missions/{mission}/responses/{response} | null         | null         | no access                              | no access
Pages        | /teams/{team}/missions/{mission}/pages/{page}         | null         | null         | no access                              | no access
