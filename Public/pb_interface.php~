<?php

/**************************************************************************************************/

    class pb_interface{
        
        /*
        This class provides an interface with pb_mgr.py
        It will take input from the user a POST to decide what kind of input
        should be accepted from the user.  
        */
        
        //this is an empty skeleton for the pb rule which will be sent to pb_mgr.py    
        public $xmlRule = "<axmlt:policybase xmlns:axmlt=\"scm.uws.edu.au\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:schemaLocation=\"scm.uws.edu.au axmlt_policybase.xsd\"><axmlt:rule></axmlt:rule></axmlt:policybase>";        
        


/**************************************************************************************************/

        public function addRuleToPB(){
            //add a rule to the pb via pb_mgr.py        
            
            //convert the single dimension post array into a 2 dimension representing the statements in the rules.
            foreach (array_keys($_POST) as $i){
                //split the post key into an id and attribute
                $split_i = preg_split("/_/", $i);
                //save into the 2 dimension hash $rule
                $rule[$split_i[0]][$split_i[1]] = $_POST[$i];                    
                                
            }        
    
            //process each statement in the rule individually. the first rule is always the head
            //while the rest are the body, with 'negated' rules indicated with the attribute 'withAbsence = true'.
        
            //re-write the head statement as an axmlt head statement
            $this->writeStatementAsXML($rule[1], "head");
        
            //now re-write the body statements. start from 2 to length of $rule (which is the number of statements in the rule).
            for ($x = 2; $x <= count($rule); $x++){
                $this->writeStatementAsXML($rule[$x], "body");                
            }
            
            //with the XML rule complete, we can write it out to a temp file for validation using xmllint
            $xmlf = fopen("newRule.xml", "w+");
            fwrite($xmlf, $this->xmlRule);
            fclose($xmlf);
            
            system("xmllint --noout --schema axmlt_policybase.xsd newRule.xml", $retVal);
            //if the returned value is not 0, then something is invalid according to the schema
            if ($retVal){
                print "error: rule does not validate with schema.";
            }else{                
                //pass the rule to pb_mgr.py
                system("./pbMan addrules newRule.xml");                
            }

            
        
        }

/**************************************************************************************************/
        
        public function writeStatementAsXML($s, $loc){
        
            //writes a statement from the interface as an xml statement to be added to the pb
  
            //using PHP's SimpleXML lib, we can append new elements to the XML string easily
            $simpXML = new SimpleXMLElement($this->xmlRule);
            $rule = $simpXML->children("axmlt", TRUE);

            //start the XML string for the statement
            if ($loc == "head"){
                $xmlStat = $rule->addChild("axmlt:head-statement");
            }else if ($loc == "body"){
                $xmlStat = $rule->addChild("axmlt:body-statement");
            }
            
            //check if the statement should be 'with absence'
            if ($s['withAbsence'] == 'true'){
                $xmlStat->addAttribute('withAbsence', 'true');
            }
                        
            //now translate the statement based on its type and add the appropriate xml elements
            if ($s['statType'] == 'role'){
                
                $rs = $xmlStat->addChild("axmlt:role-statement");
                $rs->addChild("axmlt:role-name", $s['roleName']);
                $rs->addChild("axmlt:sign", $s['sign']);
                
                $xs = $rs->addChild("axmlt:xpath-statement");
                $xs->addChild("axmlt:document-name", $s['document']);
                $xs->addChild("axmlt:xpath-expression", $s['xpath']);   
                
                $rs->addChild("axmlt:privilege", $s['privilege']);               
                
            }else if ($s['statType'] == 'grant'){
            
                $gs = $xmlStat->addChild("axmlt:grant-statement");
                $gs->addChild("axmlt:role-name", $s['roleName']);
                $gs->addChild("axmlt:subject", $s['subject']);
                $gs->addChild("axmlt:temporal-interval", $s['interval']);                
            
            }else if ($s['statType'] == 'relationship'){
            
                $rs = $xmlStat->addChild("axmlt:relationship-statement");
                $rv = $rs->addChild("axmlt:" . $s['relationshipType']);
                $rv->addChild("axmlt:value1", $s['value1']);
                $rv->addChild("axmlt:value2", $s['value2']);           
            
            }
            
            //overwrite the unchanged XML with the new one
            $this->xmlRule = $simpXML->asXML();          
        
        }
        
/**************************************************************************************************/
        
        
        public function printXMLPolicyBase($pbfile){
            //This function will print the rules from the policy base XML document in proper AXMLT syntax
            $outputpb = "";
            
            //open the document for reading/parsing
            $xmlpb = simplexml_load_file($pbfile);

            //get all the rules from the pb
            $rules = $xmlpb->children("axmlt", true);            
           
            //process and print each rule in axmlt syntax
            $ruleIndex = 0;
            foreach( $rules as $curRule ){
                
                $ruleIndex++;   
               
                //output the head statements
                $headstats = $curRule->xpath('axmlt:head-statement');
               
                foreach($headstats as $stat){
                   
                    //find all possible statement types in current statement
                    $rolestats = $stat->xpath('axmlt:role-statement');
                    $grantstats = $stat->xpath('axmlt:grant-statement');    
                    $relatestats = $stat->xpath('axmlt:relationship-statement');                                    

                    if (count($rolestats) > 0) { //output role-statement

                        $roleelements = $rolestats[0]->children("axmlt", true);
                        $xpathstat = $roleelements[2]->children("axmlt", true);
                        
                        $outputpb .= "admin creates role(" . $roleelements[0] . ", " . $roleelements[1] . ", in " . $xpathstat[0] . ", return " . $xpathstat[1] . ", " . $roleelements[3] . ")";


                    }else if (count($grantstats) > 0){ //output grant statement

                        $grantelements = $grantstats[0]->children("axmlt", true);
                        
                        $outputpb .= "admin grants " . $grantelements[0]. " to " . $grantelements[1] . " during " . $grantelements[2];
                        
                    }else if (count($relatestats) > 0){ //output relate statement

                        $relationshiptype = $relatestats[0]->children("axmlt", true);
                        
                        $rfixed = $relationshiptype->asXML();
                        $rfixed = str_replace("value1", " ", $rfixed);
                        $rfixed = str_replace("value2", " ", $rfixed);
                        $rfixed = str_replace("<", " ", $rfixed);                        
                        $rfixed = str_replace(">", " ", $rfixed);                                                
                        $rfixed = str_replace("/", " ", $rfixed);                                                
                        $rfixed = str_replace("axmlt:", " ", $rfixed);

                        $rfixed = trim($rfixed);

                        $relateelements = explode(" ", $rfixed);
                        
                        $outputpb .= "admin says " .  $relateelements[0] . "(";
                        
                        $pc = 0; //print count
                        for($x = 1; $x < count($relateelements) - 1; $x++){
                            if (trim($relateelements[$x]) != "" && trim($relateelements[$x]) != null){
                                $outputpb .= $relateelements[$x];
                                $pc++;
                                if ($pc == 1) $outputpb .= ", ";
                                
                            }                            
                        }
                        
                        $outputpb .= ")";                        

                    }
                   
                }
                
                //done with head statements, now start with body after outputting proper syntax
                $outputpb .= " :- ";
                
                //output the body statements
                $bodystats = $curRule->xpath('axmlt:body-statement');
                
                
                foreach($bodystats as $stat){         
                    
                
                    //first, determine is the a 'with absence' statement
                    $bodyAttribs = $stat->attributes();

                    foreach($bodyAttribs as $atr => $val){
                        if ($atr == "withAbsence" && $val == "true"){
                            $outputpb .= " with absence ";
                        }
                    }
                    
                    //find all possible statement types in current statement
                    $rolestats = $stat->xpath('axmlt:role-statement');
                    $grantstats = $stat->xpath('axmlt:grant-statement');    
                    $relatestats = $stat->xpath('axmlt:relationship-statement');                                    

                    if (count($rolestats) > 0) { //output role-statement

                        $roleelements = $rolestats[0]->children("axmlt", true);
                        $xpathstat = $roleelements[2]->children("axmlt", true);
                        
                        $outputpb .= "admin creates role(" . $roleelements[0] . ", " . $roleelements[1] . ", in " . $xpathstat[0] . ", return " . $xpathstat[1] . ", " . $roleelements[3] . ")";


                    }else if (count($grantstats) > 0){ //output grant statement

                        $grantelements = $grantstats[0]->children("axmlt", true);
                        
                        $outputpb .= "admin grants " . $grantelements[0]. " to " . $grantelements[1] . " during " . $grantelements[2];
                        
                    }else if (count($relatestats) > 0){ //output relate statement

                        $relationshiptype = $relatestats[0]->children("axmlt", true);
                        
                        $rfixed = $relationshiptype->asXML();
                        $rfixed = str_replace("value1", " ", $rfixed);
                        $rfixed = str_replace("value2", " ", $rfixed);
                        $rfixed = str_replace("<", " ", $rfixed);                        
                        $rfixed = str_replace(">", " ", $rfixed);                                                
                        $rfixed = str_replace("/", " ", $rfixed);                                                
                        $rfixed = str_replace("axmlt:", " ", $rfixed);

                        $rfixed = trim($rfixed);

                        $relateelements = explode(" ", $rfixed);
                        
                        $outputpb .= "admin says " .  $relateelements[0] . "(";
                        
                        $pc = 0; //print count
                        for($x = 1; $x < count($relateelements) - 1; $x++){
                            if (trim($relateelements[$x]) != "" && trim($relateelements[$x]) != null){
                                $outputpb .= $relateelements[$x];
                                $pc++;
                                if ($pc == 1) $outputpb .= ", ";
                                
                            }                            
                        }
                        
                        $outputpb .= ")";                        

                    }
                    
                    //append comma after each statement
                    $outputpb .= ", ";                   
                }
                
                //we are at the end of a rule, so replace the final comma or other nonrequired chars with period and append a newline
                //also append an html link to delete the rule
                $outputpb = rtrim($outputpb, ":-, ");
                $outputpb .= ". <a href=\"" . $_SERVER['PHP_SELF'] . "?deletei=$ruleIndex\">[X]</a>\n";                
               
            }
            
            //return the pb string
            return $outputpb;        
        
        }
        
/**************************************************************************************************/      

        public function printAuthorisations(){
            //prints the computed authorsations from the auth file
            
            $fh = fopen("auths", 'r');
            
            while (!feof($fh)){
                print fgets($fh) . "<br>";
            }
            
            fclose($fh);
        
        }        
        
/**************************************************************************************************/      

        public function deleteRuleFromPB($deletei){        
            //delete a rule based on its index
            system("./pbMan deleterule $deletei");        
        }

/**************************************************************************************************/  

        public function deletePB(){        
            //delete all rules
            system("./pbMan deletepb");        
        }
        
/**************************************************************************************************/  

        public function translatePB(){        
            system("./pbMan translatepb");       
        }    
        
/**************************************************************************************************/  

        public function computeAuths(){
            system("./pbMan solve");        
        }            

/**************************************************************************************************/ 

        public function validateQuery(){
            //validate the entered query against the authorisations in the file
            
            $fh = fopen("auths", 'r');
            
            //create alp query statement from input from user
            $query = "auth(" . $_GET['subject'] . "," . $_GET['document'] . "," . $_GET['xpath'] . "," . $_GET['privilege'] . "," . $_GET['interval'] . ")";

            while (!feof($fh)){
                $auth = trim(fgets($fh));
                if (strcmp($query,$auth) == 0){
                    print "auth found: " . $auth . "<br>";
                }
                
            }
            
            fclose($fh);
            
        }

/**************************************************************************************************/                                                                                                             
        
    } //end of class

