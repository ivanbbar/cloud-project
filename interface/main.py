import json
import os
import time
import boto3
from dotenv import load_dotenv  

def instances(session, ec2, map_variables):
    while True:
        os.system("cls")

        print("                                      [Instance Actions]                                      ")
        print("                                  [type the code of the action]                               ")
        print("   [c] Create Instance\t     [l] List Instances\t      [d] Delete Instance\t     [b] Back\t   ")
        print("\n\n")

        inst_input = input("Enter your action: ")
        inst_input = str(inst_input)

        if inst_input in ["c", "l", "d", "b"]:

            if inst_input == "c":
                os.system("cls")
                print("                                    [Instances Creation]                                     ")
                print('\n\n')
                print("                      how many t2.nano instences will be created?  [max 5]                   ")
                print('\n\n')

                n_instances_nano = input("Enter value (<= 5): ")
                n_instances_nano = limit_values(5, n_instances_nano)

                print('\n\n')
                print("                     how many t2.micro instences will be created?  [max 5]                   ")
                print('\n\n')

                n_instances_micro = input("Enter value (<= 5): ")
                n_instances_micro = limit_values(5, n_instances_micro)

                print('\n\n')

                if (n_instances_nano != 0) or (n_instances_micro != 0):
                    os.system("cls")
                    print("                                  [Instances Names]                                      ")
                    print('\n\n')
                    for i in range(1, n_instances_nano+1):
                        print("t2.nano Instance Name {}:\n".format(i))    
                        name_nano = input("Enter name: ")

                        instance = {"instance_name": [name_nano], "instance_type": "t2.nano"}
                        map_variables["configuration"].append(instance)
                        
                    print('\n\n')
                    for i in range(1, n_instances_micro+1):
                        print("t2.micro Instance Name {}:\n".format(i))    
                        name_micro = input("Enter name: ")
                        
                        instance = {"instance_name": [name_micro], "instance_type": "t2.micro"}
                        map_variables["configuration"].append(instance)
                    
                    dump_json(map_variables)
                    print("                             Creating Instance....                               ")
                    print('\n\n')
                    execute_action()

            elif inst_input == "l":
                os.system("cls")
                print("                                  [Instances List]                                   ")
                print('\n\n')
                i = 0
                for instance in ec2.instances.all():
                    if instance.state['Name'] != 'terminated':
                        print(f"Instance {i}")
                        print("{} -> name:{}".format(i,instance.tags[0]["Value"]))
                        print("{} -> type:{}".format(i,instance.instance_type))
                        print("{} -> region:{}".format(i,instance.placement['AvailabilityZone']))
                        print("{} -> status:{}".format(i,instance.state['Name']))
                        print('\n\n')
                        i += 1
                i-=1
                get_back()

            elif inst_input == "d":
                os.system("cls")
                print("                                 [Delete Instances]                                  ")
                print('\n\n')
                i = 0
                for instance in (map_variables["configuration"]):
                    print("{} -> name:{} , type: {}".format(i, instance["instance_name"][0], instance["instance_type"]))
                    print('\n\n')
                    i += 1

                if i == 0:
                    get_back()

                else:
                    i-=1
                    print("                     Type which Instance you want to delete                     ")
                    
                    delete_instance = input("Enter value: ")
                    delete_instance = limit_values(i, delete_instance)
                    map_variables['configuration'].pop(delete_instance)

                    dump_json(map_variables)
                    print("                             Deleting Instance....                               ")
                    print('\n\n')

                    execute_action()
            else:
                first_page(session, map_variables)

        else:
            print("Invalid!")
            time.sleep(3)
            instances(session, ec2, map_variables)

