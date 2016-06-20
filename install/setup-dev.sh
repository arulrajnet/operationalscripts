#! /bin/bash

if [[ -f ./setup.env ]]; then
  source ./setup.env
fi

function __get_html() {
  local html=$(curl -k -L -s $1)
  echo "$html"
}

function do_install_java() {
    sudo add-apt-repository ppa:webupd8team/java -y
    sudo apt-get update
    sudo apt-get install oracle-java8-set-default -y

    echo "Installing Maven..."
    sudo apt-get remove maven*
    sudo apt-get purge maven maven2 maven3
    sudo add-apt-repository ppa:andrei-pozolotin/maven3 -y
    sudo apt-get update && sudo apt-get install maven3 -y    
    
    # http://www.eclipse.org/downloads/packages/eclipse-ide-java-ee-developers/mars2
    __do_install_eclipse
}

function __do_install_eclipse() {

  eclipse_install_dir=${ECLIPSE_INSTALL_DIR:-./eclipse}
  mkdir -p $eclipse_install_dir

  echo "Installing eclipse in "$eclipse_install_dir

  cat <<'EOF' > /tmp/eclipse-plugin.cfg
http://beust.com/eclipse/,org.testng.eclipse
http://andrei.gmxhome.de/eclipse/,AnyEditTools.feature.group
http://eclipse-cs.sf.net/update,net.sf.eclipsecs.feature.group
http://findbugs.cs.umd.edu/eclipse,edu.umd.cs.findbugs.plugin.eclipse.feature.group
EOF

  mirrors_xml="http://www.eclipse.org/downloads/download.php?file=/technology/epp/downloads/release/mars/2/eclipse-jee-mars-2-linux-gtk-x86_64.tar.gz&format=xml"

  download_archive_link=$(__get_html "$mirrors_xml" | sed -u "s:.*url\=\"\(.*.gz\)\".*:\1:p" | sed "3q;d")

  bash <( curl -sk https://raw.githubusercontent.com/budhash/install-eclipse/master/install-eclipse ) -d $download_archive_link -f -c /tmp/eclipse-plugin.cfg $eclipse_install_dir
}

function do_install_git() {
  sudo apt-get install git-core -y

  echo "configuring git..."
  GIT_USERNAME=${GIT_USERNAME:-$USER}
  GIT_EMAIL=${GIT_EMAIL:-$GIT_USERNAME@`hostname`}
  git config --global user.name "${GIT_USERNAME}"
  git config --global user.email "${GIT_EMAIL}"
  git config --list

  tee -a ~/.gitconfig <<EOF
[alias]
  remotes = remote -v
  branches = branch -a
  tags = tag -l
  currentbranch = rev-parse --abbrev-ref HEAD
  id = rev-parse --short HEAD
  lg = log --color --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset'
  co = checkout
  sl = log --name-only --oneline

[apply]
  whitespace = fix

[color]
  ui = auto

[core]
  filemode = false
  excludesfile = ~/.gitignore_global
  whitespace = trailing-space,space-before-tab,indent-with-non-tab
  autocrlf = input
  compression = 0

[fetch]
  prune = true

[diff]
  submodule = log
  
[push]
  default = simple
EOF

  tee -a ~/.gitignore_global<<EOF
## OS generated files
**/*~
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db
*.bak
.history

## IDE files
.classpath
.project
.settings
.idea
.metadata
*.iml
*.ipr
*.class
*.log

## Maven files
target
pom.xml.tag
pom.xml.releaseBackup
pom.xml.versionsBackup
pom.xml.next

## Sublime
*.sublime-project
*.sublime-workspace
EOF

tee -a ~/.git_commit_template<<EOF
# <type>(<scope>): <subject>
#
# <body>
#
#
# <footer>
#
# ** TYPES **
# feat (new feature)
# fix (bug fix)
# docs (changes to documentation)
# style (formatting, missing semi colons, etc; no code change)
# refactor (refactoring production code)
# test (adding missing tests, refactoring tests; no production code change)
# chore (updating grunt tasks etc; no production code change)
#
# ** FOOTERS **
# References #1, #4, and #2.
# Fix #1. note this marks the item as accepted in Sprintly
# Closes #1 and #2. note this marks the item as accepted in Sprintly

# ** Fun tip **
# Work hard, play hard!  Consider prefixing your commit messages with a relevant emoji for 
# great good:
#
#   :art: `:art:` when improving the format/structure of the code
#   :racehorse: `:racehorse:` when improving performance
#   :non-potable_water: `:non-potable_water:` when plugging memory leaks
#   :memo: `:memo:` when writing docs
#   :penguin: `:penguin:` when fixing something on Linux
#   :apple: `:apple:` when fixing something on Mac OS
#   :checkered_flag: `:checkered_flag:` when fixing something on Windows
#   :bug: `:bug:` when fixing a bug
#   :fire: `:fire:` when removing code or files
#   :green_heart: `:green_heart:` when fixing the CI build
#   :white_check_mark: `:white_check_mark:` when adding tests
#   :lock: `:lock:` when dealing with security
#   :arrow_up: `:arrow_up:` when upgrading dependencies
#   :arrow_down: `:arrow_down:` when downgrading dependencies
#   :shirt: `:shirt:` when removing linter warnings
EOF

tee -a ~/.gitconfig <<EOF
[commit]
  template = ~/.git_commit_template
EOF

  echo "Installing git addons..."

  curl -sSL https://raw.github.com/nvie/gitflow/develop/contrib/gitflow-installer.sh | sudo bash
  git clone https://github.com/magicmonty/bash-git-prompt.git ~/.bash-git-prompt

  tee -a ~/.bashrc <<EOF
#
# Git Prompt
# https://github.com/magicmonty/bash-git-prompt
#
if [ -f ~/.bash-git-prompt/gitprompt.sh ]; then
    # Config
    # Set config variables first
    GIT_PROMPT_ONLY_IN_REPO=1
    . ~/.bash-git-prompt/gitprompt.sh
fi
EOF

  sudo apt-get install --reinstall make
  curl -sSL http://git.io/git-extras-setup | sudo bash /dev/stdin
}

function do_install_docker() {

  wget -qO- https://get.docker.com/ | sh
  sudo usermod -aG docker $USER
  sudo service docker restart

  echo "Installing docker autocomplete..."
  curl -ksSL https://raw.githubusercontent.com/docker/docker/$(docker --version | awk 'NR==1{print $NF}')/contrib/completion/bash/docker |sudo tee /etc/bash_completion.d/docker

  echo 'DOCKER_OPTS="-H tcp://127.0.0.1:4243 -H unix:///var/run/docker.sock --dns 8.8.8.8 --dns 8.8.4.4"' | sudo tee -a /etc/default/docker > /dev/null
  echo 'DOCKER_HOST="tcp://localhost:4243"' | sudo tee -a /etc/environment > /dev/null

  sudo service docker restart

  echo "Installing docker compose..."
  sudo apt-get install python-pip -y
  sudo pip install -U docker-compose  
}

function do_install_go() {
  echo "Installing golang.."
  sudo apt-get install curl git make binutils bison gcc build-essential -y

  bash < <(curl -s -S -L https://raw.githubusercontent.com/moovweb/gvm/master/binscripts/gvm-installer)
  source ~/.gvm/scripts/gvm
  gvm listall
  export CGO_ENABLED=0
  gvm install go1.4
  gvm use go1.4
  go version
  export GOROOT_BOOTSTRAP=$GOROOT
  gvm install go1.5.1
  gvm use go1.5.1 --default
}

function do_install_npm() {
  curl -sL https://deb.nodesource.com/setup_5.x | sudo -E bash -
  sudo apt-get install -y nodejs
  sudo npm install -g grunt-cli
}

echo "Installing Java..."
do_install_java
echo "Installing Git..."
do_install_git
echo "Installing Docker..."
do_install_docker
do_install_go
do_install_npm
