#!/usr/bin/python
import sys #used for system arguments; sys.argv[n]
import xml.dom.minidom
import libxml2
import re #regular expressions module
import subprocess #used for system procedure calls


########  CLASS DEFINITIONS  ########

class PolicyBase:
    'Class used to read, write, and update policy base rules directly into an XML document.'  
    
    ## VARIABLES ##
    
    'Location of the XML Policy base file.'
    xmlpbfile = ''     
    'DOM object for the policy base.'
    pbDOM = ''
    'alp variables'
    alp_roles = set();
    alp_subjects = set();
    alp_xpaths = set();
    alp_documents = set();
    alp_tempints = set();
    
    ## FUNCTIONS ##    
    
    '----------------------------------------------------------------------------------------------'
    
    def __init__(self, n_file):
        'On instantiation, the XML document containing the policy base must be specified and opened for reading'
        self.xmlpbfile = n_file
        
    '----------------------------------------------------------------------------------------------'       
    
    def parseXMLPB(self):
        '''Reads the specified PB XML document for reading/manipulation of rules into a local variable.
        The document is read and represented using the DOM.'''
        fh = open(self.xmlpbfile, 'r+')
        self.pbDOM = xml.dom.minidom.parse(fh)
        fh.close()      
        
    '----------------------------------------------------------------------------------------------'          
        
    def countRules(self):
        'Counts the number of occurences of the <axmlt:rule> tag in the pb DOM.'
        return len(self.pbDOM.getElementsByTagName('axmlt:rule'))
        
    ruleCount = property(countRules)        
    
    '----------------------------------------------------------------------------------------------'    
        
    def writeXMLPB(self):
        'Writes current local PB to XML document.'
        fh = open(self.xmlpbfile, 'w+')
        fh.write(self.pbDOM.toxml())
        fh.close()            
        
    '----------------------------------------------------------------------------------------------'        
        
    def addRulesToPB(self, newRulesFile):
        '''Add a created rule(s) to the PB DOM.  The rules are represented by XML element strings in an XML document (from the interface).
        The string will be parsed and added to the DOM.  The newRule must be a formatted <rule> specified in the XSD.
        Our interface will however pass the <rule> using the namespace axmlt and also nested within a <policybase> parent.
        Therefore, it must be extracted from their and then added to the pb.'''
        nrfh = open(newRulesFile, 'r+')
        nR_DOM = xml.dom.minidom.parse(nrfh)
        nrfh.close()            

        'get all the rules from the DOM'
        nrl = nR_DOM.getElementsByTagName('axmlt:rule')
        
        'for each rule, append it to the PB DOM'
        for nr in nrl:
            self.pbDOM.firstChild.appendChild(nr)

    '----------------------------------------------------------------------------------------------'            
            
    def delRuleFromPB(self, i):
        'Deletes a rule (indexed by i) from PB DOM'
        ruleList = self.pbDOM.getElementsByTagName('axmlt:rule')
        self.pbDOM.firstChild.removeChild(ruleList[i-1])  

    '----------------------------------------------------------------------------------------------'       
        
    def delRulesFromPB(self):
        'Deletes rules (all) from PB DOM'
        ruleList = self.pbDOM.getElementsByTagName('axmlt:rule')
        for r in ruleList:
            self.pbDOM.firstChild.removeChild(r)        

    '----------------------------------------------------------------------------------------------'        
        
    def writeALPPB(self, alpfile, alppb, langrules):
        '''Write the translated PB to a file document.'''
        fh = open(alpfile, 'w+')
        
        'first output the alp variables'
        self.extractALPVariables(alppb)
        varline = ""
        
        varline = "roles("
        for role in self.alp_roles:
            varline += role 
            varline += ";"
        varline = varline.rstrip(";") 
        varline += ").\n"
        fh.write(varline)
        
        varline = "subjects("
        for subject in self.alp_subjects:
            varline += subject 
            varline += ";"
        varline = varline.rstrip(";") 
        varline += ").\n"
        fh.write(varline)     
        
        varline = "xpaths("
        for xpath in self.alp_xpaths:
            varline += xpath 
            varline += ";"
        varline = varline.rstrip(";") 
        varline += ").\n"
        fh.write(varline)   
        
        varline = "documents("
        for document in self.alp_documents:
            varline += document 
            varline += ";"
        varline = varline.rstrip(";") 
        varline += ").\n"
        fh.write(varline)      
        
        varline = "tempints("
        for tempint in self.alp_tempints:
            varline += tempint 
            varline += ";"
        varline = varline.rstrip(";") 
        varline += ").\n\n"
        fh.write(varline) 
                    
        
        'now output the translated rules'
        for rule in alppb:
            fh.write(rule)
            fh.write("\n")
            
        'now append the defined axmlt/alp language rules from file'
        lrf = open(langrules, "r")
        lr = lrf.readlines()
        fh.writelines(lr)
        lrf.close()        
            
        fh.close()
        
    '----------------------------------------------------------------------------------------------'        
        
    def extractALPVariables(self, alppb):
        '''This will extract all the variables written in the axmlt/alp policy base
        and save them in distinct variable sets.'''

        'clear the variables first'        
        self.alp_roles.clear()
        self.alp_roles.add("null")
        self.alp_subjects.clear() 
        self.alp_subjects.add("null")
        self.alp_xpaths.clear()
        self.alp_xpaths.add("null");
        self.alp_documents.clear();
        self.alp_documents.add("null");        
        self.alp_tempints.clear();
        self.alp_tempints.add("null");        
               
        for rule in alppb:
            'regular expression for roles, documents, and xpaths'
            vre = re.compile(r'^role\(([a-z]{1}\w*?),\w{2},(.*?),(.*?),')
            if vre.search(rule):
                m = vre.search(rule)
                self.alp_roles.add(m.group(1)) #the rolename
                self.alp_documents.add(m.group(2)) #the document anme
                self.alp_xpaths.add(m.group(3)) #the xpath
                
            'regular expression for subjects and temporal intervals'
            vre = re.compile(r'^grant\(([a-z]{1}\w*?),[a-z]{1}\w*?,([a-z]{1}\w*)')
            if vre.search(rule): 
                m = vre.search(rule)
                self.alp_subjects.add(m.group(1)) #the subject
                self.alp_tempints.add(m.group(2)) #the interval
                
            'regular expression for other temporal intervals'
            vre = re.compile(r'^(during|starts|finishes|before|overlap|meets|equal)\(([a-z]{1}\w*?),([a-z]{1}\w*)\)')
            if vre.search(rule): 
                m = vre.search(rule)
                self.alp_tempints.add(m.group(2)) #the 1st interval
                self.alp_tempints.add(m.group(3)) #the 2nd interval                        

    '----------------------------------------------------------------------------------------------'             
        
    def translatePBtoALP(self):
        '''Converts each rule from the PB DOM into it's equivalent ALP syntax rule.
        Each converted rule is stored as dictionary and then into a list.
        The dictionaries are later output into a document to be used as the input for our stable model.'''

        alpPB = []
        xre = re.compile(r'\*|\[.*\]|//') #regular expression for checking dynamic XPath's

        'get all the rules from the PB'
        rl = self.pbDOM.getElementsByTagName('axmlt:rule')
        
        for r in rl:
            'initialise head and body lists'
            alpHead = []
            alpBodyList = []
            
            'read the head and body from each rule in the list'
            head = r.getElementsByTagName('axmlt:head-statement')
            body = r.getElementsByTagName('axmlt:body-statement')
            
            'translate the head (there should only be one). the head is stored as a dictionary inside of a list inside of another list (for consistency with body list)'
            for h in head:

                'stores the translated head statement'
                transHead = self.translateXMLStatement(h)
     
                'if its a role, check for dynamic xpaths'
                if transHead['type'] == 'role':

                    #need to expand dynamic xpath if applicable; use regular expression
                    if xre.search(transHead['xpath_exp']):
                        xl = self.expandXPath(transHead['xpath_exp'], transHead['document']) #expand the xpath
                        for newx in xl:
                            ex_transHead = transHead.copy()
                            ex_transHead['xpath_exp'] = newx
                            alpHead.append([ex_transHead]) #append each expanded xpath as an individual list (*note the [] inside the append, correct structure req. for combineLists())
            
                    else:                        
                        #just append the head because the XPath is not dynamic (*note the [] inside the append, correct structure req. for combineLists())
                        alpHead.append([transHead])                    
                        
                else:                        
                    #just append the head cause its not a role (*note the [] inside the append, correct structure req. for combineLists())
                    alpHead.append([transHead])

            
            '''translate the body (zero to many). the body element(s) are stored as dictionaries inside of lists inside of another list.
            This is because the body can contain zero or many elements.  Furthermore, because bodies can contain dynamic xpaths, we need 
            another dimension to store the multiple possibilities of bodies.  Hence the dictionary inside a list.'''
            for b in body:

                'this list is for the expanded body elements with dynamic xpaths and ALSO those with just static xpaths or no xpaths'
                expandedBodyList = []
                'translate the body statement'
                transBody = self.translateXMLStatement(b)
     
                if transBody['type'] == 'role':

                    #need to expand dynamic xpath if applicable
                    if xre.search(transBody['xpath_exp']):
                        xl = self.expandXPath(transBody['xpath_exp'], transBody['document'])
                        for newx in xl:
                            ex_transBody = transBody.copy()
                            ex_transBody['xpath_exp'] = newx
                            expandedBodyList.append(ex_transBody) #add each expanded version of the body statement to this body list
                        
                        #add the expanded list INTO the body list (not appended, its a 2 dimensional list)
                        alpBodyList.append(expandedBodyList)
                        
                    else:
                        #just append the body BUT as a single element list
                        expandedBodyList.append(transBody)
                        alpBodyList.append(expandedBodyList)                        
                        
                else:
                    #just append the body BUT as a single element list
                    expandedBodyList.append(transBody)
                    alpBodyList.append(expandedBodyList)
                    
                    
                    
            '''We need to combine the head lists and body lists now.  Because it is possible that either head or body contains multiple elements
            due to numbers or expansion from XPaths, we use a function to recursively combine the body elements with the head elements ie. combineLists.'''        
            lA = alpHead                                #start the list with just the head elements
            for lB in alpBodyList:                      #for every list item (the body statements) which is a list of dictionaries
                retList = self.combineLists(lA, lB)
                lA = retList                            #on the next iteration, use the newly generated list to combine with the next set of body statements
                
                
            '''Now turn the list item (a statement) into its respective string representation'''    
            alpRule = lA
            alpRuleStr = ''
            
            for stats in alpRule:
                'the first element of the stat list is the head'
                alpRuleStr = self.outputALPStatementString(stats[0])
                
                'if there are body statements, process them, else just print a full stop'
                blen = len(stats)               
                if blen > 1:   
                    'output the asp arrow'
                    alpRuleStr += ' :- '             
                    'the rest are the body statements'
                    bcount = 1 #skip the head
                    while bcount < blen:
                        alpRuleStr += self.outputALPStatementString(stats[bcount])
                        bcount+=1
                        if bcount == blen:
                            alpRuleStr += '.'
                        else:
                            alpRuleStr += ', '
                else:
                    alpRuleStr += '.'
                        
                'add the rule to the output list'
                alpPB.append(alpRuleStr)

                
        return alpPB      
        
    '----------------------------------------------------------------------------------------------'        

    def outputALPStatementString(self, s):
        '''Prints a translated ALP rule.  Input must be a dictionary earlier translated with translateXMLStatement()'''
        
        '''check for negation as failure 'with absence'''
        if s['withAbsence'] == 'true':
            o_s = 'not ' 
        else:
            o_s = ''
        
        if s['type'] == 'grant':
            o_s += s['type'] + '(' + s['subject'] + ',' + s['role_name'] + ',' + s['interval'] + ')'
        
        elif s['type'] == 'role':
            o_s += s['type'] + '(' + s['role_name'] + ',' + s['sign'] + ',' + s['document'] + ',' + s['xpath_exp'] + ',' + s['priv'] + ')'
            
        else:
            'all other statements are just tuples'
            o_s += s['type'] + '(' + s['val1'] + ',' + s['val2'] + ')'
       
        return o_s

    '----------------------------------------------------------------------------------------------'        
        
    def combineLists(self, lA, lB):
        '''This is used primarily with policy base translation.
        It will combine a list of a list of dictionaries with a list of dictionaries (heads and bodies).  
        This confusing function is due to dynamic XPaths producing multiple head or body items in rules.'''
    
        'Returned list with lists of dictionaries within it.'
        retList = []
        
        for a in lA:        #for every list of dictionaries in A
            for b in lB:    #take a dictionary from list B
                newListItem = a             #copy the list 'a'
                newListItem.append(b)       #append the dictionary from the second list to it
                retList.append(newListItem) #and add the new list item to the return list
                
        return retList
        
    '----------------------------------------------------------------------------------------------'        

    def translateXMLStatement(self, s):
        '''Will translate a single AXMLT element (s).  It is checked to see if it is a relationship-statement, grant-statement, or role-statement.
        A dictionary representation of the ALP string is returned.
        Note: The depths specified for the DOM elements were found through trial and error.'''
        
        'Output statements'
        o_s = {}
        
        'The first child of the argument element is the statement itself.'
        s_e = s.childNodes[0]
        s_type = s_e.nodeName

        '''Check if this statement is supposed to be 'with absence'.
        If it is, mark it as a 'not statement'. This is stored as an optional boolean attribute
        named withAbsence.'''
        if s.getAttribute('withAbsence') == 'true':
            withAbsence = 'true'
        else:
            withAbsence = 'false'

        
        if s_type == 'axmlt:relationship-statement':
            '''Translate a relationship statement. It has a relationship atom made of a tuple.
            We must dig through the element to retrieve the values for the tuple. Refer to XSD for hierarchy and depth.'''
            r_atom = s_e.childNodes[0] #1 level in is the relationship atom
            r_type = r_atom.nodeName.split(':',1)[1] #because the document is well-formed, the tag names are exactly the relationships allowed, striped of their namespace first though
            r_value1 = r_atom.childNodes[0].firstChild.nodeValue
            r_value2 = r_atom.childNodes[1].firstChild.nodeValue            
    
            'Based on the type of relationship this is (9 avail.), translate respectively.'
            o_s = {'type' : r_type, 'val1' : r_value1, 'val2' : r_value2, 'withAbsence' : withAbsence}        
            
        elif s_type == 'axmlt:grant-statement':
            '''Translate a grant statement (role name, subject, interval).'''
            role_name =  s_e.childNodes[0].firstChild.nodeValue;
            subject = s_e.childNodes[1].firstChild.nodeValue;
            interval = s_e.childNodes[2].firstChild.nodeValue;
            
            o_s = {'type' : 'grant', 'subject' : subject, 'role_name' : role_name, 'interval' : interval, 'withAbsence' : withAbsence} 
            
        elif s_type == 'axmlt:role-statement':
            'Translate a role statement (name, sign, sub element for the xpath-atom, and a privilege).'
            role_name = s_e.childNodes[0].firstChild.nodeValue
            sign = s_e.childNodes[1].firstChild.nodeValue
            xpath_stat = s_e.childNodes[2]
            priv = s_e.childNodes[3].firstChild.nodeValue
            
            document = xpath_stat.childNodes[0].firstChild.nodeValue            
            xpath_exp = xpath_stat.childNodes[1].firstChild.nodeValue            

            o_s = {'type' : 'role', 'role_name' : role_name, 'sign' : sign, 'document' : document, 'xpath_exp' : xpath_exp, 'priv' : priv, 'withAbsence' : withAbsence} 
            
        return o_s
        
    '----------------------------------------------------------------------------------------------'       
        

    def expandXPath(self, x, d, ns_prefix='axmlt', ns_uri='scm.uws.edu.au'):
        '''Rewrites an XPath that contains predicates and wildcards into a fully static one.  A document must be specified to evaluate the XPath.
        Using libxml2 for XPath evaluation instead of xml.dom library.  We parse the XML document, set a namespace, and query it.
        For each result found, we will produce the respective XPath.  Each results represents the multiple paths that the original XPath denotes.'''
        
        'output XPath list'
        xl = []
        
        doc = libxml2.parseFile("xml_db/" + d + ".xml") #parse XML file, assume no extension and in folder 'xml_db'
        ctxt = doc.xpathNewContext() #set the context node
        ctxt.xpathRegisterNs(ns_prefix, ns_uri) #specify the XML Namespace being used

        'execute the XPath query and save the resulting list of XPaths'
        nl = ctxt.xpathEval(x)        

        'for each node in the list, recursively find the parent elements to build xpaths'
        for n in nl:
            cur_n = n
            newxp = '/' + cur_n.name
            
            while cur_n.parent.name != d:
                cur_n = cur_n.parent
                newxp = '/' + cur_n.name + newxp

            newxp = '/' + cur_n.parent.name + newxp

                
            xl.append(newxp)     
            
        ctxt.xpathFreeContext()
    	doc.freeDoc()
    	
    	'''remove duplicates from xpath list xl by turning it into a set and then back to a list.
    	HOWEVER, this goes against dynamic xpaths that point to repeated nodes with the same name.
    	This can be fixed by adding id's to each node and making them distinct.'''
    	xl = list(set(xl))
            
        return xl  
        
    '----------------------------------------------------------------------------------------------'

    def solvePB(self, alpfile):
        '''This will ground and solve (gringo/clasp) a translated policy base.'''        

        'ground'
        g = subprocess.Popen([r"./gringo", alpfile], stdout=subprocess.PIPE).communicate()[0] #0 is stdout, 1 is stderr
        
        'save the grounding to file'
        fh = open("ground", 'w+')
        fh.write(g)
        fh.close()
        
        'solve'
        ans = subprocess.Popen([r"./clasp", "ground"], stdout=subprocess.PIPE).communicate()[0]
        'save the answerset to file (debugging purposes)'
        fh = open("answerset", 'w+')
        fh.write(ans)
        fh.close()            
        
        'output the auth(orisation)s from the answer set'
        'use a regexp to find them'
        authre = re.compile(r'auth\(\w+?,\w+?,\w+?,\w+?,\w+?\)')
        m = authre.findall(ans)
        
        fh = open("auths", 'w+')
        for auths in m:
            fh.write(auths + "\n")
        
        fh.close()        
                                   
    '----------------------------------------------------------------------------------------------'
    
    def fixXPaths(self, alppb):
        '''This function is a quick fix for XPaths that cannot be used with gringo/clasp.  This is because
        the forward slash is not an acceptable character.  NOTE: that wildcards and predicates are not allowed as well
        but we shouldn't have that problem since we expand all our paths manually. See doco/comments in expandXPaths().'''
        
        fixed_alppb = list()
        
        for rule in alppb:
            fixed_alppb.append(rule.replace("/","_"))
        
        return fixed_alppb
        
    '----------------------------------------------------------------------------------------------'
    
    def fixWeakVariables(self, alppb):
        '''gringo/clasp is very strict about variable usage.  If it doesn't know what a possible 
        variable can be to a certain degree, it will report a "weakly restricted variables" error.
        To alleviate this, and hopefully avoid it in all possibilities, this function will search through each
        user created rule that uses variables and try to figure out what that possible variable is.  
        It will then introduce a new predicate statement for that variable to narrow its meaning down.'''
        
        '''use regexp to find variables, designated with a capital letter, but only in the body, not 
        head of the rule. for each found, modify the rule, pop off the old one, and replace it
        with the modified one.'''
                
        for rule in alppb:
        
            mod_rule = rule.rstrip('.')
            i = alppb.index(rule)        

            #'regular expression for roles, documents, and xpaths'
            #vre = re.compile(r':- role\(([A-Z]{1}\w*?),\w{2},(.*?),(.*?),')
            #if vre.search(rule):
            #    m = vre.search(rule)
                
            'regular expression for subject variables in grant statements'
            vre = re.compile(r'grant\(([A-Z]{1}\w*?),')
            matches = vre.findall(rule)
            if len(matches) != 0:               
                for m in matches:                    
                    if rule.find("subjects(" + m + ")") == -1 and mod_rule.find("subjects(" + m + ")") == -1: #dont add the predicate if it already exists
                        mod_rule += ", subjects(" + m + ")"

                    
            'regular expression for role variables in grant statements'
            vre = re.compile(r'grant\(\w*?,([A-Z]{1}\w*?),')
            matches = vre.findall(rule)
            if len(matches) != 0:                          
                for m in matches:                    
                    if rule.find("roles(" + m + ")") == -1 and mod_rule.find("roles(" + m + ")") == -1: #dont add the predicate if it already exists
                        mod_rule += ", roles(" + m + ")"

                
            'regular expression for interval variables in grant statements'
            vre = re.compile(r'grant\(\w*?,\w*?,([A-Z]{1}\w*?)\)')
            matches = vre.findall(rule)                
            if len(matches) != 0:
                for m in matches:                    
                    if rule.find("tempints(" + m + ")") == -1 and mod_rule.find("tempints(" + m + ")") == -1: #dont add the predicate if it already exists
                        mod_rule += ", tempints(" + m + ")"
           
               
            'regular expression for interval variables used in relationships'
            vre = re.compile(r'(during|starts|finishes|before|overlap|meets|equal)\(([A-Z]{1}\w*?),')
            matches = vre.findall(rule)
            if len(matches) != 0:
                for m in matches:              
                    if rule.find("tempints(" + m[1] + ")") == -1 and mod_rule.find("tempints(" + m[1] + ")") == -1: #dont add the predicate if it already exists
                         mod_rule += ", tempints(" + m[1] + ")"
                        
            'replace the old rule with the modified one if it was modified'
            if mod_rule == rule.rstrip('.'):
                continue #skip to next rule
            else:
                mod_rule += "."                   
                alppb.pop(i)
                alppb.insert(i, mod_rule)
                
                
      

    '------------------------------------END OF CLASS----------------------------------------------'        
        
