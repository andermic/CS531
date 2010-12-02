package logic.kb;

import logic.kb.fol.*;
import logic.kb.fol.BindingSet; // Should really move this up, or make an interface,
                                // or make this an FOLKb interface.
import java.io.*;
import java.util.*;

public abstract class Kb {

    // Kb status constants
    public static final int INDETERMINATE = 0;
    public static final int TAUTOLOGY     = 1;
    public static final int INCONSISTENT  = 2;

    // Query filename to use (assigns first unused filename)
    public static String QUERY_FILE = null;

    static {
	// Find first free query file name...
	// OK to share among all KBs because only one
	// will be generating the file and calling the
	// process at a single time.
	int index = 0;
	while (true) {
	    QUERY_FILE = "query" + index++ + ".in";
	    if (!(new File(QUERY_FILE).exists())) {
		break;
	    }
	}
    }

    // Define a standard interface

    // Make a new KB to clear it!
    
    // String interface
    public abstract void       addFOPCFormula(String s);
    public abstract boolean    queryFOPC(String s); // true if kb |- s
    public abstract boolean    queryFOPC(String assume, String query); // true if kb |- s
    public abstract BindingSet queryFOPCBindings(String s);
    public abstract BindingSet queryFOPCBindings(String assume, String query);

    // FOPC.Node interface
    public abstract void       addFOPCFormula(FOPC.Node n);
    public abstract boolean    queryFOPC(FOPC.Node n); // true if kb |- s
    public abstract boolean    queryFOPC(FOPC.Node assume, FOPC.Node query); // true if kb |- s
    public abstract BindingSet queryFOPCBindings(FOPC.Node n);
    public abstract BindingSet queryFOPCBindings(FOPC.Node assume, FOPC.Node query);

    // Get query information
    public abstract float getQueryTime();
    public abstract int   getNumInfClauses();
    public abstract int   getProofLength();

    // File IO Information
    public abstract void  setQueryFile(String f);
    
    // Add formulae in a batch
    public void addAllFOPCFormula(List l) {
    	
    	Iterator i = l.iterator();
    	while (i.hasNext()) {
    		Object o = i.next();
    		if (o instanceof String) {
    			addFOPCFormula((String)o);
    		} else if (o instanceof FOPC.Node) {
   				addFOPCFormula((FOPC.Node)o);
    		} else {
    			System.err.println("Cannot process '" + o + "' of type " +
    					o.getClass());
    		}
    	}
    }

}
