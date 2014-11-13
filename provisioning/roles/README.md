# Cheatsheet Ansible Modules

## Common
Common module include this steps
- Installation of Puias 6 Computational repository
- SElinux permissive statement
- Loading of iptables rules (not in vagrant environment)

## Shelfzilla Base
This module will load all dependencies that Shelfzilla platform needs to work, and include this steps:
- Installation of Shelfzilla repository
- Installation of: 
    - Python27 and Pip
    - Nodejs and NPM
    - PostgreSQL
- Base configuration of PostgreSQL