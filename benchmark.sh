#!/bin/bash

# Define the values for the first OS parameter (vm.swappiness) - default included
os_param1_values=(20 60 80)

# Define the values for the eleventh OS parameter (vm.dirty_ratio) - default included
os_param2_values=(0 20 40)

# Define the values for the twelfth OS parameter (vm.dirty_background_ratio) - default included
os_param3_values=(10 20 60)

# Define the values for the file descriptor limit
file_descriptor_values=(4096 1024)

# Define the values for vm.nr_overcommit_hugepages
hugepages_values=(1 0)

# Store the original default values
original_swappiness=60
original_dirty_ratio=20
original_dirty_background_ratio=10
original_file_descriptor_limit=1024
original_hugepages_value=0

x=0

# Loop through each permutation of the parameters
for os_param1 in "${os_param1_values[@]}"; do
    for os_param2 in "${os_param2_values[@]}"; do
        for os_param3 in "${os_param3_values[@]}"; do
            for file_descriptor_limit in "${file_descriptor_values[@]}"; do
                for hugepages_value in "${hugepages_values[@]}"; do
            
                    # Run the command to set vm.swappiness
                    echo "Setting vm.swappiness=$os_param1"
                    sudo sysctl vm.swappiness="$os_param1"

                    # Run the command to set vm.dirty_ratio
                    echo "Setting vm.dirty_ratio=$os_param2"
                    sudo sysctl -w vm.dirty_ratio="$os_param2"

                    # Run the command to set vm.dirty_background_ratio
                    echo "Setting vm.dirty_background_ratio=$os_param3"
                    sudo sysctl -w vm.dirty_background_ratio="$os_param3"

                    # Display the current values of all parameters
                    echo "Current value of vm.swappiness:"
                    sudo sysctl vm.swappiness

                    echo "Current value of vm.dirty_ratio:"
                    sudo sysctl vm.dirty_ratio

                    echo "Current value of vm.dirty_background_ratio:"
                    sudo sysctl vm.dirty_background_ratio

                    # Set the file descriptor limit
                    echo "Setting file descriptor limit to $file_descriptor_limit"
                    ulimit -n "$file_descriptor_limit"

                    echo "Current file descriptor limit:"
                    ulimit -n

                    # Set vm.nr_overcommit_hugepages
                    echo "Setting vm.nr_overcommit_hugepages to $hugepages_value"
                    sudo sysctl vm.nr_overcommit_hugepages="$hugepages_value"

                    echo "Current value of vm.nr_overcommit_hugepages:"
                    sudo sysctl vm.nr_overcommit_hugepages

                    x=$((x + 1))

                    echo $x

                    a=1
                    b=2
                    c=3

                    output_filename="${os_param1}_${os_param2}_${os_param3}_${file_descriptor_limit}_${hugepages_value}_${a}.tsv"
                    echo "Running benchmarking script..."
                    ./run.simple.bash "$output_filename"

                    output_filename="${os_param1}_${os_param2}_${os_param3}_${file_descriptor_limit}_${hugepages_value}_${b}.tsv"
                    echo "Running benchmarking script..."
                    ./run.simple.bash "$output_filename"

                    output_filename="${os_param1}_${os_param2}_${os_param3}_${file_descriptor_limit}_${hugepages_value}_${c}.tsv"
                    echo "Running benchmarking script..."
                    ./run.simple.bash "$output_filename"

                    # Revert back to the original default values
                    echo "Reverting to default values..."
                    sudo sysctl vm.swappiness="$original_swappiness"
                    sudo sysctl -w vm.dirty_ratio="$original_dirty_ratio"
                    sudo sysctl -w vm.dirty_background_ratio="$original_dirty_background_ratio"
                    ulimit -n "$original_file_descriptor_limit"
                    sudo sysctl vm.nr_overcommit_hugepages="$original_hugepages_value"

                    echo

                done
            done
        done
    done
done
