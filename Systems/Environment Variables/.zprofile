# This is added to enable a lot of the homebrew installed stuff
SBIN="/PATH_TO_SBIN"

# Creating the path based on all the stuff above
PATH="$SBIN:$PATH"

# Terminal Configurations

## Colors
export CLICOLOR=1

# Aliases
# Syntax: alias <alias_name>="<command_to_run>"

alias la="ls -F"
alias ll="ls -Fla"
alias of="lsof -nP +c 15 | grep LISTEN"
alias vpn="cd ~/VPN && sudo openvpn --config client.conf && cd -"

# Functions
# Syntax: test_function() { echo "test_function()"; }

## Initializing jenv & pyenv
eval "$(jenv init -)"
eval "$(pyenv init -)"
