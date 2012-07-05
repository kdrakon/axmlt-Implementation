roles(role0;role1;role2;role3;role4;role5;role6;role7;role8;role9).
subjects(subject0;subject1;subject2;subject3;subject4;subject5;subject6;subject7;subject8;subject9;subject10;subject11;subject12;subject13;subject14;subject15;subject16;subject17;subject18;subject19).
xpaths(doc2xpath0;doc3xpath0;doc0xpath0;doc0xpath1;doc1xpath0;doc1xpath1;doc4xpath0;doc4xpath1).
documents(doc0;doc1;doc2;doc3;doc4).
tempints(int0;int1;int2;int3;int4;int5;int6;int7;int8;int9;int10;int11;int12;int13;int14;int15;int16;int17;int18;int19).

role(role0,mm,doc0,doc0xpath1,read).
role(role0,pp,doc3,doc3xpath0,read).
role(role0,pp,doc4,doc4xpath1,read).
role(role1,mm,doc0,doc0xpath0,read).
role(role1,pp,doc1,doc1xpath0,read).
role(role1,pp,doc2,doc2xpath0,write).
role(role1,pp,doc4,doc4xpath1,read).
role(role2,mm,doc3,doc3xpath0,read).
role(role2,pp,doc3,doc3xpath0,read).
role(role2,pp,doc0,doc0xpath0,write).
role(role2,pp,doc4,doc4xpath0,write).
role(role3,pp,doc0,doc0xpath1,read).
role(role3,pp,doc0,doc0xpath0,read).
role(role3,pp,doc2,doc2xpath0,write).
role(role4,pp,doc0,doc0xpath1,write).
role(role4,pp,doc0,doc0xpath1,write).
role(role4,pp,doc2,doc2xpath0,read).
role(role4,mm,doc1,doc1xpath0,write).
role(role4,pp,doc1,doc1xpath0,read).
role(role5,pp,doc0,doc0xpath0,write).
role(role6,pp,doc2,doc2xpath0,read).
role(role6,mm,doc0,doc0xpath0,write).
role(role7,pp,doc3,doc3xpath0,read).
role(role8,pp,doc2,doc2xpath0,read).
role(role8,mm,doc4,doc4xpath1,read).
role(role9,pp,doc4,doc4xpath1,read).
role(role9,pp,doc3,doc3xpath0,read).
role(role9,pp,doc1,doc1xpath1,write).
role(role9,mm,doc1,doc1xpath1,write).
finishes(int8,int12).
before(int2,int8).
equal(int6,int14).
equal(int14,int19).
finishes(int1,int8).
finishes(int18,int15).
finishes(int0,int18).
overlap(int13,int17).
equal(int9,int16).
starts(int11,int9).
separate(role8,role6).
separate(role5,role2).
below(role3,role7).
separate(role8,role0).
separate(role9,role1).
below(role1,role6).
below(role5,role1).
separate(role4,role0).
separate(role2,role0).
separate(role9,role7).
grant(subject18,role6,int9).
grant(subject10,role5,int18).
grant(subject2,role4,int0).
grant(subject1,role6,int16).
grant(subject13,role8,int1).
grant(subject1,role8,int4).
grant(subject15,role6,int17).
grant(subject8,role1,int17).
grant(subject2,role6,int18).
grant(subject14,role7,int19).
grant(subject18,role0,int8).
grant(subject3,role6,int6).
grant(subject11,role6,int18).
grant(subject7,role8,int12).
grant(subject19,role8,int2).
grant(subject18,role5,int15).
grant(subject14,role7,int11).
grant(subject13,role9,int4).
grant(subject1,role7,int5).
grant(subject7,role4,int19).
grant(subject17,role1,int2).
grant(subject14,role5,int4).
grant(subject3,role4,int8).
grant(subject5,role8,int6).
grant(subject7,role5,int17).
grant(subject9,role2,int17).
grant(subject15,role3,int15).
grant(subject2,role4,int10).
grant(subject18,role6,int17).
grant(subject12,role8,int8).
grant(subject15,role9,int3).
grant(subject9,role0,int14).
grant(subject14,role6,int0).
grant(subject8,role1,int3).
grant(subject8,role0,int4).
grant(subject15,role6,int7).
grant(subject18,role2,int13).
grant(subject1,role8,int4).
grant(subject2,role1,int11).
grant(subject5,role1,int7).
grant(subject7,role2,int17):-separate(role7,role2),not grant(subject12,role0,int17).
grant(subject15,role6,int7):-grant(subject18,role7,int6),not grant(subject9,role4,int3).
grant(subject4,role2,int12):-grant(subject13,role1,int1).
grant(subject19,role2,int7):-grant(subject14,role4,int18),not grant(subject8,role3,int6).
grant(subject15,role0,int7):-overlap(int18,int7),not grant(subject19,role7,int1).
grant(subject12,role3,int1):-below(role2,role3),not grant(subject3,role8,int13).
grant(subject17,role1,int17):-starts(int6,int17),not starts(int6,int17).
grant(subject10,role7,int11):-separate(role6,role7),not grant(subject11,role1,int15).
grant(subject4,role6,int14):-grant(subject0,role5,int14),not equal(int3,int14).
grant(subject11,role2,int3):-grant(subject7,role0,int18),not grant(subject17,role2,int12).

