package main

import "fmt"

func main() {
	var n int
	// read N test cases
	fmt.Scan(&n)
	run_test(n)
}

func run_test(n int) {
	var x int
	if n > 0 {
		fmt.Scan(&x)
		r := add_up(x)
		fmt.Println(r)
		run_test(n - 1)
	}
}

func add_up(x int) int {
	var m int
	if x > 0 {
		fmt.Scan(&m)
        s := 0
        if m > 0 {
		    s += m*m 
        }
        s += add_up(x-1)
		return s
	} else {
		return 0
	}
}
