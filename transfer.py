from subprocess import call

destination_name = "dantesanaei"
destination_ip = "192.168.0.153"
destination_directory = "/Users/dantesanaei/Public"
file_name = "sail.jpeg"
scp_command = "sudo scp " + file_name + " " + destination_name + "@" + destination_ip + ":" + destination_directory
print(scp_command)
call(scp_command.split(" "))