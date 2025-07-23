# Todos

- [ ] feature: check previous job runs before launch to see if it's time to run it.
- [ ] feature: save past runs of jobs somewhere
  - option 1: database (local mongo). Con: i forget to run it sometimes.. And there's no way to auto-launch.. Although, i reboot rarely. A job to check mongo and ping me to telegram if it's down? 
  - option 2: filesystem? Rocksdb? Or just json? 
- [x] a job to check local mongo and ping me to telegram if it's down.. 

- [ ] run scheduler (all jobs) once
- [ ] run scheduler continuously (how to reload jobs? a job? or just always)
- [ ] cli
  - [ ] add job -> save to the yaml? 
  - [ ] see jobs? + status, last run. Exposed result? 
- [ ] make all async? Can i make all jobs run in parallel, not one by one? and then gather

- [ ] add util tool for plist creation - from archive - use it to setup the job first run?
  - migrate to dev_env asap. Use local path or .calmmage path? 

- [ ] Launch ASAP!!! 
  - Copy the google docs job