# toof - Easy Two Factor CLI

A simple CLI application for generating MFA codes.

# Requirements

- Python3
- Keyring
- Pyperclip

# Running

`toof [generate] <alias>` - Generate a TOTP code for the specified alias and copy it to the system clipboard. Note that this is the default behavior if no recognized subcommand is provided.  
`toof add <name> <secret> [alias]` - Add an entry for a new service. Will be stored under the provided name. Optionally an initial alias can also be provided.  
`toof delete <name>` - Delete the entry for a service by name.  
`toof alias <name> <alias>` - Add an alias for an existing service.  
`toof dealias <name> <alias>` - Delete an alias for an existing service.  
`toof help` - Print instructions for using the commands.  

# Examples

$ toof add testservice MZXW6CQ test  
$ toof test  
AccountId is testservice  
Outputting code for testservice, 276738

# Installation
sudo cp dist/toof /usr/bin