def sg(session, ec2, client, map_variables):
    while True:
        os.system("cls")


        print("                                    [Security Groups Actions]                                 ")
        print("                                  [type the code of the action]                               ")
        print("[c] Create SG\t  [l] List SGs\t  [d] Delete SG\t  [a] Associate SG with Instance\t  [b] Back\t")
        print("\n\n")

        sg_input = input("Enter your action: ")
        sg_input = str(sg_input)

        if sg_input in ["c", "l", "d", "a", "b"]:

            if sg_input == "c":
                os.system("cls")
                print("                                       [SGs Creation]                                        ")
                print('\n\n')
                print("                           how many groups will be created?  [max 5]                         ")
                print('\n\n')
                n_groups = input("Enter value: ")
                n_groups = limit_values(5, n_groups)

                print('\n\n')

                if n_groups != 0:
                    for i in range(1, n_groups+1):
                        os.system("cls")
                        print("                             [SGs configuration]                                     ")
                        print('\n\n')
                        print("Group Name {}:\n".format(i))    
                        conflict = True
                        
                        while conflict:
                            conflict = False
                            name = "Group Name {}:\n".format(i)
                            for secgru in map_variables['sgs']:
                                if secgru["name"] == name:
                                    conflict = True
                                    print("Group Already Exists\n")

                        print("Group Description {}:\n".format(i))    
                        descricao = input("Enter Group Description: ")

                        ingress = [{"from_port":443, "to_port": 443, "protocol": "tcp", "cidr_blocks": ["10.0.0.0/16"]}]
                        egress = [{"from_port":443, "to_port": 443, "protocol": "tcp", "cidr_blocks": ["0.0.0.0/0"]}]

                        group = {"name": name, "description": descricao, "ingress": ingress, "egress": egress}
                        map_variables["sgs"].append(group)

                    dump_json(map_variables)

                    print("                                  Creating SG....                                     ")
                    print('\n\n')
                    execute_action()

            elif sg_input == "l":
                os.system("cls")
                print("                                       [SGs List]                                         ")
                print('\n\n')
                i = 0
                for group in (map_variables["sgs"]):
                    print(f"SG {i}")
                    print("{} -> name:{}".format(i, group["name"]))
                    print("{} -> descrição:{}".format(i, group["description"]))
                    print("{} -> ingress:{}".format(i, group["ingress"]))
                    print("{} -> egress:{}".format(i, group["egress"]))
                    print('\n\n')
                    i += 1
                i-=1
                
                get_back()

            elif sg_input == "d":
                os.system("cls")
                print("                                        [Delete SGs]                                     ")
                print('\n\n')
                i = 0
                for group in (map_variables["sgs"]):
                    print("{} -> name:{}".format(i, group["name"]))
                    print('\n\n')
                    i += 1
                
                if i == 0:
                    get_back()
                else:
                    i-=1
                    print("                            Type which SG you want to delete                        ")

                    delete_group = input("Enter value: ")
                    delete_group = limit_values(i, delete_group)

                    response = client.describe_security_groups(
                        Filters=[
                            dict(Name='group-name', Values=[map_variables['sgs'][delete_group]["name"]])
                        ]
                    )
                    new_list = [group for group in map_variables['association'] if group['GroupId'] != response['SecurityGroups'][0]['GroupId']]
                    map_variables['association'] = new_list
                    map_variables['sgs'].pop(delete_group)

                    dump_json(map_variables)
                    print("                                  Deleting SG....                                     ")
                    print('\n\n')
                    execute_action()

            elif sg_input == "a":
                os.system("cls")
                print("                                     [Associate SGs]                                     ")
                print('\n\n')
                print("......................................All Instances......................................")

                instances_list = []
                i = 0
                for instance in ec2.instances.all():
                    if instance.state['Name'] != 'terminated':
                        print("{} -> name:{}".format(i,instance.tags[0]["Value"]))
                        print("{} -> type:{}".format(i,instance.instance_type))
                        instances_list.append(instance.network_interfaces[0].id)
                        print('\n\n')
                        i += 1
                                
                print(".........................................All SGs.........................................")

                sgs_names = []
                j = 0
                for group in (map_variables["sgs"]):
                    print("{} -> name:{}".format(j, group["name"]))
                    sgs_names.append(group["name"])
                    j += 1
                    print('\n\n')
                print('\n\n')

                if i == 0 or j == 0:
                    get_back()
                else:
                    i -= 1
                    j -= 1

                    print("                        Type which Instance you want to associate                    ")
                    instance_idx = input("Enter value: ")
                    instance_idx = limit_values(i, instance_idx)

                    print("                          Type which Group you want to associate                     ")
                    group_idx = input("Enter value: ")
                    group_idx = limit_values(j, group_idx)

                    response = client.describe_security_groups(
                        Filters=[
                            dict(Name='group-name', Values=[sgs_names[group_idx]])
                        ]
                    )

                    name_association = instances_list[instance_idx] +"_"+ response['SecurityGroups'][0]['GroupId']

                    conflict2 = False
                    for assoc in map_variables["association"]:
                        if assoc["name"] == name_association:
                            print("Invalid! Association Already Exists")
                            conflict2 = True
                            time.sleep(5)

                    if not conflict2:
                        association = {"name": name_association, "instance_id":instances_list[instance_idx],"security_group_id":response['SecurityGroups'][0]['GroupId']}
                        map_variables["association"].append(association)

                        dump_json(map_variables)

                        print("                             Creating Association....                                 ")
                        print('\n\n')
                        execute_action()

            else:
                first_page(session, map_variables)

        else:
            print("Invalid!")
            time.sleep(3)
            sg(session, ec2, client, map_variables)
        
