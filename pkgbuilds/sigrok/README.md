# PKGBUILDS for sigrok
**sigrok-fw** is a patched version of [sigrok-firmware-fx2lawf](https://aur.archlinux.org/packages/sigrok-firmware-fx2lafw/)
from the *Arch User Repository*.
The original PKGBUILD declare sdcc as a dependency, but it is only needed to build the package
so it is now declared as makedependeny only.

**sigrok-udev-rules** fetches the latest udev rules for libsigrok from git and patches the group from
*plugdev* to *uucp*. After that the rules will be installed in */usr/lib/udev/rules.d/*
