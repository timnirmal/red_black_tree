# red_black_tree

Explanation: https://chat.openai.com/share/a66d55cb-a359-4448-88a6-7454f8a3d80d

Example Run:

```
Enter command (or 'Exit' to quit): 5 10 15 20 25 30 35 40 50
B20
├──R30
│  ├──B40
│  │  ├──R50
│  │  └──R35
│  └──B25
└──R10
   ├──B15
   └──B5
Enter command (or 'Exit' to quit): Delete 35
B20
├──R30
│  ├──B40
│  │  ├──R50
│  └──B25
└──R10
   ├──B15
   └──B5
Enter command (or 'Exit' to quit): Search 60
False
Enter command (or 'Exit' to quit): Min 
Minimum value: 5
Enter command (or 'Exit' to quit): Max
Maximum value: 50
```