def users(session, map_variables):
    while True:
        os.system("cls")

        print("                                       [Users Actions]                                       ")
        print("                                 [type the code of the action]                               ")
        print("     [c] Create Users\t       [l] List Users\t        [d] Delete User\t       [b] Back\t     ")
        print("\n\n")

        user_input = input("Enter your action: ")
        user_input = str(user_input)

        if user_input in ["c", "l", "d", "b"]:

            if user_input == "c":
                os.system("cls")
                print("                                       [Users Creation]                                      ")
                print('\n\n')
                print("                           how many users will be created?  [max 5]                          ")
                print('\n\n')
                n_users = input("Enter value: ")
                n_users = limit_values(5, n_users)

                print('\n\n')

                if n_users != 0:
                    os.system("cls")
                    print("                                      [Users Names]                                      ")
                    print('\n\n')
                    for i in range(1, n_users+1):
                        print("username {}:\n".format(i))    

                        conflict = True
                        while conflict:
                            conflict = False
                            name = input("username {}:\n".format(i))
                            for user in map_variables['users']:
                                if user["name"] == name:
                                    conflict = True
                                    print("User already exists\n")

                        user = {"name": name}
                        map_variables["users"].append(user)

                    dump_json(map_variables)
                        
                    print("                                  Creating Users....                                     ")
                    print('\n\n')
                    execute_action()

            elif user_input == "l":
                os.system("cls")
                print("                                         [List Users]                                       ")
                print('\n\n')
                i = 0
                for user in (map_variables["users"]):
                    print("{} -> name:{}".format(i, user["name"]))
                    i += 1
                    print('\n')

                i-=1
                
                get_back()

            elif user_input == "d":
                os.system("cls")
                print("                                      [Delete Users]                                      ")
                print('\n\n')
                i = 0
                for user in (map_variables["users"]):
                    print("{} -> name:{}".format(i, user["name"]))
                    i += 1
                    print('\n')
                
                if i == 0:
                    get_back()
                else:
                    i-=1
                    print("                            Type which user you want to delete                        ")
                    delete_user = input("Enter value: ")
                    delete_user = limit_values(5, delete_user)

                    map_variables['users'].pop(delete_user)
                    dump_json(map_variables)

                    print("                                   Deleting User....                                 ")
                    print('\n\n')
                    execute_action()
            
            else:
                first_page(session, map_variables)

        else:
            print("Invalid!")
            time.sleep(3)
            users(session, map_variables)

def main():

    load_dotenv()   
    ACCESS_KEY = os.environ.get("ACCESS_KEY")
    SECRET_KEY = os.environ.get("SECRET_KEY")

    session = boto3.Session(
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        region_name='us-east-1'
    )

    variables={
        "users": [],
        "configuration" : [],
        "sgs" : [],
        "association" : []
    }

    os.chdir("../terraform")

    if os.path.isfile("auto.tfvars.json"):
        f  = open("auto.tfvars.json")
        variables = json.load(f)
    else:
        dump_json(variables)

    while True:
        os.system("cls")
        print("                                                WELCOME!                                          ")
        print("\n\n")
        print("                                            Type y to start!                                      ")
        print("                                             Type q to quit                                       ")
        print("\n\n")
        user_input = input("Enter your value: ")
        user_input = str(user_input)
         
        if user_input == "q":
            print("Bye!")
            return
        
        if user_input != "y":
            print("Invalid, let's try again")
            user_input = input("Enter your value: ")
            if user_input == "q":
                print("Bye!")
                return

        elif user_input == "y":
            print("                                         Initializing...                                      ")
            print("\n\n")
            os.system('terraform init')
            first_page(session, variables)

def first_page(session, variables):
        print("                                          [Main Actions]                                      ")
        print("                                  [type the code of the action]                               ")
        print("    [i] Instances Menu\t     [s] Security Groups Menu\t     [u] User Menu\t     [q] Quit\t    ")
        print("\n\n")

        action_input = input("Enter your action: ")
        action_input = str(action_input)

        if action_input in ["i", "s", "u", "q"]:
            if action_input == "i":
                instances(session, session.resource('ec2'), variables)
            elif action_input == "s":
                sg(session, session.resource('ec2'), session.client('ec2'), variables)
            elif action_input == "u":
                users(session, variables)
            else:
                print("bye")
                os._exit(0)
        else:
            print("Invalid!")
            time.sleep(3)
            first_page(session, variables)

def get_back():
    back = input("Press r to return: ") 
    if back == 'r':
        return
    else:
        get_back()           

def dump_json(map_variables):
    with open('auto.tfvars.json', 'w') as fp:
        json.dump(map_variables, fp, indent=4)

def limit_values(n_options, n_input):
    i = 0
    j = n_options
    ret = i 
    while ret == i:
        n_input = input("Enter value: ")
        try:
            ret = int(n_input)
            if ret <= i or ret > j:
                ret = i
                print("Invalid!")
        except:
            print("Invalid!")
    return ret

def execute_action():
    os.system("cls")
    print("                                             EXECUTING......                                       ")
    os.system("terraform plan -var-file=./auto.tfvars.json")
    os.system("terraform apply -var-file=./auto.tfvars.json -auto-approve")
    print("                                             ......FINISHED!                                       ")
    time.sleep(3)

if __name__ == "__main__":
    main()