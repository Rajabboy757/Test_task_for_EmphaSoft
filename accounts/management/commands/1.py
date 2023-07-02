d =  [{"key1": "value1"}, {"k1": "v1", "k2": "v2", "k3": "v3"}, {}, {}, {"key1": "value1"}, {"key1": "value1"}, {"key2": "value2"}]
ans = []
for i in d:
    if i not in ans:
        ans.append(i)

print(ans)