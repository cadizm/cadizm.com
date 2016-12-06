# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.box = "bento/ubuntu-16.04"

  config.vm.network "private_network", ip: "192.168.101.3"
  config.ssh.forward_agent = true
  config.vm.network "forwarded_port", guest: 8002, host: 8002

  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "lib/ansible-provision/adduser-cadizm.yml"
    ansible.sudo = true
  end

end
