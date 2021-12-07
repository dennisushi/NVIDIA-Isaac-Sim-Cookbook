# NVIDIA IsaacSim Cookbook
NVIDIA Isaac Sim+SDK Cookbook: Recipes for NVIDIA ISAAC from the 'ingredients' to the arranged 'dish'. The original instructions and tutorials are convoluted but hopefully this guide helps you. Note, this guide was designed for Ubuntu 18, ISAAC 2021-1. The order of the sections in this guide are purposefully made to navigate your experience toward understanding the software suite. 

What this repo contains:
- [Installation](#Installation)
- [Making new Isaac SDK apps and nodelets](#Making-new-Isaac-SDK-apps-and-nodelets)
- [Connecting SDK apps to Sim](#Connecting-SDK-apps-to-Sim)
- [Making new Isaac Extensions](#Making-new-Isaac-Extensions)

What this repo doesn't contain yet:
- Everything else.

# Installation
## Sim
1) Get the Omniverse Launcher from [here](NVIDIA Isaac Sim+SDK Cookbook). You should get the Linux AppImage file.
2) Make the file executable and run it.
3) From the Omniverse Launcher, search for ISAAC Sim and download it.
4) Launch. 
5) From the same website, search for ISAAC Sim and download the latest version of Assets. These will be useful for the tutorials.
4) `cd <SIM> && ./python.sh python_samples/syntheticdata/basic/visualize_groundtruth.py`. This will create a synthetic data image in `<sdk>` that validates that cameras are correctly operating.

## SDK
1) Similarly, download the [SDK](https://developer.nvidia.com/isaac-sdk)
2) `cd <sdk>/engine && install_dependencies.sh` 
3) `cd <sdk>` and try `bazel build \\apps\samples\stereo_dummy`. If this runs okay you've got everything working correctly! You can check at localhost:3000 for the output Sight.

# Startup Tips 

## Useful aliases

Useful aliases to add to your `.bash_aliases`:

```
ISAAC_SOURCE_LOC='PATH TO YOUR ISAAC SIM'
alias isaac_start='cd $ISAAC_SOURCE_LOC && ./isaac-sim.sh --/renderer/activeGpu=1'

alias isaac_python='export EXP_PATH=$ISAAC_SOURCE_LOC/apps &&
					source $ISAAC_SOURCE_LOC/setup_python_env.sh && 
					$ISAAC_SOURCE_LOC/kit/python/bin/python3'
```

With these, you can call `isaac_python` on any python file to run it with all the needed libraries.

## Useful localhosts

- NVIDIA Sight [localhost:3000](localhost:3000)
- Upload files to Omniverse [localhost:8080](localhost:8080)
- Running apps and services [localhost:3080](localhost:3080)

## Playing with Scripting

In Isaac Sim, add a Franka robot from `Create > Isaac > Robots >From Library > Franka`. Then click `Window > Script Editor` and dock it somewhere. Try the premade snippets or your own code in the scripting editor. Finally, click on Run. No building or reloading needed! 

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

# Connecting SDK apps to Sim

The most useful tutorial for this if found [here](https://docs.nvidia.com/isaac/isaac/doc/manipulation/samples.html#manipulation-sample-applications).

You need to launch Sim, add the required asset (ur10_basic.usd), add `Isaac Utils > Robot Engine Bridge > Create Application`, press Play. Then run the tutorial as instructed. Useful takeaways from the code: 

- Manipulation components use CompositeProto messages to communicate
- The stage.usd controls are enabled by Robot Engine Bridge (REB) objects.

## REB Objects
If you want to create a scene whose camera you can use in your apps, you need to add an REB and set its cameraPrim target to the camera object. Then select the options for depth/rgb/etc with output component "output" and channel by your choice. A simple script showing these connections is shown in this repository, dubbed `tutorial1`. Hereon, [this](https://docs.nvidia.com/isaac/isaac/doc/doc/component_api.html) documentation will be your best friend. Check it for references to what the input and output messages are.

[TODO] Try isaac sim with -vulkan -isaac_sim_config_json="/PATH/TO/paths.json"

## Using ROS Bridge

In Isaac SIM, add a Ros Bridge object from `Create > Isaac > ROS >`, specify desired configuration and press play. If, for example, you added a camera and enabled the depth and color information, and connected it to a camera object, you should be able to view the images from `rosrun image_view image_view image:=TOPIC NAME`.

# Making new Isaac Extensions

- 1) Navigate to `<path>\Kit\apps\Isaac-Sim\exts`. For me, the path is located in Documents.
- 2) Add a symbolic link shortcut pointing to your custom extension folder.
- 3) In the extension folder, you should add a folder `config` containing `extension.toml`. This file should list your dependencies and custom scripts:
	```bash
	display_name = "Custom Extension Name"

	[dependencies]
	"omni.isaac.dynamic_control" = {}
	"omni.isaac.range_sensor" = {}
	"omni.syntheticdata" = {}

	[[python.module]]
	name = "DIR1.DIR2.DIR3" # Where DIR names correspond to folder structure in the extension folder
				# with extension.py found in the last folder, or the last DIR corresponding 
				# to a DIR3.py which holds the extension

	[[native.plugin]]
	recursive = false
	```
- 4) The extension file should declare a class ```python class Extension(omni.ext.IExt)```

# Interact with ML Models
[TODO]

# Simulate sensors with code
[TODO]

# Simulate robots
[TODO]
