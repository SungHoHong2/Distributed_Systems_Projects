### Skeleton 

- bank instances 
    - [ ] contains a `server` and a `client stub`
    - [ ] banks can `communicate with each other` (client consistency)  
 
- client instances 
    - [ ] contains a `client stub`
    - [ ] only communicates with the bank
    - [ ] stores a output json file after running all the requests  

- test application 
    - [ ] parse json file input to generate requests 
    - [ ] invokes the number of banks and clients 
    - [ ] returns the collective result after all the clients are terminated
