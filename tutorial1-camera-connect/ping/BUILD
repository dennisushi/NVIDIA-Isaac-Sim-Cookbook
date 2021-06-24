
load("//bzl:module.bzl", "isaac_app", "isaac_cc_module", "isaac_subgraph")
load("//bzl:py.bzl", "isaac_jupyter_app", "isaac_py_app")

"""
navsim - has the scenario manager
engine_tcp_udp - tcp communciation between ISAAC SIM and App 


utils - not sure
"""

isaac_subgraph(
    name = "interface_subgraph",
    modules = [
               "engine_tcp_udp",
               "sight",
               "navsim",
               "viewers"
    ],
    subgraph = "interface_subgraph.json",
    visibility = ["//visibility:public"],
)

isaac_py_app(
    name = "ping_py",
    srcs = ["ping_py.py"],
    data = [
        "//packages:py_init",
        ":interface_subgraph"
    ],
    modules = [
        "navsim",
        "sight",
        "viewers",
        "superpixels",
        "rgbd_processing",
        "perception",
        "cask",
    ],
    deps = [
        "//packages/pyalice",
    ],
)
