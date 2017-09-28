# kentik_add_device


This is a python script that reads device data from a .csv file and creates devices in the Kentik portal using the Kentik API. 

For example, a .csv file consisting of

```
router_test1,router,Test Router 1,2144,1365,100,10.254.254.1,10.254.254.1,testcommunity
router_test2,router,Test Router 2,2144,1365,100,10.254.254.2,10.254.254.2,testcommunity
router_test3,router,Test Router 3,2144,1365,100,10.254.254.3,10.254.254.3,testcommunity
```


Will create three new devices in the kentil portal with the minimal number of required config elements. 

Lines beginning with '#' are ignored.

There is some minimal error handling to help diagnose failed updates. 

123