%-----------------------------------------------------------------------------------------------------------------------
%CONSTANTS
%-----------------------------------------------------------------------------------------------------------------------

signs(pp; mm).
privs(read; write).

%-----------------------------------------------------------------------------------------------------------------------
%LANGUAGE RULES
%-----------------------------------------------------------------------------------------------------------------------

%RBAC RELATIONSHIPS

%role hierarchy implication
below(A,C) :- below(A,B), below(B,C), roles(A), roles(B), roles(C).
:- below(A, B), not roles(A), not roles(B).

brole(X, SIGNY, DOCUMENTY, XPATHY, PRIVILEGEY) :- below(X, Y), roles(X), roles(Y), role(X, SIGNX, DOCUMENTX, XPATHX, PRIVILEGEX), role(Y, SIGNY, DOCUMENTY, XPATHY, PRIVILEGEY), signs(SIGNX), signs(SIGNY), privs(PRIVILEGEX), privs(PRIVILEGEY), documents(DOCUMENTX), documents(DOCUMENTY), xpaths(XPATHX), xpaths(XPATHY).

%conflict resolution rule
exist_neg(SUBJECT, DOCUMENT, XPATH, PRIVILEGE, INTERVAL) :- grant(SUBJECT, ROLENAME, INTERVAL), role(ROLENAME, mm, DOCUMENT, XPATH, PRIVILEGE), privs(PRIVILEGE), tempints(INTERVAL).

%separation of duty relationship
separate(X, Y) :- separate(Y, X), roles(X), roles(Y).

%separation of duty rule
sepduty_fail(SUBJECT) :- grant(SUBJECT, ROLEX, INTERVALA), grant(SUBJECT, ROLEY, INTERVALB), tempints(INTERVALA), tempints(INTERVALB), roles(ROLEX), roles(ROLEY), separate(ROLEX, ROLEY).

%nonexistent role granting
:- grant(SUBJECT, ROLE, INTERVAL), not roles(ROLE).

%-----------------------------------------------------------------------------------------------------------------------

%THE AUTHORISATION RULE

%authorisation of subjects with roles with conflict resolution and separation of duty
auth(SUBJECT, DOCUMENT, XPATH, PRIVILEGE, INTERVAL) :- grant(SUBJECT, ROLE, INTERVAL), subjects(SUBJECT), role(ROLE, SIGN, DOCUMENT, XPATH, PRIVILEGE), privs(PRIVILEGE), signs(SIGN), not exist_neg(SUBJECT, DOCUMENT, XPATH, PRIVILEGE, INTERVAL), not sepduty_fail(SUBJECT).

