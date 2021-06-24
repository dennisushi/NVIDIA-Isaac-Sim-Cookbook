'''
Steps:
Open Isaac Sim. 
Add camera object
Add Isaac > REB > Camera
In REB Camera object settings add the camera object as target
Eable depth and color
Set topic names to color_left and depth_left
Add Isaac Utils > Robot Engine Bridge > Create Application
Press Play
In terminal from SDK workspace : bazel run package/ping:ping_py
'''

from isaac import Application, Codelet
import argparse


class MyCodelet(Codelet):
  def start(self):
    self.tick_periodically(0.01)
    return
  def tick(self):
    return
  def stop(self):
    return

if __name__ == '__main__':
  # make node : app.add(name)
  # make component instance : node.add(name, ctype=app.registry.isaac.SOMETHING)
  # config param : component.config.parametername = X

  app = Application(name="ping_py")
  app.load_module('sight')
  app.load_module("viewers")
  app.load_module("superpixels")
  app.load_module("rgbd_processing")
  app.load("packages/ping/interface_subgraph.json", "simulation")
  

  simulation_interface = app.nodes['simulation.interface']
  sight_node = app.add('sight')

  #sim_in  = simulation_interface["input"]
  sim_out = simulation_interface["output"]
  #sim_sight = simulation_interface["sight"]
  
  #########################################################
  # Function helpers
  #########################################################
  
  def get_app_nodes(app):
    print(app.nodes._names)

  def get_node_elements(node):
    print(node.components._names)

  def add_WebSight_widget(sight_node, widget_name, widget_type, channel_name):
    widget = sight_node.add(app.registry.isaac.sight.SightWidget, name=widget_name)
    widget.config.type = widget_type
    widget.config.channels = [
      {"name": channel_name}
    ]
    return

  def add_camera_widget(sight_node, cam_viz_node, 
                        channel_component, channel_topic,
                        viz_topic_name=None,
                        viewer_type = 'image'):
    """
    Creates a Viewer object and connects to WebSight

    sight_node    - node object for WebSight
    cam_viz_node  - node object for camera visualizer where 
                    viewer components will be placed
    channel_component - channel within which the input comes
    channel_topic     - name of topic for camera stream
    viz_topic_name    - name of camera viewer
    viewer_type       - Type of viewer (image or depth)          
    """
    if viewer_type == "image":
      viewer_registry_type = app.registry.isaac.viewers.ImageViewer
      suffix_input = suffix_display = "image"
    elif viewer_type == "depth":
      viewer_registry_type = app.registry.isaac.viewers.DepthCameraViewer
      suffix_input = "depth"
      suffix_display = "Depth"
    else:
      raise ValueError()

    if viz_topic_name is None:
      viz_topic_name = channel_topic
      # TODO: Check that such a topic doesnt exist already
      
    cam_viz_node_component = cam_viz_node.add(viewer_registry_type, viz_topic_name)


    app.connect(channel_component, channel_topic, 
                cam_viz_node_component, suffix_input)
    app.connect(channel_component, channel_topic+"_intrinsics",
                cam_viz_node_component, "intrinsics")

    add_WebSight_widget(sight_node, 
                        viz_topic_name, "2d", 
                        cam_viz_node.name+"/"+viz_topic_name+"/"+suffix_display)
    return cam_viz_node_component

  #########################################################
  # ADD RGB AND DEPTH CAMERAS FROM ISAAC SIM TO WEBSIGHT
  #########################################################

  camera_visualization = app.add('camera_visualization')
  rgb_viz = add_camera_widget(sight_node, camera_visualization, sim_out, 
                              "color_left", 'ImageViewerLeft',
                              viewer_type = "image")
  depth_viz = add_camera_widget(sight_node, camera_visualization, sim_out, 
                                "depth_left", 'DepthViewerLeft',
                                viewer_type = "depth")
              

  depth_points_node = camera_visualization.add(
                          app.registry.isaac.rgbd_processing.DepthPoints,
                          "depth_points_node")
  app.connect(sim_out, 'depth_left',
              depth_points_node, 'depth')
  # output is depth_points_node > points


  depth_edges_node = camera_visualization.add(
                          app.registry.isaac.rgbd_processing.DepthPoints,
                          "depth_edges_node")
  app.connect(sim_out, 'depth_left',
              depth_edges_node, 'depth')

  depth_normals_node = camera_visualization.add(
                          app.registry.isaac.rgbd_processing.DepthPoints,
                          "depth_normals_node")
  app.connect(depth_points_node, 'points',
              depth_normals_node, 'points')
  app.connect(depth_edges_node, 'edges',
              depth_normals_node, 'points')
  # output is depth_normals_node > normals



  super_pixelizer = camera_visualization.add(
                          app.registry.isaac.superpixels.RgbdSuperpixels,
                          "super_pixelizer")

  app.connect(sim_out, 'color_left',
              super_pixelizer, 'color')
  app.connect(sim_out, 'depth_left',
              super_pixelizer, 'depth')
  app.connect(depth_points_node, 'points',
              super_pixelizer, 'points')
  app.connect(depth_edges_node, 'edges',
              super_pixelizer, 'edges')
  app.connect(depth_normals_node, 'normals',
              super_pixelizer, 'normals')
  # OUTPUTS ARE SURFLETS AND SUPERPIXELS


  # run indefinitely ()
  # run set time (DURATION)
  # run until node stops (NODE NAME)
  #app.run()
