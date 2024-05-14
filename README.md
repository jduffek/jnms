
joshd:jnms-pub joshduffek$ python3 jnms.py
Would you like to input a network range(s)? (yes/file/no): file
What is the name of the file?: foo.bar
10.1.1.4 is alive
10.1.1.1 is alive
10.1.1.5 is alive
10.1.1.2 is alive
10.1.1.3 is alive
10.1.1.147 is alive
8.8.8.8 is alive
1.1.1.1 is alive
Discovery results saved to host-disco_2024-05-14_12-35-33.txt
Results also saved to nodes.db
Do you want to specify ports to scan? (yes/no): yes
Enter port(s) to scan (e.g., 8080 or 8000-8100): 10000-10005
Port 10000 is open on 10.1.1.4
Port 10001 is open on 10.1.1.4
Port 10002 is open on 10.1.1.4
Port 10003 is open on 10.1.1.4
Port 10004 is open on 10.1.1.4
Port scanning results:
10.1.1.4:10000
10.1.1.4:10001
10.1.1.4:10002
10.1.1.4:10003
10.1.1.4:10004
10.1.1.1: ICMP OK
10.1.1.2: ICMP OK
10.1.1.4: ICMP OK
10.1.1.5: ICMP OK
8.8.8.8: ICMP OK
1.1.1.1: ICMP OK
10.1.1.147: ICMP OK
10.1.1.4:10000 TCP OK
10.1.1.4:10001 TCP OK
10.1.1.4:10002 TCP OK
10.1.1.4:10003 TCP OK
10.1.1.4:10004 TCP OK
2024-05-14 12:35:48 - 1.3.6.1.2.1.1.3.0 = 6569237
2024-05-14 12:35:48 - 1.3.6.1.2.1.25.1.1.0 = 23113012
10.1.1.3: ICMP OK
10.1.1.10: ICMP OK
2024-05-14 12:35:48 - 1.3.6.1.4.1.2021.4.5.0 = N/A
2024-05-14 12:35:48 - 1.3.6.1.4.1.2021.4.6.0 = N/A
10.1.1.12: ICMP Failed
10.1.1.255: ICMP OK
10.1.1.147:21 TCP OK
10.1.1.147:22 TCP OK
10.1.1.1:53 TCP OK
10.1.1.1:80 TCP OK
10.1.1.147:80 TCP OK
10.1.1.147:111 TCP OK
10.1.1.147:139 TCP OK
10.1.1.10:80 TCP OK
10.1.1.1:443 TCP OK
10.1.1.147:443 TCP OK
10.1.1.147:445 TCP OK
10.1.1.147:548 TCP OK
10.1.1.1:631 TCP OK
10.1.1.147:631 TCP OK
10.1.1.147:873 TCP OK
1.1.1.1:53 TCP OK
8.8.8.8:53 TCP OK
=======
joshd:jnms-pub joshduffek$ python3 jnms.py<br>
Would you like to input a network range(s)? (yes/file/no): file<br>
What is the name of the file?: foo.bar<br>
10.1.1.147 is alive<br>
8.8.8.8 is alive<br>
1.1.1.1 is alive<br>
Discovery results saved to host-disco_2024-05-14_12-35-33.txt<br>
Results also saved to nodes.db<br>
Do you want to specify ports to scan? (yes/no): yes<br>
Enter port(s) to scan (e.g., 8080 or 8000-8100): 10000-10005<br>
Port 10000 is open on 10.1.1.4<br>
Port 10001 is open on 10.1.1.4<br>
Port 10002 is open on 10.1.1.4<br>
Port 10003 is open on 10.1.1.4<br>
Port 10004 is open on 10.1.1.4<br>
Port scanning results:<br>
10.1.1.4:10000<br>
10.1.1.4:10001<br>
10.1.1.4:10002<br>
10.1.1.4:10003<br>
10.1.1.4:10004<br>
10.1.1.1: ICMP OK<br>
8.8.8.8: ICMP OK<br>
1.1.1.1: ICMP OK<br>
10.1.1.147: ICMP OK<br>
10.1.1.4:10000 TCP OK<br>
10.1.1.4:10001 TCP OK<br>
10.1.1.4:10002 TCP OK<br>
10.1.1.4:10003 TCP OK<br>
10.1.1.4:10004 TCP OK<br>
2024-05-14 12:35:48 - 1.3.6.1.2.1.1.3.0 = 6569237<br>
2024-05-14 12:35:48 - 1.3.6.1.2.1.25.1.1.0 = 23113012<br>
2024-05-14 12:35:48 - 1.3.6.1.4.1.2021.4.5.0 = N/A<br>
2024-05-14 12:35:48 - 1.3.6.1.4.1.2021.4.6.0 = N/A<br>
10.1.1.12: ICMP Failed <br>
10.1.1.255: ICMP OK<br>
10.1.1.147:21 TCP OK<br>
10.1.1.147:22 TCP OK<br>
10.1.1.147:80 TCP OK<br>
1.1.1.1:80 TCP OK<br>
>>>>>>> 76c5eaea671c6ae3c3bbebef2b897d8bcdaee999
