cmake_minimum_required(VERSION 3.8)
project(demo_pkg)

# Required for ROS2 packages
find_package(ament_cmake REQUIRED)

# Python testing support
find_package(ament_cmake_pytest REQUIRED)

# Only run tests when building with testing enabled
if(BUILD_TESTING)

  # Linting (optional but recommended in ROS2 world)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()

  # Run pytest tests
  ament_add_pytest_test(test_publisher test/pytest/test_publisher.py
    TIMEOUT 60
  )

endif()

ament_package()