#! /bin/env python3

import json
import os
import subprocess
import sys

class BlockDevice:
  def __init__(self, name: str, size: str):
    self.__name = name
    self.__size = float(size.replace("G", ""))

  def name(self) -> str:
    return self.__name

  def size(self) -> float:
    return self.__size

  def mount(self, target: str) -> None:
    path = f"/media/{target}"
    if not os.path.exists(path):
      os.makedirs(path)

    os.system(f"mount /dev/{self.__name} {path}")


if __name__ == "__main__":
  args = sys.argv[1:]
  if len(args) < 1 or not args[0].endswith(".json"):
    raise Exception("No usb schema provided")

  with open(args[0]) as file:
    usb_schema = json.load(file)

    blocks = json.loads(subprocess.check_output(["lsblk", "--json"])).get("blockdevices")
    if not blocks:
      raise Exception("No devices found")

    blocks = [BlockDevice(block.get("name"), block.get("size")) for block in blocks]
    for block in blocks:
      mount_target = usb_schema.get(str(block.size()))
      if mount_target:
        block.mount(mount_target)
        print(f"Mounted {block.name()} in {mount_target}")
