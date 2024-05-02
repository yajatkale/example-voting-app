import boto3

# Getting response for 'ap-south-1' region and running instances
ec2 = boto3.client('ec2', region_name='ap-south-1')

response = ec2.describe_instances()
current_inst = ec2.describe_tags(Filters=[
        {
            'Name': 'tag:Name',
            'Values': ['Server']}
])
curr_inst_id = current_inst['Tags'][0]['ResourceId']                

# Getting Instance IDs
inst_id_running, inst_id_stopped = [], []
reservations = response['Reservations']
for reserve in reservations:
  instances = reserve['Instances']
  for inst in instances:
    print(inst['InstanceId'])
    if inst['State']['Name'] == 'running':
      inst_id_running.append(inst['InstanceId'])
    elif inst['State']['Name'] == 'stopped':
      inst_id_stopped.append(inst['InstanceId'])
   
# Starting stopped instances
for inst in inst_id_stopped:
  ec2.start_instances(InstanceIds=[inst])

# Stopping started instances
for inst in inst_id_running:
  if curr_inst_id not in inst:
    ec2.stop_instances(InstanceIds=[inst])

  