########  SCRIPT BEGINNING  ########

    
        
p = PolicyBase('pb.xml')
#p.parseXMLPB()              #<-- THIS SHOULDNT BE HAPPENNING ALL THE TIME! MOVE TO INDIVIDUAL COMMANDS

'Handle Command Line Arguments Here'

if len(sys.argv) > 1:
    
    cmd = sys.argv[1]
    try:
        para = sys.argv[2]
    except:
        para = ""

    if cmd == 'addrules': #add rule(s) from XML file to PB
        p.parseXMLPB() 
        rulefile = para
        p.addRulesToPB(rulefile)
        p.writeXMLPB()
        
    elif cmd == 'translatepb': #translate the pb to alp and output to file
        p.parseXMLPB() 
        alppb = p.translatePBtoALP()
        alppb = p.fixXPaths(alppb) #fix xpaths for compatibility
        p.fixWeakVariables(alppb)  #fix weak variables
        p.writeALPPB("alp_policy_base.asp", alppb, "axmlt_language_rules.asp")
        
    elif cmd =='solve': #ground and solve the translated policy base
        p.solvePB("alp_policy_base.asp")
        
    elif cmd == 'deletepb': #clear the pb
        p.parseXMLPB()
        p.delRulesFromPB()
        p.writeXMLPB()
        
    elif cmd == 'deleterule': #delete a rule from the pb
        p.parseXMLPB()
        ruleindex = int(para)
        p.delRuleFromPB(ruleindex)
        p.writeXMLPB()
        
    else:
        print "command unknown"      
        









