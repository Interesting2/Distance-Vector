How to Start Program and Running Environment

    Install and setup python3
    Do python3 --version to check if it is installed correctly
    If not, follow the instructions in this page: https://realpython.com/installing-python/

    Create 10 terminals
    Run the following 10 commands in 10 different terminals/shells (1 command in each terminal)

    python3 COMP3221_DiVR.py A 6000 Aconfig.txt
    python3 COMP3221_DiVR.py B 6001 Bconfig.txt
    python3 COMP3221_DiVR.py C 6002 Cconfig.txt
    python3 COMP3221_DiVR.py D 6003 Dconfig.txt
    python3 COMP3221_DiVR.py E 6004 Econfig.txt
    python3 COMP3221_DiVR.py F 6005 Fconfig.txt
    python3 COMP3221_DiVR.py G 6006 Gconfig.txt
    python3 COMP3221_DiVR.py H 6007 Hconfig.txt
    python3 COMP3221_DiVR.py I 6008 Iconfig.txt
    python3 COMP3221_DiVR.py J 6009 Jconfig.txt

    Observe the output of the terminal


Change Link Cost
    There are 10 txt files, each file contains the neighbour ids with the port and link cost.
    Example inside Aconfig.txt: B 6.1 6001
    B is the neighbour node of A, 6.1 is the link cost, and 6001 is the port number of node B
    Change Link Cost by modifying the 6.1 field to some other float numbers. 
    This applies to any given txt files, which means you can modify the middle field when any float number to change link cost

Node Failure
    If you want to test for link failures, terminate a program by pressing control+c in a certain terminal. 
    For instance, find the terminal where you ran "python3 COMP3221_DiVR.py C 6002 Cconfig.txt", and press control+c.
    Check the output of other terminals, and you will then notice the link to node C will be destroyed, and the link cost 
    of other nodes will start to change. One simulation example is shown in the report.
