//////////////////////////////////////////////////////////////////////
//
// First-Order Logic Package (Theorem Proving Examples)
//
// Class:  Example
// Author: Scott Sanner (ssanner@cs.toronto.edu)
// Date:   12/2/04
//
// TODO:
// -----
//
//////////////////////////////////////////////////////////////////////

package logic.kb.fol;

import java.io.*;
import java.text.*;
import java.util.*;
import logic.kb.*;
import logic.kb.fol.kif.*;

public class Example1 {

    static String query_string;

    public static DecimalFormat _df = new DecimalFormat("0.##");

    public static void main(String args[]) {
//	query_string = args[0];
	/*	System.out.println("\nUsing Otter theorem prover:");
	System.out.println("---------------------------");
	DoExample(new OtterKb("Examples" /* Just a kb name of your choice ));

	System.out.println("Using Vampire theorem prover:");
	System.out.println("-----------------------------");
*/
	DoExample(new CachingKb(new VampireKb(false, 5.0f /* Time limit of 5 seconds */)));

	// These are Java-based theorem provers, they are not very efficient
	// and I doubt anyone would find them useful unless they need to
	// retrieve parameter bindings.
	// DoExample(new ClauseKb(MAX_RES));
	// DoExample(new DemodClauseKb(MAX_RES));
	// DoExample(new CachingKb(new ClauseKb(MAX_RES))); // Caches results for reuse
    }

    public static void DoExample(Kb kb) {

	// To add an entire file of FOPC-style assertions, we could use
    //    kb.addAllFOPCFormula(FOPC.parseFile(filename))
    // To add an entire file of KIF assertions, we could use
    //    kb.addAllFOPCFormula(KIFParser.parseFile(filename))
    	
    // Here we add KB assertions one by one.  We'll add the first 
    // two assertions in KIF syntax by using KIFParser.parse(.) to 
    // parse its argument from KIF and return a FOPC.Node. 
    	
	// The following is the same as
    //    kb.addFOPCFormula("!A ?x cat(?x) => animal(?x)");
	//	kb.addFOPCFormula(KIFParser.parse("(FORALL (?x) (=> (cat ?x) (animal ?x)))"));
	// The following is the same as
	//    kb.addFOPCFormula("!A ?x blackAndCat(?x) <=> cat(?x) ^ black(?x)");
	//	kb.addFOPCFormula(KIFParser.parse("(FORALL (?x) (<=> (blackAndCat ?x) (and (cat ?x) (black ?x))))"));
	
	// The rest we'll add in standard FOPC syntax... we could call
	// FOPC.parse(.) to convert them to a FOPC.Node but KB will 
	// automatically parse them as FOPC if given a String.

//	kb.addFOPCFormula("!A ?x !A ?y vat(?x) ^ vat(?y) => ?x=?y");
	
//	kb.addFOPCFormula("vat(b) ^ road(a,b) ^ road(b,a) ^ nft ^ ~hs ^ sin(a)");    
    	kb.addFOPCFormula("!A ?x p(?x) => q(?x)");
    	kb.addFOPCFormula("!A ?x (q(?x) ^ (!E ?y r(?y , ?x)) => s(?x))");    
    	kb.addFOPCFormula("p(a)");    
    	kb.addFOPCFormula("r(b,a)");    
    	QueryKb(kb, "!E ?z r(?z, a)");
//    	kb.addFOPCFormula("");
    	
	// Now query the knowledge base
	System.out.println();
//		QueryKb(kb, "!E ?x vat(?x) ^ road(?x,a) ^ nft");
//		QueryKb(kb, "!E ?z p(?z) => ~(~(!E ?x !E ?y p(?x) ^ q(?y)) ^ ~(!E ?x !E ?y p(?x) ^ ~q(?y)))");
//	QueryKb(kb, "!E ?x !E ?y p(?x) ^ q(?y) => !E ?z p(?z)");
//	QueryKb(kb, KIFParser.parse("(or (EXISTS (?x) EXISTS (?y) (and (p ?x) (q ?y))) (EXISTS (?x) EXISTS (?y) (and (p ?x) (not (q ?y)))))").toFOLString()); 
//	QueryKb(kb, "!E ?z p(?z) => ((true) ^ (!E ?x !E ?y p(?x) ^ q(?y)) | (!E ?x !E ?y p(?x) ^ ~q(?y)))");

	
/*	QueryKb(kb, "!A ?x mammal(?x)");
	QueryKb(kb, "!A ?x cat(?x) => mammal(?x)");
	QueryKb(kb, "!A ?x mammal(?x) => cat(?x)");
	QueryKb(kb, "!A ?x blackAndCat(?x) => blackOrCat(?x)");
	QueryKb(kb, "!A ?x blackOrCat(?x) => blackAndCat(?x)");
	QueryKb(kb, "!E ?h hasHeart(fido, ?h)");
	QueryKb(kb, "~(!E ?h1 !E ?h2 hasHeart(fido,?h1) ^ hasHeart(fido, ?h2) ^ ?h1 ~= ?h2)");
	*/
    }

    public static void QueryKb(Kb kb, String query) {
	System.out.print("Query:  " + query + " --> ");
	System.out.println(" Result: " + (kb.queryFOPC(query) ? "*PROVED*." : "*NOT PROVED*."));
	System.out.println("Stats:  " + _df.format(kb.getQueryTime()) + " seconds, " + 
			                kb.getNumInfClauses() + " clauses generated, " +  
			                kb.getProofLength() + " proof length.");
	System.out.println();
    }
}
