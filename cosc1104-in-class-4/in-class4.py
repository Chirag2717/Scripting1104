import json

def get_valid_cpu_requirements():
    while True:
        try:
            min_cpu = int(input("Enter minimum required CPU cores (vCPUs): "))
            max_cpu = input("Enter maximum required CPU cores (vCPUs) (or press Enter to skip): ")
            max_cpu = int(max_cpu) if max_cpu else None
            return min_cpu, max_cpu
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

def get_valid_memory_requirements():
    while True:
        try:
            min_memory = float(input("Enter minimum required memory in GiB: "))
            max_memory = input("Enter maximum required memory in GiB (or press Enter to skip): ")
            max_memory = float(max_memory) if max_memory else None
            return min_memory, max_memory
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def load_ec2_instances(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def filter_ec2_instances(instances, min_cpu, max_cpu, min_memory, max_memory):
    filtered_instances = []
    for instance in instances:
        # Extract vCPU and memory values
        vcpu = int(instance['vcpu'].split()[0])  # Get the number before "vCPUs"
        memory = float(instance['memory'].split()[0])  # Get the number before "GiB"

        # Check if the instance meets the criteria
        if (vcpu >= min_cpu and (max_cpu is None or vcpu <= max_cpu) and
            memory >= min_memory and (max_memory is None or memory <= max_memory)):
            filtered_instances.append(instance)
    return filtered_instances

def print_filtered_instances(instances):
    if not instances:
        print("No instances found that meet the criteria.")
        return

    print("\nFiltered EC2 Instances:")
    for instance in instances:
        print(f"Name: {instance['name']}, vCPUs: {instance['vcpu']}, Memory: {instance['memory']}")

def main():
    # Get user input for CPU and memory requirements
    min_cpu, max_cpu = get_valid_cpu_requirements()
    min_memory, max_memory = get_valid_memory_requirements()

    # Load EC2 instances from JSON file
    instances = load_ec2_instances('ec2_instance_types.json')

    # Filter instances based on user requirements
    filtered_instances = filter_ec2_instances(instances, min_cpu, max_cpu, min_memory, max_memory)

    # Print the filtered instances
    print_filtered_instances(filtered_instances)

if __name__ == "__main__":
    main()