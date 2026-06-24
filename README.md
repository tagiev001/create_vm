# Описание
Скрипт для создания виртуальных машин на базе QEMU/KVM

# Зависимости
Помимо настроенного гипервизора(libvirtd демон) необходимы следующие пакеты:

- qemu-utils
- cloud-image-utils
- virtinst

```
#Ubuntu/Debian
apt update && apt install -y qemu-utils cloud-image-utils virtinst
```
# Первый запуск
1. Загрузить скрипт
```
git clone https://github.com/tagiev001/create_vm.git
```

2. Подготовить соотвествующие user-data.yaml, meta-data.yaml, network-config.yaml,
   в network-config.yaml указать интерфейс в зависимости от образа, указать в **CLOUD_INIT_CONFIG_PATHS** пути до соответствующих файлов

3. Указать параметры ВМ в create_vm.py

| Параметр | Описание | Тип |
|-|-|-|
| VM_NAME| Имя вм в virsh | str |
| VM_RAM | Кол-во озу вм, гб | int |
| VM_VCPUS | Кол-во vCPU | int |
| VN_NET | Сеть для вм* | str |
| VM_SIZE | Размер ВД, гб | int |
| IMAGE_LINK | Ссылка на generic-cloud образ | str |
| IMAGE_PATH | Место хранения ВМ | str |

*Сеть для VM_NET должна быть определена до скрипта(virsh net-list --all)

4. В **EXEC_VIRT_INSTALL_CMD** указать соотвествующий дистрибутив для параметра --os-variant**

**Проверить список доступных значений можно с помощью `virt-install --osinfo list`

5. Запустить скрипт
```
./create_vm.py
```

6. Подождать, пока cloud-init завершит настройку



# Скрипт проверялся на 
| Дистрибутив | ссылка на образ | Сетевой интерфейс(для network-config) |
| -|-|-|
| Debian13 | https://cloud.debian.org/images/cloud/trixie/20250806-2196/debian-13-genericcloud-amd64-20250806-2196.qcow2 | enp1s0 |
| Almalinux8 | https://repo.almalinux.org/almalinux/8/cloud/x86_64/images/AlmaLinux-8-GenericCloud-ext4-8.10-20260518.x86_64.qcow2 | eth0 |
