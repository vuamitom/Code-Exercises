-- tail recursion 
-- seem like Haskell has some optimization for this 
-- cause not only it take less space but also less time


import System.Environment

--f 1 x  = x 
--f 2 x = 1 + x 
--f n x = f (n-1) y where y = f (n-2) x 
--fib n = f n 0 
f 1 p1 p2 = p2 
f 2 p1 p2 = p1 
f n p1 p2 = f (n-1) (p1+p2) p1 
fib n = f n 1 0 
    
main = do
    --input <- getLine
    args <- getArgs
    print . fib . read  $ head args 
