
def generate_formatted_headers(s):
	temp = []
	for _ in s.split("\n"):
		words = _.split(": ")
		words[0] = "'" + words[0] + "':"
		words[1] = "'" + words[1] + "'"
		temp.append([words[0],words[1]])
	print("{")
	for index,line in enumerate(temp):
		if(index != (len(temp)-1)):
			print(line[0],line[1],sep=' ',end=',\n')
	print(temp[len(temp)-1][0],temp[len(temp)-1][1],sep=' ',end='\n}')

s = '''Host: 192.168.0.1
Connection: keep-alive
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2787.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Referer: http://192.168.0.1/advance.asp
Accept-Encoding: gzip, deflate, sdch
Accept-Language: en-US,en;q=0.8
Cookie: language=en; ecos_pw=YWRtaW4=mji:language=en'''

generate_formatted_headers(s)