/**************************************************************************************************/
/** BEGIN PROCEDURAL PROGRAM **/

    $pbi = new pb_interface();

    //check if POST has anything, usually meaning that we have a new rule to add to the pb
    #if ($_POST){
    #    $pbi->addRuleToPB();
    #}
    
    if ($_GET || $_POST){
        if (isset($_GET['deletei'])){
            $pbi->deleteRuleFromPB($_GET['deletei']);

        }else if (isset($_GET['delete'])){
            $pbi->deletePB();
                
        }else if (isset($_GET['translate'])){
            $pbi->translatePB();
        
        }else if (isset($_GET['compute'])){
            $pbi->computeAuths();
            
        }else if (isset($_GET['query'])){
            $pbi->validateQuery();            
            
        }else if ($_POST){
            $pbi->addRuleToPB();
        
        }
        
    }
    


/**************************************************************************************************/
?>

<html>

    <head>
    
        <script type="text/javascript">

            //add a new statement input to either the head or body
            function addAXMLTStatement(loc, type, relationshipType){
            
                
                //this is a counter to differentiate all the inputs
                if ( typeof statCounter == 'undefined' ) {
                        // It has not... perform the initilization
                        statCounter = 0;
                }                
                statCounter++; //increment with each function call
                
                
                //where to add the new statement to: head or body
                e = document.getElementById(loc);
                
                //append a hidden input if the statement is meant to be with absence (based on loc)
                newElems = document.createElement('input');
                newElems.setAttribute('type', 'hidden');
                newElems.setAttribute('name', statCounter + '_withAbsence');
                if (loc == "neg-body"){
                    newElems.setAttribute('value', 'true');
                }else{
                    newElems.setAttribute('value', 'false');
                }
                e.appendChild(newElems);      
                
                //append a hidden input to state what kind of statement this is
                newElems = document.createElement('input');
                newElems.setAttribute('type', 'hidden');
                newElems.setAttribute('name', statCounter + '_statType');
                newElems.setAttribute('value', type);
                e.appendChild(newElems);                                
                          
                  
                //create the statement input based on type
                if (type == "role"){                   
                
                    //some language syntax
                    e.appendChild(document.createTextNode("admin creates role("));
                    
                    //the role name
                    newElems = document.createElement('input');
                    newElems.setAttribute('type', 'text');
                    newElems.setAttribute('name', statCounter + '_roleName');
                    e.appendChild(newElems);
                    
                    e.appendChild(document.createTextNode(", "));      
                    
                    //the sign
                    newElems = document.createElement('select');
                    newElems.setAttribute('name', statCounter + '_sign');
                        newSubElems = document.createElement('option');
                        newSubElems.setAttribute('value', "pp");
                        newSubElems.innerHTML = "+";                               
                    newElems.appendChild(newSubElems);
                        newSubElems = document.createElement('option');
                        newSubElems.setAttribute('value', "mm");
                        newSubElems.innerHTML = "-";                
                    newElems.appendChild(newSubElems);
                    e.appendChild(newElems);
                    
                    e.appendChild(document.createTextNode(", "));      
                    
                    e.appendChild(document.createTextNode("in "));
                    
                    //xml document
                    newElems = document.createElement('input');
                    newElems.setAttribute('type', 'text');
                    newElems.setAttribute('name', statCounter + '_document');
                    e.appendChild(newElems);  
                    
                    e.appendChild(document.createTextNode(".xml, return "));              
                    
                    //xpath expression
                    newElems = document.createElement('input');
                    newElems.setAttribute('type', 'text');
                    newElems.setAttribute('name', statCounter + '_xpath');
                    e.appendChild(newElems);
                    
                    e.appendChild(document.createTextNode(", "));      
                    
                    //privilege
                    newElems = document.createElement('select');
                    newElems.setAttribute('name', statCounter + '_privilege');
                        newSubElems = document.createElement('option');
                        newSubElems.setAttribute('value', "read");
                        newSubElems.innerHTML = "read";                               
                    newElems.appendChild(newSubElems);
                        newSubElems = document.createElement('option');
                        newSubElems.setAttribute('value', "write");
                        newSubElems.innerHTML = "write";                
                    newElems.appendChild(newSubElems);
                    e.appendChild(newElems); 
                    
                    e.appendChild(document.createTextNode(")"));      
                              

                }else if(type == "relationship"){
                
                    //some language syntax
                    e.appendChild(document.createTextNode("admin says "));
                    
                    //relationship type
                    e.appendChild(document.createTextNode(relationshipType + "("));
                    //send the relationship type as a hidden form element
                    newElems = document.createElement('input');
                    newElems.setAttribute('type', 'hidden');
                    newElems.setAttribute('name', statCounter + '_relationshipType');                
                    newElems.setAttribute('value', relationshipType);
                    e.appendChild(newElems);
                    
                    //tuple value 1
                    newElems = document.createElement('input');
                    newElems.setAttribute('name', statCounter + '_value1');                  
                    newElems.setAttribute('type', 'text');
                    e.appendChild(newElems);
                    
                    e.appendChild(document.createTextNode(", "));    
                    
                    //tuple value 2
                    newElems = document.createElement('input');
                    newElems.setAttribute('name', statCounter + '_value2');                  
                    newElems.setAttribute('type', 'text');
                    e.appendChild(newElems);       
                    
                    e.appendChild(document.createTextNode(")"));                                         
                    
                
                }else if(type == "grant"){
                
                    //some language syntax
                    e.appendChild(document.createTextNode("admin grants "));
                    
                    //role name
                    newElems = document.createElement('input');
                    newElems.setAttribute('type', 'text');
                    newElems.setAttribute('name', statCounter + '_roleName');                
                    e.appendChild(newElems);
                    
                    e.appendChild(document.createTextNode(" to "));                
                    
                    //subject
                    newElems = document.createElement('input');
                    newElems.setAttribute('name', statCounter + '_subject');                  
                    newElems.setAttribute('type', 'text');
                    e.appendChild(newElems);
                    
                    e.appendChild(document.createTextNode(" during "));    
                    
                    //temporal interval
                    newElems = document.createElement('input');
                    newElems.setAttribute('name', statCounter + '_interval');                  
                    newElems.setAttribute('type', 'text');
                    e.appendChild(newElems);       
                    
                
                }
                
                
                
              
                
            }
            
        </script>
        
        <style type="text/css">
            
            .control{ cursor: pointer; color: blue; }
            
            span.hstatement{ color: green; }
            span.bstatement{ color: blue; }
            span.nbstatement{ color: red; }
                     
            div{border-style: none; width:1000px; padding:10px; background-color:pink}
            
            div.innerbox{ width: 1000px; background-color:lightgrey;}
            
          
        </style>            
    
    </head>


    <body>
    
            <div><img src="http://www.uws.edu.au/__data/assets/image/0007/74797/logo_top.png"/></div>
            
            <div>Prototype Implementation of A<sup>xml(T)</sup></div>
            
            <div class="innerbox">
                <a href="<?php print $_SERVER['PHP_SELF']; ?>">Refresh Page</a> | <a href="<?php print $_SERVER['PHP_SELF']; ?>?translate=y">Translate Policy Base</a> | <a href="<?php print $_SERVER['PHP_SELF']; ?>?compute=y">Compute Authorisations</a> | <a href="<?php print $_SERVER['PHP_SELF']; ?>?delete=y">Delete Policy Base</a>
            </div>              
            
            <div class="innerbox">
                <span style="color: blue;">New Rule:</span>
                <form action="pb_interface.php" method="post">

                    <span id="head" class="hstatement">[</span>  <span id="pos-body" class="bstatement"> <span class="hstatement"> ] </span> [ :- </span> <span id="neg-body" class="nbstatement"> ][with absence </span> <span class="nbstatement"> ]. </span> 
                    
                    <input type="submit" value="Add Rule">    

                </form>            
            
                <div style="font-size:9pt; width: 475px; display: table-cell">
                    <span style="font-size:12pt; color: blue;">Rule Entry:</span>
                    <div style="width: 475px">
                        <form name="locControls">
                            Add statement to                
                            <select name="loc">
                                <option value="head">head
                                <option value="pos-body">body
                                <option value="neg-body">with absence
                            </select>
                        <form>            
                    </div>
                
                    <div style="font-size:9pt; width: 475px">
                        
                        Select A<sup>xml(T)</sup> statement:            
                        <ul>

                            <li class="control" onClick="addAXMLTStatement(document.locControls.loc.options[document.locControls.loc.selectedIndex].value, 'role')">
                                admin creates role( &lt;role-name&gt;, &lt;sign&gt;, in &lt;document&gt;, return &lt;xpath&gt;, &lt;privilege&gt; )
                            </li
                            
                            <li class="control" onClick="addAXMLTStatement(document.locControls.loc.options[document.locControls.loc.selectedIndex].value, 'grant')">
                                admin grants &lt;role-name&gt; to &lt;subject&gt; during &lt;interval&gt;
                            </li>              
                        
                            <li class="control" onClick="addAXMLTStatement(document.locControls.loc.options[document.locControls.loc.selectedIndex].value, 'relationship', 'below')">
                                admin says below( &lt;role-name&gt;, &lt;role-name&gt; )
                            </li>
                            
                            <li class="control" onClick="addAXMLTStatement(document.locControls.loc.options[document.locControls.loc.selectedIndex].value, 'relationship', 'separate')">
                                admin says separate( &lt;role-name&gt;, &lt;role-name&gt; )
                            </li>                    
                            
                            <li class="control" onClick="addAXMLTStatement(document.locControls.loc.options[document.locControls.loc.selectedIndex].value, 'relationship', 'during')">
                                admin says during( &lt;interval&gt;, &lt;interval&gt; )
                            </li>  
                            
                            <li class="control" onClick="addAXMLTStatement(document.locControls.loc.options[document.locControls.loc.selectedIndex].value, 'relationship', 'starts')">
                                admin says starts( &lt;interval&gt;, &lt;interval&gt; )
                            </li>                      
                            
                            <li class="control" onClick="addAXMLTStatement(document.locControls.loc.options[document.locControls.loc.selectedIndex].value, 'relationship', 'finishes')">
                                admin says finishes( &lt;interval&gt;, &lt;interval&gt; )
                            </li>
                            
                            <li class="control" onClick="addAXMLTStatement(document.locControls.loc.options[document.locControls.loc.selectedIndex].value, 'relationship', 'before')">
                                admin says before( &lt;interval&gt;, &lt;interval&gt; )
                            </li>                                
                            
                            <li class="control" onClick="addAXMLTStatement(document.locControls.loc.options[document.locControls.loc.selectedIndex].value, 'relationship', 'overlap')">
                                admin says overlap( &lt;interval&gt;, &lt;interval&gt; )
                            </li>      
                            
                            <li class="control" onClick="addAXMLTStatement(document.locControls.loc.options[document.locControls.loc.selectedIndex].value, 'relationship', 'meets')">
                                admin says meets( &lt;interval&gt;, &lt;interval&gt; )
                            </li>                          
                            
                            <li class="control" onClick="addAXMLTStatement(document.locControls.loc.options[document.locControls.loc.selectedIndex].value, 'relationship', 'equal')">
                                admin says equal( &lt;interval&gt;, &lt;interval&gt; )
                            </li>                     
                                        
                        </ul>
                            
                    </div>   
                    
                </div> 
                
                <div style="width: 500px; display: table-cell">
                    <span style="color: blue;">Policy Base:</span>
                    <table style="font-size:11px;">
                    <tr><td>
                    <?php 
                        $pb = $pbi->printXMLPolicyBase('pb.xml'); 
                        $pb = str_replace("\n", "</td></tr>\n<tr><td>\n", $pb); 
                        print $pb;
                    ?>
                    </td></tr>
                    </table>
                </div>
                
                <div style="display: table-row">                    
                    
                    <div style="font-size:9pt; width: 500px;">
                        <span style="font-size:12pt; color: blue;">Query Test:</span>
                        <br>
                        
                        <form action="pb_interface.php" method="get">
                        
                            Does <input type="text" name="subject"/> have <select name="privilege"><option value="read">read<option value="write">write</select> 
                            rights to <input type="text" name="xpath"/> in document <input type="text" name="document"/> during <input type="text" name="interval"/> ?
                            
                            <input type="hidden" name="query" value="y">
                            <input type="submit" value="Validate">                           
                            
                        </form>
                        
                    </div>
                    
                </div>               
        
            
        </div>   <!-end of rule entry div-->   
        
        
         
        
   


    </body>

</html>

