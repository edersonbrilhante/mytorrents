VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.network "private_network", ip: "192.168.120.2", auto_config: "false"
  config.vm.hostname = "TORRENTPROJECT"
  config.omnibus.chef_version = :latest
  config.vm.provider "virtualbox" do |v|
    v.memory = 2048
  end
  config.vm.provision :shell, path: "vagrant_provision.sh"
end
