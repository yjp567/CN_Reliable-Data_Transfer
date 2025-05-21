# Course: Computer Networks

# Reliable Data Transfer Protocols

This repository contains implementations of two reliable data transfer protocols:

1. **Stop-and-Wait**
2. **Go-Back-N**

## Stop-and-Wait

### Instructions to Run:

1. In the `stopandwait` directory, open the terminal and run:
   ```bash
   sudo mn
    ```

2.  In the Mininet CLI, open terminals:
   
    ```
	  xterm h1 
	   ```
	 ```
	   xterm h2
      ```
    
3.  Set up network conditions (10Mbps bandwidth, 5ms delay, 0% loss) using commands from the problem statement.
    
4.  Run the Python scripts:
    
    -   On `h1`:
        
       ```
        python CS22BTECH11047_receiverStopWait.py
     ``` 
        
    -   On `h2`:
        
       ```
       python CS22BTECH11047_senderStopWait.py
     ```
        

## Go-Back-N

The Go-Back-N implementation is in the `gobackn` directory. Instructions to run are similar, with changes in parameters as specified in the problem.
