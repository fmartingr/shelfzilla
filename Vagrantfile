# -*- mode: ruby -*-
# vi: set ft=ruby :

# Shelfzilla Vagrantfile with Ansible provision

VAGRANTFILE_API_VERSION = "2"

BOX_MEM = ENV['BOX_MEM'] || "1024"
BOX_CORE = ENV['BOX_CORE'] || "2"
BOX_NAME =  ENV['BOX_NAME'] || "CentOS6.5"
BOX_URI = ENV['BOX_URI'] || "https://github.com/2creatives/vagrant-centos/releases/download/v6.5.3/centos65-x86_64-20140116.box"

Vagrant.require_version ">= 1.5"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |shelfzilla|
    shelfzilla.vm.box = BOX_NAME
    shelfzilla.vm.box_url = BOX_URI
    shelfzilla.vm.provider "virtualbox" do |v|
        v.customize ["modifyvm", :id, "--memory", BOX_MEM]
        v.customize ["modifyvm", :id, "--ioapic", "on"]
        v.customize ["modifyvm", :id, "--cpus", BOX_CORE]
        v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
        v.customize ["modifyvm", :id, "--natdnsproxy1", "on"]
    end
    shelfzilla.vm.network "forwarded_port", guest: 80, host: 8080
    shelfzilla.vm.network "private_network", ip: "192.168.33.10"
    shelfzilla.vm.provision "ansible" do |ansible|
        ansible.playbook = "provisioning/site.yml"
        ansible.limit = "vagrant"
        ansible.inventory_path = "provisioning/hosts"
        #ansible.verbose = "vvv"
    end
end