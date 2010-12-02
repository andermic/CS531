//////////////////////////////////////////////////////////////////////
//
// First-Order Logic Package
//
// Class:  OtterKb (dumps kb to an otter input file for theorem proving)
// Author: Scott Sanner (ssanner@cs.toronto.edu)
// Date:   7/25/03
//
// NOTES:
// ------
//
// **Use fodt.foalp.Case to verify (it first verifies the theorem prover!)**
// **Assumes path to executable binary or script is in working directory**
//
// TODO:
// -----
// - Should write a simple routine to parse output for query bindings.
//
//////////////////////////////////////////////////////////////////////

package logic.kb.fol;

import java.io.*;
import java.util.*;

import graph.*;
import logic.kb.*;
import logic.kb.fol.parser.*;

import util.WinUNIX;

public class OtterKb
    extends Kb {

    public static final boolean CONVERT_CNF = true;

    // Commands for DOS and UNIX
    // **Use CMD versions must be used when redirecting IO**

    public String _sKbName;
    public int    _nQuery;
    public Set    _sClauses;
    public int    _nSeconds;
    public int    _nClausesGen;
    public float  _fQueryTime;
    public int    _nProofLen;
    public FOPC.Node _fopcAssume;
    public String _queryFile;
    public long   _lTime;

    private OtterKb() { }

    public OtterKb(int time_out) {
	this("Timeout:" + time_out, time_out);
    }

    public OtterKb(String kbname) {
	this(kbname, 1);
    }

    public OtterKb(String kbname, int time_out) {
	_sKbName  = kbname;
	_nQuery   = 1;
	_sClauses = new HashSet();
	_nSeconds = time_out;
	_nProofLen = 0;
	_queryFile = QUERY_FILE;
    }

    public void setQueryFile(String f) {
	_queryFile = f;
    }

    // TODO: Would be nice if could access streams directly and avoid file I/O
    public boolean queryFOPC(String s) {
	return queryFOPC(FOPC.parse(s));
    }

    public boolean queryFOPC(FOPC.Node n) {
	_fopcAssume = null;
	return queryFOPC(n, true);
    }

    public boolean queryFOPC(String assume, String query) {
	return queryFOPC(FOPC.parse(assume), FOPC.parse(query));
    }

    public boolean queryFOPC(FOPC.Node assume, FOPC.Node query) {
	_fopcAssume = assume;
	return queryFOPC(query, true);
    }

    // A bit of a hack, assumes that kb is empty, need to update this code
    // to handle refutation separately from querying, ugly for now.
    public boolean canRefute(FOPC.Node n) {
	_fopcAssume = null;
	return queryFOPC(n, false);
    }

    public boolean canRefute(FOPC.Node assume, FOPC.Node n) {
	_fopcAssume = assume;
	return queryFOPC(n, false);
    }

    // A bit of a hack, assumes that kb is empty, need to update this code
    // to handle refutation separately from querying, ugly for now.
    // if prove_query_true is true, checks if query implied (negates and refutes)
    // if prove_query_true is false, checks if refutable
    private boolean queryFOPC(FOPC.Node n, boolean prove_query_true) {
	
	// Generate CNF for negation of query
	_nProofLen = 0;
	n = n.copy();
	//System.out.println("Otter generating file: " + _queryFile);
	genOtterFileForQuery(n, _queryFile, prove_query_true);

    	try {
    	       		
	    int index;
	    boolean ref_found = false;
	    
	    // Open files for reading and writing
	    //BufferedReader fis_reader = new BufferedReader(_rReader);
	    
	    ResetTimer();
	    //System.out.println("Executing: '" + WinUNIX.OTTER_CMD + " " + _queryFile + "'");
	    Process p = Runtime.getRuntime().exec(WinUNIX.OTTER_CMD + " " + _queryFile);
	    BufferedReader process_out = new BufferedReader(new InputStreamReader(p.getInputStream()));
	    //PrintWriter    process_in  = new PrintWriter(p.getOutputStream(), true);
	    
	    // Provide input to process (could come from any stream)
	    String line = null;
	    //while ((line = fis_reader.readLine()) != null) {
	    //	    process_in.println(line);
	    //}
	    //fis_reader.close();
	    //process_in.close(); // Need to close input stream so process exits!!!
	    
	    // Get output from process (can also be used by BufferedReader to get
	    // line-by-line... see how fis_reader is constructed).
	    while ((line = process_out.readLine()) != null) {
		// process line
		//System.out.println("Line: " + line);
		if (line.indexOf("end of proof") >= 0) {
		    ref_found = true;
		} else if ((index = line.indexOf("user CPU time")) >= 0) {
		    _fQueryTime = getNextNum(line, index)/1000f;
		    _fQueryTime = GetElapsedTime()/1000000f;
		} else if ((index = line.indexOf("clauses generated")) >= 0) {
		    _nClausesGen = (int)getNextNum(line, index);
		} else if ((index = line.indexOf("Length of proof is")) >= 0) {
		    _nProofLen = (int)getNextNum(line, index);
		}
	    }
	    process_out.close();
	    
	    //System.out.print("Waiting for Otter [" + _fQueryTime + "s, " + _nClausesGen + " clause]...");
	    p.waitFor();
	    //System.out.println("done.");
	    
	    return ref_found;
    		
    	} catch (InterruptedException ie) {
    		System.out.println(ie);
    		return false;
    	} catch (IOException ioe) {
    		System.out.println(ioe);
    		return false;
    	}
    }

    public float getQueryTime() {
	return (float)1000.0*_fQueryTime;
    }

    public int getNumInfClauses() {
	return _nClausesGen;
    }

    public int getProofLength() {
	return _nProofLen;
    }

    public float getNextNum(String s, int index) {
	StringBuffer num = new StringBuffer();
	while (!Character.isDigit(s.charAt(index))) { index++; }
	while (index < s.length() && (Character.isDigit(s.charAt(index)) || s.charAt(index) == '.')) 
	    { num.append(s.charAt(index++)); }
	try {
	    Float f = new Float(num.toString());
	    return f.floatValue();
	} catch (NumberFormatException e) {
	    return -1;
	}
    }

    // Query for bindings of free vars
    public BindingSet queryFOPCBindings(String query) {
	System.out.println("WARNING: Bindings query not implemented for VampireKb yet.");
	return null;
    }

    public BindingSet queryFOPCBindings(String assume, String query) {
	System.out.println("WARNING: Bindings query not implemented for VampireKb yet.");
	return null;
    }

    public BindingSet queryFOPCBindings(FOPC.Node n) {
	System.out.println("WARNING: Bindings query not implemented for VampireKb yet.");
	return null;
    }

    public BindingSet queryFOPCBindings(FOPC.Node assume, FOPC.Node n) {
	System.out.println("WARNING: Bindings query not implemented for VampireKb yet.");
	return null;
    }

    // Generate an otter file for proving this query
    public void genOtterFileForQuery(String s) {
	genOtterFileForQuery(s, _sKbName + "_q" + _nQuery);
    }

    // Generate an otter file for proving this query
    public void genOtterFileForQuery(String s, String filename) {
	genOtterFileForQuery(FOPC.parse(s), filename, true);
    }

    public void genOtterFileForQuery(FOPC.Node n, String filename, 
				     boolean prove_query_true) {
	// Generate CNF for negation of query
	Set query = new HashSet();
	FOPC.Node temp_query = n.copy().convertNNF(prove_query_true);
	if (CONVERT_CNF) {
	    System.out.print("c");
	    query.addAll(getClauses(temp_query));
	    System.out.print("[" + (query.size() + _sClauses.size()) + "]");
	} else {
	    System.out.print("f");
	    query.add(temp_query);
	}

	// Dump file
	try {
	    PrintStream os = new PrintStream(new FileOutputStream(filename));

	    // Some file information to verify correctness
	    os.println("% KB " + _sKbName + ", Query #" + _nQuery + 
		       ": FOL Kb generated from logic.kb.fol.OtterKb");
	    //if (!_sClauses.isEmpty()) {
	    //	os.println("% Kb clauses:");
	    //	Iterator ki = _sClauses.iterator();
	    //	while (ki.hasNext()) {
	    //	    os.println("% - " + ((FOPC.Node)ki.next()).toFOLString());
	    //	}
	    //} else {
	    //	os.println("% Empty kb");
	    //}	    
	    os.println("% Testing kb refutation of: " + n.toFOLString());
	    //os.println("% Refuting: " + n.convertNNF(prove_query_true).toFOLString());
	    //if (!query_cnf.isEmpty()) {
	    //	os.println("% Negated query clauses:");
	    //	Iterator qi = query_cnf.iterator();
	    //	while (qi.hasNext()) {
	    //	    os.println("% - " + ((FOPC.Node)qi.next()).toFOLString());
	    //	}
	    //} else {
	    //	os.println("% Empty query");
	    //}
	    _nQuery++; // Increment query for next time
	    os.println();
	    if (CONVERT_CNF) {
		os.println("set(prolog_style_variables).\n");
	    }
	    os.println("set(auto).\n");
	    os.println("assign(max_seconds," + _nSeconds + ").\n");
	    os.println("clear(print_given).\n");
	    //os.println("assign(max_gen,1000).\n");
	    if (CONVERT_CNF) {
		os.println("list(usable).");
	    } else {
		os.println("formula_list(usable).");
	    }
	    
	    // Print all kb clauses
	    //int cnt = 0;
	    Set axiom_clauses = new HashSet(_sClauses); // Handle assumptions!
	    if (_fopcAssume != null) {
		axiom_clauses.addAll(getClauses(_fopcAssume));
	    } 
	    Iterator i = axiom_clauses.iterator();
	    while (i.hasNext()) {
		//cnt++;
		FOPC.Node c = (FOPC.Node)i.next();
		String line = c.toOtterString();
		if (line.indexOf(".") >= 0) {
		    System.out.println("OTTER discarding: " + line);
		} else {
		    os.println(line + ".");
		}
	    }

	    // Print query clause
	    i = query.iterator();
	    while (i.hasNext()) {
		//cnt++;
		FOPC.Node c = (FOPC.Node)i.next();
		os.println(c.toOtterString() + ".");
	    }

	    os.println("end_of_list.");
	    os.close();
	    //System.out.println("Generated " + cnt + " clauses.");

	} catch (IOException ioe) {
	    System.out.println("Error: " + ioe);
	    System.exit(1);
	}
    }

    // Convert a first-order formula to clauses and add to kb
    public void addFOPCFormula(String s) {
	_sClauses.addAll(getClauses(FOPC.parse(s)));
    }

    public void addFOPCFormula(FOPC.Node n) {
	_sClauses.addAll(getClauses(n));
    }

    // Remove duplicate clauses
    public Set filterClauses(Set clauses) {
	HashSet ret = new HashSet();
	HashSet tmp = new HashSet();
	Iterator i = clauses.iterator();
	while (i.hasNext()) {
	    FOPC.ConnNode c = (FOPC.ConnNode)i.next();
	    tmp.clear();
	    tmp.addAll(c._alSubNodes); // Removes duplicates!
	    FOPC.ConnNode r = new FOPC.ConnNode(c._nType);
	    Iterator j = tmp.iterator();
	    while (j.hasNext()) {
		r.addSubNode((FOPC.Node)j.next());
	    }
	    ret.add(r);
	}
	return ret;
    }

    public Set getClauses(FOPC.Node n) {

	// DNF conversion to push down quantifiers is pointless here
	// since we'll get rid of EXISTS and CNF(DNF) will yield
	// an exponential blowup with simplification.
	boolean SAVED_ALLOW_DNF = FOPC.ALLOW_DNF;
	FOPC.ALLOW_DNF = false;
	HashSet ret = new HashSet();

	// Simpify n and convert to NNF
	n = n.copy(); // Following functions may modify original!
	n = FOPC.simplify(n); 
	n = FOPC.skolemize(n);
	n = FOPC.convertCNF(n);

	//System.out.println("Generating clauses for: " + n.toFOLString());

	// Break apart top-level, standardize apart free vars, and add to clause list
	if ((n instanceof FOPC.ConnNode) && 
	    ((FOPC.ConnNode)n)._nType == FOPC.ConnNode.AND) {

	    // Go through all subclauses
	    Iterator i = ((FOPC.ConnNode)n)._alSubNodes.iterator();
	    while (i.hasNext()) {
		FOPC.Node sn = (FOPC.Node)i.next();

		// Reality check!
		if (! (((sn instanceof FOPC.ConnNode) && 
			((FOPC.ConnNode)sn)._nType == FOPC.ConnNode.OR)
		       || (sn instanceof FOPC.PNode)
		       || (sn instanceof FOPC.TNode))) {

		    System.out.println("CNF conversion was bad: " + sn.toFOLString());
		    System.exit(1);
		}
	
		if (sn instanceof FOPC.PNode) {
		    FOPC.ConnNode cn = new FOPC.ConnNode(FOPC.ConnNode.OR);
		    cn.addSubNode(sn);
		    ret.add(cn);
		} else {
		    ret.add(sn);
		}
	    }

	} else {
	    if (! (((n instanceof FOPC.ConnNode) && 
		    ((FOPC.ConnNode)n)._nType == FOPC.ConnNode.OR)
		   || (n instanceof FOPC.PNode)
		   || (n instanceof FOPC.TNode))) {
		
		System.out.println("CNF conversion was bad: " + n.toFOLString());
		System.exit(1);
	    }
	    
	    if (n instanceof FOPC.PNode || n instanceof FOPC.TNode) {
		FOPC.ConnNode cn = new FOPC.ConnNode(FOPC.ConnNode.OR);
		cn.addSubNode(n);
		ret.add(cn);
	    } else {
		ret.add(n); 
	    } 
	}

	// Restore DNF conversion
	FOPC.ALLOW_DNF = SAVED_ALLOW_DNF;
	return filterClauses(ret); // Remove duplicates!!!
    }
    
    public void ResetTimer() {
    	_lTime = System.currentTimeMillis();
    }

    // Get the elapsed time since resetting the timer
    public long GetElapsedTime() {
    	return System.currentTimeMillis() - _lTime;
    }

}
