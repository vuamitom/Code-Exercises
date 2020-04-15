/*
 * Copyright (c) 2018-2022 by Zalo Group.
 * All Rights Reserved.
 */
package com.vng.zing.experiment.tests.regex;

import com.vng.zing.experiment.brics.*;
import org.junit.Test;

public class BricsTest {

    @Test
    public void testSimple() {
        RegExp regex = new RegExp("ab+cd|abc+d");
        Automaton auto = regex.toAutomaton();
        RunAutomaton runAuto = new RunAutomaton(auto, true);
        boolean result = runAuto.run("abcd");
        assert result == true;
    }

    @Test
    public void testFind() {
//        RegExp regex = new RegExp("(a[a-z]+cd)|(abc+d)");
        RegExp regex = new RegExp("a|b");
        Automaton auto = regex.toAutomaton();
        RunAutomaton runAuto = new RunAutomaton(auto, true);

        AutomatonMatcher m = runAuto.newMatcher("i dont lik you abcd actually i dont meant abcccde");
        m.find();
        assert m.group(1) != null;
    }

    @Test
    public void testPreBuilt() {
        assert Datatypes.exists("URI");
        Automaton auto = Datatypes.get("URI");
        RunAutomaton runAuto = new RunAutomaton(auto, true);
        AutomatonMatcher m = runAuto.newMatcher("http://abcxyz.aaa");
        m.find();
        System.out.println(m.group(1));
    }
}
