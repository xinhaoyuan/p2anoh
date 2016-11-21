import os
import sys
import subprocess
import codecs
import re
import simpleon

def main(args):
	LOCAL_DIR = os.path.dirname(os.path.abspath(__file__))
	argparser = simpleon.SimpleONParser(True, False)
	try:
		argparser.parse_lines(args)
		args = []
		while True:
			item = argparser.extract()
			if item is None:
				break
			args.append(item)
	except:
		args = None
		
	p2hex_binary = LOCAL_DIR + "/bin/p2hex/pdf2htmlEX"
	p2hex_opt = [ "--zoom", "1.5" ]
	input = None
	output = None
	library_path = LOCAL_DIR + "/lib"
	
	for item in args:
		if not isinstance(item, dict):
			continue
		if "p2hex" in item:
			p2hex_binary = item["p2hex"]
		if "p2hex-opt-base" in item:
			p2hex_opt = item["p2hex-opt-base"]
		if "p2hex-opt" in item:
			p2hex_opt.extend(item["p2hex-opt"])
		if "input" in item:
			input = item["input"]
		if "output" in item:
			output = item["output"]
		if "lib-path" in item:
			library_path = item["lib-path"]
			
	libfile_list = os.listdir(library_path)
	libfile_list.sort()
	
	if output is None:
		sys.stderr.write("output required\n")
		sys.exit(-1)
	
	if input is not None:
		cmd = [ p2hex_binary ]
		if isinstance(p2hex_opt, list):
			cmd.extend(p2hex_opt)
		cmd.append(input)
		cmd.append(output)
		p = subprocess.Popen(cmd)
		p.wait()
	
	lines = None
	with codecs.open(output, "r", "utf-8") as f:
		lines = f.readlines()
		
	out = []
	for l in lines:
		m = re.search("</head>", l)
		if m:
			out.append(l[:m.start(0)])
			for libfile in libfile_list:
				with codecs.open(library_path + "/" + libfile, "r", "utf-8") as emb_f :
					if libfile.endswith(".js"):
						out.append("<script>")
						out.append(emb_f.read())
						out.append("</script>")
					elif libfile.endswith(".css"):
						out.append('<style type="text/css">')
						out.append(emb_f.read())
						out.append("</style>")
			out.append("</head>")
			out.append(l[m.end(0):])
			pass
		else:
			out.append(l)

	with codecs.open(output, "w", "utf-8") as f:
		for l in out:
			f.write(l)

if __name__ == "__main__":
	main(sys.argv[1:])