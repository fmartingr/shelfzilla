# How Provisioning works?
The deploy of Shelfzilla use Ansible statements to load the Shelfzilla application in a server that you have in the inventory file "hosts". Thie provision have some requirements:
- Ansible >= 1.3
- Vagrant >= 1.5 (For local environment)
- Virtualbox

## How to work in a local environment?
Follow this steps and have fun:
```sh
git clone git@github.com:fmartingr/shelfzilla.git
cd shelfzilla
vagrant up
```
This provision will take about 10 minutes

### Give me more cores!
If it´s necessary to upgrade the VM you only must to modify this variables from Vagrant file:
```
BOX_MEM = ENV['BOX_MEM'] || "1024"
BOX_CORE = ENV['BOX_CORE'] || "2"
```
And if you want to make some experiments, try to change the BoxName and BoxURL:
```
BOX_NAME =  ENV['BOX_NAME'] || "CentOS6.5"
BOX_URI = ENV['BOX_URI'] || "https://github.com/2creatives/vagrant-centos/releases/download/v6.5.3/centos65-x86_64-20140116.box"
```

## How to deploy in a remote server?
Soon...

## How to add new remote server and deploy Shelfzilla?
Soon...
