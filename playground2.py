import json

# initializing string
test_str = ["[{'Gfg' : 3, 'Best' : 8}, {'Gfg' : 4, 'Best' : 9}]"]
my_string = ["[{'uid': 213063, 'location': 'serie/213063', 'language': 'Svenska', 'primary': 'true'}, {'uid': 222846, 'location': 'serie/222846', 'language': 'Sydsamiska', 'primary': 'false'}, {'uid': 217162, 'location': 'serie/217162', 'language': 'Syntolkat', 'primary': 'false'}, {'uid': 213829, 'location': 'serie/213829', 'language': 'Persiska', 'primary': 'false'}, {'uid': 221151, 'location': 'serie/221151', 'language': 'Nordsamiska', 'primary': 'false'}, {'uid': 221494, 'location': 'serie/221494', 'language': 'Lulesamiska', 'primary': 'false'}, {'uid': 216416, 'location': 'serie/216416', 'language': 'Svenskt teckenspråk', 'primary': 'false'}, {'uid': 214112, 'location': 'serie/214112', 'language': 'Meänkieli', 'primary': 'false'}, {'uid': 213978, 'location': 'serie/213978', 'language': 'Polska', 'primary': 'false'}, {'uid': 200880, 'location': 'serie/200880', 'language': 'Engelska', 'primary': 'false'}]"]
  
# printing original string
print("The original string is : " + str(my_string))
  
# replace() used to replace strings 
# loads() used to convert 
res = [json.loads(idx.replace("'", '"')) for idx in my_string]
      
# printing result 
print("Converted list of dictionaries : " + str(res)) 