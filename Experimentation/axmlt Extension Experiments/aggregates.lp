c(1..100).

enum(X, Y, J) :- grant(X, Y, Z), subject(X), roles(Y), tempints(Z), not -enum(X, Y, J), c(J).
-enum(X, Y, J) :- enum(X, Y, K), J != K, c(J), c(K), subject(X), roles(Y).
-enum(X, Y, J) :- enum(Z, Y, J), X != Z, subject(X), subject(Z), roles(Y), c(J).

one is assigned(Y) :- enum(X, Y, 1), subject(X), roles(Y).
:- grant(X, Y, Z), not one is assigned(Y), subject(X), roles(Y), tempints(Z).

numbered(Y, J) :- enum(X, Y, J), subject(X), roles(Y), c(J).
:- numbered(Y, J+1), not numbered(Y, J), J>=1, c(J), roles(Y).

card(Y, Q) ← numbered(Y, Q), not numbered(Y, Q+1), roles(Y), c(Q).

