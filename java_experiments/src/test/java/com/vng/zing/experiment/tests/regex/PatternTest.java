/*
 * Copyright (c) 2018-2022 by Zalo Group.
 * All Rights Reserved.
 */
package com.vng.zing.experiment.tests.regex;

import com.sun.org.apache.xpath.internal.operations.Bool;
import com.vng.zing.experiment.regex.Matcher;
import com.vng.zing.experiment.regex.Pattern;
import dk.brics.automaton.AutomatonMatcher;
import jdk.nashorn.internal.runtime.regexp.joni.Regex;
import org.junit.Test;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.*;
import java.util.stream.Collectors;

public class PatternTest {

    String allChars = "ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ";

    @Test
    public void testCompile() {
        Pattern p = Pattern.compile("abc+d");
        Matcher m = p.matcher("abccccd");
        System.out.println(m.matches());
        Pattern.printObjectTree(p.matchRoot);
        System.out.println(m.group(0));


        System.out.println("============== abc+d|ab+cd ===================");
        Pattern p1 = Pattern.compile("abc+d|ab+cd");
        Matcher m1 = p1.matcher("abccccd");
        System.out.println(m1.matches());
        Pattern.printObjectTree(p1.matchRoot);

        Pattern p3 = Pattern.compile("a[bc]+d");
        Matcher m3 = p3.matcher("abccccd");
        System.out.println(m3.matches());

        Pattern p4 = Pattern.compile("a(b+|c+)d");
        Matcher m4 = p4.matcher("abccccd");
        System.out.println(m4.matches());
    }

    @Test
    public void testMatchingPattern() {
        Pattern p1 = Pattern.compile("abc|xyz|sml|123|789");
        Matcher m1 = p1.matcher("i don't know abc dfsdf");
        System.out.println(m1.find());
        System.out.println(m1.group(0));
        System.out.println(m1.groupCount());
    }

    @Test
    public void testFindOutMatchingPattern() {
        Pattern p1 = Pattern.compile("(abc)|(xyz)|(sml)|(123)|(789)");
        Matcher m1 = p1.matcher("i don't know abc dfsdf");
        System.out.println(m1.find());
        System.out.println(m1.group(0));
        System.out.println(m1.group(1));
        System.out.println(m1.group(2));
        System.out.println(m1.groupCount());
    }

    private String[] generateTestInput() {
        String[] all = new String[1000];
        for (int i =0 ; i < all.length; i++) {
            all[i] = generateRandom();
        }
        return all;
    }

    private String generateRandom() {
        int size = (int)Math.round(Math.random() * 3000);
        StringBuilder b = new StringBuilder();
        for (int c = 0; c < size; c++) {
            int idx = (int) Math.round(Math.random() * this.allChars.length());
            b.append(this.allChars.charAt(idx));
        }
        return b.toString();
    }

    private String[] getTestInput() {
        try {
            List<String> r = Files.readAllLines(Paths.get("/home/tamvm/Downloads/wikivietnam_token.txt"));
            String[] x = r.toArray(new String[r.size()]);
            return x;
        } catch (IOException e) {
            e.printStackTrace();
            return new String[0];
        }
    }

    static String shuffle(String string){

        List<Character> list = string.chars().mapToObj(c -> new Character((char) c))
                .collect(Collectors.toList());
        Collections.shuffle(list);
        StringBuilder sb = new StringBuilder();
        list.forEach(c -> sb.append(c));

        return sb.toString();
    }

    private String[] getLongTestInput() {
        try {
            List<String> r = Files.readAllLines(Paths.get("/home/tamvm/Downloads/wikivietnam_token.txt"));
            String[] x = new String[4];
            for (int i = 0; i < x.length; i++) {

                if (i > 0) {
                    x[i] = shuffle(String.join(" ", r));
                }
                else {
                    x[i] = String.join(" ", r);
                }
            }
            return x;
        } catch (IOException e) {
            e.printStackTrace();
            return new String[0];
        }
    }

