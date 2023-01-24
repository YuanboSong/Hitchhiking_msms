import subprocess
import time

start_time = time.time()
command = "msms 100 5 -N 2000 -t .4 -r 380.64 5000 -Sp 0.8 -I 50"
for i in range(1, 51):
    command += " 2"
command += " -ma"
for i in range(1, 51):
    for j in range(1, 51):
        if i == j:
            command += " x"
        elif j == i + 1:
            command += " 1200"
        elif j == i - 1:
            command += " 1200"
        else:
            command += " 0"
command += " -SAA 40 -SaA 20 -SF 0"
print(command)
# Run the command and save the output
result = subprocess.run(command, stdout=subprocess.PIPE)

# Save the output to a file
with open('spatial_test.txt', 'w') as f:
    f.write(result.stdout.decode())

end_time = time.time()
run_time = end_time - start_time
print(f"Run time: {run_time:.2f} seconds")