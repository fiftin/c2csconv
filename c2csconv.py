import sys
import re
	
def RepresentsLiteral(str):
	if re.match(r'^[+-]?\d[0-9\.]*$', str) is not None:
		return True
	elif re.match(r'^"[^"]*"$', str) is not None:
		return True
	return False
	
def ConvertTypeNameToDefault(typeName):
	if typeName == 'CHAR':
		return 'char'
	elif typeName == 'DINT':
		return 'int'
	elif typeName == 'REAL':
		return 'float'
	else:
		return typeName

def GetConstOrLiteral(str):
	if RepresentsLiteral(str):
		return str
	m = re.match(r'^(.+[+-])?([\w_][\w\d_]+)[^\.]*$', str)
	while m:
		constName = m.group(2)
		print 'Definations.'+constName
		str = str.replace(constName, 'Definations.'+constName)
		print 'str2:'+str
		m = re.match(r'^(.+[+-])?([\w_][\w\d_]+)[^\.]*$', str)
	return str


inp = open(sys.argv[1], 'r')
outp = open(sys.argv[2], 'w')

defines = []

structLines = []

for line in inp:

	m = re.match(r'struct\s+([a-zA-Z_0-9]+)', line)
	if m:
		print "[StructLayout(LayoutKind.Sequential, CharSet = CharSet.Ansi)]"
		print "public struct "+m.group(1)
		structLines.append("[StructLayout(LayoutKind.Sequential, CharSet = CharSet.Ansi)]\n")
		structLines.append("public struct "+m.group(1)+"\n")
		continue
	m = re.match(r'^\s*(.+)\s+(.+)\[(.+)\]\s*\[(.+)\]\s*\[(.+)\]\s*;', line)
	if m:
		field_type = ConvertTypeNameToDefault(m.group(1))
		field_name = m.group(2)
		field_size1 = GetConstOrLiteral(m.group(3))
		field_size2 = GetConstOrLiteral(m.group(4))
		field_size3 = GetConstOrLiteral(m.group(5))
				
		print "\t[MarshalAs(UnmanagedType.ByValArray, SizeConst = ("+field_size1+") * ("+field_size2+") * ("+field_size3+"))]"
		print "\tpublic "+field_type+"[,,] "+field_name+" = new "+field_type+"["+field_size1+", "+field_size2+", "+field_size3+"];"
		structLines.append("\t[MarshalAs(UnmanagedType.ByValArray, SizeConst = ("+field_size1+") * ("+field_size2+") * ("+field_size3+"))]\n")
		structLines.append("\t[ThreeDimensionalArrayAttribute("+field_size1+", "+field_size2+", "+field_size3+")]\n");
		structLines.append("\tpublic " + field_type + "[] " + field_name + ";\n")
		continue
		
	m = re.match(r'^\s*(.+)\s+(.+)\[(.+)\]\s*\[(.+)\]\s*;', line)
	if m:
		field_type = ConvertTypeNameToDefault(m.group(1))
		field_name = m.group(2)
		field_size1 = GetConstOrLiteral(m.group(3))
		field_size2 = GetConstOrLiteral(m.group(4))
		
		print "\t[MarshalAs(UnmanagedType.ByValArray, SizeConst = ("+field_size1+") * ("+field_size2+"))]"
		print "\tpublic "+field_type+"[,] "+field_name+" = new "+field_type+"["+field_size1+", "+field_size2+"];"
		structLines.append("\t[MarshalAs(UnmanagedType.ByValArray, SizeConst = "+field_size1+" * "+field_size2+")]\n")
		structLines.append("\t[TwoDimensionalArrayAttribute("+field_size1+", "+field_size2+")]\n");		
		structLines.append("\tpublic " + field_type + "[] " + field_name + ";\n")
		continue
		
	m = re.match(r'^\s*(.+)\s+(.+)\[(.+)\]\s*;', line)
	if m:
		field_type = ConvertTypeNameToDefault(m.group(1))
		field_name = m.group(2)
		field_size = GetConstOrLiteral(m.group(3))
		print "\t[MarshalAs(UnmanagedType.ByValArray, SizeConst = "+field_size+")]"
		print "\tpublic "+field_type+"[] "+field_name+";"
		structLines.append("\t[MarshalAs(UnmanagedType.ByValArray, SizeConst = "+field_size+")]\n")
		structLines.append("\tpublic "+field_type+"[] "+field_name+";\n")
		continue
	
	m = re.match(r'^\s*(.+)\s+([\w\d_]+)\s*;\s*//.*', line)
	if m is None:
		m = re.match(r'^\s*(.+)\s+([\w\d_]+)\s*;\s*', line)
	if m:
		field_type = ConvertTypeNameToDefault(m.group(1))
		field_name = m.group(2)
		print "\tpublic "+field_type+" "+field_name+";"
		structLines.append("\tpublic "+field_type+" "+field_name+";\n")
		continue

	m = re.match(r'^\s*#define\s([^\s]+)\s+([^/]+)(//.*)?$', line)
	if m:
		const_name = m.group(1)
		const_value = m.group(2)
		const_type = 'int';
		print "\tpublic const "+const_type+" "+const_name+" = "+const_value+";";
		defines.append("\tpublic const "+const_type+" "+const_name+" = "+const_value+";\n");
		continue;
	print line
	structLines.append(line);
	
outp.write("public class Definations\n{\n");
outp.writelines(defines);
outp.write("}\n");

outp.writelines(structLines);
	