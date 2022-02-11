import os
from jinja2 import Template
import time
import sys

def read_file(path):
    with open(path, "r") as f:
        return f.readlines()

def update_line(lines, idx, updated_content):
    lines[idx] = updated_content
    return lines

def find_position_to_update(lines, f="#ADD\n"):
    return lines.index(f) - 1

def find_line_with(strings, substr):
    line = [string for string in strings if substr in string][0]
    return line, strings.index(line)

def write_file(path, lines):
    with open(path, "w+") as f:
        if type(lines) == list:
            f.writelines(lines)
        else:
            f.write(lines)

def populate_rounds(rounds, arg):
        fnames = {"store": "./storeRC.js", "assign": "./assignRC.js"}
        content = "\n".join(read_file("./benchmarks/myAssetBenchmark_temp.yaml"))
        new_content = ""
        for r in rounds:
            new_content += Template("""
      - label: createAsset_{{count1}}tps
        description: Write asset benchmark
        txNumber: 100
        rateControl: 
          type: {{fname}}
          opts:
            tps: {{count1}}
        workload:
          module: workload/createAsset.js
          arguments:
            assets: 10
            contractId: basic
        """).render(count1=r, fname=fnames[arg])
            new_content += "\n"
        content = content + "\n" + new_content
        write_file("./benchmarks/myAssetBenchmark.yaml", content)

def run_one_config(n):
    os.chdir("/home/ubuntu/fabric-samples-{}/test-network-{}nodes".format(sys.argv[1], n))
    os.system("./network.sh down")
    os.system("./network.sh up createChannel")
    os.system("./network.sh deployCC -ccn basic -ccp ../asset-transfer-basic/chaincode-javascript/ -ccl javascript")
    os.chdir("/home/ubuntu/caliper-workspace")
    count1 = count2 = 0
    tps = [100]#[[50, 100], [150, 200], [250, 300], [350, 400], [450, 500]]
    populate_rounds(tps, sys.argv[1])
    content = "\n".join(read_file("./networks/networkConfig_temp.yaml"))
    content = Template(content).render(kind=sys.argv[1], n=n)
    write_file("./networks/networkConfig.yaml", content)
    os.system("npx caliper launch manager --caliper-workspace ./ --caliper-networkconfig networks/networkConfig.yaml --caliper-benchconfig benchmarks/myAssetBenchmark.yaml --caliper-flow-only-test --caliper-fabric-gateway-enabled --caliper-fabric-timeout-invokeorquery 600")
    time.sleep(1)
    os.system("mv report.html /home/ubuntu/reports/"+str(n)+"nodes"+str(count1)+"_"+str(count2)+".html")
    
    os.chdir("/home/ubuntu")

for i in range(2,5):
    run_one_config(i)