#!/usr/bin/python3
import subprocess
import os
import urllib.request
import json



def exec_command(args):
    res = subprocess.run(args,capture_output=True,text=True)
    return res.returncode, res.stdout

def download_image(image_link, image_path, image_name):
    print("Downloading cloudimage...")
    def progress(block_num, block_size,total_size):
        downloaded = block_num * block_size
        print(f"\r{downloaded} / {total_size}", end="",flush=True)
    urllib.request.urlretrieve(image_link, image_path, reporthook=progress)
    filepath = os.path.abspath(image_name)
    print("\nDone! Image path:", filepath)


def check_configs(udp, mdp, ncp):
    config_files = [udp, mdp, ncp]
    for file in config_files:
        if os.path.isfile(file) == False:
            print(f"something wrong with {file}. Check is exists, perms")
            return 1
    print("Configs acceptable")


def create_seed_img(userdata_path, metadata_path, networkconfig_path):
    EXEC_SEED_CMD = ["cloud-localds", SEED_IMAGE_PATH, userdata_path, metadata_path, "--network-config", networkconfig_path]
    check_configs(userdata_path, metadata_path, networkconfig_path)
    print("Creating seed image with cloud-init configs....")
    exec_command(EXEC_SEED_CMD)
    filepath = os.path.abspath(SEED_IMAGE_PATH)
    print("Done! Seed image path:", filepath)


def resize_image(image_path, image_size):
    EXEC_QEMUIMG_CMD = ["qemu-img", "info", "--output=json", image_path]
    size = exec_command(EXEC_QEMUIMG_CMD)[1]
    virtual_size = json.loads(size)["virtual-size"]
    how_many_add_to_image = image_size*1024*1024*1024 - int(virtual_size)
    EXEC_RESIZE_CMD = ["qemu-img" , "resize", image_path, f"+{how_many_add_to_image}"]
    exec_command(EXEC_RESIZE_CMD)


def create_virtual_machine(vm_name, vm_ram, vm_vcpus, vm_net, vm_disk):
    print("Creating VM...")

    EXEC_VIRT_INSTALL_CMD = [
        "virt-install",
        "--name", vm_name,
        "--memory", f"{vm_ram*1024}",
        "--vcpus", str(vm_vcpus),
        "--disk", str(vm_disk),
        "--disk", f"{SEED_IMAGE_PATH},device=cdrom",
        "--import",
        "--os-variant", "almalinux8",
        "--network", f"network={vm_net}",
        "--noautoconsole",
        "--wait", "0"
    ]

    exec_command(EXEC_VIRT_INSTALL_CMD)
    print(f"{vm_name} created! Wait, while cloud-init is working")

def show_virtual_machine_info():
    pass

def is_cloudinit_finished():
    pass

def create_network():
    pass

def install_deps():
    pass


VM_NAME = "test-vm"
VM_RAM = 2
VM_VCPUS = 2
VM_NET = "homelab"
VM_SIZE = 15


IMAGE_LINK = "https://cloud.debian.org/images/cloud/trixie/20250806-2196/debian-13-genericcloud-amd64-20250806-2196.qcow2"
IMAGE_NAME = f"{VM_NAME}.qcow2"
IMAGE_PATH = f"/var/lib/libvirt/images/{IMAGE_NAME}"

SEED_IMAGE_PATH = f"/var/lib/libvirt/images/{VM_NAME}_seed.img"

CLOUD_INIT_CONFIGS_PATHS = {
    "user-data":"user-data.yaml",
    "meta-data":"meta-data.yaml",
    "network-config":"network-config.yaml"
}




if __name__ == "__main__":
    download_image(IMAGE_LINK,IMAGE_PATH,IMAGE_NAME)

    create_seed_img(CLOUD_INIT_CONFIGS_PATHS["user-data"],
                    CLOUD_INIT_CONFIGS_PATHS["meta-data"],
                    CLOUD_INIT_CONFIGS_PATHS["network-config"])
    resize_image(IMAGE_PATH, VM_SIZE)
    create_virtual_machine(VM_NAME, VM_RAM, VM_VCPUS, VM_NET, IMAGE_PATH)
