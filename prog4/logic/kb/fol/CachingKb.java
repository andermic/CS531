//////////////////////////////////////////////////////////////////////
//
// First-Order Logic Package
//
// Class:  CachingKb
// Author: Scott Sanner (ssanner@cs.toronto.edu)
// Date:   7/25/03
//
// TODO:
// -----
//
//////////////////////////////////////////////////////////////////////

package logic.kb.fol;

import java.io.*;
import java.util.*;

import graph.*;
import logic.kb.*;
import logic.kb.fol.parser.*;

public class CachingKb
    extends Kb {

    // The file name to load the formula disk cache from
    public static final String DEFAULT_CACHE_ROOT = "PCACHE";

    public static String  CACHE_ROOT = null;    
    public static String  CACHE_FILE = null;
    public static HashMap _hmTPCache = null;
    public static boolean _bLastQueryCached = false;

    // Searches for the first free file starting with root,
    // and leaves CACHE_FILE set to that.
    public static void SetCacheFileRoot(String root) {
	CACHE_ROOT = root;

	CACHE_FILE = CACHE_ROOT;
	File f1 = new File(CACHE_FILE + ".UN");
	File f2 = new File(CACHE_FILE + ".PR");
	if (!f1.exists() || !f2.exists()) {
	    try { 
		f1.createNewFile(); 
		f2.createNewFile(); 
	    } catch (IOException e) { 
		System.out.println(e); System.exit(1);
	    }
	    System.out.println("Using CACHE FILE PREFIX: " + CACHE_FILE);
	    return; // New files created
	}
	long last_mod1 = f1.lastModified()/1000l;
	long last_mod2 = f2.lastModified()/1000l;
	long cur_time  = System.currentTimeMillis()/1000l;

	// If modified within last 15 seconds, search for next free file
	if (cur_time - last_mod1 < 15l || cur_time - last_mod2 < 15l) {
	    System.out.println("Appears " + CACHE_ROOT + " in use, making a temp file");
	    int index = 0;
	    while (true) {
		CACHE_FILE = CACHE_ROOT + index++;
		File unf = new File(CACHE_FILE + ".UN");
		File prf = new File(CACHE_FILE + ".PR");
		if (!unf.exists() && !prf.exists()) {
		    try {
			unf.createNewFile();
			prf.createNewFile();
			break;
		    } catch (IOException ioe) {
			continue;
		    }
		}
	    }
	}
	System.out.println("Using CACHE FILE PREFIX: " + CACHE_FILE);
    }

    // The kb to use for theorem proving when not in cache
    public Kb _kb;

    public CachingKb(Kb kb) {

	if (CACHE_ROOT == null) {
	    SetCacheFileRoot(DEFAULT_CACHE_ROOT);
	}

	// Will only do once
	if (_hmTPCache == null) {
	    _hmTPCache = new HashMap();
	    System.out.println("\n  [**Static Initializer: Using disk-based FOL Cache**]\n");
	    ReadCache();
	}
	_kb = kb;
    }

    public void setQueryFile(String f) {
	_kb.setQueryFile(f);
    }

    /////////////////////////////////////////////////////////////////////////////
    //                              Kb Interface
    /////////////////////////////////////////////////////////////////////////////
    
    // Convert a first-order formula to clauses and add to kb
    public void addFOPCFormula(String s) {
	_kb.addFOPCFormula(s);
    }

    public void addFOPCFormula(FOPC.Node n) {
	_kb.addFOPCFormula(n);
    }

    // Query to see if kb entails s (false only implies could not be proven)
    public boolean queryFOPC(String assume, String query) {

	// Check cache
	_bLastQueryCached = false;
	Boolean result = null;
	if ((result = (Boolean)_hmTPCache.get(query)) != null) {
	    _bLastQueryCached = true;
	    return result.booleanValue();
	}

	boolean res = _kb.queryFOPC(assume, query);

	// Add result to cache (note assumptions are not cached - should be OK!)
	_hmTPCache.put(query, new Boolean(res));
	AppendCache(query, res);

	return res;		
    }

    public boolean queryFOPC(String query) {

	// Check cache
	_bLastQueryCached = false;
	Boolean result = null;
	if ((result = (Boolean)_hmTPCache.get(query)) != null) {
	    _bLastQueryCached = true;
	    return result.booleanValue();
	}

	boolean res = _kb.queryFOPC(query);

	// Add result to cache
	_hmTPCache.put(query, new Boolean(res));
	AppendCache(query, res);

	return res;	
    }

    public boolean queryFOPC(FOPC.Node assume, FOPC.Node query) {

	// Check cache
	_bLastQueryCached = false;
	Boolean result = null;
	String query_str = query.toFOLString();
	if ((result = (Boolean)_hmTPCache.get(query_str)) != null) {
	    _bLastQueryCached = true;
	    return result.booleanValue();
	}

	boolean res = _kb.queryFOPC(assume, query);

	// Add result to cache
	_hmTPCache.put(query_str, new Boolean(res));
	AppendCache(query_str, res);

	return res;
    }

    public boolean queryFOPC(FOPC.Node query) {

	//System.out.println("CKB: " + query);

	// Check cache
	_bLastQueryCached = false;
	Boolean result = null;
	String query_str = query.toFOLString();
	if ((result = (Boolean)_hmTPCache.get(query_str)) != null) {
	    _bLastQueryCached = true;
	    System.out.print(result.booleanValue() ? "$T" : "$F");
	    return result.booleanValue();
	}

	boolean res = _kb.queryFOPC(query);

	// Add result to cache
	_hmTPCache.put(query_str, new Boolean(res));
	AppendCache(query_str, res);

	return res;
    }

    // Query for bindings of free vars - no caching here
    public BindingSet queryFOPCBindings(String assume, String query) {
	return _kb.queryFOPCBindings(assume, query);
    }

    public BindingSet queryFOPCBindings(String query) {
	return _kb.queryFOPCBindings(query);
    }

    public BindingSet queryFOPCBindings(FOPC.Node assume, FOPC.Node query) {
	return _kb.queryFOPCBindings(assume, query);
    }

    public BindingSet queryFOPCBindings(FOPC.Node query) {
	return _kb.queryFOPCBindings(query);
    }

    // Data would not be accurate if data was found in cache!
    public float getQueryTime() {
	if (_bLastQueryCached) {
	    return -1f; 
	} else {
	    return _kb.getQueryTime();
	}
    }

    public int getNumInfClauses() {
	if (_bLastQueryCached) {
	    return -1; 
	} else {
	    return _kb.getNumInfClauses();
	}
    }

    public int getProofLength() {
	if (_bLastQueryCached) {
	    return -1; 
	} else {
	    return _kb.getProofLength();
	}
    }

    /////////////////////////////////////////////////////////////////////////////
    //                           Disk Cache Interface
    /////////////////////////////////////////////////////////////////////////////    

    public static void ReadCache() {
	
	try {

	    // Read all of the contents and place them in the cache
	    DataInputStream dsp = new DataInputStream(new FileInputStream(CACHE_FILE + ".PR"));
	    Boolean bt = new Boolean(true);
	    while (true) {
		String theorem = dsp.readUTF();
		dsp.readChar();
		_hmTPCache.put(theorem, bt);
	    }

	} catch (EOFException e) { 
	    // Do nothing - expected
	} catch (IOException ioe) { 
	    System.out.println(ioe.toString());
	    System.exit(1);
	}

	try {

	    // Read all of the contents and place them in the cache
	    DataInputStream dsn = new DataInputStream(new FileInputStream(CACHE_FILE + ".UN"));
	    Boolean bf = new Boolean(false);
	    while (true) {
		String theorem = dsn.readUTF();
		dsn.readChar();
		_hmTPCache.put(theorem, bf);
	    }

	} catch (EOFException e) { 
	    // Do nothing - expected
	} catch (IOException ioe) { 
	    System.out.println(ioe.toString());
	    System.exit(1);
	}
    }

    // A persistent output stream - should close itself upon exit
    public static DataOutputStream dsop = null;
    public static DataOutputStream dson = null;

    public static void AppendCache(String query, boolean result) {

	// Open files if required
	if (dsop == null) {
	    try {
		dsop = new DataOutputStream(new FileOutputStream(CACHE_FILE + ".PR"));
		dson = new DataOutputStream(new FileOutputStream(CACHE_FILE + ".UN"));
		Iterator i = _hmTPCache.entrySet().iterator();
		while (i.hasNext()) {
		    Map.Entry me = (Map.Entry)i.next();
		    String theorem = (String)me.getKey();
		    Boolean bresult = (Boolean)me.getValue();
		    if (bresult.booleanValue()) {
			dsop.writeUTF(theorem); 
			dsop.writeChar('\n');
		    } else {
			dson.writeUTF(theorem);
			dson.writeChar('\n');
		    }
		    dsop.flush();
		    dson.flush();
		}
	    } catch (IOException ioe) {
		System.out.println(ioe.toString());
		System.exit(1);		
	    }
	}

	// Now append current theorem
	try {
	    if (result) {
		dsop.writeUTF(query);
		dsop.writeChar('\n');
		dsop.flush();
	    } else {
		dson.writeUTF(query);
		dson.writeChar('\n');
		dson.flush();
	    }
	} catch (IOException ioe) {
		System.out.println(ioe.toString());
		System.exit(1);		
	}
    }
}
