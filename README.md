# NVIDIA-Isaac-Sim-SDK-Cookbook
NVIDIA Isaac Sim+SDK Cookbook: Recipes for NVIDIA ISAAC from the 'ingredients' to the arranged 'dish'. The original instructions and tutorials are convoluted but hopefully this guide helps you. Note, this guide was designed for Ubuntu 18, ISAAC 2021-1. 

What this repo contains:
- [Installation](#Installation)
- [Making new Isaac SDK apps and nodelets](#Making-new-Isaac-SDK-apps-and-nodelets)

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
4) [Optional] `cd <sdk> && ./python.sh python_samples/syntheticdata/basic/visualize_groundtruth.py`. This will create a synthetic data image in `<sdk>` that validates that cameras are correctly operating.

# Making new Isaac SDK apps and nodelets

Full guide [here](https://docs.nvidia.com/isaac/archive/2019.1/apps/tutorials/doc/ping.html#cplusplus-ping)

1) Make package

```bash
cd <ISAAC SDK>/packages
mkdir <NAME OF PACKAGE>
touch <NAME>.app.json
touch BUILD
```

2) In json, add:

```bash
{
  "name": "ping",
  "graph": {
    "nodes": [
      {
        "name": "ping",
        "components": []
      }
    ],
    "edges": []
  }
}
```
This adds a new node with name ping to the app with name ping. 

3) In BUILD add dependencies to load and start:

```bash
load("//bzl:module.bzl", "isaac_app", "isaac_cc_module")

isaac_app(
     name = "ping"
)

isaac_cc_module(
  name = "ping_components",
  srcs = ["ping.cpp"],
  hdrs = ["ping.hpp"],
)
```

This adds ISAAC, and loads headers and cpp files.

4) Make `Ping.hpp` and `Ping.cpp` files in the same directorty with the following content:

```cpp
#include "Ping.hpp"
void Ping::start() {
  tickPeriodically();
}
void Ping::tick() {
  LOG_INFO("ping");
}

void Ping::stop() {}
```

```cpp
#pragma once
#include "engine/alice/alice_codelet.hpp"
class Ping : public isaac::alice::Codelet {
 public:
  void start() override;
  void tick() override;
  void stop() override;
};
ISAAC_ALICE_REGISTER_CODELET(Ping);
```

These define a simple Codelet with the three basic Codelet functions - start, tick, stop.

5) Then, change configurations for BUILD and json as:

```bash
isaac_app(
     name = "ping"
    modules = ["//packages/ping:ping_components"]
)
```
```bash
{
  "name": "ping",
  "modules": [
    "ping:ping_components"
  ],
  "graph": {
    ...
  }
}
```
These link BUILD and Isaac App to the isaac_cc_module added earlier.

Finally,

```bash
{
  "name": "ping",
  ...
  "config": {
    "ping" : { 
      "ping" : {
        "tick_period" : "1Hz"
      }
    }
  }
}
```

# Interact with ML Models
[TODO]

# Simulate sensors with code
[TODO]

# Simulate robots
[TODO]
