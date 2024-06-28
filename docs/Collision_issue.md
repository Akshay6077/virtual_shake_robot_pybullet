# README: Setting Contact Stiffness and Contact Damping in PyBullet

## Introduction

In physics simulations, particularly those involving rigid body dynamics, setting the correct contact parameters is crucial for realistic and stable interactions between objects. Two key parameters in this context are **contact stiffness** and **contact damping**. This document explains how to configure these parameters in PyBullet to achieve desired collision behaviors.

## Contact Parameters Overview

### Contact Stiffness
- **Definition**: Contact stiffness determines the resistance of an object to deformation upon collision. Higher values result in less deformation, mimicking harder materials.
- **Effect**: Affects the positional level of collision response. Higher stiffness reduces penetration depth but can lead to instability if set too high without proper damping.

### Contact Damping
- **Definition**: Contact damping controls the dissipation of kinetic energy during collisions. It acts like a damper in a spring-damper system.
- **Effect**: Affects the velocity level of collision response. Higher damping helps in reducing oscillations and stabilizing the simulation.

## Why Higher Mass Requires Higher Stiffness

Heavier objects exert more force upon collision due to their greater inertia. To prevent significant interpenetration and ensure realistic collision behavior, the contact stiffness must be increased proportionally. However, this also necessitates careful tuning of the damping to maintain stability.

## Example Script for Setting Contact Parameters

Here’s an example script demonstrating how to set up a simple simulation in PyBullet with specific contact stiffness and damping values:

```python
import pybullet as p
import pybullet_data
import time

# Connect to PyBullet
p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# Set up the environment
p.setGravity(0, 0, -9.81)
p.setRealTimeSimulation(1)

# Define the base of the shake table
base_collision_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=[25, 7, 1])
base_visual_shape = p.createVisualShape(p.GEOM_BOX, halfExtents=[25, 7, 1], rgbaColor=[1, 1, 0, 1])  # Yellow color

# Define the slide pad of the shake table
slide_pad_collision_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=[5, 5, 0.05])
slide_pad_visual_shape = p.createVisualShape(p.GEOM_BOX, halfExtents=[5, 5, 0.05], rgbaColor=[1, 0, 0, 1])  # Red color

# Create the base and slide pad as a single multi-body
base_position = [0, 0, 0.5]
base_orientation = p.getQuaternionFromEuler([0, 0, 0])

link_masses = [10000.0]
link_collision_shapes = [slide_pad_collision_shape]
link_visual_shapes = [slide_pad_visual_shape]
link_positions = [[0, 0, 1.025]]  # Adjusted to ensure the slide pad is above the base
link_orientations = [p.getQuaternionFromEuler([0, 0, 0])]
link_inertial_frame_positions = [[0, 0, 0]]
link_inertial_frame_orientations = [p.getQuaternionFromEuler([0, 0, 0])]
indices = [0]
joint_types = [p.JOINT_PRISMATIC]
joint_axis = [[1, 0, 0]]

base = p.createMultiBody(
    baseMass=0,
    baseCollisionShapeIndex=base_collision_shape,
    baseVisualShapeIndex=base_visual_shape,
    basePosition=base_position,
    baseOrientation=base_orientation,
    linkMasses=link_masses,
    linkCollisionShapeIndices=link_collision_shapes,
    linkVisualShapeIndices=link_visual_shapes,
    linkPositions=link_positions,
    linkOrientations=link_orientations,
    linkInertialFramePositions=link_inertial_frame_positions,
    linkInertialFrameOrientations=link_inertial_frame_orientations,
    linkParentIndices=indices,
    linkJointTypes=joint_types,
    linkJointAxis=joint_axis
)

# Change contact stiffness for the slide pad
p.changeDynamics(base, 0, contactStiffness=1e7, contactDamping=0.5)
p.changeDynamics(base, 1, contactStiffness=1e7, contactDamping=0.5)

# Load a box on top of the shake table
box_collision_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.5, 1, 1.5])
box_visual_shape = p.createVisualShape(p.GEOM_BOX, halfExtents=[0.5, 1, 1.5], rgbaColor=[0, 0, 1, 1])  # Blue color
box_position = [0, 0, 4]

box = p.createMultiBody(baseMass=5000.0, baseCollisionShapeIndex=box_collision_shape, baseVisualShapeIndex=box_visual_shape, basePosition=box_position)

# Change contact stiffness for the box
p.changeDynamics(box, -1, contactStiffness=1e7, contactDamping=0.5)

# Run the simulation
try:
    while True:
        p.stepSimulation()
        time.sleep(1./240.)
except KeyboardInterrupt:
    pass

# Disconnect from PyBullet
p.disconnect()

```