    @Test
    public void testCorrectNess() {
        String[] spams = {
            "vay",
            "kho[aả]n vay",
            "vay v[oố]n",
            "vay ti[eề]n",
            "vay (?:t[ií]n|th[eế]) ch[aấ]p"
        };
        StringBuilder b = new StringBuilder();
        for (int i = 0; i < spams.length; i++) {
            b.append("("); b.append(spams[i]);
            b.append(")");
            if (i < spams.length - 1)
                b.append("|");
        }
        String merged = b.toString();
        String[] inputs = {
                "em cho vay",
                "khoản vay này quá lớn",
                "xdsfdf 123123 vay vốn không ",
                "cho tôi tiền",
                "vay tín chấp okela"
        };

        boolean[] results = new boolean[inputs.length];
        java.util.regex.Pattern p = java.util.regex.Pattern.compile(merged);
        for (int i = 0; i < inputs.length; i++) {
            java.util.regex.Matcher m = p.matcher(inputs[i]);
            results[i] = m.find();
        }
        String ref = "";
        for (int i = 0; i < results.length; i++) {
            ref += results[i] + " ";
        }
        System.out.println(" ref result = " + ref);
        com.google.re2j.Pattern re2Pattern = com.google.re2j.Pattern.compile(merged);
        for (int i = 0; i < inputs.length; i++) {
            com.google.re2j.Matcher m = re2Pattern.matcher(inputs[i]);
            assert results[i] == m.find();
        }

        dk.brics.automaton.RegExp regexpr = new dk.brics.automaton.RegExp(merged);
        dk.brics.automaton.Automaton auto = regexpr.toAutomaton();
        dk.brics.automaton.RunAutomaton runauto = new dk.brics.automaton.RunAutomaton(auto, true);
        for (int i = 0; i < inputs.length; i++) {
            AutomatonMatcher m = runauto.newMatcher(inputs[i]);
            assert results[i] == m.find();
        }

    }

