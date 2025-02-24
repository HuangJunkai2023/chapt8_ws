import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # 包名和URDF文件名
    package_name = 'fishbot_description'
    urdf_name = "fishbot_base.urdf"

    # 获取包的共享目录路径
    pkg_share = get_package_share_directory(package_name)
    urdf_model_path = os.path.join(pkg_share, 'urdf', urdf_name)

    # 读取URDF文件内容
    with open(urdf_model_path, 'r') as infp:
        robot_description = infp.read()

    # 配置 GAZEBO_MODEL_PATH 环境变量
    pkg_prefix = get_package_share_directory(package_name)
    if 'GAZEBO_MODEL_PATH' in os.environ:
        os.environ['GAZEBO_MODEL_PATH'] += os.pathsep + pkg_prefix
    else:
        os.environ['GAZEBO_MODEL_PATH'] = pkg_prefix

    # 配置 robot_state_publisher 节点
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description}]
    )

    # 配置 joint_state_publisher_gui 节点
    joint_state_publisher_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        output='screen'
    )

    # 配置 rviz2 节点
    rviz2_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
    )

    # 将节点添加到启动描述中
    ld = LaunchDescription()
    ld.add_action(robot_state_publisher_node)
    ld.add_action(joint_state_publisher_node)
    ld.add_action(rviz2_node)

    return ld