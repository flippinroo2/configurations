# Python Environment Variables
PYENV_HOME="$HOME/PATH_TO_PYENV_SHIMS"

# Java Environment Variables
JENV_ROOT="PATH_TO_JENV"
JENV_HOME="$HOME/.jenv/bin"
# JENV_HOME="$HOME/.jenv/bin:$HOME/.jenv/shims"

# Android Environment Variables
ANDROID_HOME="$HOME/PATH_TO_ANDROID_SDK"
ANDROID_BUILD_TOOLS="$HOME/PATH_TO_ANDROID_BUILD_TOOLS"
ANDROID_PLATFORM_TOOLS="$HOME/PATH_TO_ANDROID_PLATFORM_TOOLS"

# OpenSSL Environment Variable (Upgrading OpenSSL: https://medium.com/@katopz/how-to-upgrade-openssl-8d005554401)
OPENSSL="PATH_TO_OPENSSL"

# OPENVPN Environment Variable
OPENVPN="PATH_TO_OPENVPN"

# Rust Environment Variables
CARGO_HOME="$HOME/PATH_TO_CARGO_ENV"

## Initialize cargo
. "$CARGO_HOME"

# Solana
SOLANA_HOME="$HOME/PATH_TO_SOLANA_BINARY"

# Specific makefile entries for libressl (Trying to resolve Pyenv 3.4.6 install issue: https://github.com/pyenv/pyenv/wiki/common-build-problems)

CFLAGS="-I/HOMEBREW_INCLUDES"
CPPFLAGS="-I/HOMEBREW_INCLUDES"
LDFLAGS="-L/HOMEBREW_LIBRARIES -L/HOMEBREW_LIBRARIES"
# PKG_CONFIG_PATH="LIBRESSL_PACKAGE_CONFIG"

# More makefile stuff (has to do with C compilers and GNU stuff)
CPATH="/HOMOEBREW_INCLUDES"
LIBRARY_PATH="/USER_LIBRARIES:/USER_LOCAL_LIBRARIES"
LD_LIBRARY_PATH="/USER_LIBRARIES:/USER_LOCAL_LIBRARIES"
PKG_CONFIG_PATH="/LIBRESSL_PACKAGE_CONFIG"

# Adding to PATH before exporting
PATH="$JENV_HOME:$PYENV_HOME:$SOLANA_HOME:$PATH"
# PATH="$OPENVPN:$OPENSSL:$PATH"

# Exporting all of the Environment Variables
export ANDROID_HOME
export ANDROID_BUILD_TOOLS
export ANDROID_PLATFORM_TOOLS
export JENV_ROOT
export CFLAGS
export LDFLAGS
export CPPFLAGS
export CPATH
export LIBRARY_PATH
export PKG_CONFIG_PATH
export PATH
export LC_ALL="en_US.UTF-8"
export LANG="en_US.UTF-8"
export LANGUAGE="en_US.UTF-8"
