# Internet Speed Data Collection

To use this program, run

```
$ make run
```

Dependencies are

- `wget`
- Python 3.7+

I am using this to analyse my internet speed in the future.

Upon running the program, a list of servers will be written to `data/servers.csv`. These servers will be used for each consecutive run unless the list is removed.

The output data is stored in `data/<year>-<month>-<day>.csv`. Once a new day starts, a new file is created.

# TODO

- [ ] Add automatic architecture recognition (for use on ARM)