    @Test
    public void testGroupingCost() {

        String[] spams = {
                "vay",
                "kho[aả]n vay",
                "vay v[oố]n",
                "vay ti[eề]n",
                "vay (?:t[ií]n|th[eế]) ch[aấ]p",
                "cho vay",
                "[uư]u [dđ][aã]i",
                "hỗ tr[oợ] v[oố]n",
                "gi[aả]i ng[aâ]n",
                "(?:cty|c[oô]ng ty) (?:t[aà]i ch[ií]nh|tc)",
                "(?:vay|v[oố]n|cvay) ti[eê]u d[uù]ng",
                "b[aả]o hi[eể]m nh[aâ]n th[oọ]",
                "th[eế] ch[aấ]p t[aà]i s[aả]n",
                "th[eẻ] t[ií]n d[uụ]ng",
                "l[aã]i su[aâấ]t|ls",
                "nv|(?:nh[aâ]n|chuy[eê]n) vi[eê]n",
                "t[uư] v[aấ]n",
                "ng[aâ]n h[aà]ng|nhnn",
                "điện thoại|s?[đd]t|tel\\b|telephone|call|liên (?:lạc|hệ)|\\blh\\b|gọi|contact|nhắn tin|(?:tin|lời) nhắn|sms"
        };

        int noIter = 1;

        // generate test input
        String[] inputs = getTestInput();
        // get a list of pattern
        StringBuilder b = new StringBuilder();
        for (int i = 0; i < spams.length; i++) {
            String s = spams[i];
            b.append("(?:");
            b.append(s);
            b.append(")");
            if ( i < spams.length - 1) {
                b.append("|");
            }
        }

        String nonCaptureMerged = b.toString();

        // capturing pattern
        b = new StringBuilder();
        for (int i = 0; i < spams.length; i++) {
            String s = spams[i];
            b.append("(");
            b.append(s);
            b.append(")");
            if ( i < spams.length - 1) {
                b.append("|");
            }
        }

        String captureMerged = b.toString();
        System.out.println("Capture regex " + captureMerged);
        System.out.println("NON Capture regex " + nonCaptureMerged);
        System.out.println(">>>>>>>>>>>>> java.util.regex.Pattern");
        Date start = new Date();
        java.util.regex.Pattern mergedPattern = java.util.regex.Pattern.compile(nonCaptureMerged);
        System.out.println("compile take " + (new Date().getTime() - start.getTime()) + " ms");
        start = new Date();
        for (int j = 0; j < noIter; j++) {
            for (String in : inputs) {
                java.util.regex.Matcher m = mergedPattern.matcher(in);
                m.find();
            }
        }
        // compare 2 different run
        long dur = new Date().getTime() - start.getTime();
        System.out.println("Running simple merge with non-capturing took " + dur + " ms");


        start = new Date();
        mergedPattern = java.util.regex.Pattern.compile(captureMerged);
        System.out.println("compile take " + (new Date().getTime() - start.getTime()) + " ms");
        start = new Date();
        for (int j = 0; j < noIter; j++) {
            for (String in : inputs) {
                java.util.regex.Matcher m = mergedPattern.matcher(in);
                m.find();
            }
        }

        dur = new Date().getTime() - start.getTime();
        System.out.println("Running simple merge with capturing group took " + dur + " ms");

        // compare speed of separate pattern matching

        java.util.regex.Pattern[] ps = new java.util.regex.Pattern[spams.length];
        start = new Date();
        for (int i = 0; i < ps.length; i++) {
            ps[i] = java.util.regex.Pattern.compile(spams[i]);
        }
        System.out.println("compile take " + (new Date().getTime() - start.getTime()) + " ms");
        start = new Date();
        for (int j = 0; j < noIter; j++) {
            for (String in: inputs) {
                for (java.util.regex.Pattern p: ps) {
                    java.util.regex.Matcher m = p.matcher(in);
                    m.find();
                }
            }
        }
        dur = new Date().getTime() - start.getTime();
        System.out.println("Running separate regex pattern took " + dur + " ms");
        ps = null;
        // ======================================================================================
        // testing google re2j
        System.out.println(">>>>>>>>>>>>> com.google.re2j.Pattern");

        start = new Date();
        com.google.re2j.Pattern re2Pattern = com.google.re2j.Pattern.compile(nonCaptureMerged);
        System.out.println("compile take " + (new Date().getTime() - start.getTime()) + " ms");
        start = new Date();
        for (int j = 0; j < noIter; j++) {
            for (String in : inputs) {
                com.google.re2j.Matcher m = re2Pattern.matcher(in);
                m.find();
            }
        }
        dur = new Date().getTime() - start.getTime();
        System.out.println("Running Google r2 nonCapture " + dur + " ms");
        start = new Date();
        re2Pattern = com.google.re2j.Pattern.compile(captureMerged);
        System.out.println("compile take " + (new Date().getTime() - start.getTime()) + " ms");
        start = new Date();
        for (int j = 0; j < noIter; j++) {
            for (String in : inputs) {
                com.google.re2j.Matcher m = re2Pattern.matcher(in);
                m.find();
            }
        }
        dur = new Date().getTime() - start.getTime();
        System.out.println("Running Google r2 capturing " + dur + " ms");

        // compare speed of separate pattern matching
        com.google.re2j.Pattern[] re2Ps = new com.google.re2j.Pattern[spams.length];
        start = new Date();
        for (int i = 0; i < re2Ps.length; i++) {
            re2Ps[i] = com.google.re2j.Pattern.compile(spams[i]);
        }
        System.out.println("compile take " + (new Date().getTime() - start.getTime()) + " ms");
        start = new Date();
        for (int j = 0; j < noIter; j++) {
            for (String in: inputs) {
                for (com.google.re2j.Pattern p: re2Ps) {
                    com.google.re2j.Matcher m = p.matcher(in);
                    m.find();
                }
            }
        }
        dur = new Date().getTime() - start.getTime();
        System.out.println("Running separate Google re2 regex pattern took " + dur + " ms");
        re2Ps = null;
        // ======================================================================================
        System.out.println(">>>>>>>>>>>>> dk.brics.automaton.RegExp");
        // http://www.brics.dk/automaton/
        start = new Date();
        dk.brics.automaton.RegExp regexpr = new dk.brics.automaton.RegExp(nonCaptureMerged);
        dk.brics.automaton.Automaton auto = regexpr.toAutomaton();
        dk.brics.automaton.RunAutomaton runauto = new dk.brics.automaton.RunAutomaton(auto, true);
        System.out.println("compile take " + (new Date().getTime() - start.getTime()) + " ms");
        // http://jregex.sourceforge.net/
        start = new Date();
        for (int j = 0; j < noIter; j++) {
            for (String in : inputs) {
//                runauto.run(in);
                AutomatonMatcher m = runauto.newMatcher(in);
                m.find();
            }
        }
        dur = new Date().getTime() - start.getTime();
        System.out.println("Running dkbrics automation nonCapture " + dur + " ms");

        start = new Date();
        regexpr = new dk.brics.automaton.RegExp(captureMerged);
        auto = regexpr.toAutomaton();
        runauto = new dk.brics.automaton.RunAutomaton(auto, true);
        System.out.println("compile take " + (new Date().getTime() - start.getTime()) + " ms");
        start = new Date();
        for (int j = 0; j < noIter; j++) {
            for (String in : inputs) {
//                runauto.run(in);
                AutomatonMatcher m = runauto.newMatcher(in);
                m.find();
            }

        }
        dur = new Date().getTime() - start.getTime();
        System.out.println("Running dkbrics automation capturing " + dur + " ms");

        dk.brics.automaton.RunAutomaton [] runautos = new dk.brics.automaton.RunAutomaton[spams.length];

        start = new Date();
        for (int i = 0; i < runautos.length; i++) {
            dk.brics.automaton.RegExp regexpr1 = new dk.brics.automaton.RegExp(spams[i]);
            dk.brics.automaton.Automaton auto1 = regexpr1.toAutomaton();
            runautos[i] = new dk.brics.automaton.RunAutomaton(auto1, true);
        }
        System.out.println("compile take " + (new Date().getTime() - start.getTime()) + " ms");

        start = new Date();
        for (int j = 0; j < noIter; j++) {
            for (String in: inputs) {
                for (dk.brics.automaton.RunAutomaton p: runautos) {
//                    p.run(in);
                    AutomatonMatcher m = p.newMatcher(in);
                    m.find();
                }
            }
        }
        dur = new Date().getTime() - start.getTime();
        System.out.println("Running separate dk.brics automation regex pattern took " + dur + " ms");
        runautos = null;
        // ======================================================================================
//        System.out.println(">>>>>>>>>>>>> com.karneim.util.collection.regex.Pattern (does not support group capturing)");
//        start = new Date();
//        com.karneim.util.collection.regex.Pattern jrexxP = new com.karneim.util.collection.regex.Pattern(captureMerged);
//        System.out.println("compile take " + (new Date().getTime() - start.getTime()) + " ms");
//        start = new Date();
//        for (int j = 0; j < noIter; j++) {
//            for (String in : inputs) {
//                jrexxP.contains(in);
//            }
//        }
//        dur = new Date().getTime() - start.getTime();
//        System.out.println("Running com.karneim.util.collection.regex nonCapture " + dur + " ms");
//
//        com.karneim.util.collection.regex.Pattern jrexxPs[] = new com.karneim.util.collection.regex.Pattern[spams.length];
//        start = new Date();
//        for (int i = 0; i < jrexxPs.length; i++) {
//            jrexxPs[i] = new com.karneim.util.collection.regex.Pattern(spams[i]);
//        }
//        System.out.println("compile take " + (new Date().getTime() - start.getTime()) + " ms");
//        start = new Date();
//        for (int j = 0; j < noIter; j++) {
//            for (String in: inputs) {
//                for (com.karneim.util.collection.regex.Pattern p: jrexxPs) {
////                    p.run(in);
//                    p.contains(in);
//                }
//            }
//        }
//        dur = new Date().getTime() - start.getTime();
//        System.out.println("Running separate com.karneim.util.collection regex pattern took " + dur + " ms");
//        jrexxPs = null;
    }