auth(SUBJECT, DOCUMENT, XPATH, PRIVILEGE, INTERVAL) :- grant(SUBJECT, ROLE, INTERVAL), subjects(SUBJECT), brole(ROLE, SIGN, DOCUMENT, XPATH, PRIVILEGE), privs(PRIVILEGE), signs(SIGN), not exist_neg(SUBJECT, DOCUMENT, XPATH, PRIVILEGE, INTERVAL), not sepduty_fail(SUBJECT).


%-----------------------------------------------------------------------------------------------------------------------

%TEMPORAL INTERVAL RELATIONSHIPS AND IMPLICATIONS

%temporal interval containment rule
grant(SUBJECT, ROLE, INTERVALB) :- grant(SUBJECT, ROLE, INTERVALA), during(INTERVALB, INTERVALA), roles(ROLE), tempints(INTERVALA), tempints(INTERVALB), subjects(SUBJECT).

%implicit relationships (for containment)
during(A, B) :- starts(A, B), tempints(A), tempints(B).
during(A, B) :- finishes(A, B), tempints(A), tempints(B).
before(A, B) :- meets(A, B), tempints(A), tempints(B).

before(A, C) :- before(A, B), before(B, C), tempints(A), tempints(B), tempints(C).
during(A, C) :- during(A, B), during(B, C), tempints(A), tempints(B), tempints(C).
starts(A, C) :- starts(A, B), starts(B, C), tempints(A), tempints(B), tempints(C).
finishes(A, C) :- finishes(A, B), finishes(B, C), tempints(A), tempints(B), tempints(C).
equal(A, C) :- equal(A, B), equal(B, C), tempints(A), tempints(B), tempints(C).

%classically negated rules
-before(A, B) :- during(A, B), tempints(A), tempints(B).
-overlap(A, B) :- during(A, B), tempints(A), tempints(B).
-meets(A, B) :- during(A, B), tempints(A), tempints(B).
-equal(A, B) :- during(A, B), tempints(A), tempints(B).

-during(A, B) :- before(A, B), tempints(A), tempints(B).
-during(A, B) :- overlap(A, B), tempints(A), tempints(B).
-during(A, B) :- meets(A, B), tempints(A), tempints(B).
-during(A, B) :- equal(A, B), tempints(A), tempints(B).

-before(A, B) :- overlap(A, B), tempints(A), tempints(B).
-meets(A, B) :- overlap(A, B), tempints(A), tempints(B).
-equal(A, B) :- overlap(A, B), tempints(A), tempints(B).

-overlap(A, B) :- before(A, B), tempints(A), tempints(B).
-equal(A, B) :- before(A, B), tempints(A), tempints(B).

-equal(A, B) :- meets(A, B), tempints(A), tempints(B).
-overlap(A, B) :- meets(A, B), tempints(A), tempints(B).

-before(A, B) :- equal(A, B), tempints(A), tempints(B).
-overlap(A, B) :- equal(A, B), tempints(A), tempints(B).
-meets(A, B) :- equal(A, B), tempints(A), tempints(B).

:- -during(A, B), during(A, B), tempints(A), tempints(B).
:- -before(A, B), before(A, B), tempints(A), tempints(B).
:- -overlap(A, B), overlap(A, B), tempints(A), tempints(B).
:- -meets(A, B), meets(A, B), tempints(A), tempints(B).
:- -equal(A, B), equal(A, B), tempints(A), tempints(B).

%bounded temporal interval rule
during(D, A) :- starts(B, A), finishes(C, A), before(B, D), before(D, C), tempints(A), tempints(B), tempints(C), tempints(D).

%equality rules
during(C, B) :- equal(A, B), during(C, A), tempints(A), tempints(B), tempints(C).
starts(C, B) :- equal(A, B), starts(C, A), tempints(A), tempints(B), tempints(C).
finishes(C, B) :- equal(A, B), finishes(C, A), tempints(A), tempints(B), tempints(C).
before(C, B) :- equal(A, B), before(C, A), tempints(A), tempints(B), tempints(C).
overlap(C, B) :- equal(A, B), overlap(C, A), tempints(A), tempints(B), tempints(C).
meets(C, B) :- equal(A, B), meets(C, A), tempints(A), tempints(B), tempints(C).


%-----------------------------------------------------------------------------------------------------------------------

