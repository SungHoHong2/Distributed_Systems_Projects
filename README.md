# Distributed Systems
Three Projects for Distributed Systems course in [Coursera](https://www.coursera.org/).
The repository includes the documentation and implementation of the project.
The ultimate goal of the three projects is to create a marketplace where independent sellers and buyers follow the consistency model.  

- ### gRPC
1. [x] Guarantee that the clients will get the same result from the final query request
   - Add sleep to make sure the final result is completely propagated.
2. [x] Clients will get success or fail from the withdraw and deposit requests
3. [x] Make the client id identical to the bank id
4. [ ] Save the output of all the operation in the XML file
   - The test application will collect the output
   - Only clients return the record of operations


- ### Logical Clock 
    - [benchmark for logical clock](lamportBenchmark) 
    - [implementation of logical clock for independent processes](lamportClocks)

- ### Client Consistency     
 