    @Test
    public void compareSpeed() {
        Pattern p1 = Pattern.compile("abc+d|ab+cd");
        Pattern p2 = Pattern.compile("a(b+|c+)d");

        // generate random input string
        List<String> randomInputs = new ArrayList<String>();
        for (int i = 0; i < 1000; i++) {
            int size = (int)Math.round(Math.random() * 200);
            int range = 'Z' - '0' + 1;
            char gen[] = new char[size];
            for (int j = 0; j < size; j++) {
                char x = (char)Math.round(Math.random() * range);
                gen[j] = x;
            }
            randomInputs.add(new String(gen));
        }

        // test separately
        int totalRound = 100000;
        System.out.println("===== test Pattern 1 =====");
        Date start = new Date();
        for (int r = 0; r < totalRound; r++) {
            for (int t = 0; t < randomInputs.size(); t++) {
                p1.matcher(randomInputs.get(t)).matches();
            }
        }
        System.out.println("Done in " + (new Date().getTime() - start.getTime()) + "ms");
        System.out.println("===== test Pattern 2 =====");
        start = new Date();
        for (int r = 0; r < totalRound; r++) {
            for (int t = 0; t < randomInputs.size(); t++) {
                p2.matcher(randomInputs.get(t)).matches();
            }
        }
        System.out.println("Done in " + (new Date().getTime() - start.getTime()) + "ms");
    }
}
