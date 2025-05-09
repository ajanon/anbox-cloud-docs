## ams.amc image show

Show information about an image

### Synopsis

Show information about an image.

Formatting can be controlled with the '--format' flag.
Valid formats are 'json' and 'yaml'.

```
ams.amc image show ( <id> | <name> ) [flags]
```

### Examples

```
$ amc image show foo
id: bkkbiaphpuo3mh78ain0
name: foo
status: active
versions:
  0:
    size: 2.26MB
    created-at: 2019-07-12 16:45:31 +0000 UTC
    status: active
used_by:
- bkmtdm9hpuo01q954fng
architecture: x86_64
default: true
type: container
variant: android

```

### Options

```
      --format string   Output format - 'json' or 'yaml' (default "yaml")
  -h, --help            help for show
      --vm              Show the virtual machine image instead of a container image
```

### SEE ALSO

* [ams.amc image](ams.amc_image.md)	 - Manage images

