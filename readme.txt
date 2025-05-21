Instructions to run the code:

- In the current directory (stopandwait), open the terminal and run : sudo mn
- In the mininet environment, run:
    - xterm h1
    - xterm h2
- Now, execute the commands mentioned in problem statement to set up the network conditions (10Mbps bandwidth, 5ms propagation delay and 0% packet loss rate)
- Lastly, run the python scriots:
    - python CS22BTECH11047_receiverStopWait.py     (From xterm h1)
    - python CS22BTECH11047_senderStopWait.py     (From xterm h2)