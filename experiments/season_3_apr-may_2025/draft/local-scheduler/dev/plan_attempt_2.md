1) prototype in nmp
2) then move to dev_env
3) Draw a diagram

- a
	- run scheduler once
		- check if any of the tasks are due
		- Run the overdue ones
		- try-except? Subprocess? 
	- run scheduler continuously
		- period? 
- b
	- Where and how to store info?
	- DataStorageBase
		- Cache layer for better speed / avoid i/o for frequent updates?
	- DataStorageMemory
	- DataStorageMongo
	- DataStorageFilesystem
- c
	- What info to store?
	- 1 - event to run. Job - fields:
		- executable (default - poetry in dev_env)
		- 
		- flags - args, kwargs (default - None)
		- env file (default - ~/.env)
	- 2 - log run events
		- timestamp
		- status?
		- 
- d
	- cli - commands to support
- e
	- aliases
	- 1) run scheduler (once)
	- 2) launch scheduler (continuously)
