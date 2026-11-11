#!/usr/bin/env python3
# Builds config/nav2_params.yaml from the Nav2 defaults, patched for sophus
import os
import yaml

SRC = '/opt/ros/jazzy/share/nav2_bringup/params/nav2_params.yaml'
DST = os.path.expanduser('~/jazzy_ws/src/my_robot_description/config/nav2_params.yaml')

# ---- EDIT THESE ----
# Footprint in base_link [x, y]. Your URDF has wheels at y = +/-1.07 m, so this is ~2.3 m wide.
# Measure the real extent in RViz and adjust.
FOOTPRINT = "[[1.2, 1.15], [1.2, -1.15], [-0.6, -1.15], [-0.6, 1.15]]"
INFLATION = 0.35
MAX_V = 0.5          # m/s
MAX_W = 0.5          # rad/s (diff-drive wheel accel limit is low, keep modest)
INIT_POSE = dict(x=0.0, y=0.0, z=0.0, yaw=0.0)   # must match the spawn pose used when mapping
LIDAR_MAX = 8.0
# --------------------

with open(SRC) as f:
    cfg = yaml.safe_load(f)

def walk(node):
    """use_sim_time everywhere, base_footprint -> base_link everywhere."""
    if isinstance(node, dict):
        for k, v in list(node.items()):
            if k == 'use_sim_time':
                node[k] = True
            elif v == 'base_footprint':
                node[k] = 'base_link'
            else:
                walk(v)
    elif isinstance(node, list):
        for i in node:
            walk(i)

walk(cfg)

def P(name):
    return cfg[name]['ros__parameters']

# AMCL
a = P('amcl')
a['robot_model_type'] = 'nav2_amcl::DifferentialMotionModel'
a['scan_topic'] = 'scan'
a['laser_max_range'] = LIDAR_MAX
a['set_initial_pose'] = True
a['initial_pose'] = INIT_POSE

# Costmaps
for name in ('local_costmap', 'global_costmap'):
    c = cfg[name][name]['ros__parameters']
    c.pop('robot_radius', None)
    c['footprint'] = FOOTPRINT
    c['inflation_layer']['inflation_radius'] = INFLATION
    c['inflation_layer']['cost_scaling_factor'] = 3.0
    for layer in ('voxel_layer', 'obstacle_layer'):
        if layer in c and 'scan' in c[layer]:
            c[layer]['scan']['topic'] = '/scan'
            c[layer]['scan']['obstacle_max_range'] = LIDAR_MAX - 0.5
            c[layer]['scan']['raytrace_max_range'] = LIDAR_MAX

# Controller speed limits
fp = P('controller_server').get('FollowPath', {})
for k, v in dict(max_vel_x=MAX_V, max_speed_xy=MAX_V, max_vel_theta=MAX_W).items():
    if k in fp:
        fp[k] = v

# Velocity smoother
vs = P('velocity_smoother')
vs['max_velocity'] = [MAX_V, 0.0, MAX_W]
vs['min_velocity'] = [-MAX_V, 0.0, -MAX_W]
vs['max_accel'] = [0.5, 0.0, 0.5]
vs['max_decel'] = [-0.5, 0.0, -0.5]
vs['odom_topic'] = '/odom'

P('bt_navigator')['odom_topic'] = '/odom'

with open(DST, 'w') as f:
    yaml.safe_dump(cfg, f, sort_keys=False)
print('wrote', DST)