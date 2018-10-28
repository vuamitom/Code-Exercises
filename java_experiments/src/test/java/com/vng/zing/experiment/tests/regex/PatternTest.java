/*
 * Copyright (c) 2018-2022 by Zalo Group.
 * All Rights Reserved.
 */
package com.vng.zing.experiment.tests.regex;

import com.vng.zing.experiment.regex.Matcher;
import com.vng.zing.experiment.regex.Pattern;
import org.junit.Test;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;

public class PatternTest {

    @Test
    public void testCompile() {
        Pattern p = Pattern.compile("abc+d");
        Matcher m = p.matcher("abccccd");
        System.out.println(m.matches());
        Pattern.printObjectTree(p.matchRoot);
        System.out.println(m.group(0));

        Pattern p1 = Pattern.compile("abc+d|ab+cd");
        Matcher m1 = p1.matcher("abccccd");
        System.out.println(m1.matches());

        Pattern p3 = Pattern.compile("a[bc]+d");
        Matcher m3 = p3.matcher("abccccd");
        System.out.println(m3.matches());

        Pattern p4 = Pattern.compile("a(b+|c+)d");
        Matcher m4 = p4.matcher("abccccd");
        System.out.println(m4.matches());
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
