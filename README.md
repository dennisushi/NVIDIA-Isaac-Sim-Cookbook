# NVIDIA-Isaac-Sim-SDK-Cookbook
NVIDIA Isaac Sim+SDK Cookbook: Recipes for NVIDIA ISAAC from the 'ingredients' to the arranged 'dish'. The original instructions and tutorials are convoluted but hopefully this guide helps you. Note, this guide was designed for Ubuntu 18, ISAAC 2021-1. 

What this repo contains:
- [Installation](#Installation)

What this repo doesn't contain yet:
- Everything else.

# Installation
## Sim
1) Get the Omniverse Launcher from [here](NVIDIA Isaac Sim+SDK Cookbook). You should get the Linux AppImage file.
2) Make the file executable and run it.
3) From the Omniverse Launcher, search for ISAAC Sim and download it.
4) Launch. 
5) From the same website, search for ISAAC Sim and download the latest version of Assets. These will be useful for the tutorials.

## SDK
1) Similarly, download the [SDK](https://developer.nvidia.com/isaac-sdk)
2) `cd <sdk>/engine && install_dependencies.sh` 
3) `cd <sdk>` and try `bazel build \\apps\samples\stereo_dummy`. If this runs okay you've got everything working correctly! You can check at localhost:3000 for the output Sight.

# Making new SDK apps
[TODO]

# Interact with ML Models
[TODO]

# Simulate sensors with code
[TODO]

# Simulate robots
[TODO]
