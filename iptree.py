import json
from collections import defaultdict
'''
This will return JSON data for IPs with Tree Structure
for eg;
{
    "result": [
        {
            "count": 30, 
            "ip": "172.X.X.X", 
            "children": [
                {
                    "count": 30, 
                    "ip": "172.16.X.X", 
                    "children": [
                        {
                            "count": 1, 
                            "ip": "172.16.40.X", 
                            "children": ["172.16.40.200"]
                        }, 
                {
                    "count": 1, 
                    "ip": "172.16.9.X", 
                    "children": ["172.16.9.200"]
                }, 
                {
                    "count": 2, 
                    "ip": "172.16.66.X", 
                    "children": ["172.16.66.251", "172.16.66.250"]
                }, 
                {
                    "count": 1, 
                    "ip": "172.16.35.X", 
                    "children": ["172.16.35.204"]
                }, 
                {
                    "count": 25, 
                    "ip": "172.16.12.X", 
                    "children": ["172.16.12.20", "172.16.12.224", "172.16.12.192", "172.16.12.190", "172.16.12.14", "172.16.12.193", "172.16.12.191", "172.16.12.194", "172.16.12.229", "172.16.12.233", "172.16.12.228", "172.16.12.231", "172.16.12.19", "172.16.12.240", "172.16.12.230", "172.16.12.232", "172.16.12.238", "172.16.12.227", "172.16.12.237", "172.16.12.24", "172.16.12.235", "172.16.12.200", "172.16.12.236", "172.16.12.239", "172.16.12.224"]
                }
            ]
        }]
    }]
}
'''
def generate_ip_tree(ips = []):
    if not ips:
        return "Please Provide IPs list"
    if not isinstance(ips, list):
        return "ips should be of type list"

    return_data = []
    consumed_ips = [map(int, ip.split(".")) for ip in ips]
    ip_collection = defaultdict(list)
    for ip in consumed_ips:
        ip_collection[ip[0]].append(ip)

    ip_tree_collection = {}
    ip_childs = []

    for key, val in ip_collection.iteritems():
        ip_child_collection = {}
        ip_tree_collection[key] = val
        ip_child_collection['A'] = key
        coll_b, coll_c = defaultdict(list), defaultdict(list)
        for i in val:
            coll_b[i[1]].append(i)
            coll_c[i[2]].append(i)
        ip_tree_collection[key].append(coll_b)
        ip_child_collection['B'] = coll_b.keys()
        ip_tree_collection[key].append(coll_c)
        ip_child_collection['C'] = coll_c.keys()
        ip_childs.append(ip_child_collection)

    for child in ip_childs:
        tree_dict = {}
        octate_a, octate_b, octate_c = child.get('A'), child.get('B'), child.get('C')
        octate_a_ips = ip_tree_collection.get(octate_a)

        all_ips = [ip for ip in octate_a_ips if type(ip) == list]

        tree_dict['ip'] = "{}.X.X.X".format(octate_a)
        tree_dict['children'] = get_childs(octate_a, octate_b, octate_c, all_ips)
        tree_dict['count'] = len(all_ips)

        return_data.append(tree_dict)
    return json.dumps({'result':return_data})

def get_childs(octate_a, octate_b, octate_c, all_ips):
    octate_b_childs = []
    for b in octate_b:
        b_child_count = 0
        octate_b_dict = {}
        octate_b_dict['ip'] = "{}.{}.X.X".format(octate_a, b)
        octate_b_dict['children'] = []
        for c in octate_c:
            octate_c_dict = {}
            octate_c_dict['ip'] = "{}.{}.{}.X".format(octate_a, b, c)
            c_childs = get_triplet_childs('{}.{}.{}'.format(octate_a, b, c), all_ips)
            octate_c_dict['children'] = c_childs
            c_child_count = len(c_childs)
            octate_c_dict['count'] = c_child_count
            b_child_count = b_child_count + c_child_count
            octate_b_dict['children'].append(octate_c_dict)
        octate_b_dict['count'] = b_child_count
        octate_b_childs.append(octate_b_dict)
    return octate_b_childs

def get_triplet_childs(triplet, ips):
    triplet_dict = defaultdict(list)
    for ip in ips:
        tpl = '{}.{}.{}'.format(ip[0], ip[1], ip[2])
        triplet_dict[tpl].append(ip)
    triplet_ips = triplet_dict.get(triplet, [])
    return ['.'.join(map(str, ip)) for ip in triplet_ips]

if __name__ == "__main__":
    test_data=['172.16.12.20', '172.16.12.224', '172.16.12.192', '172.16.12.190', '172.16.12.14', '172.16.12.193', '172.16.12.191', '172.16.12.194', '172.16.35.204', '172.16.40.200', '172.16.9.200', '172.16.12.229', '172.16.12.233', '172.16.12.228', '172.16.66.251', '172.16.12.231', '172.16.12.19', '172.16.12.240', '172.16.12.230', '172.16.12.232', '172.16.12.238', '172.16.12.227', '172.16.12.237', '172.16.12.24', '172.16.12.235', '172.16.12.200', '172.16.66.250', '172.16.12.236', '172.16.12.239', '172.16.12.224']
    print generate_ip_tree(test_data)