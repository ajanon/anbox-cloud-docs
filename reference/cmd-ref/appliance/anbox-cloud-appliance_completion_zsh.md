## anbox-cloud-appliance completion zsh

Generate the autocompletion script for zsh

### Synopsis

Generate the autocompletion script for the zsh shell.

If shell completion is not already enabled in your environment you will need
to enable it.  You can execute the following once:

	echo "autoload -U compinit; compinit" >> ~/.zshrc

To load completions in your current shell session:

	source <(anbox-cloud-appliance completion zsh)

To load completions for every new session, execute once:

#### Linux:

	anbox-cloud-appliance completion zsh > "${fpath[1]}/_anbox-cloud-appliance"

#### macOS:

	anbox-cloud-appliance completion zsh > $(brew --prefix)/share/zsh/site-functions/_anbox-cloud-appliance

You will need to start a new shell for this setup to take effect.


```
anbox-cloud-appliance completion zsh [flags]
```

### Options

```
  -h, --help              help for zsh
      --no-descriptions   disable completion descriptions
```

### SEE ALSO

* [anbox-cloud-appliance completion](anbox-cloud-appliance_completion.md)	 - Generate the autocompletion script for the specified shell

