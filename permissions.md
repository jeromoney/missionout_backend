A table illustrating the permissions for user roles and documents. The permissions can be read left to right with additional permissions stacked on. e.g. An editor has all the permissions of a user and more.

Documents are associated with either a user or a team. No user can access a document of another team or user in that team. 


--- | Location                                              | Anonymous      | User        | Editor
---          | ---                                                   | ---          | ---                                  | ---
User    | /users/{user}                                         | no access |get,update own self | read,update own team 
Team    | /teams/{team}    | no access                                     | get own team         | update own team                                  
Mission | /teams/{team}/missions/{mission}        | no access              | read own team         | write own team                               
Responses    | /teams/{team}/missions/{mission}/responses/{response}| no access | read own team, write own response         | --                                  
Pages        | /teams/{team}/missions/{mission}/pages/{page}         | no access         | --                                      | create own team
