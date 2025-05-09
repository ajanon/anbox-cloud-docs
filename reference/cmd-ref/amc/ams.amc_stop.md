## ams.amc stop

Stop a running instance

### Synopsis

Stop a running instance.

If the instance is in 'running' status, you can stop it with the 'amc stop' command.


```
ams.amc stop <instance_id> [flags]
```

### Examples

```
  Launch an instance:
  $ amc launch <image_id|app_id>
  ceg2ukbhc8ic3ftkc990

  Stop the running instance:
  $ amc stop ceg2ukbhc8ic3ftkc990
```

### Options

```
  -h, --help             help for stop
      --no-wait          Don't wait for the instance to stop before returning (default disabled)
  -t, --timeout string   Maximum time to wait for the operation to complete (default "5m")
```

### SEE ALSO

* [ams.amc](ams.amc.md)	 - Anbox Management Client

