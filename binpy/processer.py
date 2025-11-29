def process(file):
    # syntax
    formaters = ['=', '"',"'", "{", "}", "(", ")"]
    nonMethods = ["for", "if"]
    builtInMain = ["print", "printf"]
    
    # 'type' : [startOfMem,endOfMem,length,currPointer]
    class_mems = {'bit':[0,4096,1,0],
                'char':[4096,12288,8,4096],
                'int':[12288,45056,32,12288],
                'long':[45056,77824,64,45056]}
    
    # 'type' : 'parent'
    {'bit':'bit', 'char' : 'bit', 'int':'bit', 'long': 'bit'}

    # 'var_name'+'?'+'scope' : ['type',startofMemAdress]
    register = {}
    
    # Bits that are tampered with should reset to zero at every EOF
    changes=[]

    def check_scopes(var_name):
        for find_scopes in range(int(curr_scope[len(curr_scope)-1]),-1,-1):
            if (var_name + '?' + curr_scope[0:find_scopes+1]) in register:
                found = var_name + '?' + curr_scope[0:find_scopes+1]
                return found
                break
            else:
                continue
    import mmap
    blocks=[]
    with open(file, "r") as c:
        temp=""
        commented=False;
        for x in c.read():
            if x=="\n" or x=="\t":
                continue
            if x==";":
                temp = temp.strip()
                blocks.append(temp)
                temp=""
            
            else:
                temp+=x
            
        
        
    import os

    
    script_dir = os.path.dirname(os.path.abspath(__file__))

    
    bin_path = os.path.join(script_dir, "BIN.txt")
    max_scope = 0
    curr_scope = "0"
    in_string = False
    with open(bin_path, "r+") as f:
        file = mmap.mmap(f.fileno(), 0)
        
        for statement in blocks:
            statement_temp=""
            for char in statement:
                
                if char in formaters:
                    
                    statement_temp+=" "+char+" "
                else:
                    statement_temp+=char
            EVN = ""
            EV = False
            ignore = False
            parsed = statement_temp.split()
            found_var = ""
            function = ""
            for word in range(len(parsed)):
                if parsed[word] == '"' or parsed[word] == "'":
                    if in_string == False:
                        in_string = True
                    else:
                        in_string = False
                if parsed[word] in list(class_mems.keys()) and not in_string:
                    EVN = parsed[word]
                    continue
                if EVN!="":
                    register[parsed[word]+'?'+curr_scope] = [EVN, class_mems.get(EVN)[3]]
                    class_mems.get(EVN)[3]+=class_mems.get(EVN)[2]
                    EVN = ""
                if parsed[word] == ')'  and not in_string:
                    function == ""
                if parsed[word] == '(' and not in_string:
                    if parsed[word-1] not in nonMethods:
                        function = parsed[word-1]
                        continue
                             
                if function != "":
                    if function == "printlnf":
                        funcLoopBI = 0
                        varNameBI = ""
                        
                        checkBI = ""
                        for comb in range(len(parsed)-word):
                            checkBI+=parsed[word+comb]
                        
                        while checkBI[funcLoopBI]!=",":
                            if parsed[word][funcLoopBI]!=" ":
                                varNameBI+=checkBI[funcLoopBI]
                            funcLoopBI+=1
                        found2 = check_scopes(varNameBI)
                        format_specifier = checkBI[funcLoopBI+1:funcLoopBI+3].replace(" ", "")
                        if format_specifier == '%d':
                            
                            print(int(file[register.get(found2)[1]+1:register.get(found2)[1]+class_mems.get(register.get(found2)[0])[2]+1],2))
                        function=""
                    if function == "printf":
                        funcLoopBI = 0
                        varNameBI = ""
                        
                        checkBI = ""
                        for comb in range(len(parsed)-word):
                            checkBI+=parsed[word+comb]
                        
                        while checkBI[funcLoopBI]!=",":
                            if parsed[word][funcLoopBI]!=" ":
                                varNameBI+=checkBI[funcLoopBI]
                            funcLoopBI+=1
                        found2 = check_scopes(varNameBI)
                        format_specifier = checkBI[funcLoopBI+1:funcLoopBI+3].replace(" ", "")
                        if format_specifier == '%d':
                            
                            print(int(file[register.get(found2)[1]+1:register.get(found2)[1]+class_mems.get(register.get(found2)[0])[2]+1],2), end = "")
                        function=""
                    if function == "print":
                        printed=""
                        if parsed[word] == '"':
                            for print_inc in range(word+1, len(parsed)):
                                if parsed[print_inc] == '"':
                                    break
                                printed+=parsed[print_inc]+" "
                        print(printed, end="")
                        function=""
                    if function == "println":
                        printed=""
                        if parsed[word] == '"':
                            for print_inc in range(word+1, len(parsed)):
                                if parsed[print_inc] == '"':
                                    break
                                printed+=parsed[print_inc]+" "
                        print(printed)
                        function=""
                    funcLoopBI=0
                    varNameBI=""
                    
                    continue
                if parsed[word] == '{' and not in_string:
                    curr_scope += str(max_scope+1)
                    max_scope += 1
                if parsed[word] == '}' and not in_string:
                    curr_scope = curr_scope[0:len(curr_scope)-1]
                
                if parsed[word] == '=' and not in_string:
                    change = bin(int(parsed[word+1]))[2:len(bin(int(parsed[word+1])))]
                    inc_change = 0
                    found1 = check_scopes(parsed[word-1])
                    ### locates variable location in register then finds info on type then edits BIN file accordingly
                    for binary in range(register.get(found1)[1]+1, register.get(found1)[1]+class_mems.get(register.get(found1)[0])[2]+1):
                        
                        if (
                                (class_mems.get(register.get(found1)[0]))[2]
                                - len(change)
                            ) >= (
                                binary - register.get(found1)[1]
                        ):
                            
                            file[binary:binary+1] = '0'.encode('utf-8')
                        else:
                             
                            
                            file[binary:binary+1] = change[inc_change].encode('utf-8')
                            changes.append(binary)
                            
                            inc_change+=1
                    
                    
        for clean in changes:
            file[clean:clean+1] = '0'.encode('utf-8')
        
        file.close()



