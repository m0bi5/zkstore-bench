def read_file(path):
    try:
        with open(path, "r") as f:
            return f.readlines()
    except:
        return []

def find_line_with(strings, substr):
    line = [string for string in strings if substr in string][0]
    return line, strings.index(line)
from collections import defaultdict

tps = {}
throughput_nums = defaultdict(list)

for i in range(2, 15):
    tps[i] = {}
    for count1, count2 in [[0,0]]:# [[50, 100], [150, 200], [250, 300], [350, 400], [450, 500]]:
        count1 = str(count1)
        count2 = str(count2)
        
        lines = read_file("/home/ubuntu/reports/"+str(i)+"nodes"+str(count1)+"_"+str(count2)+".html")
        if lines == []:
            throughput_nums[count1].append(" ")
            throughput_nums[count2].append(" ")
            continue
        line1, idx1 = find_line_with(lines, "<td>createAsset_100tps")
        #line2, idx2 = find_line_with(lines, "<td>createAsset_"+count2+"tps")
        throughput1 = line1.split("</td>")[-3].split("<td>")[1] #change to -3 for latency, -2 for throughput
        #throughput2 = line2.split("</td>")[-2].split("<td>")[1]
        tps[i][count1] = throughput1
        #tps[i][count2] = throughput2
        throughput_nums[count1].append(throughput1)
        #throughput_nums[count2].append(throughput2)
print(tps)
        
for key in throughput_nums:
    print("=============="+key)
    for k in throughput_nums[key]:
        print(k)

        
