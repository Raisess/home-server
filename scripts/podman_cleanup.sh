#! /usr/bin/env sh

echo "Cleaning unused volumes and images..."

podman volume prune
podman image prune --all

echo "Done!"
