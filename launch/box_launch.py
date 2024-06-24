#!/usr/bin/env python3

from launch import LaunchDescription
from launch_ros.actions import Node
import os

def generate_launch_description():
    
    ros2_ws = os.getenv('ROS2_WS', default=os.path.expanduser('~/ros2_ws'))

    
    config_directory = os.path.join(ros2_ws, 'virtual_shake_robot_pybullet/config')

    physics_engine_parameters_path = os.path.join(config_directory, 'physics_engine_parameters.yaml')
    physics_parameters_path = os.path.join(config_directory, 'physics_parameters.yaml')
    vsr_structure_path = os.path.join(config_directory, 'vsr_structure_box.yaml')
    pbr_structure_path = os.path.join(config_directory, 'pbr_box.yaml')
    pbr_mesh_structure_path = os.path.join(config_directory, 'pbr_mesh.yaml')

    simulation_node = Node(
        package='virtual_shake_robot_pybullet',  
        executable='simulation_node.py',  
        name='simulation_node', 
        output='screen',
        parameters=[
            physics_engine_parameters_path,
            physics_parameters_path,
            vsr_structure_path,
            pbr_structure_path,
            pbr_mesh_structure_path
        ]
    )

    control_node = Node(
        package='virtual_shake_robot_pybullet',  
        executable='control_node.py',  
        name='control_node',
        output='screen'
    )

    return LaunchDescription([
        simulation_node,
        control_node
    ])
